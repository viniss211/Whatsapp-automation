import time
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from threading import Thread

global stop_process
stop_process = False

def escolher_arquivo():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
    if arquivo:
        entry_arquivo.delete(0, tk.END)
        entry_arquivo.insert(0, arquivo)

def iniciar_automacao():
    global stop_process
    stop_process = False
    arquivo = entry_arquivo.get()
    if not arquivo:
        messagebox.showerror("Erro", "Escolha um arquivo Excel contendo os links!")
        return
    
    thread = Thread(target=executar_bot, args=(arquivo,))
    thread.start()

def parar_automacao():
    global stop_process
    stop_process = True
    print("Automação interrompida pelo usuário.")
    root.quit()

def executar_bot(arquivo):
    global stop_process
    try:
        df = pd.read_excel(arquivo, header=None)
        df.columns = ["Link"]
        df["Link"] = df["Link"].astype(str).str.strip()
        links = df["Link"].dropna().tolist()
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        #chrome_options.add_argument("--user-data-dir=C:\\Users\\vinis\\AppData\\Local\\Google\\Chrome\\User Data\\Profile_Automacao")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get("https://web.whatsapp.com")
        messagebox.showinfo("Ação necessária", "Escaneie o QR Code no WhatsApp Web, aguarde o whatsapp abrir as conversas e clique em OK para continuar...")

        for link in tqdm(links, desc="Processando grupos", unit="grupo"):
            if stop_process:
                print("Processo interrompido pelo usuário.")
                driver.quit()
                root.quit()
                return
            
            try:
                driver.get(link)
                time.sleep(2)  # Tempo reduzido para garantir carregamento
                
                # Aguarda o botão "Juntar-se à conversa" aparecer
                try:
                    entrar_botao = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.ID, "action-button"))
                    )
                    driver.execute_script("arguments[0].click();", entrar_botao)
                    time.sleep(1.5)  # Pequena pausa para carregamento
                except:
                    print("Botão 'Juntar-se à conversa' não encontrado imediatamente.")
                
                # Aguarda o botão "Usar WhatsApp Web" se necessário
                try:
                    usar_web = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'web.whatsapp.com/accept')]")
                    ))
                    driver.execute_script("arguments[0].click();", usar_web)
                    time.sleep(2)
                except:
                    pass
                
                # Aguarda o pop-up de confirmação de entrada no grupo
                try:
                    entrar_no_grupo = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.XPATH, "//button//div[contains(text(),'Entrar no grupo')]")
                    ))
                    driver.execute_script("arguments[0].click();", entrar_no_grupo)
                    time.sleep(3)
                except:
                    print("Botão 'Entrar no grupo' não encontrado.")
                
                if stop_process:
                    print("Processo interrompido pelo usuário.")
                    driver.quit()
                    root.quit()
                    return
                
                time.sleep(3)  # Tempo de respiro entre cada grupo
                
            except Exception as e:
                print(f"Erro ao entrar no grupo {link}: {e}")

        messagebox.showinfo("Concluído", "Todos os links foram processados!")
        driver.quit()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Criar interface gráfica
root = tk.Tk()
root.title("Bot de Entrada em Grupos do WhatsApp")
root.geometry("400x250")

tk.Label(root, text="Escolha o arquivo Excel com os links:").pack(pady=10)

entry_arquivo = tk.Entry(root, width=40)
entry_arquivo.pack(pady=5)

btn_escolher = tk.Button(root, text="Selecionar Arquivo", command=escolher_arquivo)
btn_escolher.pack(pady=5)

btn_iniciar = tk.Button(root, text="Iniciar Automação", command=iniciar_automacao, bg="green", fg="white")
btn_iniciar.pack(pady=10)

btn_parar = tk.Button(root, text="Parar Automação", command=parar_automacao, bg="red", fg="white")
btn_parar.pack(pady=10)

root.mainloop()