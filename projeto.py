import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import re

class WebScraping():

	def __init__(self, url, cidade, arquivo):
		# Alocando argumentos
		self.url = url
		self.cidade = cidade
		self.nome_arquivo = arquivo

		# Inicializando objetos
		self.site = None
		self.navegador = None
		self.hospedagens = None
		self.dados_hospedagens = []

		# Expecifica configurações de inicialização do navegador -- Selenium
		self.options = Options()
		self.options.add_argument('window-size=maximized')  # Especifica as dimensões da janela aberta
		self.options.add_experimental_option("detach", True) # Manter o Chrome aberto
		## self.options.add_argument('--headless')  # Realiza a rotina sem abrir o navegador

		print('Web Scraping inicializado!')

	def run(self):
		self.get_url()
		print('get_url executado com sucesso')
		self.clica_busca()
		print('clica_busca executado com sucesso')
		self.input_cidade()
		print('input_cidade executado com sucesso')
		self.integracao_bs()
		print('integracao_bs executado com sucesso')
		self.identifica_anuncio()
		print('identifica_anuncio executado com sucesso')
		self.raspagem_dados()
		print('raspagem_dados executado com sucesso')
		self.criar_tabela()
		print('criar_tabela executado com sucesso')
	
	def get_url(self):
		# Indicando a automação do Chrome 
		self.navegador = webdriver.Chrome(options=self.options)
		self.navegador.get(self.url)

		sleep(5)

	def clica_busca(self):
		# Indentificando o botão de busca
		button = self.navegador.find_element(By.TAG_NAME, "button")
		button.click()

		sleep(3)

	def input_cidade(self):
		# Identificando o input e enviando a busca desejada
		input_place = self.navegador.find_element(By.XPATH, "//*[@id='bigsearch-query-location-input']")
		input_place.send_keys(self.cidade)
		sleep(1)
		input_place.submit()
		sleep(3)

	def integracao_bs(self):
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
		self.site = BeautifulSoup(self.navegador.page_source, 'html.parser')
		
	def identifica_anuncio(self):
		self.hospedagens = self.site.findAll('div', attrs={'itemprop': 'itemListElement'})

	def raspagem_dados(self):
		for hospedagem in self.hospedagens:
		
			hospedagem_descricao = hospedagem.find('div', class_='t1jojoys dir dir-ltr').get_text()
			hospedagem_detalhes = hospedagem.find('span', class_='t6mzqp7 dir dir-ltr').get_text()
			hospedagem_leitos = hospedagem.find('span', class_='dir dir-ltr').get_text()   
			hospedagem_valor = hospedagem.find('span', class_='_tyxjp1').get_text()
			hospedagem_url = hospedagem.find('meta', attrs={'itemprop': 'url'})
			hospedagem_avaliacao = hospedagem.find('span', class_='r1dxllyb dir dir-ltr').get_text()
	
			print('Descrição:', hospedagem_descricao)
			print('Detalhes:', hospedagem_detalhes)
			print('Leitos:', hospedagem_leitos)
			print('Valor:', hospedagem_valor)
			print('Avaliação:', hospedagem_avaliacao)
			
			#Adicionar a informação dentro do atributo content
			hospedagem_url = hospedagem_url['content'] 
			print('URL:', hospedagem_url)
	
			# Utilizado para quebra de linhas
			print() 

			self.dados_hospedagens.append([hospedagem_descricao,
							  				hospedagem_detalhes,
							 				hospedagem_valor, 
							  				hospedagem_avaliacao, 
							  				hospedagem_url])
		

	def criar_tabela(self): 							  
			dados = pd.DataFrame(self.dados_hospedagens, columns=['Descrição', 
													'Detalhes', 
													'Valor', 
													'Avaliação', 
													'URL'])

			dados.to_excel(self.nome_arquivo, index=False)


airbnb = WebScraping(url='http://www.airbnb.com.br', cidade='Rio de Janeiro', arquivo='dados_hospedagens.xlsx')
airbnb.run()