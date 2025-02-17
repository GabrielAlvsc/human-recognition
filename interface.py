import tkinter as tk
from tkinter import messagebox
import psycopg2
import datetime
import subprocess
import sys


# Função para conectar ao banco de dados
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password="engcomp1413",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as error:
        messagebox.showerror("Erro de conexão", str(error))

# Função para inserir um novo telefone
def insert_phone():
    telefone = phone_entry.get()
    if telefone:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO telefones (telefone) VALUES (%s)", (telefone,))
        conn.commit()
        cur.close()
        conn.close()
        phone_entry.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Telefone cadastrado com sucesso!")
        list_phones()
    else:
        messagebox.showerror("Erro", "Digite um número de telefone!")

# Função para listar telefones cadastrados
def list_phones():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT telefone FROM telefones")
    records = cur.fetchall()
    listbox.delete(0, tk.END)
    for record in records:
        listbox.insert(tk.END, record[0])
    cur.close()
    conn.close()

# def run_open():
#     result = subprocess.call("py Open.py", shell=True)
#     print(result)
#     # z = subprocess.Popen("py Open.py", stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
#     # print(z)

# Interface gráfica
root = tk.Tk()
root.title("Cadastro de Telefones")

tk.Label(root, text="Inserir telefone de aviso:").pack(pady=(10, 0))
phone_entry = tk.Entry(root)
phone_entry.pack(pady=5)

tk.Button(root, text="Inserir", command=insert_phone).pack(pady=(5, 10))


#tk.Button(root, text="Rodar", command=run_open).pack(pady=(5, 10))

tk.Label(root, text="Números cadastrados:").pack(pady=(10, 0))
listbox = tk.Listbox(root, height=10, width=50)
listbox.pack(pady=5)

list_phones()

root.mainloop()
