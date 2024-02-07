import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection);
from tkinter import *
from tkinter import messagebox
import os #Biblioteca para importar o comando 'CLS'

def Criar_Tabela(nome):

	db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '1234', database = 'Resultado_testes');
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

def Entrada_Dados_Cria_Tabela():
	janela = Tk();
	janela.geometry("220x105");
	janela.title("");
	
	texto_print = Label(janela, text = "Digite o nome da tabela a ser criada: ");
	texto_print.grid(column = 0, row = 0, padx = 10, pady = 3);

	textoEntrada = Text(janela, height= 1, width = 20, padx = 3, pady = 3);
	textoEntrada.grid(column = 0, row = 1);

	btnRead = Button(janela, height = 1, width = 8, padx = 5, pady = 5, text="Criar tabela",
	command = lambda: Criar_Tabela(textoEntrada.get("1.0","end")));
	btnRead.grid(column = 0, row = 2);

def Entrada_Dados_Tabela():
	janela = Tk();
	janela.geometry("300x100");
	janela.title("Entrada de Dados");
	
	texto_print = Label(janela, text = "Digite o nome da tabela: ");
	texto_print.pack();

	textoEntrada = Text(janela, height= 1, width = 20, padx = 3, pady = 3);
	textoEntrada.pack();

	btnRead = Button(janela, height=1, width=5, padx = 5, pady = 5, text="Verificar", command = 
	lambda: Mostrar_Tabela(textoEntrada.get("1.0","end")));
	btnRead.pack()


def Mostrar_Tabela(nome):

	nome = str(nome);
	db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '1234', database = 'Resultado_testes');
	cursor = db_connection.cursor();
	sql = (f"SELECT * FROM resultado_testes.{nome};");

	try:
		cursor.execute(sql);
	except Exception as erro:
		messagebox.showinfo(title = "Erro", message = 
		"A tabela digitada não existe. Por favor, digite uma tabela\nválida na próxima tentativa!")
		print(f"A tabela digitada não existe. Por favor, digite uma tabela válida na próxima tentativa!");
		return 0;

	janela = Tk();
	janela.geometry("500x320");
	janela.title("Resultados dos testes");

	cont_aux = 1;

	texto_descricao = Label(janela, text = "Data | Horário | Download | Upload | Ping | Jitter");
	texto_descricao.grid(column = 0, row = 0, padx = 5, pady = 5)

	for (Linha) in cursor:
		texto_print = Label(janela, text = f"Teste {cont_aux}: {Linha} ");
		texto_print.grid(column = 0, row = (1 + cont_aux), padx = 5, pady = 5);	
		print(f'\nTeste {cont_aux} : {Linha}');
		cont_aux += 1;

	cursor.close();
	db_connection.close();

	input('Pressione qualquer tecla para continuar');
	os.system("cls");	