from os import system, name
import time
import paho.mqtt.client as mqtt
from tabulate import tabulate
import json

#######FUNÇÕES MQTT######
def on_log(client, userdata, level, buf):
	print("log: ", buf)
	time.sleep(1)
def on_message(client, userdata, message):
	#print("Mensagem recebida: ", str(message.payload.decode("utf-8")), "do Tópico: ", message.topic)
	global inic
	if message.topic == 'teste_a':
		inic[0] = int(message.payload)
		pass
	if message.topic == 'teste_t':
		inic[1] = int(message.payload)
		pass
	if message.topic == 'teste_f':
		inic[2] = int(message.payload)
		pass
	if message.topic == 'fresa/pedidos':
		global fresa_req
		pedido = json.loads(message.payload)
		fresa_req = pedido["entidade"]
		print("FRESA RECEBEU PEDIDO: ", fresa_req)
	if message.topic == 'torno/pedidos':
		global torno_req
		pedido = json.loads(message.payload)
		torno_req = pedido["entidade"]
		print("TORNO RECEBEU PEDIDO: ", torno_req)
	if message.topic == 'asrs/responde':
		global resp_fresa
		global resp_torno
		pedido = json.loads(message.payload)
		print("ASRS RECEBEU PEDIDO: ", pedido)
		#json = entidade/carro/pallet/est
		entidade_req = pedido["entidade"]
		carro_req = pedido["carro"]
		pallet_req = pedido["pallet"]
		est_req = pedido["est"]
		if est_req == 'fresa':
			resp_fresa = ['fresa', entidade_req, carro_req, pallet_req]
		if est_req == 'torno':
			resp_torno = ['torno', entidade_req, carro_req, pallet_req]
	if message.topic == 'fresa/pedidos/log':
		global ultimospedidos_fresa
		ultimospedidos_fresa = rotate(ultimospedidos_fresa,-1)
		ultimospedidos_fresa[0] = str(message.payload.decode("utf-8"))
	if message.topic == 'torno/pedidos/log':
		global ultimospedidos_torno
		ultimospedidos_torno = rotate(ultimospedidos_torno,-1)
		ultimospedidos_torno[0] = str(message.payload.decode("utf-8"))
	if message.topic == 'carros/pallet/ent':
		#json de troca = {'#carro':'carro_n','#pallet':'pallet_n','entidade':'entidade'}
		print("MENSAGEM DE TROCA DETECTADA")
		global pallet
		global carro_ent
		msg = json.loads(message.payload)
		nc = msg['#carro']          #numero de carros
		np = msg['#pallet']         #numero de pallet    
		ent = msg['entidade']       #    
		pallet[int(np)-1] = ent
		carro_ent[int(nc)-1] = np		
	else:
		stops[int(message.topic)-1] = str(message.payload.decode("utf-8"))
def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("Conexão OK")
	else:
		print("Falha de conexão, código = ", rc)
def connect_start():
	clear()
	print("Conectando...")
	client.connect(broker, port=1883)
	client.loop_start()
	time.sleep(0.5)				
def subscribestops():
	print("Subscribing...")
	subs=[str(x) for x in range(0,num_carros)]
	for x in range(0,num_carros):
		client.subscribe(subs[x])
		
	print(subs)	
	time.sleep(0.5)
	teste_a = 1
	teste_t = 1
	teste_f = 1
	print("Inscrito nas estações")
	time.sleep(0.5)
'''	client.subscribe("teste_a")#comentar
	client.subscribe("teste_t")
	client.subscribe("teste_f")
	client.subscribe("stops")
	client.publish("teste_a","1", 1 , True)
	client.publish("teste_t","1", 1, True)
	client.publish("teste_f","1", 1, True)#comentar'''
	
def subscribetalk():
	client.subscribe("asrs/#")  #Comunicar com ASRS
	client.subscribe("torno/#") #Comunicar com TORNO
	client.subscribe("fresa/#") #Comunicar com FRESA
	client.subscribe("fresa/pedidos/log") #ver se da p remover
	client.subscribe("asrs/responde") #sepa da p tirar tb
	client.subscribe("carros/pallet/ent")
	

broker = '127.0.0.1'   #alterar para teste publicando mqttfx "broker.mqtt-dacomshboard."
broker = '172.28.34.196'
broker = 'test.mosquitto.org'
client = mqtt.Client("Esteira")
#client.on_log=on_log
client.on_connect=on_connect
client.on_message=on_message
#########################

	
######FUNÇÕES DO PROGRAMA######
def clear():
	if name == 'nt':
		_ = system('cls') 		
def rotate(seq,n):
    n = n%len(seq)
    return seq[n:]+seq[:n]
def start():
	global carro_ent
	global pallet
	num_carros=int(input("Quantos carrinhos? "))
	print("Posicionando carrinhos...")
	pallet = ['vazio' for i in range(0,num_pallet)]
	carro_ent = ['vazio' for i in range(0,num_carros)]
	time.sleep(1)
	pos_carros = [x for x in range(0,num_carros)]
	stops = ['n/a' for x in range(0,num_carros)]
	inic = [1 for x in range(0,3)]		
	#print(stops)
	return num_carros, pos_carros, stops, inic	
def pos_update():
	"""Atualiza as tabelas na tela"""
	clear()
	lista1 = [i for i in range(0,num_carros)]
	lista2 = [str(inic[0]), str(inic[1]), str(inic[2])]
	lista3 =[[ultimospedidos_fresa[x],ultimospedidos_torno[x]] for x in range(0,5)]
	lista4 = ultimasrespostas
	lista5 = [[str(x+1), str(pallet[x])] for x in range(0,num_pallet)]
	for x in range(0,num_carros):
		if carro_ent[x] == 'vazio':
			pallet_usado = 'vazio'
			entidade_usada = 'vazio'
		else:
			pallet_usado = carro_ent[x]
			entidade_usada = pallet[int(pallet_usado)-1]
			print("ENTIDADE NO PALLET ", pallet_usado, entidade_usada)

		lista1[x] = [str(x+1), str(pallet_usado), str(entidade_usada), str(pos_carros[x]), str(stops[x])]


		#print('Carro ', x+1, ': ', pos_carros[x], "Próxima parada: ", stops[x])

	print(tabulate(lista1, headers = ['#Carro', '#Pallet', 'Entidade', 'Pos_Atual', 'Pos_stop'], tablefmt = 'psql'))
	#print(tabulate(lista2, headers = ['Vetor INIC[]:'], tablefmt = 'psql'))
	print("LOG DE PEDIDOS")
	print(tabulate(lista3, headers =['PEDIDOS FRESA','PEDIDOS TORNO'],tablefmt = 'psql'))
	print("LOG DE ENVIOS")
	print(tabulate(lista4, headers = ['ESTACAO', 'ENTIDADE','#CARRO','#PALLET'], tablefmt = 'psql'))
	print(tabulate(lista5, headers = ['#PALLET','ENTIDADE'], tablefmt = 'psql'))
	#print tabulate(lista)
def pos_increment():
	for x in range(num_carros-1,-1,-1):
		i = checkstop(x)
		if i == True:
			pos_carros[x]=pos_carros[x]
			
		else:
			if pos_carros[x]>=tamanho_esteira:
				pos_carros[x]=0
				
			else:	
				pos_carros[x]+=1
		pos_update() 	
def checkstop(a):	
	posatual=pos_carros[a]
	if posatual!=30:
		np=posatual+1
		
	else:
		np=0
	if a!=num_carros-1:
		if np==pos_carros[a+1]:
			return True
			
		else:
			if posatual==stops[a]:
				return	True
					
			else:
				parar = device_check(posatual)
				return parar
		
	else:
		if np==pos_carros[0]:
			return True
			
		else:
			if posatual==stops[a]:
				return True
			parar = device_check(posatual)
			return parar		 
def device_check(posatual):
	global teste_a
	global teste_f
	global teste_t
	if posatual == pos_asrs:
		if inic[0]==1:
			parar=True
			teste_a=0
			#client.publish('teste_a', "0")
			return parar
			
		else:
			parar = False
			teste_a=1
			#client.publish('teste_a',"1")
			return parar

	if posatual == pos_torno:
		if inic[1] == True:
			parar = True
			teste_t = 0
			#client.publish('teste_t', "0")
			return parar
		else:
			parar = False
			teste_t = 1
			#client.publish('teste_t', "1")
			return parar
	
	if posatual == pos_fresa:
		if inic[2]==True:
			parar = True
			teste_f = 0
			#client.publish('teste_f', "0")
			return parar
			
		else:
			parar = False
			teste_f = 1
			#client.publish('teste_f', "1")
			return parar		
###############################		


######COMUNICAÇÃO######
def atualizar_pedidos():
	global fresa_req
	global torno_req
    global esteira_sol
    global asrs_sol
    client.publish("fresa/pedidos/log", str(fresa_req))
	if fresa_req != 'n/a':
		print("PEDIDO DA FRESA DETECTADO")
		pedido = json.dumps({"est":"fresa","entidade":fresa_req})
		client.publish("asrs/pedidos", pedido)
		client.publish("fresa/pedidos/log", str(fresa_req))
		fresa_req = 'n/a'
	if torno_req != 'n/a':
		print("PEDIDO DO TORNO DETECTADO")
		pedido = json.dumps({"est":"torno","entidade":torno_req})
		client.publish("asrs/pedidos", pedido)
		client.publish("torno/pedidos/log", str(torno_req))
		torno_req = 'n/a'
def atualizar_respostas():
	global resp_torno
	global resp_fresa
	global ultimasrespostas
	if resp_torno[0] != 'n/a':
		global stops
		entidade = resp_torno[1]
		carro_n = resp_torno[2]
		pallet_n = resp_torno[3]
		resposta = json.dumps({"entidade":resp_torno[1],"carro":resp_torno[2],"pallet":resp_torno[3]})
		stops[int(carro_n)]=pos_torno
		client.publish("torno/resposta", resposta)
		entidade_update(resp_torno[2],resp_torno[3],resp_torno[1])
		ultimasrespostas = rotate(ultimasrespostas,-1)
		ultimasrespostas[0] = resp_torno
		resp_torno = ['n/a', 'n/a', 'n/a']

	if resp_fresa[0] != 'n/a':
		entidade = resp_fresa[1]
		carro_n = resp_fresa[2]
		pallet_n = resp_fresa[3]
		resposta = json.dumps({"entidade":resp_fresa[1],"carro":resp_fresa[2],"pallet":resp_fresa[3]})
		stops[int(carro_n)]=pos_fresa
		client.publish("fresa/resposta", resposta)	
		entidade_update(resp_fresa[2],resp_fresa[3],resp_fresa[1])
		ultimasrespostas = rotate(ultimasrespostas,-1)
		ultimasrespostas[0] = resp_fresa
		resp_fresa = ['n/a', 'n/a', 'n/a']
def entidade_update(n_carro, n_pallet, entidade):
	global carro_ent
	global pallet
	pallet[int(n_pallet)-1] = entidade
	carro_ent[int(n_carro)-1] = n_pallet
def troca_pallet(ent, pallet_n, pallet):
	pallet[pallet_n] = ent
	return pallet

def troca_carro(pallet_n, carro_n, carro_ent):
	carro_ent[carro_n] = pallet_n
	return carro_ent
#######################

######DEFINIÇÕES DE VARIAVEIS######
tamanho_esteira = 30
pos_asrs = 0
pos_torno = 10
pos_fresa = 20
num_pallet = 10
#VETORES LOG DE PEDIDOS
ultimospedidos_torno = ['n/a', 'n/a', 'n/a', 'n/a', 'n/a']
ultimospedidos_fresa = ['n/a', 'n/a', 'n/a', 'n/a', 'n/a']
 #EST/ENT/CARRO/PALLET - MATRIZ QUE ATUALIZA LOG DE ENVIOS:
ultimasrespostas = [['n/a', 'n/a', 'n/a', 'n/a'], ['n/a', 'n/a', 'n/a', 'n/a'], ['n/a', 'n/a', 'n/a', 'n/a'],['n/a', 'n/a', 'n/a', 'n/a'], ['n/a', 'n/a', 'n/a', 'n/a']]
#RESPOSTA AO TORNO/FRESA
resp_torno = ['n/a', 'n/a', 'n/a', 'n/a'] #estação, entidade req, carro_req, pallet-req
resp_fresa = ['n/a', 'n/a', 'n/a', 'n/a'] #estação, entidade req, carro_req, pallet-req
#PEDIDOS:
fresa_req = 'n/a' #entidade req
torno_req = 'n/a'
###################################



######INICIALIZAR CONEXÃO######
connect_start()
time.sleep(0.5)
###############################

######INICIALIZAR CARRINHOS######
clear()
num_carros, pos_carros, stops, inic = start()
#################################


######INSCREVER NOS TÓPICOS######
clear()	
subscribestops()
subscribetalk()
time.sleep(0.25)
pos_update()
#################################
 
while True:
	pos_increment()
	atualizar_pedidos()
	atualizar_respostas()
	time.sleep(1)
	
