import os #Biblioteca para importar o comando 'CLS'
from time import sleep
import mysql.connector
from tkinter import *
from tkinter import messagebox

def Entrada_Dados_Anatel():
	janela2 = Tk();
	janela2.geometry("300x160");
	janela2.title("Entrada de Dados");

	textExample = Label(janela2, text = "Velocidade de Download contratada:");
	textExample.pack();
	
	textExample2 = Text(janela2, height = 2, padx = 3, pady = 3);
	textExample2.pack();

	textExample3 = Label(janela2, text = "Velocidade de Upload contratada:");
	textExample3.pack();

	textExample4 = Text(janela2, height = 2, padx = 3, pady = 3);
	textExample4.pack();

	btnRead = Button(janela2, height = 1, width = 10, padx = 5, pady = 5, text = "Verificar",
	command = lambda: Verificar_Condicao_Anatel(textExample2.get("1.0","end"), textExample4.get("1.0","end")));
	btnRead.pack();

def Verificar_Condicao_Anatel(Vel_Down_Contratada, Vel_Up_Contratada, velocidade_download, velocidade_upload):
	try:
		Vel_Down_Contratada = abs(float(Vel_Down_Contratada));
		Vel_Up_Contratada = abs(float(Vel_Up_Contratada));
	except Exception as erro:
		messagebox.showinfo(title = "Erro", message = "Falha ao obter os números. Por favor,\ntente novamente!");
		print(f"Falha ao obter números. O erro foi {erro.__class__}!");
		print(f"Por favor, tente novamente em alguns momentos...");
		return 0;

	if(velocidade_download >= Vel_Down_Contratada * 0.8):
		messagebox.showinfo(title = "Requisito de Download", message =
		"A velocidade de download atingiu pelo menos\no mínimo dos 80% da velocidade contratada.\nLogo, este requisto da ANATEL foi cumprido!");
	else:
		messagebox.showinfo(title = "Requisito de Download", message = 
		"A velocidade de download não atingiu pelo menos\no mínimo dos 80% da velocidade contratada.\nPortanto, este requisito da ANATEL não foi cumprido!");
	
	if(velocidade_upload >= Vel_Up_Contratada * 0.8):
		messagebox.showinfo(title = "Requisito de Upload", message = 
		"A velocidade de upload atingiu pelo menos\no mínimo dos 80% da velocidade contratada.\nLogo, este requisto da ANATEL foi cumprido!");
	else:
		messagebox.showinfo(title = "Requisito de Upload", message = 
		"A velocidade de upload não atingiu pelo menos\no mínimo dos 80% da velocidade contratada.\nPortanto, este requisito da ANATEL não foi cumprido!");

def Verificar_Conexao_Jogos(ping, jitter):

	if(0 < ping < 60):
		print("\nEsta internet possuí uma boa latência para jogar em servidores próximos\n");
	elif (60 <= ping < 100):
		print("\nEsta internet possuí uma latência razoável para jogar em servidores próximos\n");
	else:
		print("\nNão é recomendável utilizar esta internet para jogos online!\n");

	if(0 < jitter < 20):
		print(f"\nEsta internet possui uma um jitter ideal para jogar em servidores próximos\n");
	elif(20 <= jitter):
		print("\nEsta internet possuí um jitter razoável para jogar em servidores próximos\n");
	else:
		print("\nEsta internet pode apresentar muitas inconsistências na conexão, seu jitter não é bom!\n");

	input('Pressione qualquer tecla para continuar');
	os.system("cls");

def Verificar_Velocidade_Media():
	db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '1234', database = 'Resultado_testes');
	cursor = db_connection.cursor();
	sql = ("SELECT AVG(Download), AVG(Upload), AVG(Ping), AVG(Jitter) FROM Resultados");
	cursor.execute(sql);

	for(Download, Upload, Ping, Jitter) in cursor:
		print('\n\n'); #quebra de linha
		print(f'Média de Download: {Download:.02f} Mbps');
		print(f'Média de Upload: {Upload:.02f} Mbps');
		print(f'Média da Latência (Ping): {Ping:.02f} ms');
		print(f'Média do Jitter: {Jitter:.02f} ms');
		print('\n');

	cursor.close();
	db_connection.close();

	input('Pressione qualquer tecla para continuar');
	os.system("cls");