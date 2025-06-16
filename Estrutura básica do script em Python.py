from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def obter_resposta_com_xpath(driver, xpath="//div[@data-message-id][last()]"):
    """Retorna o texto da última resposta encontrada pelo XPath."""
    elemento = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    return elemento.text.strip()


def enviar_mensagem(driver, mensagem, campo_xpath="//textarea"):
    """Envia uma mensagem no campo indicado pelo XPath."""
    campo = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, campo_xpath))
    )
    campo.clear()
    campo.send_keys(mensagem + Keys.ENTER)
    
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
