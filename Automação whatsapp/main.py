import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do WebDriver
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:\\Users\\vinis\\AppData\\Local\\Google\\Chrome\\User Data\\Profile_Automacao")
chrome_options.add_argument("--start-maximized")

# Iniciar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ler planilha e renomear coluna corretamente
df = pd.read_excel("grupos.xlsx", header=None)
df.columns = ["Link"]
df["Link"] = df["Link"].astype(str).str.strip()  # Remove espaços extras

# Função para verificar se o WhatsApp Web carregou
def esperar_whatsapp_carregar():
    try:
        print("[Verificação] Checando se o WhatsApp Web carregou completamente...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Caixa de texto para pesquisa')]"))
        )
        print("[OK] WhatsApp Web carregado com sucesso!")
    except:
        print("[Erro] O WhatsApp Web travou na tela de carregamento! Tentando recarregar...")
        driver.refresh()  # Recarrega a página
        time.sleep(15)  # Aguarda mais tempo após recarregar

# Percorrer os links e entrar nos grupos
for index, row in df.iterrows():
    link = row["Link"]
    
    try:
        print(f"\n[Ação] Acessando o link: {link}")
        driver.get(link)

        print("[Aguardando] Esperando 15 segundos para carregamento completo...")
        time.sleep(15)

        # Clicar no botão "Juntar-se à conversa"
        try:
            print("[Aguardando] Procurando botão 'Juntar-se à conversa'...")
            entrar_botao = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@id='action-button']"))
            )
            print("[Clique] Botão encontrado! Tentando clicar...")
            driver.execute_script("arguments[0].click();", entrar_botao)
            
            print("[Aguardando] Aguardando 15 segundos para transição...")
            time.sleep(15)
            
            # Se aparecer a opção "Usar o WhatsApp Web"
            try:
                print("[Verificação] Checando se a opção 'Usar o WhatsApp Web' apareceu...")
                usar_web = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'web.whatsapp.com/accept')]"))
                )
                print("[Clique] Alternativa 'Usar o WhatsApp Web' detectada! Clicando...")
                driver.execute_script("arguments[0].click();", usar_web)
                
                print("[Aguardando] Aguardando 20 segundos para carregamento do WhatsApp Web...")
                time.sleep(20)

            except:
                print("[OK] Não foi necessário clicar em 'usar o WhatsApp Web'.")

            # Verifica se o WhatsApp Web realmente carregou antes de continuar
            esperar_whatsapp_carregar()

            # **Novo Passo:** Clicar no botão "Aderir ao grupo"
            try:
                print("[Aguardando] Esperando 15 segundos antes de procurar o botão 'Aderir ao grupo'...")
                time.sleep(15)

                print("[Procurando] Buscando botão 'Aderir ao grupo'...")
                aderir_botao = WebDriverWait(driver, 25).until(
                    EC.element_to_be_clickable((By.XPATH, "//button//div[contains(text(),'Aderir ao grupo')]"))
                )
                print("[Clique] Botão 'Aderir ao grupo' encontrado! Clicando...")
                driver.execute_script("arguments[0].click();", aderir_botao)
                print("✅ [Sucesso] Agora você faz parte do grupo!")

                print("[Aguardando] Esperando 20 segundos antes de prosseguir para o próximo grupo...")
                time.sleep(20)
                
            except Exception as e:
                print(f"[Erro] Não foi possível clicar em 'Aderir ao grupo': {e}")

        except Exception as e:
            print(f"[Erro] Não foi possível clicar em 'Juntar-se à conversa': {e}")

        print("[Pausa] Esperando 15 segundos antes do próximo link...")
        time.sleep(15)  # Tempo extra antes de acessar o próximo grupo
        
    except Exception as e:
        print(f"[Erro] Falha ao processar o link: {e}")

# Fechar navegador
print("\n[FIM] Processo finalizado! Fechando navegador...")
driver.quit()
