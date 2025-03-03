# mqtt-repo

# MQTT Simulator

Questo progetto è un simulatore MQTT che genera e pubblica dati casuali su un broker MQTT, simulando il controllo visivo di sensori.  

## 📌 Funzionalità
- Si connette a un broker MQTT specificato tramite variabili d'ambiente.
- Pubblica dati simulati su un topic MQTT.
- Riceve comandi su un topic dedicato e modifica il comportamento della simulazione.
- Logga informazioni di connessione e pubblicazione per monitoraggio.

---

## 🚀 Avvio del Simulatore

### 1️⃣ **Esecuzione con Docker**
Per avviare il container, usa il seguente comando:
```bash
docker run -e MQTT_BROKER=your-mqtt-broker \
           -e MQTT_PORT=1883 \
           -e MQTT_USERNAME=user \
           -e MQTT_PASSWORD=pass \
           -e MQTT_TOPIC=sensor/visual_control \
           -e MQTT_TOPIC_COMMAND=sensor/command \
           ghcr.io/ilpupo02/mqtt-repo/mqtt-simulator:latest
