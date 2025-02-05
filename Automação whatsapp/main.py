import os
import sys
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

# Se estiver rodando como .exe, redirecionar stdout e stderr para evitar erro de NoneType
if getattr(sys, 'frozen', False):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

# Configurar caminhos do Tcl/Tk se o programa for executado como .exe
if hasattr(sys, '_MEIPASS'):
    os.environ['TCL_LIBRARY'] = os.path.join(sys._MEIPASS, 'tcl')
    os.environ['TK_LIBRARY'] = os.path.join(sys._MEIPASS, 'tk')

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
    
    btn_iniciar.config(state=tk.DISABLED, bg="gray")  # Desabilita o botão e muda a cor
    lbl_status.config(text="Automação em andamento...", fg="blue")
    btn_parar.config(state=tk.NORMAL, bg="red")  # Habilita o botão de parar
    thread = Thread(target=executar_bot, args=(arquivo,))
    thread.start()

def parar_automacao():
    global stop_process
    stop_process = True
    print("Automação interrompida pelo usuário.")
    btn_parar.config(state=tk.DISABLED, bg="gray")  # Desabilita o botão
    lbl_status.config(text="Automação interrompida.", fg="red")

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

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get("https://web.whatsapp.com")
        
        try:
            messagebox.showinfo("Ação necessária", "Escaneie o QR Code no WhatsApp Web, aguarde o WhatsApp abrir as conversas e clique em OK para continuar...")
        except Exception as e:
            print(f"Erro no messagebox: {e}")
        
        for link in tqdm(links, desc="Processando grupos", unit="grupo"):
            if stop_process:
                print("Processo interrompido pelo usuário.")
                driver.quit()
                btn_iniciar.config(state=tk.NORMAL, bg="green")  # Habilita o botão novamente
                lbl_status.config(text="Automação interrompida.", fg="red")
                return
            
            try:
                driver.get(link)
                time.sleep(2)
                
                try:
                    entrar_botao = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.ID, "action-button"))
                    )
                    driver.execute_script("arguments[0].click();", entrar_botao)
                    time.sleep(1.5)
                except:
                    print("Botão 'Juntar-se à conversa' não encontrado imediatamente.")
                
                try:
                    usar_web = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'web.whatsapp.com/accept')]")
                    ))
                    driver.execute_script("arguments[0].click();", usar_web)
                    time.sleep(2)
                except:
                    pass
                
                try:
                    entrar_no_grupo = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.XPATH, "//button//div[contains(text(),'Entrar no grupo')]"))
                    )
                    driver.execute_script("arguments[0].click();", entrar_no_grupo)
                    time.sleep(3)
                except:
                    print("Botão 'Entrar no grupo' não encontrado.")
                    
                    try:
                        enviar_pedido = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button//div[contains(text(),'Enviar pedido')]"))
                        )
                        driver.execute_script("arguments[0].click();", enviar_pedido)
                        print("Pedido de entrada no grupo enviado.")
                        time.sleep(3)
                    except:
                        print("Botão 'Enviar pedido' não encontrado. Pulando grupo...")
                
                if stop_process:
                    print("Processo interrompido pelo usuário.")
                    driver.quit()
                    btn_iniciar.config(state=tk.NORMAL, bg="green")  # Habilita o botão novamente
                    lbl_status.config(text="Automação interrompida.", fg="red")
                    return
                
                time.sleep(3)  # Tempo de respiro entre cada grupo
                
            except Exception as e:
                print(f"Erro ao entrar no grupo {link}: {e}")

        messagebox.showinfo("Concluído", "Todos os links foram processados!")
        driver.quit()
        btn_iniciar.config(state=tk.NORMAL, bg="green")  # Habilita o botão novamente
        lbl_status.config(text="Automação concluída!", fg="green")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
