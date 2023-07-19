import speedtest; #Biblioteca referente ao medidor de velocidade speedtest, o qual contém 3 funcionalidades fundamentais para o programa
from datetime import datetime #Biblioteca para obter informações a respeito do horário 
from time import sleep
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection);
from datetime import date
import os #Biblioteca para importar o comando 'CLS'
import socket; #Biblioteca para importar o ip interno do computador
from requests import get #Para obter uma requisição de um site
from tkinter import *
from tkinter import messagebox

def Efetuar_Teste():
	messagebox.showinfo(title = "AVISO", message = "O teste será inicializado após clicar\nem ok ou a aba ser fechada!");
	for q in range(quantidade_testes):
	    data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter = teste_internet();
	    db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '', database = 'Resultado_testes');
	    cursor = db_connection.cursor();
	    #Essa linha que diz em qual tabela será inserido os resultados no MySQL:
	    sql = "INSERT INTO brasilnet (Data, Horário, Download, Upload, Ping, Jitter) VALUES (%s, %s, %s, %s, %s, %s)"; 
	    values = (data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter);
	    cursor.execute(sql, values);
	    current_date = date.today();
	    formatted_date = current_date.strftime('%d/%m/%Y');

	    ImprimeResultados(q, data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter);
	    
	    db_connection.commit();
	    cursor.close();
	    db_connection.close();

	    os.system("cls");	

def Verificar_IP():

	janela = Tk();
	janela.geometry("150x75");
	janela.title("IP Externo e Interno");

	IP_Externo = get('https://api.ipify.org').text;
	texto_print = Label(janela, text = "IP Externo: " + IP_Externo);
	texto_print.grid(column = 0, row = 0, padx = 5, pady = 5);

	texto_print2 = Label(janela, text = "IP Interno: " + f"{socket.gethostbyname(socket.gethostname())}");
	texto_print2.grid(column = 0, row = 2, padx = 5, pady = 5);

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
	db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '', database = 'Resultado_testes');
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

def testa_Jitter():
	test = speedtest.Speedtest(); 
	ping_result = [0,0,0,0,0]; #é criado um vetor para armazenar os valores do ping
	jitter_result = [0,0,0,0]; #é criado um vetor para armazenar as variações entre (n - 1)... pings para o cálculo do jitter	 
	for c in range(0, 5):
		if(c == 0):
			best = test.get_best_server(); #é pego o melhor servidor baseado no quesito distância x ping
			print(f"Ping {c + 1} : {test.results.ping}");
			ping_result[c] = test.results.ping; #o valor do ping é adicionado ao vetor
		else:
			best = test.get_best_server();
			print(f"Ping {c + 1} : {test.results.ping}");
			ping_result[c] = test.results.ping; 
			jitter_result[c - 1] = abs(ping_result[c] - ping_result[c - 1]); #o valor pego entre a subtração da variação 
			#entre o ping (n - 1) é armazenado no vetor jitter_result, para que no final o resultado seja divido por 4,
			#que foi o valor optado para trabalhar neste programa
			#Utiliza a função abs para que a soma seja efetuada  

	jitter_final = (sum(jitter_result))/4; #a função sum soma todos os valores obtidos das variações obtidas das latências
	return jitter_final;	

def conecta_MySQL():
	try:
	    db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '', database = 'Resultado_testes'); 
	    #aqui é realizado a tentativa de conectar ao host local do computador
	    print("Conexão com o Banco de Dados feita com sucesso!");
	    return 1;
	except mysql.connector.Error as error:
		if error.errno == errorcode.ER_BAD_DB_ERROR:
		    print("O banco de dados não existe!"); #caso isso aconteça, é porque o banco de dados não existe
		else:
			print("O servidor do banco de dados está indisponível no momento!"); #o servidor está offline;
			return 0;
	else:
	    db_connection.close();


def teste_internet():
    # Instanciando a função de test do Speedtest
	teste = speedtest.Speedtest();
	print("\nCarregando a lista de servidores...");
	teste.get_servers(); #a função get_servers serve para obter as informações referentes ao servidores disponíveis
	print("\nEscolhendo o melhor servidor...");   
	melhor_servidor = teste.get_best_server(); 
	#o objeto melhor_servidor recebe o melhor servidor escolhido baseado na medida ping x distância
	print(f"\nMelhor servidor: {melhor_servidor['host']} localizado em {melhor_servidor['country']}\n");

    # Testando velocidades
	print('\nRealizando o teste de download...');
	velocidade_download = round(teste.download(threads=None)*(10**-6)) #armazena os dados do teste de download nesta variável
	# é dividido por 10^6 por conta do valor não ser retornado na medida de Mb/s (megabits por segundo) 
	print('\nRealizando o teste de upload...');
	velocidade_upload = round(teste.upload(threads=None)*(10**-6)); #armazena os dados do teste de upload nesta variável
	
	print('\nTestando a latência (ping)...');
	ping_result = round(teste.results.ping); #A função round serve para arrendodar as casas decimais
	#para que dessa forma o número final esteja com casas decimais satisfatórias.	
	print('\nCalculando o Jitter...');  
	jitter_result = round(testa_Jitter()); 

    # Capturando data e hora do teste através das funções da biblioteca datetime.
	data_atual = datetime.now().strftime('%d/%m/%Y');
	hora_atual = datetime.now().strftime('%H:%M');

	return data_atual, hora_atual, velocidade_download, velocidade_upload, ping_result, jitter_result;

def ImprimeResultados(q, data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter):
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
	command = lambda: VerificarCondicaoAnatel(textExample2.get("1.0","end"), textExample4.get("1.0","end")));
	btnRead.pack();

def VerificarCondicaoAnatel(Vel_Down_Contratada, Vel_Up_Contratada):
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
		messagebox.showinfo(title = "Análise do PING", message = 
		"Esta internet possuí uma boa latência para jogar em servidores próximos!");
	elif (60 <= ping < 100):
		messagebox.showinfo(title = "Análise do PING", message = 
		"Esta internet possuí uma latência razoável para jogar em servidores próximos!\nPode apenas apresentar um leve delay!");
	else:
		messagebox.showinfo(title = "Análise do PING", message = 
		"Esta internet possui uma alta latência para se conectar em servidores próximos!\nPortanto, pode apresentar um delay considerável!");

	if(0 < jitter < 20):
		messagebox.showinfo(title = "Análise do JITTER", message = 
		"Esta internet possui uma um jitter ideal para jogar em servidores próximos!\n");
	elif(50 <= jitter):
		messagebox.showinfo(title = "Análise do JITTER", message = 
		"Esta internet possuí um jitter razoável para jogar em servidores próximos\nPode apenas apresentar algumas leves travadas!");
	else:
		messagebox.showinfo(title = "Análise do JITTER", message = 
		"Esta internet pode apresentar muitas inconsistências na conexão, pois seu jitter não é o ideal\nTravadas podem ser bem frequentes!!");

def Verificar_Velocidade_Media():
	db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '', database = 'Resultado_testes');
	cursor = db_connection.cursor();
	sql = ("SELECT AVG(Download), AVG(Upload), AVG(Ping), AVG(Jitter) FROM Resultados");
	cursor.execute(sql);

	janela = Tk();
	janela.geometry("300x80");
	janela.title("Velocidade Média");

	for(Download, Upload, Ping, Jitter) in cursor:
		print('\n\n'); #quebra de linha
		texto = f'''Velocidade de Download: {Download:.02f} Mbps
    Velocidade de Upload: {Upload:.02f} Mbps  
    Ping: {Ping:.02f} ms 
    Jitter: {Jitter:.02f} ms'''
		texto_print = Label(janela, text = texto);
		#texto_print.grid(column = 0, row = 2, padx = 10, pady = 10);
		texto_print.pack();

		print(f'Média de Download: {Download:.02f} Mbps');
		print(f'Média de Upload: {Upload:.02f} Mbps');
		print(f'Média da Latência (Ping): {Ping:.02f} ms');
		print(f'Média do Jitter: {Jitter:.02f} ms');
		print('\n');

	cursor.close();
	db_connection.close();

	input('Pressione qualquer tecla para continuar');
	os.system("cls");


def Get_Dados_MySQL():
	db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '', database = 'Resultado_testes');
	cursor = db_connection.cursor();
	sql = ("SELECT AVG(Download), AVG(Upload), AVG(Ping), AVG(Jitter) FROM Resultados");
	cursor.execute(sql);
	for(Download, Upload, Ping, Jitter) in cursor:
		velocidade_download = float(Download);
		velocidade_upload = float(Upload);
		ping = float(Ping);
		jitter = float(Jitter);

	cursor.close();
	db_connection.close();
	return velocidade_download, velocidade_upload, ping, jitter;

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
	lambda: Monitorar_SegundoPlano(textExample2.get("1.0","end"), textExample4.get("1.0","end")));
	btnRead.pack();

def Monitorar_SegundoPlano(quantidade_testes, intervalo_minutos):

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
		data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter = teste_internet();
		db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '', database = 'Resultado_testes');
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
			ImprimeResultados(q, data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter);	
	
		os.system("cls");	


def Melhores_Piores_Horarios():
	db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '', database = 'Resultado_testes');

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


 # Definição de variáveis globais para usar a velocidade média de todos os testes já realizados

quantidade_testes = 1 #utilizado nas funções de teste
intervalo_minutos = 1 #utilizado nas funções de teste
velocidade_download = 0
velocidade_download = float(velocidade_download);
velocidade_upload = 0;
velocidade_upload = float(velocidade_upload);
ping = 0;
jitter = 0;


print('Inicializando o programa...\n');
sleep(1);

while(1):

	servidorEstado = 0; 

	servidor = conecta_MySQL(); #a variável irá receber um valor para indicar se a conexão foi estabelecida ou não

	if(servidor == 1):
		velocidade_download, velocidade_upload, ping, jitter = Get_Dados_MySQL();

		janela = Tk(); #é criado um objeto janela através da função da biblioteca Tkinter
		janela.title("Monitoramento de Qualidade de Internet"); #título da janela inicial do programa

		texto_MenuPrincipal = Label(janela, text="Bem-vindo ao Monitoramento de Qualidade de Internet. Selecione uma opção abaixo:");
		texto_MenuPrincipal.grid(column = 0, row = 0, padx = 20, pady = 20);

		botao_1 = Button(janela, text ="Inciar um teste", command = Efetuar_Teste);
		botao_1.grid(column = 0, row = 1, padx = 10, pady = 10);

		botao_2 = Button(janela, text ="Velocidade média", command = Verificar_Velocidade_Media);
		botao_2.grid(column = 0, row = 2, padx = 10, pady = 10);

		botao_3 = Button(janela, text ="Requisitos da ANATEL", command = Entrada_Dados_Anatel);
		botao_3.grid(column = 0, row = 3, padx = 10, pady = 10);

		botao_4 = Button(janela, text ="Análise do ping e jitter", command = lambda: Verificar_Conexao_Jogos(ping, jitter));
		botao_4.grid(column = 0, row = 4, padx = 10, pady = 10);

		botao_5 = Button(janela, text ="Resultados", command = Entrada_Dados_Tabela);
		botao_5.grid(column = 0, row = 5, padx = 10, pady = 10);

		botao_6 = Button(janela, text ="Criar tabela", command = Entrada_Dados_Cria_Tabela);
		botao_6.grid(column = 0, row = 6, padx = 10, pady = 10);

		botao_7 = Button(janela, text ="Obter IP", command = Verificar_IP);
		botao_7.grid(column = 0, row = 7, padx = 10, pady = 10);

		botao_8 = Button(janela, text ="Monitorar rede", command = Entrada_Dados_Monitoramento);
		botao_8.grid(column = 0, row = 8, padx = 10, pady = 10);

		botao_10 = Button(janela, text ="Detalhes", command = lambda: messagebox.showinfo(title = "Ajuda", message = 
		"Este comando irá efetuar um teste de velocidade!"));
		botao_10.grid(column = 1, row = 1, padx = 10, pady = 10);

		botao_11 = Button(janela, text ="Detalhes", command = lambda: messagebox.showinfo(title = "Ajuda", message = 
		"Este comando irá medir a velocidade média de\ntodos os testes salvos no banco de dados!"));
		botao_11.grid(column = 1, row = 2, padx = 10, pady = 10);

		botao_12 = Button(janela, text ="Detalhes", command = lambda: messagebox.showinfo(title = "Ajuda", message = 
		"Este comando irá verificar se a velocidade média\nestá condizente com os requisitos da ANATEL!"));
		botao_12.grid(column = 1, row = 3, padx = 10, pady = 10);

		botao_13 = Button(janela, text ="Detalhes", command = lambda: messagebox.showinfo(title = "Ajuda", message = 
		"Este comando irá verificar se o ping e o jitter\nestão adequados para uma jogantina tranquila!"));
		botao_13.grid(column = 1, row = 4, padx = 10, pady = 10);

		botao_14 = Button(janela, text ="Detalhes", command = lambda: messagebox.showinfo(title = "Ajuda", message = 
		"Este comando irá mostrar os resultados de uma tabela existente do banco de dados!"));
		botao_14.grid(column = 1, row = 5, padx = 10, pady = 10);

		botao_15 = Button(janela, text ="Detalhes", command = lambda: messagebox.showinfo(title = "Ajuda", message = 
		"Este comando irá criar uma nova tabela no banco de dados!"));
		botao_15.grid(column = 1, row = 6, padx = 10, pady = 10);

		botao_16 = Button(janela, text ="Detalhes", command = lambda: messagebox.showinfo(title = "Ajuda", message = 
		"Este comando irá obter os IPs externo e IP interno!\n"));
		botao_16.grid(column = 1, row = 7, padx = 10, pady = 10);

		botao_17 = Button(janela, text ="Detalhes", command = lambda: messagebox.showinfo(title = "Ajuda", message = 
		'''Este comando irá realizar um monitoramento da rede\nO usuário poderá indicar o número de testes a ser realizado,\nalém de escolher o intervalo em minutos entre cada teste!'''));
		botao_17.grid(column = 1, row = 8, padx = 10, pady = 10);

		botao_19 = Button(janela, text = "Servidor e tabelas", command = lambda: messagebox.showinfo(title = "", message = 
		"O nome do servidor é 'Resultados_testes'\nAs tabelas padrões disponíveis são as seguintes:\n1 - 'resultados'\n2 - 'resultados2'\n3 - 'resultadostim'"));
		botao_19.grid(column = 0, row = 9, padx = 10, pady = 10);

		botao_20 = Button(janela, text ="Detalhes", command = lambda: messagebox.showinfo(title = "Ajuda", message = 
		'''Este comando irá fornecer o nome do banco de dados\nao usuário, bem como o nome das tabelas padrões do programa!'''));
		botao_20.grid(column = 1, row = 9, padx = 10, pady = 10);

		botao_21 = Button(janela, text = "Comparar períodos", command = Melhores_Piores_Horarios);
		botao_21.grid(column = 0, row = 10, padx = 10, pady = 10);

		botao_22 = Button(janela, text ="Detalhes", command = lambda: messagebox.showinfo(title = "Ajuda", message = 
		'''Este comando irá fornecer os melhores e piores momentos\npara as velocidades de Download e Upload. Desta forma,\né possível saber quais são os melhores e piores horários para a navegação!'''));
		botao_22.grid(column = 1, row = 10, padx = 10, pady = 10);

		janela.mainloop();

		break;

	else:
		messagebox.showinfo(title = "AVISO", message = "Falha ao conectar com os servidores MySQL!\nPor favor, tente abrir novamente o programa mais tarde!\n");
		break;
