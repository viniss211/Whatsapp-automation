# 📖 Manual de Usuário - Bot de Entrada em Grupos do WhatsApp

Este manual fornece instruções detalhadas sobre como utilizar o Bot de Entrada em Grupos do WhatsApp.

---

## 1️⃣ Introdução
O bot foi criado para facilitar a entrada automática em grupos do WhatsApp utilizando links armazenados em um arquivo Excel.

Ele permite:
✅ Entrada automática em grupos do WhatsApp via **WhatsApp Web**.
✅ Detecção de grupos que requerem **solicitação de permissão** e ignora esses grupos.
✅ Parada do processo a qualquer momento.

---

## 2️⃣ Requisitos
Antes de iniciar, certifique-se de que possui:
- **Google Chrome** instalado e atualizado.
- **Python 3.8+** instalado.
- **Bibliotecas Python** necessárias (instalar com o comando abaixo no terminal):
  ```bash
  pip install selenium pandas openpyxl webdriver-manager tqdm
  ```

---

## 3️⃣ Configuração do Arquivo Excel
Crie um arquivo Excel contendo os links dos grupos do WhatsApp na **primeira coluna**.

Exemplo:
| Links dos Grupos |
|------------------|
| https://chat.whatsapp.com/XXXXXXXXXXXXXX |
| https://chat.whatsapp.com/YYYYYYYYYYYYYY |

⚠️ **Certifique-se de que os links são válidos e que a primeira linha contém um link válido.**

---

## 4️⃣ Como Usar a Aplicação

### 📌 1. Iniciar o Programa
1️⃣ Abra o **terminal** ou **prompt de comando**.
2️⃣ Navegue até a pasta onde o **arquivo do bot** está salvo.
3️⃣ Execute o comando:
   ```bash
   python nome_do_arquivo.py
   ```

### 📌 2. Usar a Interface Gráfica
1️⃣ Clique no botão **"Selecionar Arquivo"** e escolha seu arquivo Excel.
2️⃣ Clique em **"Iniciar Automação"**.
3️⃣ **Escaneie o QR Code no WhatsApp Web** (caso solicitado).
4️⃣ Aguarde o bot entrar nos grupos automaticamente.
5️⃣ Caso deseje interromper o processo, clique em **"Parar Automação"**.

---

## 5️⃣ Possíveis Mensagens e Soluções

🔹 **O bot não entra nos grupos:**
- Verifique se os links são válidos e ainda estão ativos.
- Confirme que o WhatsApp Web está funcionando corretamente.

🔹 **O QR Code do WhatsApp sempre aparece:**
- Pode ser necessário configurar o Chrome para utilizar um perfil salvo.
- O login no WhatsApp Web pode ter expirado.

🔹 **O bot pula alguns grupos:**
- Se um grupo exigir permissão para entrar, o bot automaticamente ignora e segue para o próximo.

---

## 6️⃣ Conclusão
Com este manual, você pode utilizar o bot de forma eficiente para automatizar a entrada em grupos do WhatsApp.
Caso tenha dúvidas, revise os requisitos e siga os passos corretamente. 🚀

