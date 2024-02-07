
from time import sleep
from tkinter import *
from tkinter import messagebox

from Functions.Teste import Efetuar_Teste
from Functions.ConexaoMySQL import Conecta_MySQL, Get_Dados_MySQL
from Functions.AnatelQualidade import Entrada_Dados_Anatel, Verificar_Conexao_Jogos, Verificar_Velocidade_Media
from Functions.VerificarIP import Verificar_IP
from Functions.Tabela import Entrada_Dados_Cria_Tabela, Entrada_Dados_Tabela
from Functions.Monitoramento import Entrada_Dados_Monitoramento
from Functions.ObterResultados import Melhores_Piores_Horarios



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

	servidor = Conecta_MySQL(); #a variável irá receber um valor para indicar se a conexão foi estabelecida ou não

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
