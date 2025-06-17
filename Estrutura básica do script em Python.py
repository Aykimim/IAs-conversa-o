from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def obter_resposta_com_xpath(driver, xpaths=None):
    """Retorna o texto da última resposta, tentando vários XPaths."""
    if xpaths is None:
        xpaths = [
            "(//div[@data-message-author-role='assistant'])[last()]",
            "(//div[contains(@class,'markdown')])[last()]",
        ]

    for xpath in xpaths:
        try:
            elemento = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
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
            campo = WebDriverWait(driver, 20).until(
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

def main():
    driver = webdriver.Chrome()

    # Abrir ChatGPT em duas abas separadas
    # É necessário estar logado previamente para que o envio funcione.
    driver.get("https://chat.openai.com/")              # Primeira aba do ChatGPT
    driver.execute_script("window.open('https://chat.openai.com/', '_blank');")
    time.sleep(5)                                       # Aguarda o carregamento

    abas = driver.window_handles

    for _ in range(5):
        # --- Obter resposta do ChatGPT ---
        driver.switch_to.window(abas[0])                # Abre aba do ChatGPT
        resposta = obter_resposta_com_xpath(driver)

        # --- Enviar a resposta para a segunda aba ---
        driver.switch_to.window(abas[1])                # Abre segunda aba
        enviar_mensagem(driver, resposta)


        # --- Pegar a réplica da segunda aba ---
        resposta = obter_resposta_com_xpath(driver)


        # --- Enviar para o ChatGPT novamente ---
        driver.switch_to.window(abas[0])
        enviar_mensagem(driver, resposta)


    driver.quit()

    enviar_mensagem(driver, resposta)
if __name__ == "__main__":
    main()