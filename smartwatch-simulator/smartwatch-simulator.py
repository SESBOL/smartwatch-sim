from tkinter import Canvas
from PIL import Image, ImageTk
from flask import Flask, jsonify
import socket, errno
import tkinter as tk
import time
import random
import threading
import sys

# Inicializa o Flask
flask_app = Flask(__name__)

# Dados iniciais
data = {
    'imei': '',
    'date': '',
    'time': '',
    'bpm': 0,
    'mmhg': '0/0',
    'temperature': '0°C'
}

@flask_app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

class DynamicOverlayApp:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Wear OS")

        # Definir o ícone da aplicação
        self.root.iconbitmap("wear-os.ico")
        
        # Desabilitar o redimensionamento de janela
        self.root.resizable(False, False)
        
        # Carregar e redimensionar a imagem do aparelho
        self.image = Image.open(image_path)
        original_size = self.image.size
        new_size = (original_size[0] // 3, original_size[1] // 3)
        self.image = self.image.resize(new_size, Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Criar um canvas para exibir o aparelho
        self.canvas = Canvas(root, width=new_size[0], height=new_size[1])
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

############################ EXIBIÇÃO DE INFORMAÇÕES ###########################

        # Carregar e redimensionar a imagem adicional
        self.additional_image = Image.open(additional_image_path)
        additional_size = (20, 20)
        self.additional_image = self.additional_image.resize(additional_size, Image.LANCZOS)
        self.tk_additional_image = ImageTk.PhotoImage(self.additional_image)

        # Adicionar a imagem adicional ao Canvas
        if image_path == 'clock-1.png':
            self.canvas.create_image(
                new_size[0] // 2 - 10,  # Posição x
                new_size[1] // 2 - 93,  # Posição y
                anchor=tk.NW,
                image=self.tk_additional_image
            )
        elif image_path == 'clock-2.png':
            self.canvas.create_image(
                new_size[0] // 2 - 10,  # Posição x
                new_size[1] // 2 - 73,  # Posição y
                anchor=tk.NW,
                image=self.tk_additional_image
            )

        # Exibir a data atual na tela do aparelho
        self.date_text_id = self.canvas.create_text(
            new_size[0] // 2, new_size[1] // 4 + 45,  # Ajustar a posição para cima da hora
            text="", fill="white", font=("Arial", 8)
        )

        # Exibir a hora atual na tela do aparelho
        self.hour_text_id = self.canvas.create_text(
            new_size[0] // 2, new_size[1] // 2 - 5,
            text="", fill="white", font=("Arial", 24)
        )

        # Exibir um grid de dados abaixo da hora atual
        self.grid_text_ids = []
        grid_start_y = new_size[1] // 2 + 40 #Ajuste global vertical
        grid_spacing = new_size[0] // 4 #Ajuste global horizontal

        # Exibir o valor de batimentos cardiacos
        bpm_text_id = self.canvas.create_text(
            new_size[0] // 2 - grid_spacing,
            grid_start_y,
            text="", fill="white", font=("Arial", 8)
        )
        self.grid_text_ids.append(bpm_text_id)

        # Exibir o valor de pressao arterial
        mmhg_text_id = self.canvas.create_text(
            new_size[0] // 1.92,
            grid_start_y,
            text="", fill="white", font=("Arial", 8)
        )
        self.grid_text_ids.append(mmhg_text_id)

        # Exibir o valor de temperatura corporal
        temperature_text_id = self.canvas.create_text(
            new_size[0] // 2 + grid_spacing,
            grid_start_y,
            text="", fill="white", font=("Arial", 8)
        )
        self.grid_text_ids.append(temperature_text_id)

######################### ATUALIZAÇÃO DE INFORMAÇÕES ###########################

        # Atualizar a data do aparelho
        self.update_date()

        # Atualizar a hora do aparelho
        self.update_time()

        # Atualizar os dados de batimento cardiaco do aparelho
        self.bpm_value = random.randint(30, 140)
        self.update_bpm()

        # Atualizar os dados de pressao sanguinea do aparelho
        self.mmhg_value = [60, 120]
        self.update_mmhg()

        # Atualizar os dados de temperatura do aparelho
        self.temperature_value = random.randint(40, 100)
        self.update_temperature()

        flask_thread = threading.Thread(target=self.start_flask_server)
        flask_thread.daemon = True
        flask_thread.start()

############################### DEFINIÇÃO DE MÉTODOS ###########################

    def update_date(self):
        current_date = time.strftime("%A, %d/%m/%Y")
        self.canvas.itemconfig(self.date_text_id, text=current_date)
        data['date'] = current_date
        self.root.after(1000, self.update_date)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.canvas.itemconfig(self.hour_text_id, text=current_time)
        data['time'] = current_time
        self.root.after(1000, self.update_time)

    def update_bpm(self):
        self.bpm_value += random.choice([-1, 1])
        self.bpm_value = max(30, min(self.bpm_value, 140))
        self.canvas.itemconfig(self.grid_text_ids[0], text=f"Bpm {self.bpm_value}")
        data['bpm'] = self.bpm_value
        self.root.after(5000, self.update_bpm)

    def update_mmhg(self):
        self.mmhg_value[0] += random.choice([-1, 1])
        self.mmhg_value[1] += random.choice([-1, 1])

        self.mmhg_value[0] = max(50, min(self.mmhg_value[0], 120))
        self.mmhg_value[1] = max(100, min(self.mmhg_value[1], 150))

        self.canvas.itemconfig(self.grid_text_ids[1], text=f"mmHg {self.mmhg_value[0]}/{self.mmhg_value[1]}")
        data['mmhg'] = f"{self.mmhg_value[0]}/{self.mmhg_value[1]}"
        self.root.after(60000, self.update_mmhg)

    def update_temperature(self):
        self.temperature_value += random.choice([-1, 1])
        self.temperature_value = max(40, min(self.temperature_value, 100))
        self.canvas.itemconfig(self.grid_text_ids[2], text=f"{self.temperature_value}°C")
        data['temperature'] = f"{self.temperature_value}°C"
        self.root.after(10000, self.update_temperature)

    # Encontrar portas disponiveis para execucao do servico
    def find_available_port(self, start_port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", start_port))
            s.close()
            return start_port
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                return self.find_available_port(start_port + 1)
            else:
                print(e)
                s.close()
                return None

    # Enviar dados para a porta 5000 ou superior
    def start_flask_server(self):
        new_port = self.find_available_port(5000)
        if new_port is None:
            sys.exit("No available port found, terminating the program.")
        flask_app.run(port=new_port)

################################ FUNÇÃO PRINCIPAL ##############################

# Criar a janela principal
root = tk.Tk()

# Caminhos para as imagens exibidas e o imei do dispositivo
image_path = sys.argv[1]
data['imei'] = sys.argv[2]
if image_path == 'clock-1.png':
    additional_image_path = 'gps-disabled-1.png'
elif image_path == 'clock-2.png':
    additional_image_path = 'gps-disabled-2.png'
    
# Rodando o aplicativo
app = DynamicOverlayApp(root, image_path)
root.mainloop()
