import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection);
from datetime import date
from tkinter import messagebox
import os
from Functions.ObterResultados import Imprime_Resultados;
import speedtest
from datetime import datetime

def Efetuar_Teste(quantidade_testes):
	messagebox.showinfo(title = "AVISO", message = "O teste será inicializado após clicar\nem ok ou a aba ser fechada!");
	for q in range(quantidade_testes):
		data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter = Teste_Internet();
		db_connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', password = '1234', database = 'Resultado_testes');
		cursor = db_connection.cursor();
		sql = "INSERT INTO Resultados (Data, Horário, Download, Upload, Ping, Jitter) VALUES (%s, %s, %s, %s, %s, %s)";
		values = (data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter);
		cursor.execute(sql, values);
		current_date = date.today();
		formatted_date = current_date.strftime('%d/%m/%Y');

		Imprime_Resultados(q, data_atual, hora_atual, velocidade_download, velocidade_upload, ping, jitter);

		db_connection.commit();
		cursor.close();
		db_connection.close();

		os.system("cls");	

def Teste_Internet():
    # Instanciando a função de test do Speedtest
	teste = speedtest.Speedtest(secure = True);
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
	jitter_result = round(Testa_Jitter()); 

    # Capturando data e hora do teste através das funções da biblioteca datetime.
	data_atual = datetime.now().strftime('%d/%m/%Y');
	hora_atual = datetime.now().strftime('%H:%M');

	return data_atual, hora_atual, velocidade_download, velocidade_upload, ping_result, jitter_result;

def Testa_Jitter():
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