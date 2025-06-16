from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Inicializar o Chrome (Selenium 4.x)
driver = webdriver.Chrome()

# Abrir ChatGPT e Gemini em abas separadas
driver.get("https://chat.openai.com/")              # ChatGPT
driver.execute_script("window.open('https://gemini.google.com/', '_blank');")
time.sleep(5)                                       # Aguarda o carregamento

abas = driver.window_handles

for i in range(5):  # Exemplo de 5 interações
    # --- Obter resposta do ChatGPT ---
    driver.switch_to.window(abas[0])                # Abre aba do ChatGPT
    resposta = obter_resposta_com_xpath(driver)     # Função que lê o texto

    # --- Enviar a resposta para o Gemini ---
    driver.switch_to.window(abas[1])                # Abre aba do Gemini
    enviar_mensagem(driver, resposta)               # Função que escreve e envia

    # --- Pegar a réplica do Gemini ---
    resposta = obter_resposta_com_xpath(driver)

    # --- Enviar para o ChatGPT novamente ---
    driver.switch_to.window(abas[0])
    enviar_mensagem(driver, resposta)
