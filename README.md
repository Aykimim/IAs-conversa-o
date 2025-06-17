# IAs-conversa-o
Criar uma ponte entre duas IAs, de forma que elas “conversem” entre si.

## Uso rápido

1. Instale as dependências do Selenium e o driver do seu navegador (por exemplo, o ChromeDriver).
2. Execute `python 'Estrutura básica do script em Python.py'`.

O script abre duas abas do ChatGPT e alterna as mensagens entre elas. É preciso
estar logado previamente no site para que o envio funcione. Ao final do ciclo,
o navegador é encerrado automaticamente.

Caso o script não encontre os campos de texto, atualize as listas de XPaths e
seletores em `obter_resposta_com_xpath` e `enviar_mensagem`. As páginas podem
mudar de layout ao longo do tempo.