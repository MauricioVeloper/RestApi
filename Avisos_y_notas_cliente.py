import requests
import tkinter as tk
from tkinter import messagebox, simpledialog

API_URL = "http://127.0.0.1:8000/avisos"

# Función para cargar avisos
def cargar_avisos():
    response = requests.get(API_URL)
    if response.status_code == 200:
        avisos = response.json()
        listbox.delete(0, tk.END)
        for aviso in avisos:
            listbox.insert(tk.END, f"{aviso['id']} - {aviso['titulo']}")

# Función para agregar un aviso
def agregar_aviso():
    titulo = simpledialog.askstring("Nuevo Aviso", "Ingrese el título:")
    contenido = simpledialog.askstring("Nuevo Aviso", "Ingrese el contenido:")
    if titulo and contenido:
        response = requests.post(API_URL, json={"titulo": titulo, "contenido": contenido})
        if response.status_code == 200:
            cargar_avisos()

# Función para eliminar un aviso
def eliminar_aviso():
    seleccion = listbox.curselection()
    if seleccion:
        aviso_id = listbox.get(seleccion[0]).split(" - ")[0]
        response = requests.delete(f"{API_URL}/{aviso_id}")
        if response.status_code == 200:
            cargar_avisos()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el aviso")

# Crear ventana
root = tk.Tk()
root.title("Cliente de Avisos")

frame = tk.Frame(root)
frame.pack(pady=10)

listbox = tk.Listbox(frame, width=50, height=10)
listbox.pack()

btn_cargar = tk.Button(root, text="Cargar Avisos", command=cargar_avisos)
btn_cargar.pack(pady=5)

btn_agregar = tk.Button(root, text="Agregar Aviso", command=agregar_aviso)
btn_agregar.pack(pady=5)

btn_eliminar = tk.Button(root, text="Eliminar Aviso", command=eliminar_aviso)
btn_eliminar.pack(pady=5)

cargar_avisos()
root.mainloop()
