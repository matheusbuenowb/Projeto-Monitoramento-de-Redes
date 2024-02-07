from tkinter import *
import os
from tkinter import messagebox
from time import sleep 
from datetime import date
from Functions.ObterResultados import Imprime_Resultados
import mysql
from Functions.Teste import Teste_Internet

def Entrada_Dados_Monitoramento():
	janela = Tk();
	janela.geometry("375x200");
	janela.title("Entrada de Dados");

	textExample = Label(janela, text = "Digite quantos testes deseja realizar:\n(Exemplo: '10' ou '100')");
	textExample.pack();
	
	textExample2 = Text(janela, height=2, padx = 3, pady = 3);
	textExample2.pack();

	textExample3 = Label(janela, text = 
	"Digite qual será o intervalo em minutos entre os testes:\n(Exemplo: para uma pausa de 1 hora, digite '60')");
	textExample3.pack();

	textExample4 = Text(janela, height=2, padx = 3, pady = 3);
	textExample4.pack();

	btnRead = Button(janela, height=1, width=10, padx = 5, pady = 5, text="Iniciar", command =
	lambda: Monitorar_Segundo_Plano(textExample2.get("1.0","end"), textExample4.get("1.0","end")));
	btnRead.pack();

def Monitorar_Segundo_Plano(quantidade_testes, intervalo_minutos):

	nome = "Resultados";	

	try:
		quantidade_testes = int(quantidade_testes);
		intervalo_minutos = int(intervalo_minutos);
	except Exception as erro:
		messagebox.showinfo(title = "Erro", message = "Falha ao obter os números\nTente novamente!");
		print(f"Falha ao obter números. O erro foi {erro.__class__}!");
		print(f"Por favor, tente novamente em alguns momentos...");
		sleep(2);
		os.system("cls");
		return 0;

	messagebox.showinfo(title = "AVISO", message = 
	"O monitoramento irá começar logo após\n clicar em ok! Por favor, aguarde até que o processo finalize!\n");	
	Efetuar_Teste_Monitoramento(quantidade_testes, intervalo_minutos, nome);
		
	os.system("cls");
	print("Testes finalizados. A tela limpará em 3 segundos.");
	sleep(3);

def Efetuar_Teste_Monitoramento(quantidade_testes, intervalo_minutos, nome):

	for q in range(quantidade_testes):
		data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter = Teste_Internet();
		db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '1234', database = 'Resultado_testes');
		cursor = db_connection.cursor();
		sql = (f"INSERT INTO {nome} (Data, Horário, Download, Upload, Ping, Jitter) VALUES (%s, %s, %s, %s, %s, %s)");
		values = (data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter);
		cursor.execute(sql, values);
		current_date = date.today();
		formatted_date = current_date.strftime('%d/%m/%Y');

		db_connection.commit();

		cursor.close();
		db_connection.close();

		if (q + 1) < quantidade_testes:
			sleep(intervalo_minutos * 60); #60 segundos
		else:
			Imprime_Resultados(q, data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter);	
	
		os.system("cls");	