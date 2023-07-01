# Client

Unter dem Client werden alle Dienste zusammengefasst, die auf dem Client, in diesem Fall ein Raspberry PI, ausgeführt werden.

## Docker
Alle Dienste werden isoliert als Docker-Container gestartet. Dazu enthält jeder Dienst ein eigenes Dockerfile um das jeweilige Image zu bauen. Alle Dienste können mit Docker-Compose gestaretet werden. Die Einstellungen befinden sich dafür in der Datei "docker-compose.yml".

Images:
    - htwberlin/mdwvzaehlerstaende-client-watcher
    - htwberlin/mdwvzaehlerstaende-client-ws

### Docker-Compose
Damit innerhalb des Docker-Containers des Watcher-Dienstes auf den Kamera des Raspberry PI zugeriffen werden kann, muss der Zugriff erlaubt werden. Dazu werden Die Geräte "/dev/vchiq" und "/dev/vcsm", sowie das Verzeichnis "/opt/vc" in der docker-compose.yml gemapped werden. 

Außerdem wurde mit dem Script "docker_compose_start.sh" die Möglichkeit geschaffen vor Ausführung des Docker-Compose-Befehls zu überprüfen, ob eine Kamera mit dem Raspberry PI verbunden ist. Dadurch lässt sich dieser mögliche Fehler vor Ausführung der einzelnen Docker-Container aufspüren.