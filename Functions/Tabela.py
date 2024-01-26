import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection);
from tkinter import *
from tkinter import messagebox
import os #Biblioteca para importar o comando 'CLS'

def Criar_Tabela(nome):

	db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '', database = 'Resultado_testes');
	cursor = db_connection.cursor();
	sql = (f"CREATE TABLE `{nome}`(  `Teste` SERIAL PRIMARY KEY,`Data` VARCHAR(20) NOT NULL ,`Horário` VARCHAR(30) NOT NULL,`Download` VARCHAR(20) NOT NULL,`Upload` VARCHAR(20) NOT NULL,`Ping` VARCHAR(20) NOT NULL,`Jitter` VARCHAR(20) NOT NULL  )");
	
	try:
		cursor.execute(sql);
	except Exception as erro:
		messagebox.showinfo(title = "Erro", message = 
		"A tabela digitada já existe. Por favor, digite um nome\ndiferente na próxima tentativa!")
		print(nome);
		print(f"Falha ao obter números. O erro foi {erro.__class__}!");
		print(f"Por favor, tente novamente em alguns momentos...");
		return 0;

	cursor.close();
	db_connection.close();

	messagebox.showinfo(title ="Mensagem de notificação", message = "Tabela criada com sucesso!");

	input('Pressione qualquer tecla para continuar');
	os.system("cls");	