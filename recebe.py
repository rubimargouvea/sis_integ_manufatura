import paho.mqtt.client as mqtt
import time
#from wireless import wireless
import os
cod_inic_TORNO = "T0"
cod_inic_FRESA = "F0"
cod_inic_ESTEIRA = "E0"
cod_inic_ASRS = "A0"
TORNO_LIVRE = "T_P0"
FRESA_LIVRE = "F_F0"
ESTEIRA_LIVRE = "E_E0"
ASRS_LIVRE = "A_A0"
cod_ENVIA_EIXO_1 = "EIX1"
cod_ENVIA_EIXO_2 = "EIX2"
cod_ENVIA_ENG_1 = "ENG1"
cod_ENVIA_ENG_2 = "ENG2"
cod_ENVIA_CARCAÇA = "CARC1"
cod_ENVIA_PALET_EIXO = "P_E"
cod_ENVIA_PALET_EIXO = "P_ENG"
cod_RECEB_ID_CAR = "ID_CAR"
cod_RECEB_ID_CONJ = "ID_CONJ"

def manipulamsg(message):
    #client1.subscribe(,2)
    #client.subscribe('ESTEIRA/#')
    #client.subscribe('FRESA/#')
    #client.subscribe('ASRS/#')
    #print(msg.topic+"-"+str(msg.payload.decode("utf-8")))
    #client.publish("tst", out_msg)
    if message == TORNO_LIVRE:
        log_int = "Internal Log: "
        print("Log: Torno inicializando...")
        #time.sleep(2)
    client.publish("#", TORNO_LIVRE)
    if message == FRESA_LIVRE:
        log_int = "Internal Log: "
        print("Log: Fresa inicializando...")
        #time.sleep(2)
    client.publish("#", FRESA_LIVRE)
    if message == ESTEIRA_LIVRE:
        log_int = "Internal Log: "
        print("Log: Torno inicializando...")
        #time.sleep(2)
    client.publish("#", TORNO_LIVRE)
    if message == TORNO_LIVRE:
        log_int = "Internal Log: "
        print("Log: Torno inicializando...")
        #time.sleep(2)
    client.publish("#", TORNO_LIVRE)
  
def on_connect(client,userdata,flags,rc):
    print("Conectado com código:" + str(rc))
    client.subscribe("#")
    client.publish("TORNO/#", cod_inic_TORNO)
    client.publish("FRESA/#", cod_inic_FRESA)
    client.publish("ESTEIRA/#", cod_inic_ESTEIRA)
    client.publish("ASRS/#", cod_inic_ASRS)



def on_message(client, userdata, msg):
    global msg_in
    msg_in = str(msg.payload.decode("utf-8"))
    print(msg_in)
    manipulamsg(msg_in)
def on_publish(client,userdata,result):  #manipular a msg recebida
    print("\nCódigo Enviado")
    pass


#broker_address = "192.168.0.105"  #racquel
broker_address ="127.0.0.1"
port = 1883 
client = mqtt.Client("MANAGER")
client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port ,60)
# Inicia o loop
client.loop_forever()
# Seta um usuário e senha para o Broker, se não tem, não use esta linha
#client.username_pw_set("USUARIO", password="SENHA")
# Conecta no MQTT Broker, no meu caso, o Mosquitto
