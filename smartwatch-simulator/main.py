import tkinter as tk
from tkinter import messagebox
import subprocess
import signal

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu de Emulação")
        self.root.iconbitmap("wear-os.ico")
        self.root.resizable(False, False)

        # Centralizar a janela
        self.center_window()

        # Campo de texto para inserir o IMEI
        self.imei_label = tk.Label(root, text="IMEI:")
        self.imei_label.pack()
        self.imei_entry = tk.Entry(root, width=20)
        self.imei_entry.pack()

        # Botões para iniciar o smartwatch-simulator.py
        self.button1 = tk.Button(root, text="Smartwatch Quadrado", command=self.start_simulator_clock1, height = 2, width = 50)
        self.button1.pack()

        self.button2 = tk.Button(root, text="Smartwatch Arredondado", command=self.start_simulator_clock2, height = 2, width = 50)
        self.button2.pack()

        # Lista de subprocessos
        self.subprocesses = []

        # Configurar a função de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self):
        # Obter as dimensões da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Obter as dimensões da janela
        window_width = 270  # Defina a largura da janela
        window_height = 120  # Defina a altura da janela

        # Calcular a posição x e y
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Definir o tamanho e a posição da janela
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def start_simulator_clock1(self):
        self.start_simulator('clock-1.png')

    def start_simulator_clock2(self):
        self.start_simulator('clock-2.png')

    def start_simulator(self, clock_image):
        imei = self.imei_entry.get().strip()
        if not imei:
            messagebox.showwarning("Aviso", "Por favor, insira um IMEI.")
            return

        if not imei.isdigit():
            messagebox.showwarning("Aviso", "O IMEI deve ser um número inteiro.")
            return

        if self.is_imei_running(imei):
            messagebox.showwarning("Aviso", f"Um simulador com o IMEI {imei} já está em execução.")
            return

        try:
            # Iniciar o smartwatch-simulator.py com os parâmetros desejados
            proc = subprocess.Popen(
                ['python', 'smartwatch-simulator.py', clock_image, imei],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.subprocesses.append((proc, imei))
            messagebox.showinfo("Sucesso", f"Simulador iniciado com o IMEI {imei}.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível iniciar o simulador: {e}")

    def is_imei_running(self, imei):
        for proc, running_imei in self.subprocesses:
            if running_imei == imei and proc.poll() is None:
                return True
        return False
        
    def terminate_process(self, proc):
        try:
            # Encerrar o subprocesso
            proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=5)  # Aguarda até 5 segundos para o processo terminar
        except subprocess.TimeoutExpired:
            # Forçar a finalização se o processo não terminar a tempo
            proc.kill()
            proc.wait()
        except Exception as e:
            print(f"Erro ao encerrar o subprocesso: {e}")

    def on_close(self):
        # Encerrar todos os subprocessos
        for proc, _ in self.subprocesses:
            self.terminate_process(proc)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
