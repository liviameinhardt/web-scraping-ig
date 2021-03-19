import ig_scrape as ig
import pandas as pd
from time import sleep

cliente = ""
usuario = ""
senha = ""
pagina = ""

try:
    df = pd.read_excel(f"{cliente}.xlsx")
except:
    df = pd.DataFrame(columns=['User','Url', 'Data','Curtidas/Views','Tipo','Comentários','Contagem de Hashtags','Hashtags'])

links_posts = []

ig.login(usuario,senha)

links_posts = ig.recent_posts(pagina,1)

ig.logout(usuario)

df = ig.detalhes_publi(links_posts,df,pagina)

ig.driverquit()

df.to_excel(f"{cliente}.xlsx",index=False)
