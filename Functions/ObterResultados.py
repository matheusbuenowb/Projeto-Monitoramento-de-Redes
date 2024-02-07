from tkinter import *
import os
import mysql

def Imprime_Resultados(q, data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter):
	janela2 = Tk();
	janela2.geometry("300x160");
	janela2.title("Resultados do teste");

	texto = f'''\n  
    Data: {data_atual}
    Horário: {hora_atual}
    Velocidade de Download: {velocidade_download:.02f} Mbps
    Velocidade de Upload: {velocidade_upload:.02f} Mbps  
    Ping: {ping:.02f} ms 
    Jitter: {jitter:.02f} ms'''

	#texto_print["text"] = texto;

	texto_print = Label(janela2, text = texto);
	texto_print.grid(column = 0, row = 2, padx = 30);

	input('Pressione qualquer tecla para continuar');
	os.system("cls");	

def Melhores_Piores_Horarios():
	db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '1234', database = 'Resultado_testes');

	cursor = db_connection.cursor();
	cursor2 = db_connection.cursor();
	cursor3 = db_connection.cursor();
	cursor4 = db_connection.cursor();

	sql = ("SELECT Data, Horário, Download, Upload from resultados order by Download DESC LIMIT 3"); 
	sql2 = ("SELECT Data, Horário, Download, Upload from resultados order by Upload DESC LIMIT 3"); 
	sql3 = ("SELECT Data, Horário, Download, Upload from resultados order by Download ASC LIMIT 3");
	sql4 = ("SELECT Data, Horário, Download, Upload from resultados order by Upload ASC LIMIT 3");


	cursor.execute(sql);

	janela = Tk();
	janela.geometry("500x370");
	janela.title("Melhores e piores horários");

	cont_aux = 1;

	texto_descricao = Label(janela, text = "Melhores testes de download:");
	texto_descricao.grid(column = 0, row = 0, padx = 5, pady = 5);
	texto_descricao = Label(janela, text = "Data | Horário | Download | Upload");
	texto_descricao.grid(column = 0, row = 1, padx = 5, pady = 5);

	for (Linha) in cursor:
		texto_print = Label(janela, text = f"{cont_aux}º : {Linha} ");
		texto_print.grid(column = 0, row = (2 + cont_aux), padx = 5, pady = 5);	
		print(f'\n{cont_aux}º : {Linha}');
		cont_aux += 1;

	cursor.close();

	cursor3.execute(sql3);

	cont_aux = 1;

	texto_descricao = Label(janela, text = "Piores testes de download:");
	texto_descricao.grid(column = 1, row = 0, padx = 5, pady = 5);
	texto_descricao = Label(janela, text = "Data | Horário | Download | Upload");
	texto_descricao.grid(column = 1, row = 1, padx = 5, pady = 5)

	for (Linha) in cursor3:
		texto_print = Label(janela, text = f"{cont_aux}º : {Linha} ");
		texto_print.grid(column = 1, row = (2 + cont_aux), padx = 5, pady = 5);	
		print(f'\n{cont_aux}º : {Linha}');
		cont_aux += 1;	

	cursor3.close();

	cursor2.execute(sql2);

	cont_aux = 1;

	texto_descricao = Label(janela, text = "Melhores testes de Upload:");
	texto_descricao.grid(column = 0, row = 7, padx = 5, pady = 5);
	texto_descricao = Label(janela, text = "Data | Horário | Download | Upload");
	texto_descricao.grid(column = 0, row = 8, padx = 5, pady = 5);

	for (Linha) in cursor2:
		texto_print = Label(janela, text = f"{cont_aux}º : {Linha} ");
		texto_print.grid(column = 0, row = (9 + cont_aux), padx = 5, pady = 5);	
		print(f'\n{cont_aux}º : {Linha}');
		cont_aux += 1;

	cursor2.close();

	cursor4.execute(sql4);

	cont_aux = 1;

	texto_descricao = Label(janela, text = "Piores testes de upload:");
	texto_descricao.grid(column = 1, row = 7, padx = 5, pady = 5);
	texto_descricao = Label(janela, text = "Data | Horário | Download | Upload");
	texto_descricao.grid(column = 1, row = 8, padx = 5, pady = 5)

	for (Linha) in cursor4:
		texto_print = Label(janela, text = f"{cont_aux}º : {Linha} ");
		texto_print.grid(column = 1, row = (9 + cont_aux), padx = 5, pady = 5);	
		print(f'\n{cont_aux}º : {Linha}');
		cont_aux += 1;	

	cursor4.close();

	db_connection.close();
