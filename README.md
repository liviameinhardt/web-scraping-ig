# Instagram Scrape

Código desenvolvido em [Selenium](https://selenium-python.readthedocs.io/) que coleta comentários, número de curtidas, hashtags e data de posts do Instagram. Para isso, basta passar o número de posts a serem considerados, usuário e um login e senha. Esses dados são interessantes para análise de engajamento em Planos de Marketing.

## Utilização
Basta inserir as informações desejadas no módulo main.py. 

## Funcionamento
Primeiro são coletadas todas as urls dos n posts mais recentes do usuário dado. Na segunda parte, o bot visita cada um desses links coletando as informações.

## Erros
Algumas vezes o Instagram detecta o bot e para de permitir a extração dos dados, nesse caso, basta executar as duas partes do código separadamente. Para isso primeiro execute somente esse trecho:

```pyhton
cliente = ""
login = ""
senha = ""
usuario = ""
numero_posts = 21

ig.login(usuario,senha)
links_posts = ig.recent_posts(pagina,21)
print(links_posts)
ig.logout(usuario)
```

Copie a lista links_posts printada no terminal e adicione essa variável ao código. Depois, execute somente:


```pyhton

try:
    df = pd.read_excel(f"{cliente}.xlsx")
except:
    df = pd.DataFrame(columns=['User','Url', 'Data','Curtidas/Views','Tipo','Comentários','Contagem de Hashtags','Hashtags'])

links_posts = [] # atualize com as urls printadas na tela

df = ig.detalhes_publi(links_posts,df,pagina)

ig.driverquit()

df.to_excel(f"{cliente}.xlsx",index=False)

```

## Pontos de Melhoria

* O erro apresentado acima
* Tratar para dados faltantes (posts sem curtidas, comentários)
* Coleta de número de comentários mais eficiente
* Coletar número de seguidores e calcular engajamento
* Adicionar outras métricas de forma automática na planilha
* Adicionar visualizações de forma automática na planilha (macro?)
