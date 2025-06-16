from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def obter_resposta_com_xpath(driver, xpaths=None):
    """Tenta retornar o texto da última resposta usando uma lista de XPaths."""
    if xpaths is None:
        xpaths = [
            "(//div[@data-message-author-role='assistant'])[last()]",
            "(//div[contains(@class,'markdown')])[last()]",
        ]

    for xpath in xpaths:
        try:
            elemento = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            texto = elemento.text.strip()
            if texto:
                return texto
        except TimeoutException:
            continue
    return ""


def enviar_mensagem(driver, mensagem, seletores=None):
    """Envia uma mensagem tentando vários seletores de campo."""
    if seletores is None:
        seletores = [
            "textarea[data-testid='prompt-textarea']",
            "textarea",
            "div[contenteditable='true']",
        ]

    for seletor in seletores:
        try:
            campo = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, seletor))
            )
            campo.clear()
            campo.send_keys(mensagem)
            campo.send_keys(Keys.ENTER)
            return True
        except TimeoutException:
            continue
    raise TimeoutException("Campo de mensagem não encontrado")

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