import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import os  

class PipelineInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Painel de Controle do Pipeline de Cervejarias")
        self.root.geometry("800x600")
        
        # Configuração do estilo
        self.root.configure(bg='#f0f0f0')
        button_font = ('Arial', 10, 'bold')
        
        # Frame principal
        main_frame = tk.Frame(root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Pipeline de Dados de Cervejarias",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            pady=10
        )
        title_label.pack()
        
        # Frame dos botões
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        # Botões de teste
        self.create_button(button_frame, "Testar Consumidor API", 
                         lambda: self.run_script("test_consumidor_api.py"), 
                         '#4a6baf', button_font).grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        self.create_button(button_frame, "Testar Transformação", 
                         lambda: self.run_script("test_transformacao.py"), 
                         '#4a6baf', button_font).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        self.create_button(button_frame, "Testar Qualidade", 
                         lambda: self.run_script("test_verificacao_qualidade.py"), 
                         '#4a6baf', button_font).grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        
        self.create_button(button_frame, "Testar Monitoramento", 
                         lambda: self.run_script("test_monitoramento.py"), 
                         '#4a6baf', button_font).grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Botão de visualização
        self.create_button(main_frame, "Visualizar Dados", 
                         lambda: self.run_script("visualizar_dados.py"), 
                         '#2e7d32', button_font).pack(pady=10, fill=tk.X)
        
        # Área de saída
        output_label = tk.Label(
            main_frame, 
            text="Saída:", 
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            anchor='w'
        )
        output_label.pack(fill=tk.X)
        
        self.output_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=('Consolas', 9)
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = tk.Label(
            root, 
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#e0e0e0'
        )
        status_bar.pack(fill=tk.X)
        
    def create_button(self, parent, text, command, color, font):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            activebackground=color,
            activeforeground='white',
            font=font,
            padx=10,
            pady=5,
            relief=tk.RAISED,
            bd=2
        )
    
    def run_script(self, script_name):
        self.output_area.insert(tk.END, f"\n=== Executando {script_name} ===\n")
        self.output_area.see(tk.END)
        self.status_var.set(f"Executando {script_name}...")
        
        # Desabilitar botões durante a execução
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.DISABLED)
        
        # Executar em uma thread separada para não travar a interface
        threading.Thread(
            target=self.execute_python_script,
            args=(script_name,),
            daemon=True
        ).start()
    
    def execute_python_script(self, script_name):
        try:
            # Configurar ambiente para UTF-8
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
        
            if script_name.endswith('.py'):
                if script_name.startswith('test_'):
                    command = f"python -m pytest testes/{script_name} -v"
                else:
                    command = f"python {script_name}"
            
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    env=env
                            )
                
                # Ler a saída em tempo real
                while True:
                    output = process.stdout.readline()
                    error = process.stderr.readline()
                    
                    if output == '' and error == '' and process.poll() is not None:
                        break
                    
                    if output:
                        self.output_area.insert(tk.END, output)
                        self.output_area.see(tk.END)
                    if error:
                        self.output_area.insert(tk.END, f"ERRO: {error}")
                        self.output_area.see(tk.END)
                
                return_code = process.poll()
                
                if return_code == 0:
                    self.output_area.insert(tk.END, f"\n{script_name} concluído com sucesso!\n")
                else:
                    self.output_area.insert(tk.END, f"\n{script_name} falhou com código {return_code}\n")
                
        except Exception as e:
            self.output_area.insert(tk.END, f"\nErro ao executar {script_name}: {str(e)}\n")
        finally:
            self.output_area.see(tk.END)
            self.status_var.set("Pronto")
            
            # Reabilitar botões
            self.root.after(100, self.enable_buttons)
    
    def enable_buttons(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = PipelineInterface(root)
    root.mainloop()