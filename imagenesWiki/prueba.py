import json
import time
import sqlite3
import threading
import queue
import logging

import paho.mqtt.client as mqtt

# ————— Configuración de logging —————
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ————— Configuración de brokers y topics —————
LOCAL_MQTT_HOST  = "localhost"
LOCAL_MQTT_PORT  = 1883
LOCAL_MQTT_TOPIC = "cerrosorientales/sensores"

# Ubidots MQTT
UBIDOTS_MQTT_HOST       = "industrial.api.ubidots.com"
UBIDOTS_MQTT_PORT       = 1883
UBIDOTS_TOKEN           = "BBUS-rQCiovHXafW96RXcBDczlsPFCFp1RI"
UBIDOTS_DEVICE_LABEL    = "raspi"
UBIDOTS_TOPICS = {
    "temperatura": f"/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/temperatura",
    "gas":         f"/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/gas",
    "llama":       f"/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/llama",
    "alarma":       f"/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/alarma"
}
# Topic para recibir comandos de Ubidots
UBIDOTS_CONTROL_TOPIC = f"/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/alarm_control/lv"

# ————— Base de datos SQLite —————
DB_PATH = "/home/pi/sensores.db"

# Cola para procesar mensajes MQTT entrantes
message_queue = queue.Queue()

# Clientes MQTT
local_mqtt_client  = mqtt.Client(client_id="local_client")
ubidots_mqtt_client = mqtt.Client(client_id="ubidots_client")



# ————— Funciones de base de datos —————
def connect_db():
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error al conectar a SQLite: {e}")
        return None

def save_to_db(temperatura, gas, llama, alarma):
    conn = connect_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO datos (temperatura, gas, llama, alarma)
            VALUES (?, ?, ?, ?)
        """, (temperatura, gas, int(llama), alarma))
        conn.commit()
        logging.info(f"Guardado en DB: temp={temperatura}, gas={gas}, flame={llama}, alarma={alarma}")
    except sqlite3.Error as e:
        logging.error(f"Error al guardar en DB: {e}")
    finally:
        conn.close()


# ————— Callback: cuando llega un mensaje de Ubidots —————
def on_ubidots_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        value = float(payload)
        # Si Ubidots envía 0 => turn off buzzer; 1 => turn on buzzer
        state = "ON" if value == 1 else "OFF"
        topic = "cerrosorientales/control/zumbon"
        local_mqtt_client.publish(topic, state)
        logging.info(f"Forward to ESP32: topic={topic}, state={state}")
    except Exception as e:
        logging.error(f"Error procesando mensaje Ubidots: {e}")

def on_ubidots_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conectado broker Ubidots")
        client.subscribe(UBIDOTS_CONTROL_TOPIC)
        logging.info(f"Suscrito a control: {UBIDOTS_CONTROL_TOPIC}")
    else:
        logging.error(f"Fallo conexión Ubidots, rc={rc}")


# ————— Callback: cuando llega un mensaje del broker local —————
def on_local_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        message_queue.put(payload)
        logging.info(f"Mensaje local recibido y encolado: {payload}")
    except Exception as e:
        logging.error(f"Error recibiendo mensaje local: {e}")

def on_local_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conectado al broker local")
        client.subscribe(LOCAL_MQTT_TOPIC)
        logging.info(f"Suscrito a: {LOCAL_MQTT_TOPIC}")
    else:
        logging.error(f"Fallo conexión local, rc={rc}")


# ————— Hilo de procesamiento de mensajes —————
def process_messages():
    while True:
        payload = message_queue.get()  # bloquea hasta haber mensaje
        try:
            data = json.loads(payload)
            temperatura = float(data.get("temperatura"))
            gas         = int(data.get("gas"))
            llama       = bool(data.get("llama"))
            alarma       = int(data.get("alarma"))

            # 1) Almacenar en SQLite
            save_to_db(temperatura, gas, llama, alarma)

            # 2) Publicar a Ubidots vía MQTT
            for var, topic in UBIDOTS_TOPICS.items():
                value = {
                    "temperatura": temperatura,
                    "gas": gas,
                    "llama": int(llama),
                    "alarma": alarma
                }[var]
                payload_ub = json.dumps({"value": value})
                ubidots_mqtt_client.publish(topic, payload_ub)
                logging.info(f"Enviado a Ubidots: topic={topic}, payload={payload_ub}")

        except Exception as e:
            logging.error(f"Error procesando payload: {e}")
        finally:
            message_queue.task_done()


# ————— Inicialización de MQTT —————
def start_mqtt_clients():
    # Local
    local_mqtt_client.on_connect = on_local_connect
    local_mqtt_client.on_message = on_local_message
    local_mqtt_client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT)

    # Ubidots
    ubidots_mqtt_client.username_pw_set(UBIDOTS_TOKEN, "")
    ubidots_mqtt_client.on_connect = on_ubidots_connect
    ubidots_mqtt_client.on_message = on_ubidots_message
    ubidots_mqtt_client.connect(UBIDOTS_MQTT_HOST, UBIDOTS_MQTT_PORT)

    # Iniciar bucles en hilos separados
    local_mqtt_client.loop_start()
    ubidots_mqtt_client.loop_start()


# ————— Punto de entrada —————
if name == "_main_":
    # Crear tabla SQLite si no existe
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS datos (
                    timestamp INTEGER,
                    temperatura REAL,
                    gas INTEGER,
                    llama INTEGER,
                    alarma INTEGER
                );
            """)
            conn.commit()
            logging.info("Tabla SQLite verificada/creada")
        except sqlite3.Error as e:
            logging.error(f"Error creando tabla: {e}")
        finally:
            conn.close()

    # Arrancar hilo de procesamiento
    threading.Thread(target=process_messages, daemon=True).start()

    # Conectar a ambos brokers MQTT
    start_mqtt_clients()

    # Mantener vivo el programa
    try:
        while True:
            logging.info(f"Mensajes en cola: {message_queue.qsize()}")
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Terminando clientes MQTT...")
        local_mqtt_client.loop_stop()
        ubidots_mqtt_client.loop_stop()
        local_mqtt_client.disconnect()
        ubidots_mqtt_client.disconnect()
        logging.info("Script finalizado")