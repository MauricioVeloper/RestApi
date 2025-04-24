import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://192.168.100.199:5000/avisos"  

def obtener_avisos():
    try:
        respuesta = requests.get(API_URL)
        if respuesta.status_code == 200:
            lista_avisos.delete(0, tk.END)  
            for aviso in respuesta.json():
                lista_avisos.insert(tk.END, f"ID {aviso['id']}: {aviso['mensaje']}")
        else:
            messagebox.showerror("Error", "No se pudieron obtener los avisos")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor: {e}")

def agregar_aviso():
    mensaje = entrada_mensaje.get()
    if mensaje:
        try:
            respuesta = requests.post(API_URL, json={"mensaje": mensaje})
            if respuesta.status_code == 201:
                messagebox.showinfo("Éxito", "Aviso agregado correctamente")
                obtener_avisos()
                entrada_mensaje.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo agregar el aviso")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor: {e}")
    else:
        messagebox.showwarning("Advertencia", "Ingresa un mensaje")

def actualizar_aviso():
    seleccionado = lista_avisos.curselection()
    if seleccionado:
        aviso_texto = lista_avisos.get(seleccionado[0])
        aviso_id = aviso_texto.split(":")[0].replace("ID", "").strip()  # Extrae el ID correctamente
        nuevo_mensaje = entrada_mensaje.get()

        if nuevo_mensaje:
            url = f"{API_URL}/{aviso_id}"
            try:
                respuesta = requests.put(url, json={"mensaje": nuevo_mensaje})
                if respuesta.status_code == 200:
                    messagebox.showinfo("Éxito", "Aviso actualizado correctamente")
                    obtener_avisos()
                    entrada_mensaje.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", f"No se pudo actualizar el aviso (Código {respuesta.status_code})")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor: {e}")
        else:
            messagebox.showwarning("Advertencia", "Debes ingresar un mensaje nuevo")
    else:
        messagebox.showwarning("Advertencia", "Selecciona un aviso para actualizar")

def eliminar_aviso():
    seleccionado = lista_avisos.curselection()
    if seleccionado:
        aviso_texto = lista_avisos.get(seleccionado[0])
        aviso_id = aviso_texto.split(":")[0].replace("ID", "").strip()  # Extrae el ID correctamente

        url = f"{API_URL}/{aviso_id}"
        try:
            respuesta = requests.delete(url)
            if respuesta.status_code == 200:
                messagebox.showinfo("Éxito", "Aviso eliminado correctamente")
                obtener_avisos()
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el aviso (Código {respuesta.status_code})")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor: {e}")
    else:
        messagebox.showwarning("Advertencia", "Selecciona un aviso para eliminar")

# Interfaz gráfica
root = tk.Tk()
root.title("Cliente de Avisos")

frame = tk.Frame(root)
frame.pack(pady=10)

lista_avisos = tk.Listbox(frame, width=50, height=10)
lista_avisos.pack(side=tk.LEFT)

scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=lista_avisos.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
lista_avisos.config(yscrollcommand=scroll.set)

entrada_mensaje = tk.Entry(root, width=50)
entrada_mensaje.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

btn_obtener = tk.Button(btn_frame, text="Obtener Avisos", command=obtener_avisos)
btn_obtener.grid(row=0, column=0, padx=5)

btn_agregar = tk.Button(btn_frame, text="Agregar Aviso", command=agregar_aviso)
btn_agregar.grid(row=0, column=1, padx=5)

btn_actualizar = tk.Button(btn_frame, text="Actualizar Aviso", command=actualizar_aviso)
btn_actualizar.grid(row=0, column=2, padx=5)

btn_eliminar = tk.Button(btn_frame, text="Eliminar Aviso", command=eliminar_aviso)
btn_eliminar.grid(row=0, column=3, padx=5)

obtener_avisos()  # Cargar avisos al iniciar

root.mainloop()
