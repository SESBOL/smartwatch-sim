# Smartwatch Simulator
Programa feito em Python para simular as propriedades de um Smartwatch e enviar suas informações por um tráfego de rede. </br>

# Compilando o Projeto
1. Instale o Python (https://www.python.org/downloads/) </br>
2. Instale as seguintes bibliotecas através do comando no terminal: **pip install flask-socketio requests pillow** </br>

# Executando o Projeto
<p align="center">
<img src="https://github.com/user-attachments/assets/c43dbbe5-96f6-4c9f-bed8-95a4bcc4a4e4"/> </br>
Insira um valor de IMEI para o dispositivo smartwatch simulado e selecione o formato gráfico do smartwatch.
</p> </br>
<p align="center">
<img src="https://github.com/user-attachments/assets/47763f92-338f-4add-910c-34434a0cf309"/> </br>
As informações gráficas do smartwatch são geradas aleatoriamente ao aparecerem em tela.
</p> </br>
<p align="center">
<img src="https://github.com/user-attachments/assets/fd96a6d0-a869-474c-a25b-ac6c23adf89e"/> </br>
À partir da porta "http://localhost:5000" em diante (somando-se um), todos os smartwatches irão transmitir seus dados pela rede.
</p> </br>
<p align="center">
<img src="https://github.com/user-attachments/assets/d0855910-6643-4618-9929-2e2b7796c330"/> </br>
Observação: Caso tente iniciar outro smartwatch com o mesmo IMEI, o programa irá imediatamente rejeitá-lo.
</p>
