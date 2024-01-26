import mysql
from mysql import errorcode

def Conecta_MySQL():
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