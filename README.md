# IAs-conversa-o
Criar uma ponte entre duas IAs, de forma que elas “conversem” entre si.

## Uso rápido

1. Instale as dependências do Selenium e o driver do seu navegador (por exemplo, o ChromeDriver).
2. Execute `python 'Estrutura básica do script em Python.py'`.

O script abre duas abas (ChatGPT e Gemini) e alterna as mensagens entre elas.

Os seletores de elementos podem mudar conforme as páginas evoluem. Se as mensagens não forem enviadas ou lidas corretamente, ajuste as listas de XPaths/seletores nas funções `obter_resposta_com_xpath` e `enviar_mensagem`.