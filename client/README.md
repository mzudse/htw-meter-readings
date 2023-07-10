# Client

Unter dem Client werden alle Dienste zusammengefasst, die auf dem Client, in diesem Fall einem Raspberry PI, ausgeführt werden.

## Getting started

In der Datei *docker-compose.yml* müssen für die Container *watcher* und *clientws* die Umgebungsvariablen angepasst werden. Für den Watcher und den Client-Webservice muss die URL für den Server-Webservice angepasst werden und zusätzlich bei dem Watcher der Client-Name. Der Client-Name dient dabei der Identifikation des Datenpunktes in der InfluxDB.

```yaml
watcher:
    environment:
        - SERVER_WEBSERVICE=http://server-webservice.local:5002/
        - CLIENT_NAME=raspberrypi-keller
clientws:
    environment:
      - SERVER_WEBSERVICE=http://server-webservice.local:5002/
```

Alle Dienste können mit dem folgenden Befehl gestartet werden.
```console
docker compose up
```

**Kein Docker installiert?**

[Anleitung zum Installieren von Docker auf Raspberry OS](https://docs.docker.com/engine/install/raspbian/)


## Docker
Alle Dienste werden isoliert als Docker-Container gestartet. Dazu enthält jeder Dienst ein eigenes Dockerfile, um das jeweilige Image zu bauen. Alle Dienste können mit Docker-Compose gestartet werden. Die Einstellungen dafür befinden sich in der Datei "docker-compose.yml".

Docker Images:
- htwberlin/mdwvzaehlerstaende-client-watcher
- htwberlin/mdwvzaehlerstaende-client-ws

### Docker-Compose
Damit innerhalb des Docker-Containers des Watcher-Dienstes auf die Kamera des Raspberry PI zugeriffen werden kann, muss der Zugriff auf diese erlaubt werden. Dazu werden Die Geräte "/dev/vchiq" und "/dev/vcsm", sowie das Verzeichnis "/opt/vc" in der docker-compose.yml eingebunden. 

Damit auf Dateien, wie Einstellungen oder Bilddateien, von beiden Containern zugeriffen werden können, existiert das Volume "/var/shared_client_files".

Außerdem wurde mit dem Script "docker_compose_start.sh" die Möglichkeit geschaffen vor Ausführung des Docker-Compose-Befehls zu überprüfen, ob eine Kamera mit dem Raspberry PI verbunden ist. Dadurch lässt sich dieser mögliche Fehler vor Ausführung der einzelnen Docker-Container aufspüren.