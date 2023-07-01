# Client

Unter dem Client werden alle Dienste zusammengefasst, die auf dem Client, in diesem Fall ein Raspberry PI, ausgeführt werden.

## Getting started

Alle Dienste können mit dem folgenden Befehl gestartet werden.
```console
docker compose up
```

**Kein Docker installiert?**

[Anleitung zum Installieren von Docker auf Raspberry OS](https://docs.docker.com/engine/install/raspbian/)


## Docker
Alle Dienste werden isoliert als Docker-Container gestartet. Dazu enthält jeder Dienst ein eigenes Dockerfile um das jeweilige Image zu bauen. Alle Dienste können mit Docker-Compose gestaretet werden. Die Einstellungen befinden sich dafür in der Datei "docker-compose.yml".

Docker Images:
- htwberlin/mdwvzaehlerstaende-client-watcher
- htwberlin/mdwvzaehlerstaende-client-ws

### Docker-Compose
Damit innerhalb des Docker-Containers des Watcher-Dienstes auf den Kamera des Raspberry PI zugeriffen werden kann, muss der Zugriff erlaubt werden. Dazu werden Die Geräte "/dev/vchiq" und "/dev/vcsm", sowie das Verzeichnis "/opt/vc" in der docker-compose.yml gemapped werden. 

Damit auf Dateien, wie Einstellungen oder Bilddateien, von beiden Containern zugeriffen werden können, existiert das Volume "/var/shared_client_files".

Außerdem wurde mit dem Script "docker_compose_start.sh" die Möglichkeit geschaffen vor Ausführung des Docker-Compose-Befehls zu überprüfen, ob eine Kamera mit dem Raspberry PI verbunden ist. Dadurch lässt sich dieser mögliche Fehler vor Ausführung der einzelnen Docker-Container aufspüren.