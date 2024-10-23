import requests
import webbrowser
from bs4 import BeautifulSoup
from tkinter import *
from datetime import date

class Jornal:

    def __init__(self):
        self.titulos = []
        self.subtitulos = []
        self.links = []
        self.iterador = 0

        site_g1 = 'http://www.g1.globo.com'
        response = requests.get(site_g1)
        content = response.content
        site = BeautifulSoup(content, 'html.parser')
        lista_div_noticias = site.findAll('div', attrs={'class': 'bastian-feed-item'})
        for noticia in lista_div_noticias:
            titulo = noticia.find('h2')
            link = titulo.find('a')
            if 'Jogos do g1' in titulo.text:
                continue
            self.titulos.append(titulo.text)
            link_https = link['href'] 
            link_http = 'http://' + link_https[8:]
            self.links.append(link_http)

    def buscaNoticia(self):
        response = requests.get(self.links[self.iterador])
        content = response.content
        site = BeautifulSoup(content, 'html.parser')
        subtitulo = site.find('div', attrs = {'class': 'medium-centered subtitle'})
        if subtitulo is not None:
            self.subtitulos.append(subtitulo.text)
        else:
            self.subtitulos.append('Erro ao carregar o corpo da notícia.')
        self.iterador += 1
        
    def imprimeNoticia(self):
        if (self.iterador < len(self.titulos)):
            self.buscaNoticia()
            titulo_noticia['text'] = self.titulos[self.iterador - 1]
            subtitulo_noticia['text'] = self.subtitulos[self.iterador - 1]
            link_noticia['text'] = 'Link para a reportagem'
            link_noticia.bind('<Button-1>', self.acessarLink)
        else:
            titulo_noticia['text'] = "Fim das notícias."
            subtitulo_noticia['text'] = ""
            link_noticia['text'] = ""
            link_noticia.bind('<Button-1>')
    
    def acessarLink(self, link):
        webbrowser.open_new(self.links[self.iterador - 1])



#inicializacao 
jornal = Jornal()
hoje = date.today()

width = 500
height = 700
padX= 10
padY = 10
janela = Tk()
janela.geometry(f"{width}x{height}")
janela.resizable(False, True)
janela.title('Portal de Notícias')
cabecalho = Label(janela, text="As notícias de hoje do G1")
cabecalho.grid(column=0, row=0, padx=padX, pady=padY)
texto_data = Label(janela, text=f"{hoje.day}/{hoje.month}/{hoje.year}")
texto_data.grid(column=0, row=1, padx=padX,pady=padY)
titulo_noticia = Label(janela, wraplength=width - 2*padX, text="")
titulo_noticia.grid(column=0,row=3,padx=padX, pady=padY)
subtitulo_noticia = Label(janela, wraplength=width - 2*padX, text="")
subtitulo_noticia.grid(column=0,row=4,padx=10,pady=10)
link_noticia = Label(janela, text="")
link_noticia.grid(column=0,row=5, padx=padX, pady=padY)
botao = Button(janela, text="Próxima Notícia", command=jornal.imprimeNoticia)
botao.grid(column=0, row=7, padx=padX, pady=padY)


janela.mainloop()
