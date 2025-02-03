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

def escolher_arquivo():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
    if arquivo:
        entry_arquivo.delete(0, tk.END)
        entry_arquivo.insert(0, arquivo)

def iniciar_automacao():
    arquivo = entry_arquivo.get()
    if not arquivo:
        messagebox.showerror("Erro", "Escolha um arquivo Excel contendo os links!")
        return
    
    thread = Thread(target=executar_bot, args=(arquivo,))
    thread.start()

def executar_bot(arquivo):
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
        chrome_options.add_argument("--user-data-dir=C:\\Users\\vinis\\AppData\\Local\\Google\\Chrome\\User Data\\Profile_Automacao")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get("https://web.whatsapp.com")
        messagebox.showinfo("Ação necessária", "Escaneie o QR Code no WhatsApp Web e clique em OK para continuar...")

        for link in tqdm(links, desc="Processando grupos", unit="grupo"):
            try:
                driver.get(link)
                time.sleep(15)
                
                try:
                    entrar_botao = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[@id='action-button']"))
                    )
                    driver.execute_script("arguments[0].click();", entrar_botao)
                    time.sleep(5)
                    
                    try:
                        usar_web = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'web.whatsapp.com/accept')]")
                        ))
                        driver.execute_script("arguments[0].click();", usar_web)
                        time.sleep(5)
                    except:
                        pass

                    try:
                        pop_up = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
                        )
                        if pop_up:
                            entrar_no_grupo = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH, "//button//div[contains(text(),'Entrar no grupo')]")
                            ))
                            driver.execute_script("arguments[0].click();", entrar_no_grupo)
                            time.sleep(5)
                    except:
                        pass
                except:
                    pass
                
                time.sleep(10)
            except Exception as e:
                print(f"Erro ao entrar no grupo {link}: {e}")

        messagebox.showinfo("Concluído", "Todos os links foram processados!")
        driver.quit()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Criar interface gráfica
root = tk.Tk()
root.title("Bot de Entrada em Grupos do WhatsApp")
root.geometry("400x200")

tk.Label(root, text="Escolha o arquivo Excel com os links:").pack(pady=10)

entry_arquivo = tk.Entry(root, width=40)
entry_arquivo.pack(pady=5)

btn_escolher = tk.Button(root, text="Selecionar Arquivo", command=escolher_arquivo)
btn_escolher.pack(pady=5)

btn_iniciar = tk.Button(root, text="Iniciar Automação", command=iniciar_automacao, bg="green", fg="white")
btn_iniciar.pack(pady=10)

root.mainloop()
