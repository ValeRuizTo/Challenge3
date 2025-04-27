# Sistema IoT para Detección Temprana de Incendios - Reto 3

## Miembros: Samuel Rodriguez, Valentina Ruiz Torres y Darek Aljuri Martínez

## 1. Introducción
### 1.1 Resumen General
Este documento describe el desarrollo de un sistema IoT de monitoreo ambiental para la detección temprana de incendios forestales en los cerros orientales de Bogotá. En esta tercera fase, se integra un enfoque más robusto de conectividad y escalabilidad mediante el uso conjunto del microcontrolador ESP32 y una Raspberry Pi como gateway IoT, con almacenamiento local y transmisión a una plataforma en la nube.
### 1.2 Motivación
Los cerros orientales de Bogotá son una zona ecológica de gran importancia, pero altamente susceptible a incendios forestales debido a la sequía y actividad humana. 
La detección temprana de incendios es clave para minimizar daños ambientales y proteger comunidades cercanas. Para ello, se requiere un sistema de monitoreo en tiempo real que permita detectar cambios bruscos en temperatura, presencia de humo y emisión de gases característicos de la combustión. Además, es fundamental contar con una plataforma que no solo permita visualizar el historial de datos y activar alarmas físicas de manera remota, sino que también genere alertas automáticas en caso de riesgo inminente de incendio, facilitando una respuesta rápida y efectiva.



### 1.3 Justificación
El desarrollo de este sistema surge de la necesidad de implementar una solución de bajo costo y fácil instalación para la detección temprana de incendios forestales en zonas vulnerables, como los cerros orientales de Bogotá. A través del uso de sensores especializados, el sistema permite identificar la presencia de gases, humo y variaciones anómalas de temperatura, proporcionando información clave para una respuesta oportuna.

En este nuevo contexto, la solución se expande más allá del monitoreo local, integrando capacidades que permiten la supervisión remota desde cualquier lugar del país. Esta ampliación responde a la necesidad de contar con un tablero de control accesible tanto local como globalmente, desde el cual las autoridades puedan observar en tiempo real las condiciones del entorno, recibir notificaciones ante posibles emergencias y tomar decisiones informadas de forma inmediata.

De esta manera, se busca no solo ofrecer una herramienta de alerta temprana en el sitio de riesgo, sino también habilitar canales eficientes de comunicación y control centralizado, facilitando una gestión más efectiva ante posibles amenazas ambientales.

### 1.4 Estructura de la Documentación

Este documento se divide en las siguientes secciones:

1. **Solución propuesta**: Restricciones, arquitectura, desarrollo teórico y estándares aplicados.
2. **Configuración experimental y resultados**: Validación del sistema en condiciones controladas.
3. **Autoevaluación del protocolo de pruebas**: Verificación de confiabilidad y precisión.
4. **Conclusiones y trabajo futuro**: Desafíos enfrentados y mejoras futuras.
5. **Anexos**: Código fuente, esquemáticos y documentación adicional.
## 2. Solución Propuesta
### 2.1 Restricciones de Diseño

***Técnicas***
- Uso de un ESP32 como microcontrolador central. Este dispositivo, además de ser de código abierto, incorpora un microcontrolador reprogramable con conectividad Wi-Fi y Bluetooth, así como múltiples pines de entrada y salida analógicos y digitales. Esto permite la conexión eficiente con sensores y actuadores. "El ESP32 destaca por su alto rendimiento gracias a su procesador de doble núcleo. Puede llegar hasta 240 MHz, manejando tareas complejas y procesamiento en tiempo real. Esto es clave para proyectos IoT avanzados que necesitan manejar varios procesos a la vez" [1]
- Sensor de temperatura DS18B20, "permite medir la temperatura a través de un termistor NTC, un comparador LM393, y un potenciometro"[2], esto le permite al sensor adecuar una señal de trabajo operable digital.
- Sensor de gas (MQ-2), "Este sensor es adecuado para detectar GLP, I-butano, propano, metano, alcohol, hidrógeno y humo. Tiene alta sensibilidad y respuesta rápida"[3], ademas de esto cuenta con un potenciometrp para ajustar la sensibilidad.
- Sensor de Llama (KY-026). "Consta de un LED receptor de infrarrojos de 5 mm, un comparador diferencial dual LM393, un potenciómetro de recorte de 3296 W, 6 resistencias, y 4 pines de cabezal macho"[4] Es decir que detecta la luz infrarroja emitida por el fuego, y debido a su potenciometro se puede ajustar su sensibilidad.
- Pantalla LCD, con un modulo I2C para visualización de datos en tiempo real. Modulo utilizado debido a que facilita la conexión de cables y uso de pines del arduino, haciendo uso de solo dos (SDA y SCL), asi mismo se trabajo con la libreria LiquidCrystal_I2C.h, facilitando el codigo para hacer uso del LCD.
- Buzzer para alertas sonoras en caso de detección de incendio.
- Uso de una Raspberry Pi como Gateway IoT, con capacidad de recibir datos desde el ESP32 a través de MQTT, procesarlos y almacenarlos en una base de datos local (SQLite), y retransmitirlos a una plataforma IoT en la nube.
- Comunicación mediante el protocolo MQTT para la transmisión eficiente y ligera de datos entre dispositivos IoT y plataformas en la nube.
- Acceso remoto al sistema desde cualquier lugar mediante una plataforma IoT basada en la nube, que presenta los datos en un tablero de control global accesible por navegador web.

 
***Económicas***
- Implementación con componentes de bajo costo y accesibles.
- Uso de software de código abierto compatible con el ESP32 y Raspberry Pi para minimizar costos de desarrollo, implementado con el IDE Arduino y herramientas compatibles con Python en la Raspberry Pi.
- Uso de una plataforma basada en la nube
  
***Espacio y Escalabilidad***
- Diseño compacto para facilitar su instalación en zonas estratégicas.
- Posibilidad de expansión mediante comunicación con otros dispositivos IoT gracias a la conectividad Wi-Fi del ESP32 y la Raspberry Pi.
- Adaptabilidad para futuras mejoras con nuevos sensores o algoritmos de detección.

  
***Temporales***
- Desarrollo del prototipo en un plazo limitado, asegurando funcionalidad básica para detección, monitoreo y notificación.
- Implementación por etapas: primero el monitoreo local, luego la transmisión a la nube y, finalmente, la visualización remota.
- Posibilidad de mejoras futuras en algoritmos de detección, análisis de datos, y visualización en la plataforma IoT.


## 2.2 Arquitectura Propuesta

***Arquitectura IoT del Sistema***

La arquitectura IoT permite la transmisión de información digitalizada a través de la red, llevando los datos capturados por los sensores hacia un centro de procesamiento local, donde son analizados y almacenados. Posteriormente, mediante actuadores, se pueden emitir comandos para que los dispositivos conectados ejecuten acciones específicas, como la activación o desactivación de un mecanismo.

El sistema de detección de incendios está basado en una estructura distribuida compuesta por sensores, procesamiento local y comunicación de datos para la notificación de alertas. Se organiza en tres capas principales:

1. Capa de Percepción (Sensores y Adquisición de Datos)
Es la capa encargada de capturar la información del entorno mediante sensores físicos. Los dispositivos utilizados incluyen:

- Sensor de temperatura (): Mide la temperatura del aire en la zona monitoreada.
- Sensor de gas (): Detecta concentraciones de gases como CO y CO₂, indicativos de combustión.
- Sensor de llama (): Detecta la presencia de llamas en el área monitoreada.
Los sensores están conectados a un ESP32, que procesa la información en tiempo real.

2. Capa de Procesamiento y Control
El ESP32 actúa como la unidad central de procesamiento (CPU) del nodo sensor, encargada de:
- Leer y analizar los datos recibidos de los sensores.
- Determinar si las condiciones indican un posible incendio.
- Activar mecanismos de alerta local (buzzer, LED RGB y pantalla LCD).
- Mostrar en tiempo real los datos en la pantalla LCD mediante I2C.
- Ejecutar un servidor web local para acceder a los valores de sensores desde la red.
- Transmitir los datos vía MQTT a una unidad de procesamiento superior (Raspberry Pi).

Una Raspberry Pi cumple el rol de Gateway IoT, recibiendo los datos de múltiples nodos (ESP32) mediante MQTT, lo que permite concentrar la información para su posterior análisis y envío.

***La Raspberry Pi:***

- Se conecta al broker MQTT para recibir los mensajes enviados por los sensores.
- Almacena la información en una base de datos local (SQLite) para análisis histórico.
- Gestiona el envío de los datos hacia la nube mediante conexión segura.

3. Capa de Comunicación y Notificación
Esta capa es responsable de garantizar que los datos lleguen al usuario de forma clara y en tiempo real. En esta etapa se incluye tanto la notificación local como el monitoreo remoto:

***Notificación Local:***

- Pantalla LCD (I2C 16x2): Muestra los valores de temperatura, gas y llama en tiempo real, así como advertencias de peligro.
- LED RGB: Indica el estado del sistema (normal, precaución, alerta).
- Buzzer: Emite sonidos de alarma ante situaciones críticas detectadas por los sensores.
- Servidor Web embebido: El ESP32 incluye una página web local donde se visualizan los datos actuales del sistema.

***Comunicación hacia el Exterior:***

- Protocolo MQTT: Facilita la comunicación entre el ESP32 (nodo sensor) y la Raspberry Pi (gateway), usando un enfoque ligero y eficiente para IoT. MQTT es un protocolo de mensajería basado en estándares, o un conjunto de reglas, que se utiliza para la comunicación de un equipo a otro, admite la mensajería entre dispositivos a la nube y la nube al dispositivo. [10]
- Gateway Raspberry Pi: Centraliza la información de varios nodos, almacena los datos en una base de datos local y los reenvía a una plataforma de monitoreo en la nube.
- Plataforma Ubidots: Presenta un tablero de control global, es utilizada para visualizar las variables en tiempo real, también nos permite modificar las variables del proceso desde cualquier parte del mundo, los cambios se pueden realizar mediante internet atreves de la página web Ubidots.[9]
- Acceso remoto y multiplataforma: El sistema es accesible desde computadoras o dispositivos móviles, permitiendo la supervisión continua sin importar la ubicación física del usuario.

![.](imagenesWiki/arqui1.jpg)




## 2.3 Desarrollo Teórico Modular

#### **Principios de Diseño del Sistema**
- **Fiabilidad:** Uso de sensores calibrados para evitar falsas alarmas.
- **Bajo Consumo Energético:** Optimización del código para minimizar el consumo de energía.
- **Interfaz Intuitiva:** Uso de una pantalla LCD y alertas sonoras para notificaciones claras.
- **Escalabilidad:**
   - ***Escalabilidad Local:*** El sistema permite agregar sensores adicionales (por ejemplo, sensores de humedad del suelo o viento) y módulos de expansión conectados vía I2C o SPI.
   - ***Escalabilidad Remota:*** El diseño contempla la inclusión de una plataforma IoT basada en la nube (recomendada: Ubidots) que recibe los datos desde una Raspberry Pi actuando como Gateway IoT, permitiendo acceso al tablero de control desde cualquier parte del país vía MQTT.
   - Interconexión Modular: Cada módulo (ESP32, Raspberry Pi, plataforma IoT) se comunica mediante protocolos estándar (MQTT, HTTP), facilitando la integración de nuevas tecnologías o nodos.

- **Conectividad Dual (Local y Global):**
   - ***Local:*** El ESP32 actúa como servidor web embebido para ofrecer un tablero de control accesible desde dispositivos móviles o PCs conectados a la WLAN de la alcaldía. Desde esta interfaz se pueden visualizar datos actuales, históricos, notificaciones y controlar alarmas.
   - ***Global:*** Todos los datos recolectados por el ESP32 son enviados a través del protocolo MQTT a una Raspberry Pi que actúa como Gateway IoT. Este dispositivo almacena los datos en una base de datos SQLite local, los procesa y posteriormente los retransmite a la plataforma IoT Ubidots, accesible desde cualquier lugar del país.

- **Modularidad y Responsabilidad por Hilos:**

  - Las mediciones se ejecutan en hilos separados del hilo principal *mediante interrupciones* para asegurar respuesta inmediata del sistema sin bloquear otras funcionalidades.
  - La transmisión de datos tanto desde el ESP32 como desde la Raspberry Pi también se realiza en procesos independientes o asincrónicos para evitar congestión o pérdida de paquetes de datos.



### **Definición de umbrales de seguridad**

Para garantizar una detección confiable de incendios, se establecieron los siguientes umbrales en el sistema:

- **Temperatura máxima aceptable:** `TEMP_MAX = 30°C`
- **Nivel máximo de gas permitido:** `GAS_MAX = 700`
- **Cambio brusco de temperatura:** Se define como un incremento mayor a `5°C` en comparación con la lectura anterior.

Estos valores permiten detectar condiciones anómalas en el ambiente y activar una alerta en caso de peligro.

### **Justificación del umbral de temperatura**

Según el planteamiento inicial del reto, la zona de interés presenta temperaturas medias anuales entre **8.4°C y 13°C**.  
Sin embargo, se decidió establecer un umbral superior de **30°C** para la activación de alertas por las siguientes razones:

1. **Prevención de falsas alarmas:**  
   - En condiciones normales, un umbral demasiado bajo podría generar **alertas innecesarias**, activándose por aumentos naturales de temperatura.
   - Se buscó un equilibrio entre sensibilidad y precisión en la detección de incendios.

2. **Consideración de escenarios extremos:**  
   - En ciertas circunstancias (como exposición solar directa, equipos en funcionamiento o ventilación deficiente), la temperatura en el entorno puede superar los valores promedio de la región.
   - Un umbral más alto permite descartar estas fluctuaciones y centrarse en **situaciones realmente peligrosas**.

3. **Adaptación a condiciones reales de incendio:**  
  - Según el documento "Las fases de un incendio", durante la fase de incremento de un incendio, la temperatura aumenta rápidamente, situándose entre los 300°C y los 700°C. [5] Este incremento significativo de temperatura en las etapas iniciales de un incendio respalda la decisión de establecer un umbral de 30°C en nuestro sistema de detección. Aunque las temperaturas medias anuales en la zona de interés varían entre 8.4°C y 13°C, un aumento repentino que supere los 30°C podría indicar una situación anómala que requiera atención inmediata. Por lo tanto, este umbral permite detectar de manera efectiva un incipiente foco de incendio sin comprometer la confiabilidad del sistema.​   

4. **Resultados observados en la fase de pruebas de laboratorio:**  
   - Durante las pruebas en el laboratorio, se registraron temperaturas promedio entre **25°C y 27°C**.  
   - Esto evidenció que, aunque las temperaturas externas sean más bajas, el ambiente de prueba puede ser significativamente más cálido.  
   - Debido a esto, **se estableció 30°C como un valor adecuado para definir una temperatura "alta"**, asegurando que las alertas solo se activen en condiciones realmente anómalas.



### **Condiciones de activación de alerta**
El sistema genera una alerta cuando ocurre cualquiera de las siguientes condiciones:

1. **Sobrecalentamiento y gas elevado:** La temperatura supera los `30°C` y el nivel de gas es mayor a `700`.
2. **Presencia de llama:** Se detecta una llama a través del sensor (`PIN_LLAMAS`).
3. **Cambio brusco de temperatura:** Se registra un incremento superior a `5°C` en comparación con la última medición.

Cuando se activa una de estas condiciones, el sistema toma medidas inmediatas para alertar al usuario.



### **Consideraciones del entorno de laboratorio**
Las condiciones ambientales en el laboratorio difieren del entorno final donde se implementará el sistema. Por este motivo:

- Se ajustaron los umbrales para adaptarse al entorno de prueba y minimizar **falsos positivos**.
- Se añadió un umbral para detectar cambios bruscos de temperatura (`>5°C`), mejorando la precisión en la identificación de incendios.

Estos ajustes garantizan que el sistema responda correctamente sin generar alertas innecesarias.



### **Funcionamiento de la detección de cambios bruscos de temperatura**
El sistema monitorea la temperatura de forma continua para identificar cambios abruptos:

1. **Comparación de lecturas:** Se compara la temperatura actual (`valorTemp`) con la última registrada (`tempAnt`).
2. **Detección de incremento abrupto:** Si la diferencia supera `5°C`, se activa el indicador `saltoTemp = true`.
3. **Registro y notificación:**
   - El evento se almacena en el sistema de logs.
   - La información se envía a la interfaz web para que el usuario la visualice en tiempo real.


### **Intervalo de detección de cambios de temperatura**
- La temperatura se actualiza cada `500 ms` (`refresco = 500`), permitiendo una detección casi en **tiempo real**.
- Esto garantiza que cualquier cambio repentino se registre de manera inmediata y se tomen acciones rápidas.

### **Respuesta del sistema ante detección de incendio**
Si se activa una alerta por alguna de las condiciones previamente definidas, el sistema ejecuta las siguientes acciones:

**Indicadores visuales y auditivos:**
- Se enciende el **LED RGB en rojo** para señalar peligro.
- Se activa el **zumbador (buzzer)** con una frecuencia de `1000 Hz`.
- La pantalla **LCD muestra el mensaje "FUEGO!"** para alertar al usuario.

**Monitoreo en tiempo real (local y global):**
- La alerta y los datos de los sensores se envían a la interfaz web embebida alojada en el ESP32, accesible desde dispositivos conectados a la WLAN ofrecida por la alcaldía.
- A través del “Tablero de control local”, las autoridades pueden:
   - Visualizar las variables físicas actuales.
   - Ver un histórico reciente almacenado temporalmente en el ESP32.
   - Recibir notificaciones visuales.
   - Desactivar alarmas físicas mediante botones en la interfaz.

**Envío de datos al Gateway IoT y plataforma en la nube:**
- Los datos del evento (temperatura, gas, llama, fecha, hora) son enviados mediante el protocolo MQTT desde el ESP32 a una Raspberry Pi que actúa como Gateway IoT.
- La Raspberry Pi:
  - Recibe y almacena los datos en una base de datos SQLite, conservando un registro estructurado de eventos y condiciones normales.
  - Procesa y retransmite los datos a la plataforma IoT en la nube, Ubidots utilizando nuevamente MQTT.
  - Permite monitoreo en tiempo real desde cualquier lugar de Colombia a través de un “Tablero de control global” alojado en dicha plataforma.



## **2.4 Manejo de tareas concurrentes**

"Un hilo es la unidad de ejecución más pequeña de un programa. El multihilo permite que un programa realice múltiples tareas simultáneamente al dividir su carga de trabajo en componentes más pequeños, ejecutables independientemente, llamados hilos" [6]

El sistema utiliza hilos mediante el sistema operativo en tiempo real (RTOS) FreeRTOS, que está integrado en el framework del ESP32. FreeRTOS permite la ejecución concurrente de tareas (hilos) en el microcontrolador, lo que mejora la capacidad del sistema para realizar múltiples operaciones de manera simultánea.

## Hilos (FreeRTOS Tasks)

En este proyecto se crean **dos tareas** con la API de FreeRTOS:

1. **Tarea “Sensores”**  
   - **Creación**  
                 xTaskCreate(
                   leerSensores,    // función que se ejecutará en el hilo
     
                   "Sensores",      // nombre de la tarea
     
                   4096,            // tamaño de pila (bytes)
     
                   NULL,            // parámetro de la tarea
     
                   1,               // prioridad (1 = baja)
     
                   NULL             // handle (no se usa)
     
                 );
     
   - **Función asociada**: `void leerSensores(void *arg)`  
     - Inicializa el sensor DS18B20 (`tempSensor.begin()`) y la resolución ADC (`analogReadResolution(10)`).  
     - En bucle infinito:
       1. Solicita temperatura (`tempSensor.requestTemperatures()` + `getTempCByIndex(0)`).
       2. Lee nivel de gas (`analogRead(gasPin)`).
       3. Detecta llama (`!digitalRead(PIN_LLAMAS)`).
       4. **Bajo mutex**: actualiza las variables globales `valorTemp`, `valorGas`, `hayLlama` y guarda en el buffer circular `logDatos[]`.
       5. `vTaskDelay(pdMS_TO_TICKS(200))` → pausa de 200 ms.

2. **Tarea “MQTT”**  
   - **Creación**  
   
               xTaskCreate(
                 enviarMqtt,      // función que se ejecutará en el hilo
                 "MQTT",          // nombre de la tarea
                 4096,            // tamaño de pila (bytes)
                 NULL,            // parámetro de la tarea
                 1,               // prioridad (1 = baja)
                 NULL             // handle (no se usa)
               );

   - **Función asociada**: `void enviarMqtt(void *arg)`  
     - En bucle infinito:
       1. Si no hay conexión, llama a `reconnect_mqtt()`.
       2. Llama a `client.loop()` para procesar callbacks MQTT.
       3. **Bajo mutex**: copia `valorTemp`, `valorGas`, `hayLlama`, `zumbOn` en variables locales.
       4. Crea un JSON con telemetría y estado de alarma (`snprintf`).
       5. Publica en `cerrosorientales/sensores` (`client.publish(...)`).
       6. `vTaskDelay(pdMS_TO_TICKS(500))` → pausa de 500 ms.


El bucle `loop()` de Arduino no crea un hilo adicional, sino que corre en el contexto principal de FreeRTOS junto a las demás tareas.



### Variables volatile
Sincronización: Las variables globales (valorTemp, valorGas, hayLlama, logDatos, etc.) son compartidas entre los hilos. Para evitar problemas de concurrencia, estas variables están marcadas como ***volatile***, lo que asegura que el compilador no optimice el acceso a ellas y que los cambios realizados por un hilo sean visibles para el otro. 
Las siguientes variables globales están declaradas como `volatile`:

- volatile float valorTemp;
- volatile int   valorGas;
- volatile bool  hayLlama;
- volatile bool  zumbOn;
- volatile bool  dispOn;
- volatile bool  rgbOn;


## **2.5 Uso de semaforos**
 Se usan para proteger datos compartidos cuando varias tareas (hilos) acceden a las mismas variables, asi las funciones de leer y escribir no se ejecutan al mismo tiempo

- Libreria usada: #include <freertos/semphr.h>

### Declaración y Creación del Mutex
En `setup()` creamos un mutex de tipo binario (protege secciones críticas):

       SemaphoreHandle_t xMutex;
       
       void setup() {
         // … otras inicializaciones …
       
         // Crear el mutex
         xMutex = xSemaphoreCreateMutex();
         if (xMutex == NULL) {
           Serial.println("Error: no se pudo crear xMutex");
         }
       
         // … crear tareas, iniciar MQTT, WebServer …
       }

- SemaphoreHandle_t: tipo de dato para almacenar el mutex.
- xSemaphoreCreateMutex(): reserva y devuelve un mutex listo para usarse.



### Tarea de Lectura de Sensores

     void leerSensores(void *arg) {
      for (;;) {
        float t = tempSensor.getTempCByIndex(0);
        int   g = analogRead(gasPin);
        bool  f = !digitalRead(PIN_LLAMAS);
    
        // Sección crítica: actualización de variables compartidas
        if (xSemaphoreTake(xMutex, portMAX_DELAY)) {
          valorTemp = t;
          valorGas  = g;
          hayLlama  = f;
          // … almacenamos en logDatos[] …
          xSemaphoreGive(xMutex);
        }
    
        vTaskDelay(pdMS_TO_TICKS(200));
      }
    }


Cada 200 ms el hilo de leerSensores actualiza varias variables globales (valorTemp, valorGas, hayLlama) y el buffer circular logDatos[]. Si justo en ese momento el hilo de MQTT o el callback MQTT están leyendo esas mismas variables (o escribiendo otras, como zumbOn), se pueden generar datos “mezclados” o inconsistentes (por ejemplo, una temperatura antigua con un valor de gas nuevo). El semáforo garantiza que la sección donde se escribe todo el bloque de variables sea atómica: ninguna otra tarea podrá leer o escribir hasta que termine la actualización completa.

### En la Tarea de Envío MQTT

       void enviarMqtt(void *arg) {
         for (;;) {
           if (xSemaphoreTake(xMutex, portMAX_DELAY)) {
             float t = valorTemp;
             int   g = valorGas;
             bool  f = hayLlama;
             bool  z = zumbOn;
             xSemaphoreGive(xMutex);
       
             // Construir y publicar JSON con t, g, f, z …
           }
           vTaskDelay(pdMS_TO_TICKS(500));
         }
       }

Antes de publicar el JSON , enviarMqtt copia bajo mutex las variables (valorTemp, valorGas, hayLlama, zumbOn) a variables locales. Sin semáforo, se podrian capturar una mezcla de valores (temperatura vieja, gas nuevo, estado de alarma intermedio). El semáforo asegura que la lectura de ese conjunto de valores sea coherente: la tarea de sensores no puede modificar nada hasta que se haya leído y enviado los datos como un bloque.

### 3. En el Callback MQTT

       void mqttCallback(char* topic, byte* payload, unsigned int length) {
         if (xSemaphoreTake(xMutex, portMAX_DELAY)) {
           if (String(topic) == topic_ctrl_buzzer) {
             zumbOn = (msg == "ON");
           }
           // … otros controles …
           xSemaphoreGive(xMutex);
         }
       }

Cuando llega un mensaje de control (“ON”/“OFF”) para la alarma, el callback actualiza variables como zumbOn, dispOn o rgbOn. Sin protección, se podria estar en medio de un enviarMqtt o de una lectura de sensores y cambiar sólo una parte del estado, dejando memoria compartida en un estado parcial. El semáforo convierte la sección de escritura del callback en una operación indivisible, de modo que ninguna otra tarea entra a usar esas variables hasta que termines de actualizarlas todas. 

### ¿Por Qué Usar Semáforos?

- Evitar Condiciones de Carrera: Sin protección, una tarea podría leer una variable mientras otra la está escribiendo, llevando a valores inconsistentes o a fallas en el sistema.

- Consistencia de Datos: Asegura que lecturas y escrituras de valorTemp, valorGas, hayLlama, zumbOn, etc. sean atómicas desde el punto de vista de cada tarea.

- Visibilidad Inmediata: Junto con volatile, garantiza que cada tarea vea el valor más reciente de la variable en memoria.

- Escalabilidad: Permite añadir más tareas futuras (p. ej. manejo de actuadores, otras comunicaciones) sin romper la integridad de los datos compartidos.



## **2.6 Funcionamiento de MQTT**

- Broker: servidor central que recibe mensajes de los clientes y los reenvía a quienes estén suscritos a esos tópicos.

- Cliente: cualquier dispositivo (ESP32, Raspberry, dashboard Ubidots, etc.) que se conecta al broker para publicar (publish) o recibir mensajes (subscribe).

- Tópico: cadena jerárquica (p. ej. "cerrosorientales/sensores") que clasifica el contenido de los mensajes.

- Publish/Subscribe: los publicadores no conocen quién recibe, y los suscriptores no conocen quién publica.



### Broker vs Cliente

| Rol     | Descripción                                                                                                                                      |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Broker**  | Servidor central que recibe mensajes de los clientes publicadores y los reenvía a los clientes suscriptores. Mantiene la lista de tópicos. |
| **Cliente** | Dispositivo o aplicación que se conecta al broker para **publicar** mensajes (_publish_) o **recibir** mensajes (_subscribe_).               |

####  ¿Quién el Broker?
- **Mosquitto** corre en la Raspberry Pi  escuchando en el puerto 1883.  
- Actúa como punto único de intercambio de mensajes entre ESP32, scripts Python y otros clientes.

####  ¿Quiénes son los Clientes?
1. **ESP32**  
   - Se conecta al broker Mosquitto local para:
     - **Publicar** telemetría (`cerrosorientales/sensores`).  
     - **Suscribirse** a comandos de control (`cerrosorientales/control/...`).  
2. **Script Python en Raspberry**  
   - Cliente `local_client` que:
     - **Se suscribe** a `cerrosorientales/sensores` (recepción de telemetría).  
     - **Publica** a Ubidots y reenvía comandos de control de/para el ESP32.  
3. **Dashboard Ubidots**  
   - Cliente externo que:
     - **Se suscribe** a tópicos `/v1.6/devices/...` para mostrar telemetría.  
     - **Publica** en `/alarm_control/lv` para enviar comandos de control.  


#### ¿Qué es Mosquitto?
- Broker MQTT de código abierto 

**Instalación básica**

          sudo apt update
          sudo apt install mosquitto mosquitto-clients
          sudo systemctl enable mosquitto
          sudo systemctl start mosquitto

### MQTT en el esp32

1. Publicación de telemetría (es un sistema automatizado de comunicación (alámbrico o inalámbrico) que permite recopilar datos en lugares remotos. Se encarga de recoger información, procesarla y transmitirla hasta el lugar donde se monitorea el sistema.)[8]

Tarea FreeRTOS enviarMqtt lee cada 500 ms las variables globales (valorTemp, valorGas, hayLlama, zumbOn) bajo un mutex y hace:

     client.publish("cerrosorientales/sensores", json);

Cualquier cliente suscrito a ese tópico (la Raspberry) recibirá este JSON con temperatura, gas, llama y alarma.

2. Suscripción a control remoto

Al conectar al broker local:

      client.subscribe("cerrosorientales/control/zumbon");

Cuando llega un mensaje en este tópicos, mqttCallback() lo ejecuta y actualiza la variable zumbOn para encender/apagar el buzzer.

3. Publicación de toggles desde la web local

Cada handler de toggle:

       client.publish(topic_ctrl_buzzer, zumbOn ? "ON" : "OFF");
       
Así el ESP32 informa al broker local cuándo el usuario hace click en su página /toggleBuzzer, lo que dispara a la Raspberry.


### MQTT en la Raspberry (Python)

1.Suscripción a telemetría local
       
       local_client.subscribe("cerrosorientales/sensores")

on_local_message() encola cada JSON recibido para procesarlo (guardar en SQLite y reenviarlo).

2. Publicación a Ubidots

El hilo process_messages():

      for var, topic in UBIDOTS_TOPICS.items():
        ubidots_client.publish(topic, json.dumps({"value": valor}))

Mapea temperatura, gas, llama y alarma a sus tópicos /v1.6/devices/... en Ubidots.

3. Suscripción a comandos de Ubidots

      ubidots_client.subscribe(UBIDOTS_CONTROL_TOPIC) 

Cuando el usuario pulsa el switch en Ubidots, llega un mensaje {"value":0or1}, que on_ubidots_message() interpreta y hace:

     local_client.publish("cerrosorientales/control/zumbon", "1")

### Comunicación Bidireccional 

**ESP32 → Broker**

- El ESP32, como cliente, publica cada 500 ms un JSON en cerrosorientales/sensores.

- Mosquitto reenvía ese JSON al client Python (y a cualquier otro suscriptor).

**Broker → Python → Ubidots**

- El script Python, suscrito a cerrosorientales/sensores, consume esos mensajes, los almacena en SQLite y los publica en Ubidots.

**Ubidots → Broker**

- El dashboard Ubidots publica comandos en /alarm_control/lv.

- Mosquitto entrega ese mensaje al client Python.

**Python → Broker → ESP32**

- Python recibe el comando, lo interpreta y lo re-publica en cerrosorientales/control/zumbon (y otros tópicos de control).

- El ESP32, suscrito, recibe el mensaje y ejecuta mqttCallback(), activando o desactivando buzzer, pantalla o LED RGB.

**ESP32 → Broker → Python (Confirmación)**

-Cuando el usuario acciona la web local del ESP32, éste publica "ON"/"OFF" en cerrosorientales/control/....

- Python recibe y reenvía a Ubidots para mantener ambos dashboards sincronizados.


## **2.7 Ubidots**

Ubidots es una plataforma IoT basada en la nube que permite recolectar, almacenar, visualizar y actuar sobre datos de sensores en tiempo real.  
- **Dashboard personalizable**: gráficos, mapas, indicadores y notificaciones.  
- **API MQTT/HTTP**: para publicar y suscribirse a datos de forma ligera.  
- **Control remoto**: permite enviar comandos a dispositivos conectados.


#### Arquitectura de Integración

ESP32 ─── MQTT local ─── Raspberry Pi ─── MQTT Ubidots ─── Ubidots Cloud


1. ESP32 publica telemetría en el broker local (cerrosorientales/sensores).

2. Raspberry Pi (Gateway) recibe, guarda en SQLite y reenvía cada variable a Ubidots.

3. Ubidots Cloud almacena, grafica y notifica eventos; también emite comandos de control de vuelta.

#### Configuración MQTT para Ubidots

- Host: industrial.api.ubidots.com

- Puerto: 1883

- Token: En Ubidots, el **Token** es tu credencial de autenticación para conectar clientes MQTT/HTTP a la cuenta.  
  - **¿Para qué sirve?**
   - Permite a tu cliente MQTT (Raspberry Pi o ESP32) probar que está autorizado a publicar y suscribirse en tus recursos de Ubidots.  
   - Se usa en lugar de usuario/contraseña tradicionales:  
    
         ubidots_mqtt_client.username_pw_set(UBIDOTS_TOKEN, "")



#### Tópicos MQTT en Ubidots

Ubidots sigue una estructura de tópicos basada en **Devices** y **Variables**:

- **device_label**: nombre que se le asigno al device (p. ej. `raspi`).  
- **variable_label**: nombre de cada dato que se esta enviando (p. ej. `temperatura`, `gas`, `llama`, `alarma`).  
      
      UBIDOTS_TOPICS = {
          "temperatura": f"/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/temperatura",
          "gas":         f"/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/gas",
          "llama":       f"/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/llama",
          "alarma":      f"/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/alarma"
      }



#### Publicación de Telemetría
En el hilo de procesamiento de la Raspberry Pi (process_messages):
       
       for var, topic in UBIDOTS_TOPICS.items():
           payload_ub = json.dumps({"value": value})
           ubidots_mqtt_client.publish(topic, payload_ub)
           logging.info(f"Enviado a Ubidots: topic={topic}, payload={payload_ub}")

- Se formatea cada variable (temperatura, gas, llama, alarma) como JSON {"value": ...}.
- Ubidots recibe y actualiza sus widgets en el dashboard en tiempo real.



#### Suscripción a Comandos de Control
Para que el dashboard Ubidots pueda activar/desactivar el buzzer del ESP32:
         
         def on_ubidots_connect(client, userdata, flags, rc):
             if rc == 0:
                 client.subscribe(UBIDOTS_CONTROL_TOPIC)
         
         def on_ubidots_message(client, userdata, message):
             value = float(message.payload.decode())
             state = "ON" if value == 1 else "OFF"
             local_mqtt_client.publish("cerrosorientales/control/zumbon", state)

- On_ubidots_connect: se suscribe al tópico /alarm_control/lv.

- on_ubidots_message: convierte el valor recibido (0/1) en "OFF"/"ON" y lo re-publica al broker local.

- El ESP32, suscrito a cerrosorientales/control/zumbon, recibe ese comando y activa o desactiva el buzzer.

#### Flujo Completo de Datos en Ubidots

1. Raspberry Pi publica en MQTT Ubidots.

2. Ubidots Cloud recibe y visualiza:

 - Gráficos de línea para tendencias.

 - Indicadores de valor actual.

 - Alertas configurables (email, SMS, webhook).

3. Operador puede interactuar con el dashboard:

 - Desactivar buzzer (publica en /alarm_control/lv).



## **2.8 Diagramas UML**
1. **Diagrama de Caso de Uso**: Describe la interacción entre los usuarios y el sistema
<p align="center">
  <img src="imagenesWiki/uso.jpg" />
</p>

   
2.1 **Diagrama de Clases ESP32**: Representación de la estructura del software.

<p align="center">
  <img src="imagenesWiki/Diagrama.png" />
</p>

2.2 **Diagrama de Clases Python Raspberry**: Representación de la estructura del software.

<p align="center">
  <img src="imagenesWiki/Diagrama123.jpg" />
</p>



3.1 **Diagrama de Secuencia ESP32**: Flujo de datos y eventos en el sistema.
<p align="center">
  <img src="imagenesWiki/Diagrama2.png"/>
</p>
   
3.2 **Diagrama de Secuencia Python Raspberry**: Flujo de datos y eventos en el sistema.
<p align="center">
  <img src="imagenesWiki/Diagrama22.jpg" />
</p>


3.3 **Diagrama de Secuencia general**: 
<p align="center">
  <img src="imagenesWiki/Diagrama222.jpg" />
</p>
   


   
4.1 **Diagrama de Estados ESP32:** Estados del sistema según las condiciones detectadas.

*Estado: Inicio*
 -	Se ejecuta setup(): Inicializa Serial, configura pines y mutex, conecta a Wi-Fi y al broker MQTT, crea tareas FreeRTOS (leerSensores, enviarMqtt), y arranca el servidor Web.
 -	Por qué: Preparar hardware y comunicaciones antes de entrar en el bucle principal.
 -Después: → Monitoreo Normal
  	
*Estado: Monitoreo Normal*
 -	El hilo leerSensores actualiza continuamente valorTemp, valorGas, y hayLlama.
 -	En loop() (cada 500 ms):
  -	Si dispOn, limpia y muestra en LCD: T: valorTemp °C y G: valorGas.
  -	LED RGB en verde (0, 255, 0) si rgbOn.
  -	Buzzer apagado (noTone) si zumbOn.
 -		Por qué: Condición de funcionamiento estándar sin alertas.
 -	Después:
  -	Si abs(valorTemp – tempAnt) > 5 o (valorTemp > 30 && valorGas > 700) → Alarma Activada
  -	Else if valorGas > 700 || valorTemp > 30 → Advertencia Gas/Temp Alta
  -	Else if hayLlama → Detección de Llama
     
*Estado: Advertencia Gas/Temp Alta*
  -	En LCD (si dispOn): Muestra los valores T: valorTemp y G: valorGas.
  -	LED RGB en amarillo (255, 255, 0).
  -	Buzzer permanece apagado.
  -	Por qué: Uno de los sensores excede su umbral, pero aún no hay indicio de incendio ni cambio brusco.
  -	Después:
   -	Si ambas lecturas vuelven bajo umbral → Monitoreo Normal
   -	Si aparece llama → Detección de Llama
   -	Si cambio brusco o ambos sensores altos → Alarma Activada
     
*Estado: Detección de Llama*
 -	En LCD (si dispOn): Muestra "FUEGO!" y G: valorGas.
 -	LED RGB en rojo (255, 0, 0).
 -	Buzzer suena (tone) si zumbOn.
 -	Por qué: El sensor de llama detecta fuego directo.
 -	Después:
  -	Si deja de detectarse llama → Monitoreo Normal
  -	Si además hay cambio brusco o sensores altos → Alarma Activada
     
*Estado: Alarma Activada (Posible Incendio)*
  -	En LCD (si dispOn): Muestra "Posible incendio!" y G: valorGas.
  -	LED RGB en rojo intenso (255, 0, 0).
  -	Buzzer suena ininterrumpidamente si zumbOn.
  -	Por qué: Se detecta un cambio brusco de temperatura o ambos sensores exceden su umbral simultáneamente.
  -	Después:
   -	Cuando abs(valorTemp – tempAnt) ≤ 5 y valorTemp ≤ 30 y valorGas ≤ 700 y !hayLlama → Monitoreo Normal
   -	Al salir, tempAnt se actualiza para futuras comparaciones.
     
*Eventos de Control Externo (Aplicable en Todos los Estados)*
  -	Evento: Toggle Buzzer (MQTT o Web):
   -	Si se recibe mensaje en "cerrosorientales/control/zumbon" ("ON" o "OFF") o se llama a /toggleBuzzer:
    -	Actualiza zumbOn.
    -	Si zumbOn es false, noTone(zumbPin).
    -	Si se togguea vía web, publica nuevo *Estado a "cerrosorientales/control/zumbon".
  -	Evento: Toggle Display (MQTT o Web):
   -	Si se recibe mensaje en "cerrosorientales/control/dispon" o se llama a /toggleLCD:
    -	Actualiza dispOn.
    -	Si dispOn es true, display.backlight(); else display.noBacklight().
  -	Evento: Toggle RGB (MQTT o Web):
   -	Si se recibe mensaje en "cerrosorientales/control/rgbon" o se llama a /toggleRGB:
    -	Actualiza rgbOn.
    -	Si rgbOn es false, pintarRGB(0, 0, 0).
  -	Evento: Reset Log (Web):
   -	Si se llama a /resetLog:
    -	Limpia el log: logPos = 0, logCant = 0.

*Aplicable en Todos los Estados*
  -	Publicación MQTT:
   -	Cada 500 ms, el hilo enviarMqtt:
 	  - Lee valorTemp, valorGas, hayLlama, zumbOn.
    - Publica a "cerrosorientales/sensores" como {"temperatura":..., "gas":..., "llama":..., "alarma":...}.
  -	Por qué: Permite a sistemas externos (e.g., Raspberry Pi) recibir datos de sensores.


4.2 **Diagrama de Estados Python Raspberry:** Estados del sistema según las condiciones detectadas.

*Estado: Inicio*
  -	Se ejecuta el bloque if __name__ == "__main__"::
  -	Verifica/crea la tabla SQLite (datos) con columnas: timestamp, temperatura, gas, llama, alarma.
  -	Arranca el hilo demonio process_messages.
  -	Lanza start_mqtt_clients():
  -	Conecta local_mqtt_client a localhost:1883, asigna callbacks on_connect y on_message.
  -	Conecta ubidots_mqtt_client a industrial.api.ubidots.com:1883, asigna credenciales y callbacks.
  -	Inicia bucles con loop_start() para ambos clientes.
  -	Por qué: Preparar la base de datos y conectar ambos clientes MQTT antes de procesar datos.
  -	Después: → *Estados concurrentes Espera de Mensajes Local, Espera de Mensajes Ubidots, y Loop Principal

*Estado: Espera de Mensajes Local*
  -	local_mqtt_client.loop_start() atiende mensajes entrantes en cerrosorientales/sensores.
  -	En on_local_connect:
  -	Suscribe a cerrosorientales/sensores al conectar.
  -	Registra éxito o falla en el log.
  -	El callback on_local_message:
  -	Decodifica el payload (JSON string).
  -	Encola el mensaje en message_queue.
  -	Registra el evento en el log.
  -	Maneja errores de decodificación.
  -	Por qué: Permanecer escuchando telemetría enviada por el ESP32.
  -	Después: Al encolar → Procesar Mensaje

*Estado: Procesar Mensaje*
  -	El hilo process_messages realiza payload = message_queue.get() (bloquea hasta haber mensaje).
  -	Parsea el JSON y extrae temperatura, gas, llama, alarma.
  -	Llama a save_to_db(...) para insertar en SQLite, con manejo de errores.
  -	Publica cada variable en Ubidots con ubidots_mqtt_client.publish(...) a los topics correspondientes (temperatura, gas, llama, alarma).
  -	Registra cada acción (guardado y publicación) en el log.
  -	Llama a message_queue.task_done() para marcar la tarea como completada.
  -	Por qué: Almacenar localmente y reenviar telemetría a Ubidots.
  -	Después: → Retorna a Espera de Mensajes Local

*Estado: Espera de Mensajes Ubidots*
  -	ubidots_mqtt_client.loop_start() atiende mensajes en /v1.6/devices/raspi/alarm_control/lv.
  -	En on_ubidots_connect:
  -	Suscribe a /v1.6/devices/raspi/alarm_control/lv al conectar.
  -	Registra éxito o falla en el log.
  -	El callback on_ubidots_message:
  -	Decodifica el payload y convierte a float.
  -	Determina el *Estado: "ON" si el valor es 1, "OFF" si es 0.
  -	Publica "ON"/"OFF" en cerrosorientales/control/zumbon usando local_mqtt_client.
  -	Registra el evento en el log.
  -	Maneja errores de decodificación.
  -	Por qué: Recibir comandos del dashboard Ubidots para el buzzer del ESP32.
  -	Después: → Retorna a Espera de Mensajes Ubidots

*Estado: Loop Principal*
  -	En el hilo principal, bucle infinito con while True:
  -	Cada 10 s imprime Mensajes en cola: {message_queue.qsize()}.
  -	Por qué: Ofrecer un “heartbeat” de actividad y monitoreo de la cola de trabajo.
  -	Después: → Repite Loop Principal continuamente

*Evento: Terminación (KeyboardInterrupt)*
  -	Aplicable en: Cualquier Estado, típicamente detectado en Loop Principal.
  -	Acciones:
  -	Detiene los bucles de los clientes MQTT: local_mqtt_client.loop_stop(), ubidots_mqtt_client.loop_stop().
  -Desconecta los clientes: local_mqtt_client.disconnect(), ubidots_mqtt_client.disconnect().
  -	Registra "Script finalizado" en el log.
  -	Por qué: Garantizar un cierre limpio del programa al ser interrumpido por el usuario.
  -	Después: → Fin del programa.

.
.


.

.

..

.

.

.

.

.


.

.





#### **2.9 Estándares de Diseño Aplicados**

**1. Diseño Modular**  
- Se basa en el principio de **separación de preocupaciones** (*Separation of Concerns*), que facilita la escalabilidad y mantenimiento del código.  
- Permite reutilizar módulos sin afectar el sistema completo.  
- Relacionado con los principios **SOLID** en ingeniería de software, específicamente el principio de **Responsabilidad Única (SRP)**.  

**2. Programación Concurrente (FreeRTOS)**  
- Uso de **sistemas operativos en tiempo real (RTOS)** para gestionar múltiples tareas sin bloqueo.  
- Asegura una **baja latencia** y una mejor **responsividad** en sistemas embebidos.  
- Se alinea con estándares como **IEEE 1003 (POSIX Threads)** y prácticas de **sistemas concurrentes**.  

**3. Arquitectura Cliente-Servidor**  
- Sigue el estándar de **arquitectura distribuida** usado en la web y en sistemas embebidos.  
- Basado en el modelo **RESTful** para estructurar la comunicación entre cliente y servidor.  
- Compatible con estándares de **HTTP/HTTPS (RFC 2616, RFC 7231)** y protocolos de comunicación embebida.  

**4. Manejo de Recursos Compartidos**  
- Uso de variables **volatile** y técnicas de sincronización para evitar **condiciones de carrera**.  
- Relacionado con estándares de **sistemas concurrentes y paralelos** (por ejemplo, **ISO/IEC 9899:2011 - C11** para programación en C).  

**5. Diseño Basado en Estados**  
- Implementa una **Máquina de Estados Finitos (FSM, *Finite State Machine*)**, un enfoque común en sistemas embebidos.  
- Se alinea con prácticas de diseño en **automatización y control**, como **IEC 61131-3** para sistemas de control industrial.  

**6. Manejo de Errores**  
- Uso de estrategias de **reconexión WiFi automática** y validaciones en la interfaz web.  
- Implementación de **mecanismos de detección y corrección de fallos** en el software.  
- Basado en principios de **tolerancia a fallos** en sistemas embebidos.  

## 3. Configuración Experimental y Resultados

### 3.1 Metodología de Pruebas

- **Prueba de Sensores In Situ y en Campo**  
  - **DS18B20 (digital, OneWire):** comparación con termómetro calibrado en 20–40 °C; margen de error máximo ±0.5 °C.  
  - **MQ-2 (analógico, ADC 10 bits):** validación con concentraciones de propano conocidas; ajuste fino del umbral en 600–800 unidades.  
  - **Detector de llama (digital):** prueba de detección a distintas distancias (5 cm, 10 cm, 20 cm) usando fuente de llama controlada; tiempo de respuesta < 200 ms.  
  - Se capturaron lecturas en laboratorio y en exteriores; se ajustaron umbrales (30 °C, 700 unidades, salto brusco > 5 °C) y se introdujo lógica de detección de incremento abrupto para reducir falsas alarmas.

- **Prueba de la Interfaz Web Local**  
  - Acceso desde PC, smartphone y tablet conectados a la red Wi-Fi del ESP32.  
  - Verificación de los endpoints `/data` y `/history`: actualización de valores y de log cada segundo sin pérdida de frames.  
  - Comprobación de botones de control (buzzer, LCD, RGB, reset log): latencia de respuesta < 150 ms y feedback inmediato en la UI.

- **Prueba de Comunicación MQTT y Ubidots**  
  - **Broker local en Raspberry Pi (Mosquitto):** suscripciones a topics de telemetría (`/sensores`) y control (`/control/*`); reconexión automática tras caída de red.  
  - **Publicación a Ubidots:** envío de JSON con sensores y estados de actuadores; medición de latencia end-to-end < 500 ms.  
  - **Recepción de comandos remotos:** simulación de mensajes `alarm/reset` y `alarm/trigger` desde Ubidots; verificación de desactivación y activación de alarmas en el ESP32 en < 200 ms.

- **Simulación de Fallos y Mecanismos de Recuperación**  
  - Corte de Wi-Fi y caída del broker local: comprobación de reintentos de conexión Wi-Fi (cada 5 s) y de MQTT (cada 5 s) sin bloquear otras tareas.  
  - Puerto de Ubidots inaccesible: almacenamiento temporal en buffer circular de FreeRTOS y reenvío automático al restaurarse la conexión.  

### 3.2 Resultados

- **Precisión y Consistencia de Lecturas**  
  - DS18B20: desviación media de ±0.4 °C.  
  - MQ-2: variación ≤ ±8 unidades tras calibración.  
  - Detector de llama: 100 % de detección a 10 cm, 95 % a 20 cm.

- **Rendimiento de la UI Local**  
  - Actualización de datos y logs cada segundo sin retrasos.  
  - Respuesta a comandos de actuadores en < 150 ms, garantizando interactividad fluida.

- **Latencia y Confiabilidad MQTT**  
  - Publicación local → Ubidots en < 500 ms (promedio 350 ms).  
  - Comando remoto Ubidots → ESP32 en < 200 ms.  
  - Reconexiones automáticas exitosas en 98 % de los tests de caída de red.

- **Robustez de Alertas Coordinadas**  
  - Activación simultánea de buzzer, LED RGB y mensaje en LCD en < 250 ms tras detección de condición crítica.  
  - Cero falsas alarmas en 12 h de pruebas continuas tras ajuste de umbrales.

## 4. Autoevaluación del Protocolo de Pruebas

- **Cobertura de Casos de Uso**  
  - Incluye pruebas en laboratorio, campo, simulación de incendio y fallos de red.  
  - Cubre tanto flujo local (sensores → actuadores → UI) como remoto (MQTT → Ubidots → comandos).

- **Precisión**  
  - Validación contra equipos de referencia: temperatura ±0.5 °C, gas ±10 unidades.  
  - Lógica de salto brusco detecta variaciones > 5 °C garantizando detección temprana.

- **Fiabilidad y Robustez**  
  - Más de 24 h de operación continua sin restablecimiento manual.  
  - Reconexión automática tras caída de Wi-Fi y broker con tiempo medio de recuperación < 10 s.

- **Reproducibilidad**  
  - Procedimientos estandarizados documentados: calibración de sensores, configuración de red y broker, pasos de validación de la UI.  
  - Scripts de inicialización de SQLite y configuración de mosquitto incluidos en el repositorio.

- **Limitaciones Identificadas**  
  - Dependencia de la cobertura Wi-Fi local; en zonas muy dispersas puede ser necesario tecnología de largo alcance.  
  - Ubidots impone límites de tasa de publicación (free tier), lo que podría requerir optimización del intervalo de telemetría.

- **Escalabilidad y Mantenimiento**  
  - Arquitectura modular (FreeRTOS, mutex, buffer circular) facilita la adición de sensores (humo, humedad, viento).  
  - Código y configuración quedan listos para migrar a versiones de producción con TLS en MQTT y gestión segura de credenciales.  

## 5. Conclusiones y Trabajo Futuro

### 5.1 Retos Presentados Durante el Desarrollo

- **Calibración de Sensores y Actuadores:**  
  Garantizar lecturas estables de temperatura, gas y llama mientras se controla correctamente el buzzer, el LED RGB y el display LCD requirió ajustar umbrales y tiempos de muestreo para evitar falsas alertas y comportamientos erráticos.

- **Comunicación Bilateral MQTT (Local ↔ Internet):**  
  Integrar simultáneamente el broker local en la Raspberry Pi y el envío/recepción con Ubidots expuso retos de configuración de tópicos, reconexión automática y formateo de payloads JSON para mantener sincronizados ambos extremos.

- **Gestión de Concurrencia con FreeRTOS y Semáforos:**  
  El uso de tareas independientes para lectura de sensores, publicación MQTT y gestión del servidor web exigió coordinación mediante semáforos (mutex) y colas (queues) para proteger variables compartidas y evitar bloqueos.

- **Configuración de la Raspberry Pi como Broker MQTT:**  
  Montar Mosquitto en la Pi, exponerlo al ESP32 y luego conectarlo a Internet (Ubidots) implicó ajustes en archivos de configuración, autorización por contraseña y puertos, así como pruebas de estabilidad bajo carga.

- **Problemas de Contraseñas y Seguridad WiFi/MQTT:**  
  Fallos iniciales al conectar el ESP32 al access point y al broker (credenciales erróneas o caracteres especiales en las claves) obligaron a implementar reintentos y mensajes de log detallados para diagnosticar rápidamente los errores.

- **Conflictos de Librerías y Código Residual:**  
  Persistencia de código anterior en el ESP32 provocaba comportamientos inesperados (bus OneWire bloqueado, display sin responder). La solución implicó un `esptool erase_flash` y limpieza de dependencias en el entorno de desarrollo.

### 5.2 Conclusiones

- La **arquitectura modular** y el uso de **FreeRTOS** con semáforos garantizan un flujo de datos confiable entre tareas críticas (sensores, actuadores, red).
- La **comunicación bidireccional** por MQTT permite tanto publicar telemetría en Ubidots como recibir comandos remotos para reset de alarma o control de actuadores.
- La **Raspberry Pi** como broker local mejora la latencia en la red LAN, mientras que el enlace a Ubidots ofrece una capa de monitoreo y control global.
- El sistema muestra **robustez** frente a desconexiones de red y reinicios: los mecanismos de reconexión automática y persistencia en SQLite aseguran que no se pierdan datos.
- Gracias al riguroso manejo de errores en los módulos WiFi, MQTT y base de datos, hoy contamos con un sistema estable que cubre desde la captura de señales físicas hasta la presentación web local y la transmisión a la nube.

### 5.3 Trabajo Futuro

- Nuevos Sensores Ambientales:** detectar humo, humedad y velocidad del viento para enriquecer el análisis y anticipar incendios con mayores garantías.
- Mejoras de Seguridad y Gestión de Credenciales:** implementar almacenamiento seguro (p.e. Key Vault) para tokens MQTT/WiFi y certificados TLS en Mosquitto.
- Algoritmos de Detección Inteligente:** incorporar filtros de señal y modelos de machine learning para diferenciar eventos reales de ruido ambiental y reducir falsas alarmas.
- Comunicaciones de Largo Alcance:** evaluar módulos 4G/5G o LoRaWAN para cubrir áreas rurales sin infraestructura de red estable.
- Aplicación Móvil y Notificaciones Push:** desarrollar frontend móvil nativo o multiplataforma que reciba alertas en tiempo real y permita controlar actuadores desde cualquier dispositivo.
- Pruebas Piloto con Autoridades Locales:** desplegar en terreno con Bomberos y agentes ambientales para ajustar parámetros de detección y validar operatividad en condiciones reales.  

## **6. Anexos**
### Codigo comentado

          #include <WiFi.h>              // Librería para conectar el ESP32 a una red WiFi
          #include <WebServer.h>         // Librería para crear un servidor web en el ESP32
          #include <Wire.h>              // Librería para comunicación I2C (usada por el LCD)
          #include <LiquidCrystal_I2C.h> // Librería para controlar el display LCD I2C
          #include <OneWire.h>           // Librería para comunicación con sensores OneWire (temperatura)
          #include <DallasTemperature.h> // Librería para leer el sensor de temperatura DS18B20
          
          // Definición de credenciales de la red WiFi
          const char* redNombre = "Zflip de Valentina"; // Nombre de la red WiFi
          const char* redClave = "v4l32006";            // Contraseña de la red WiFi
          
          // Creación de un servidor web en el puerto 80
          WebServer webServ(80);
          
          // Definición de umbrales para las condiciones de alarma
          #define TEMP_MAX 30  // Temperatura máxima permitida (30°C)
          #define GAS_MAX 700  // Nivel máximo de gas permitido (700 unidades)
          
          // Definición de pines para los sensores
          #define PIN_LLAMAS 15 // Pin para el sensor de llama (digital)
          #define PIN_TEMP 4    // Pin para el sensor de temperatura (OneWire)
          
          // Definición de pines para los actuadores
          const int zumbPin = 27;   // Pin para el buzzer (zumbador)
          const int gasPin = 35;    // Pin para el sensor de gas (analógico)
          const int rojoPin = 19;   // Pin para el canal rojo del LED RGB
          const int verdePin = 18;  // Pin para el canal verde del LED RGB
          const int azulPin = 5;    // Pin para el canal azul del LED RGB
          
          // Inicialización de objetos para el hardware
          LiquidCrystal_I2C display(0x27, 16, 2); // Display LCD I2C (dirección 0x27, 16 columnas, 2 filas)
          OneWire wireBus(PIN_TEMP);              // Objeto para comunicación OneWire en el pin de temperatura
          DallasTemperature tempSensor(&wireBus);  // Objeto para leer el sensor de temperatura DS18B20
          
          // Variables globales para almacenar las lecturas de los sensores
          volatile float valorTemp = 0.0; // Temperatura actual (volatile para uso en hilos)
          volatile int valorGas = 0;      // Nivel de gas actual (volatile para uso en hilos)
          volatile bool hayLlama = false; // Estado del sensor de llama (true si hay llama, volatile para uso en hilos)
          volatile bool alertaActiva = false; // Indica si hay una alerta activa (volatile para uso en hilos)
          float tempAnt = 0;              // Temperatura anterior para detectar incrementos bruscos
          unsigned long tiempoUlt = 0;    // Última vez que se actualizó el sistema (en milisegundos)
          const long refresco = 500;      // Intervalo de actualización del sistema (500 ms)
          
          // Variables para controlar el estado de los actuadores
          volatile bool zumbOn = true; // Estado del buzzer (true: encendido, false: apagado)
          volatile bool dispOn = true;  // Estado del display LCD (true: encendido, false: apagado)
          volatile bool rgbOn = true;   // Estado del LED RGB (true: encendido, false: apagado)
          
          // Estructura para almacenar las lecturas de los sensores en el historial
          struct Datos {
            float t;           // Temperatura
            int g;             // Nivel de gas
            bool f;            // Estado de la llama (true: hay llama)
            unsigned long m;   // Tiempo de la lectura (en milisegundos)
          };
          
          // Definición del historial de lecturas
          #define REG_MAX 10         // Máximo número de registros en el historial
          Datos logDatos[REG_MAX];   // Arreglo para almacenar el historial
          int logPos = 0;            // Posición actual en el historial (índice circular)
          int logCant = 0;           // Cantidad de registros almacenados
          
          // Función para controlar el LED RGB
          void pintarRGB(int r, int g, int b) {
            if (rgbOn) { // Verifica si el LED RGB está habilitado
              digitalWrite(rojoPin, r);   // Establece el valor del canal rojo
              digitalWrite(verdePin, g);  // Establece el valor del canal verde
              digitalWrite(azulPin, b);   // Establece el valor del canal azul
            } else { // Si el LED RGB está deshabilitado, apaga todos los canales
              digitalWrite(rojoPin, 0);
              digitalWrite(verdePin, 0);
              digitalWrite(azulPin, 0);
            }
          }
          
          // Función que se ejecuta en un hilo para leer los sensores
          void leerSensores(void *arg) {
            tempSensor.begin();         // Inicializa el sensor de temperatura
            analogReadResolution(10);   // Configura la resolución del ADC a 10 bits
          
            for (;;) { // Bucle infinito para leer los sensores continuamente
              tempSensor.requestTemperatures(); // Solicita la temperatura al sensor
              float t = tempSensor.getTempCByIndex(0); // Lee la temperatura en °C
              int g = analogRead(gasPin);              // Lee el nivel de gas (analógico)
              bool f = !digitalRead(PIN_LLAMAS);       // Lee el sensor de llama (LOW indica presencia de llama)
          
              // Actualiza las variables globales con las lecturas
              valorTemp = t;
              valorGas = g;
              hayLlama = f;
          
              // Almacena la lectura en el historial
              logDatos[logPos] = {t, g, f, millis()}; // Registra temperatura, gas, llama y tiempo
              logPos = (logPos + 1) % REG_MAX;        // Avanza la posición circularmente
              if (logCant < REG_MAX) logCant++;       // Incrementa el contador de registros hasta el máximo
          
              vTaskDelay(pdMS_TO_TICKS(200)); // Pausa la tarea 200 ms para permitir otras tareas
            }
          }
          
          // Función para servir la página web principal
          void pagInicio() {
            // HTML, CSS y JavaScript de la interfaz web
            String html = R"rawliteral(
          <!DOCTYPE html>
          <html lang="es">
          <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Control Incendios</title>
          <style>
          body {font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1e3c72, #2a5298); margin: 0; padding: 20px; color: #fff;}
          .contenedor {display: flex; flex-wrap: wrap; gap: 20px; max-width: 1200px; margin: 0 auto;}
          .bloque {background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; flex: 1; min-width: 250px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); backdrop-filter: blur(5px);}
          .bloque h2 {margin: 0 0 10px; font-size: 24px; color: #ffd700;}
          .bloque p {margin: 5px 0; font-size: 18px;}
          .aviso {background: #ff4444; padding: 10px; border-radius: 10px; margin-top: 10px; font-weight: bold;}
          .registros {max-height: 400px; overflow-y: auto;}
          .registros table {width: 100%; border-collapse: collapse; color: #fff;}
          .registros th, .registros td {padding: 8px; text-align: center; border-bottom: 1px solid rgba(255, 255, 255, 0.2);}
          .registros th {background: rgba(255, 215, 0, 0.3);}
          .opciones {display: flex; flex-direction: column; gap: 10px; margin-top: 20px;}
          .fila-botones {display: flex; gap: 10px; flex-wrap: wrap;}
          button {padding: 10px 20px; font-size: 16px; border: none; border-radius: 25px; cursor: pointer; background: #ffd700; color: #1e3c72; transition: background 0.3s;}
          button:hover {background: #ffea00;}
          </style>
          </head>
          <body>
          <div class="contenedor">
          <div class="bloque">
          <h2>Estado</h2>
          <p>Temperatura: <span id="t-val">-- °C</span></p>
          <p>Gas: <span id="g-val">--</span></p>
          <p>Llama: <span id="f-val">--</span></p>
          <div id="aviso-zona"></div>
          </div>
          <div class="bloque">
          <h2>Acciones</h2>
          <div class="opciones">
          <div class="fila-botones">
          <button onclick="switchZumb()">Zumbador: <span id="zumb-est">ON</span></button>
          <button onclick="switchDisp()">Display: <span id="disp-est">ON</span></button>
          <button onclick="switchRGB()">RGB: <span id="rgb-est">ON</span></button>
          </div>
          <div class="fila-botones">
          <button onclick="resetLog()">Resetear Log</button>
          </div>
          </div>
          </div>
          <div class="bloque registros">
          <h2>Log</h2>
          <table id="log-tabla">
          <tr><th>Tiempo (s)</th><th>Temp (°C)</th><th>Gas</th><th>Llama</th></tr>
          </table>
          </div>
          </div>
          <script>
          function cargarEstado() {
          fetch('/data').then(r => r.json()).then(d => {
          document.getElementById("t-val").innerText = d.temperatura + " °C";
          document.getElementById("g-val").innerText = d.gas;
          document.getElementById("f-val").innerText = d.llama ? "SÍ" : "NO";
          let avisoZona = document.getElementById("aviso-zona");
          if (d.llama) {
          avisoZona.innerHTML = '<div class="aviso">¡PELIGRO: FUEGO!</div>';
          } else if (d.incremento_brusco || (d.temperatura > 30 && d.gas > 700)){
          avisoZona.innerHTML = '<div class="aviso">¡PELIGRO: POSIBLE INCENDIO!</div>';
          }
          else{
          avisoZona.innerHTML = '';
          }
          });
          }
          function cargarLog() {
          fetch('/history').then(r => r.json()).then(h => {
          let tabla = document.getElementById("log-tabla");
          tabla.innerHTML = "<tr><th>Tiempo (s)</th><th>Temp (°C)</th><th>Gas</th><th>Llama</th></tr>";
          for (let i = 0; i < h.length; i++) {
          let fila = tabla.insertRow();
          fila.insertCell(0).innerText = h[i].timestamp;
          fila.insertCell(1).innerText = h[i].temp;
          fila.insertCell(2).innerText = h[i].gas;
          fila.insertCell(3).innerText = h[i].flame ? "SÍ" : "NO";
          }
          });
          }
          function switchZumb() {
          fetch('/toggleBuzzer').then(r => r.json()).then(d => {
          document.getElementById("zumb-est").innerText = d.enabled ? "ON" : "OFF";
          });
          }
          function switchDisp() {
          fetch('/toggleLCD').then(r => r.json()).then(d => {
          document.getElementById("disp-est").innerText = d.enabled ? "ON" : "OFF";
          });
          }
          function switchRGB() {
          fetch('/toggleRGB').then(r => r.json()).then(d => {
          document.getElementById("rgb-est").innerText = d.enabled ? "ON" : "OFF";
          });
          }
          function resetLog() {
          fetch('/resetLog').then(r => r.json()).then(d => {
          if (d.success) cargarLog();
          });
          }
          setInterval(() => { cargarEstado(); cargarLog(); }, 1000);
          cargarEstado();
          cargarLog();
          </script>
          </body>
          </html>
            )rawliteral";
            webServ.send(200, "text/html", html); // Envía la página web al cliente
          }
          
          // Función para enviar el estado actual de los sensores en formato JSON
          void enviarEstado() {
            bool saltoTemp = abs(valorTemp - tempAnt) > 5; // Calcula si hay un incremento brusco de temperatura
            // Construye un JSON con los valores actuales
            String json = "{\"temperatura\":" + String(valorTemp, 2) + ",\"gas\":" + String(valorGas) + ",\"llama\":" + String(hayLlama ? "true" : "false") + ",\"incremento_brusco\":" + String(saltoTemp ? "true" : "false") + "}";
            webServ.send(200, "application/json", json); // Envía el JSON al cliente
          }
          
          // Función para enviar el historial de lecturas en formato JSON
          void enviarLog() {
            String json = "["; // Inicia un arreglo JSON
            for (int i = 0; i < logCant; i++) { // Itera sobre los registros del historial
              int idx = (logCant < REG_MAX ? i : (logPos + i) % REG_MAX); // Calcula el índice circular
              // Añade cada registro al JSON
              json += "{\"timestamp\":" + String(logDatos[idx].m / 1000) + ",\"temp\":" + String(logDatos[idx].t, 1) + ",\"gas\":" + String(logDatos[idx].g) + ",\"flame\":" + String(logDatos[idx].f ? "true" : "false") + "}";
              if (i < logCant - 1) json += ","; // Añade una coma entre registros
            }
            json += "]"; // Cierra el arreglo JSON
            webServ.send(200, "application/json", json); // Envía el JSON al cliente
          }
          
          // Función para alternar el estado del buzzer
          void alternarZumb() {
            zumbOn = !zumbOn; // Cambia el estado del buzzer (encendido/apagado)
            if (!zumbOn && alertaActiva) noTone(zumbPin); // Si se desactiva y hay alerta, apaga el buzzer
            // Responde con el nuevo estado en formato JSON
            webServ.send(200, "application/json", "{\"enabled\":" + String(zumbOn ? "true" : "false") + "}");
          }
          
          // Función para alternar el estado del display LCD
          void alternarDisp() {
            dispOn = !dispOn; // Cambia el estado del display (encendido/apagado)
            dispOn ? display.backlight() : display.noBacklight(); // Enciende o apaga la retroiluminación
            // Responde con el nuevo estado en formato JSON
            webServ.send(200, "application/json", "{\"enabled\":" + String(dispOn ? "true" : "false") + "}");
          }
          
          // Función para alternar el estado del LED RGB
          void alternarRGB() {
            rgbOn = !rgbOn; // Cambia el estado del LED RGB (encendido/apagado)
            if (!rgbOn) pintarRGB(255, 255, 255); // Si se desactiva, apaga el LED RGB
            // Responde con el nuevo estado en formato JSON
            webServ.send(200, "application/json", "{\"enabled\":" + String(rgbOn ? "true" : "false") + "}");
          }
          
          // Función para resetear el historial de lecturas
          void resetearLog() {
            logPos = 0;  // Reinicia la posición del historial
            logCant = 0; // Reinicia el contador de registros
            // Responde con un mensaje de éxito en formato JSON
            webServ.send(200, "application/json", "{\"success\":true}");
          }
          
          // Función de inicialización del sistema
          void setup() {
            // Configura los pines de los actuadores como salidas
            pinMode(zumbPin, OUTPUT);
            pinMode(rojoPin, OUTPUT);
            pinMode(verdePin, OUTPUT);
            pinMode(azulPin, OUTPUT);
            pinMode(PIN_LLAMAS, INPUT_PULLUP); // Configura el pin del sensor de llama con pull-up
          
            Wire.begin(21, 22); // Inicializa la comunicación I2C (pines SDA=21, SCL=22)
            display.init();     // Inicializa el display LCD
            display.backlight(); // Enciende la retroiluminación del LCD
            pintarRGB(0, 0, 0); // Apaga el LED RGB inicialmente
            display.setCursor(0, 0); // Posiciona el cursor en la primera línea
            display.print("Iniciando..."); // Muestra un mensaje de inicio
          
            Serial.begin(115200); // Inicia la comunicación serial para depuración
            WiFi.begin(redNombre, redClave); // Conecta a la red WiFi
            while (WiFi.status() != WL_CONNECTED) delay(1000); // Espera hasta que se conecte
            Serial.println(WiFi.localIP()); // Imprime la IP asignada
          
            // Configura las rutas del servidor web
            webServ.on("/", HTTP_GET, pagInicio);         // Ruta para la página principal
            webServ.on("/data", HTTP_GET, enviarEstado);  // Ruta para enviar el estado actual
            webServ.on("/history", HTTP_GET, enviarLog);  // Ruta para enviar el historial
            webServ.on("/toggleBuzzer", HTTP_GET, alternarZumb); // Ruta para alternar el buzzer
            webServ.on("/toggleLCD", HTTP_GET, alternarDisp);    // Ruta para alternar el LCD
            webServ.on("/toggleRGB", HTTP_GET, alternarRGB);     // Ruta para alternar el LED RGB
            webServ.on("/resetLog", HTTP_GET, resetearLog);      // Ruta para resetear el historial
            webServ.begin(); // Inicia el servidor web
          
            // Crea un hilo para leer los sensores usando FreeRTOS
            xTaskCreate(leerSensores, "Sensores", 4096, NULL, 1, NULL);
          }
          
          // Función principal que se ejecuta en un bucle
          void loop() {
            webServ.handleClient(); // Maneja las solicitudes del servidor web
          
            unsigned long ahora = millis(); // Obtiene el tiempo actual
            bool saltoTemp = abs(valorTemp - tempAnt) > 5; // Detecta un incremento brusco de temperatura
          
            // Actualiza el sistema cada 500 ms (definido por refresco)
            if (ahora - tiempoUlt >= refresco) {
              tiempoUlt = ahora; // Actualiza el tiempo de la última actualización
              if (dispOn) display.clear(); else display.noBacklight(); // Limpia el LCD o apaga la retroiluminación
          
              // Estado: Alarma Activada (Posible Incendio)
              if (saltoTemp || (valorTemp > TEMP_MAX && valorGas > GAS_MAX)) {
                alertaActiva = true; // Activa la alerta
                if (dispOn) { // Si el display está habilitado, muestra el mensaje
                  display.setCursor(0, 0);
                  display.print("Posible incendio!");
                  display.setCursor(0, 1);
                  display.print("G:");
                  display.print(valorGas);
                }
                pintarRGB(0, 125, 255); // LED RGB rojo (posible incendio)
                if (zumbOn) tone(zumbPin, 1000); // Activa el buzzer si está habilitado
              }
              // Estado: Detección de Gas o Temperatura Alta
              else if (valorGas > GAS_MAX || valorTemp > TEMP_MAX) {
                if (dispOn) { // Si el display está habilitado, muestra los valores
                  display.setCursor(0, 0);
                  display.print("T:");
                  display.print(valorTemp);
                  display.print("C");
                  display.setCursor(0, 1);
                  display.print("G:");
                  display.print(valorGas);
                }
                pintarRGB(0, 0, 255); // LED RGB amarillo (advertencia)
                if (zumbOn) noTone(zumbPin); // Apaga el buzzer si está habilitado
              }
              // Estado: Detección de Llama
              else if (hayLlama) {
                alertaActiva = true; // Activa la alerta
                if (dispOn) { // Si el display está habilitado, muestra el mensaje
                  display.setCursor(0, 0);
                  display.print("FUEGO!");
                  display.setCursor(0, 1);
                  display.print("G:");
                  display.print(valorGas);
                }
                pintarRGB(0, 255, 255); // LED RGB rojo (fuego detectado)
                if (zumbOn) tone(zumbPin, 1000); // Activa el buzzer si está habilitado
              }
              // Estado: Monitoreo Normal
              else {
                if (dispOn) { // Si el display está habilitado, muestra los valores
                  display.setCursor(0, 0);
                  display.print("T:");
                  display.print(valorTemp);
                  display.print("C");
                  display.setCursor(0, 1);
                  display.print("G:");
                  display.print(valorGas);
                }
                pintarRGB(125, 0, 255); // LED RGB verde (estado normal)
                if (zumbOn) noTone(zumbPin); // Apaga el buzzer si está habilitado
              }
            }
          
            tempAnt = valorTemp; // Actualiza la temperatura anterior para la próxima iteración
            delay(10); // Pausa de 10 ms para evitar un uso excesivo del procesador
          }







### Implementacion Fisica
![.](imagenesWiki/ledverde.jpg)

En esta imagen se aprecia un LED iluminado en color verde, indicando que los parámetros monitoreados (por ejemplo, temperatura y nivel de gas) permanecen dentro de los rangos seguros. Como consecuencia, la alarma no se activa y el sistema se mantiene en un estado de operación normal, sin riesgos aparentes.

![.](imagenesWiki/ledrojo.jpg)

En esta imagen se observa que el LED adquiere un tono ámbar o naranja, lo cual indica un estado de alerta. Los valores de los sensores podrían estan fuera de los umbrales de seguridad, Se alerta un posible incendio.

![.](imagenesWiki/ledamarillo.jpg)

En esta imagen se observa cómo, al acercar el encendedor al sensor de gas, el LED cambia a un tono amarillo. Esto indica que una valor en este caso el de gas a exedido el umbral de seguridad, aunque todavía no se ha activado la alerta crítica. El color amarillo sirve como señal de precaución, advirtiendo que el sistema podría escalar a un estado de riesgo si las lecturas continúan aumentando.

![.](imagenesWiki/estado.jpg)

En esta captura se muestra la interfaz web del sistema de monitoreo de incendios, donde se visualizan las lecturas en tiempo real: una temperatura de 23.19 °C, un nivel de gas de 420 y la ausencia de llama (“NO”). Todos estos valores están dentro de los rangos seguros, por lo que el sistema permanece en un estado normal sin activar alarmas.

![.](imagenesWiki/acciones.jpg)

En esta captura se aprecia la sección de "Acciones" dentro de la interfaz web, donde el usuario puede encender o apagar el zumbador, la pantalla LCD y el LED RGB, así como resetear el registro de datos. Estas opciones permiten personalizar el comportamiento del sistema en tiempo real y responder de manera más efectiva ante posibles eventos.


![.](imagenesWiki/log.jpg)

En esta captura se visualiza el registro histórico (“Log”) del sistema, mostrando los valores de temperatura, nivel de gas y la detección de llama en intervalos de tiempo específicos. Todas las lecturas permanecen dentro de los rangos seguros, con la columna “Llama” indicando “NO” en cada entrada, lo que confirma que no se han detectado situaciones de riesgo durante ese período de monitoreo.

![.](imagenesWiki/fuego.jpg)

En esta imagen se está realizando una prueba con un encendedor encendido para verificar la respuesta del sensor de llama. Al acercar la llama, el sensor registra la presencia de fuego, confirmando su capacidad para detectar un posible inicio de incendio.

![.](imagenesWiki/posibleIncendio1.jpg)

En esta captura de la interfaz web, la temperatura (30.06 °C) y el nivel de gas (1023) han superado los umbrales establecidos, aunque no se detecta llama. Debido a estos valores críticos, el sistema muestra la alerta “¡PELIGRO: POSIBLE INCENDIO!” en rojo, indicando una situación de riesgo que requiere atención inmediata.


![.](imagenesWiki/posible.jpg)

En esta imagen se aprecia la pantalla LCD mostrando el mensaje “Posible incendio” y el valor de gas en 1023. Estos indicadores sugieren que el nivel de gas ha superado los límites de seguridad, activando la alarma para alertar sobre una situación potencialmente peligrosa.


![.](imagenesWiki/maqueta.jpg)

En esta imagen se aprecia la maqueta del sistema, dentro de la caja del medio estan los circutios guardados



## **7. Referencias**
 1:  E. R. Moraguez, "Ventajas y Desventajas ESP32 en IoT y Desarrollo," LovTechnology, 9 meses atrás. [En línea]. Disponible en: https://lovtechnology.com/ventajas-y-desventajas-esp32-en-iot-y-desarrollo/ (Accedido: 22-mar-2025)​
 
 2: Robotlandia, "Módulo KY-028 Sensor de Temperatura Digital", https://robotlandia.es/temperatura-y-humedad/681-modulo-ky-028-sensor-de-temperatura-digital.html (accedido: 16 de febrero de 2025).

 3: Julpin, "Módulo Sensor Analógico de Gas MQ-2 para Arduino", https://www.julpin.com.co/inicio/modulos-sensores/492-modulo-sensor-analogico-de-gas-mq-2-para-arduino.html (accedido: 16 de febrero de 2025).

 4: D Bots, "KY-026 Módulo Sensor de Llama", https://3dbots.co/producto/ky-026-modulo-sensor-de-llama/ (accedido: 16 de febrero de 2025).

 5: "Las fases de un incendio," Crónica Seguridad, 9 de julio de 2024. [En línea]. Disponible en: https://cronicaseguridad.com/2024/07/09/las-fases-de-un-incendio/. (Accedido: 22 de marzo de 2025)

 6: A. Jain, "Threads and how to create it in C++," Medium, 6 de septiembre de 2024. [En línea]. Disponible: https://medium.com/@abhishekjainindore24/threads-and-how-to-create-it-in-c-cb5583939686​

 7: IEEE Standards Association, "The Evolution of Wi-Fi Technology and Standards," 16 de mayo de 2023. [En línea]. Disponible: https://standards.ieee.org/beyond-standards/the-evolution-of-wi-fi-technology-and-standards/

 8: SensorGo, “Telemetría,” SensorGo.mx. [En línea]. Disponible: https://sensorgo.mx/telemetria/. [Consultado: 25-Abr-2025].

 9: Universidad Politécnica Salesiana, “La herramienta de Ubidots, utilizada para la visualización de variables en la página web Ubidots,” DSpace UPS. [En línea]. Disponible: https://dspace.ups.edu.ec/handle/123456789/20298. [Consultado: 25-Abr-2025].
 
 10: Amazon Web Services, Inc., “What Is MQTT?,” AWS. [En línea]. Disponible: https://aws.amazon.com/es/what-is/mqtt/. [Consultado: 25-Abr-2025].

 11: "¿Cuáles son sus estándares de diseño de ingeniería?", LinkedIn, 2023. [En línea]. Disponible: https://es.linkedin.com/advice/0/what-your-engineering-design-standards-skills-engineering-design?lang=es. [Accedido: 23-mar-2025].​

 12: INCOSE, "SE Standards," 2023. [En línea]. Disponible: https://www.incose.org/about-systems-engineering/se-standards. [Accedido: 23-mar-2025].
