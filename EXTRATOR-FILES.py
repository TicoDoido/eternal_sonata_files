import os
import struct
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_files_from_container(container_path, output_dir):
    # Extract the container's base name without extension
    container_name = os.path.splitext(os.path.basename(container_path))[0]
    # Create a directory named after the container in the output directory
    container_output_dir = os.path.join(output_dir, container_name)
    os.makedirs(container_output_dir, exist_ok=True)
    
    try:
        with open(container_path, 'rb') as container:
            container.seek(8)
            num_files = struct.unpack('>I', container.read(4))[0]
            
            header_offset = 16
            
            for _ in range(num_files):
                container.seek(header_offset)
                
                filename = container.read(32).decode('utf-8').strip('\x00')
                file_start = struct.unpack('>I', container.read(4))[0]
                file_size = struct.unpack('>I', container.read(4))[0]
                
                header_offset += 48
                
                container.seek(file_start)
                file_data = container.read(file_size)
                
                full_output_path = os.path.join(container_output_dir, filename)
                os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
                
                with open(full_output_path, 'wb') as output_file:
                    output_file.write(file_data)
                
                print(f'Extraiu {filename} para {full_output_path}')
        
        messagebox.showinfo("Sucesso", "Arquivos extraídos com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def select_container():
    file_path = filedialog.askopenfilename(title="Selecione o arquivo", filetypes=[("Arquivos .files", "*.files"), ("Todos os Arquivos", "*.*")])
    if file_path:
        container_path.set(file_path)

def select_output_dir():
    dir_path = filedialog.askdirectory(title="Selecione o Diretório de Saída")
    if dir_path:
        output_dir.set(dir_path)

def start_extraction():
    if container_path.get() and output_dir.get():
        extract_files_from_container(container_path.get(), output_dir.get())
    else:
        messagebox.showwarning("Comando Faltando", "Por favor, selecione tanto o arquivo de contêiner quanto o diretório de saída.")

# Create the main window
root = tk.Tk()
root.title("Extrator de arquivos .files")

container_path = tk.StringVar()
output_dir = tk.StringVar()

# Create and place widgets
tk.Label(root, text="Arquivo .files:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(root, textvariable=container_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Escolher Arquivo", command=select_container).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Diretório de Saída:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
tk.Entry(root, textvariable=output_dir, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Escolher Diretório", command=select_output_dir).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Começar Extração", command=start_extraction).grid(row=2, column=1, padx=10, pady=20)

root.mainloop()
