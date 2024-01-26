import socket; #Biblioteca para importar o ip interno do computador
import os #Biblioteca para importar o comando 'CLS'
from requests import get #Para obter um valor de um site
from tkinter import *

def Verificar_IP():

	janela = Tk();
	janela.geometry("150x75");
	janela.title("IP Externo e Interno");

	IP_Externo = get('https://api.ipify.org').text;
	texto_print = Label(janela, text = "IP Externo: " + IP_Externo);
	texto_print.grid(column = 0, row = 0, padx = 5, pady = 5);

	texto_print2 = Label(janela, text = "IP Interno: " + f"{socket.gethostbyname(socket.gethostname())}");
	texto_print2.grid(column = 0, row = 2, padx = 5, pady = 5);