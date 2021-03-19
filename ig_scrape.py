# -*- coding: utf-8 -*-
"""
Created on Sex Jan 22 2021
@author: livia
"""

#Coleta de dados do Instagram
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import modulo_tratamento as mt

driver = webdriver.Chrome()

def driverquit():
    driver.quit()


def login(login,senha): # não há tratamento para senhas incorretas (ainda)
    """
    Faz login de forma automática no instagram, 
    fechando janelas de 'salvar senha' e 'receber notificações'
    sleep para simular interacao mais natural

    Parameters
    ----------
    username : str
        usuario str
    senha: senha str

    Returns
    -------
    None.    
    """
    
    driver.get('https://www.instagram.com/')
    sleep(5) #mais tempo -> para esperar o carregamento
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(login)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(senha)
    try:
        sleep(0.5)
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
        sleep(3)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        sleep(3.5)
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    except:
        print("Senha incorreta")
    

def logout(username):
    """
    Faz o logout automático do instagram

    Parameters
    ----------
    username : str
        usuário logado 

    Returns
    -------
    None.

    """
    url = "https://www.instagram.com/" + username + "/"
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/button').click()
    sleep(1)
    driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/button[9]').click()
    driver.quit()



#Função retirada de: https://medium.com/swlh/tutorial-web-scraping-instagrams-most-precious-resource-corgis-235bf0389b0c
def recent_posts(username,num_publi=21):
    """
    Coleta o link das publicações mais recentes de um usuário

    Parameters
    ----------
    username : str
        nome do usuário a ser analisado.
    num_publi : int, opcional
        número de publicações, default = 21.

    Returns
    -------
    list
        links das publicações.

    """
    url = "https://www.instagram.com/" + username + "/"
    driver.get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < num_publi:
        links = [a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME,'a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(scroll_down)
        sleep(5)
    else:
        return post_links[:num_publi]
    
def detalhes_publi(urls,df,pagina):
    """
    Coleta a contagem de curtidas/views, comentários e hashtags, além da data e hashtags usadas.
    
    Parameters
    ----------
    urls : list
        lista dos links das publicações
    df: DataFrame
        dataframe para os dados da publicação 

    Returns
    -------
    DataFrame 
        adiciona os novos elementos ao dataframe 
    """
    for url in urls:
            #acessa a url
        driver.get(url)
            
            # extrair quantidade de comentários
        comentarios = driver.find_elements(By.CLASS_NAME, "Mr508") #pega os comentarios principais
        resposta = driver.find_elements(By.CLASS_NAME,"TCSYW") #pega respostas a comentários
        comentarios = len(comentarios)
        comentarios += len(resposta)
    
        # extrair quantidade de curtidas
        try:
            xpath_likes = '//*[@id="react-root"]/section/main/div/div/article/div[3]/section[2]/div/div'
            curtidas = driver.find_element(By.XPATH,xpath_likes).text
            #tratar o dado
            curtidas = mt.trata_curtidas(curtidas)
            tipo ="curtida"
        except:
            xpath_likes = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/span'
            curtidas = driver.find_element(By.XPATH,xpath_likes).text
            curtidas = mt.trata_curtidas(curtidas)
            tipo ="view"
               
        # extrair a data da publicação
        xpath_data = '//*[@id="react-root"]/section/main/div/div/article/div[3]/div[2]/a/time'
        data = driver.find_element(By.XPATH, xpath_data).get_attribute("datetime")

        #tratar o dadoattribute
        data = mt.trata_data(data)
        
        #extrair hashtags
                    
        hashtag_list = []       
        hashtag = driver.find_elements(By.CLASS_NAME, "xil3i")
        contagem_hashtag = len(hashtag)
        for texto in hashtag:
            hashtag_list.append(texto.text)
        
        df = df.append({'User':pagina,'Url':url, 'Data':data,'Curtidas/Views':curtidas,'Tipo':tipo,'Comentários':comentarios,
                        'Contagem de Hashtags':contagem_hashtag,'Hashtags':hashtag_list},ignore_index=True)
    return df

