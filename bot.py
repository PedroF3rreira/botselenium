import os
import time
import re

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from selenium import webdriver
from selenium.webdriver.common.by import By


class Wppbot:
	# pega caminho da aplicação
	dir_path = os.getcwd()

	# recebe o nome do bot
	def __init__(self, name_bot):
		self.bot = ChatBot(name_bot)
		# seta como o bot irar treinar
		#self.bot.set_trainer(ListTrainer)
		self.trainer = ListTrainer(self.bot)
		# seta nde esta o driver
		self.chrome = self.dir_path+'\\chromedriver.exe'

		#configurarmos m profile no chrome para não precivsar logar no wp sempre que abrir o bot
		self.options = webdriver.ChromeOptions()
		self.options.add_argument(r"user-data-dir="+self.dir_path+"\profile\wpp")
		self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)

	def iniciar(self, nome_contato):
		# entra no link so wp
		self.driver.get('https://web.whatsapp.com/')
		self.driver.implicitly_wait(15)# aguarda 15 segundos

		# pega elemento da caixa de pesquisa

		self.caixa_pesquisa = self.driver.find_element(By.CLASS_NAME, 'iq0m558w')
		self.caixa_pesquisa.send_keys(nome_contato)# busca pelo nome do contato
		time.sleep(2)

		# procura contato/grupo que esta na tag span e possui o nome que pesquisamos eclicamos nele
		self.contato = self.driver.find_element(By.XPATH, '//span[@title = "{}"]'.format(nome_contato))
		self.contato.click()
		time.sleep(2)

	
	def saudacoe(self, frase_inicial):
		self.caixa_menssagen = self.driver.find_element(By.CLASS_NAME, '_3Uu1_')

		if type(frase_inicial) == list:
			for frase in frase_inicial:
				self.caixa_menssagen.send_keys(frase)
				time.sleep(1)
				self.botao_enviar = self.driver.find_element(By.XPATH, "//button[@aria-label='Enviar']")
				self.botao_enviar.click()
				time.sleep(1)
		else:
			return False


	def escuta(self):
		post = self.driver.find_elements(By.CLASS_NAME, '_21Ahp')
		ultimo = len(post) - 1
		texto = post[ultimo].find_element(By.CSS_SELECTOR, 'span.selectable-text').text
		return texto


	def responde(self, texto):
		response = self.bot.get_response(texto)
		response = str(response)
		response = 'bot:' + response

		self.caixa_menssagen = self.driver.find_element(By.CLASS_NAME, '_3Uu1_')
		self.caixa_menssagen.send_keys(response)
		time.sleep(1)
		self.botao_enviar = self.driver.find_element(By.XPATH, "//button[@aria-label='Enviar']")
		self.botao_enviar.click()


	def treinar(self, nome_pasta):
		for treino in os.listdir(nome_pasta):
			conversas = open(nome_pasta+'/'+treino, 'r').readlines()
			self.trainer.train(conversas)