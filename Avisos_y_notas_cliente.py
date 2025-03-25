import requests
import tkinter as tk
from tkinter import messagebox, simpledialog

API_URL = "http://192.168.106.123:8000/avisos"  # Asegúrate de que la IP y puerto sean correctos

# Función para cargar avisos desde el servidor
def cargar_avisos():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Verifica errores HTTP
        avisos = response.json()
        listbox.delete(0, tk.END)  # Limpiar la lista actual
        
        # Mostrar solo avisos con estructura válida
        for aviso in avisos:
            if "id" in aviso and "titulo" in aviso:  # Verificar campos requeridos
                listbox.insert(tk.END, f"{aviso['id']} - {aviso['titulo']}")
            else:
                print(f"⚠ Aviso omitido (estructura inválida): {aviso}")  # Depuración
                
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudieron cargar los avisos:\n{str(e)}")

# Función para agregar un nuevo aviso
def agregar_aviso():
    titulo = simpledialog.askstring("Nuevo Aviso", "Ingrese el título:")
    contenido = simpledialog.askstring("Nuevo Aviso", "Ingrese el contenido:")
    
    if titulo and contenido:  # Solo proceder si ambos campos tienen datos
        try:
            response = requests.post(
                API_URL,
                json={"titulo": titulo, "contenido": contenido}
            )
            response.raise_for_status()
            cargar_avisos()  # Recargar la lista después de agregar
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422:
                messagebox.showerror("Error", "Datos inválidos. Revise el formato.")
            else:
                messagebox.showerror("Error", f"Error del servidor:\n{str(e)}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor:\n{str(e)}")

# Función para eliminar un aviso seleccionado
def eliminar_aviso():
    seleccion = listbox.curselection()
    if seleccion:  # Verificar si hay un elemento seleccionado
        aviso_id = listbox.get(seleccion[0]).split(" - ")[0]  # Extraer el ID
        
        try:
            response = requests.delete(f"{API_URL}/{aviso_id}")
            response.raise_for_status()
            cargar_avisos()  # Recargar la lista después de eliminar
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo eliminar el aviso:\n{str(e)}")
    else:
        messagebox.showwarning("Advertencia", "Seleccione un aviso para eliminar.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestor de Avisos")
root.geometry("400x300")

# Frame para la lista de avisos
frame = tk.Frame(root)
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Listbox para mostrar los avisos
listbox = tk.Listbox(
    frame,
    width=50,
    height=10,
    font=("Arial", 10)
)
listbox.pack(fill=tk.BOTH, expand=True)

# Barra de desplazamiento
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Botones
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

btn_cargar = tk.Button(
    btn_frame,
    text="Actualizar Avisos",
    command=cargar_avisos,
    width=15
)
btn_cargar.pack(side=tk.LEFT, padx=5)

btn_agregar = tk.Button(
    btn_frame,
    text="Agregar Aviso",
    command=agregar_aviso,
    width=15
)
btn_agregar.pack(side=tk.LEFT, padx=5)

btn_eliminar = tk.Button(
    btn_frame,
    text="Eliminar Aviso",
    command=eliminar_aviso,
    width=15
)
btn_eliminar.pack(side=tk.LEFT, padx=5)

# Cargar avisos al iniciar
cargar_avisos()

# Iniciar la aplicación
root.mainloop()