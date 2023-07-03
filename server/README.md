# Server
Unter dem Server werden alle Dienste zusammengefasst, die auf dem Server. Dies kein ein lokaler, z.B. ein weiterer Raspberry PI sein, oder ein Server in einem Rechenzentrum.

## Getting started
Alle Dienste können mit dem folgenden Befehl gestartet werden.
```console
docker compose up
```

**Kein Docker installiert?**
[Anleitung zum Installieren von Docker auf Raspberry OS](https://docs.docker.com/engine/install/raspbian/)

## Webservice
[Klicke hier um zur README des Webservices zu kommen.](./webservice/README.md)

## InfluxDB
InfluxDB ist eine Open-Source-Datenbank, die speziell für die Verarbeitung von Zeitreihendaten entwickelt wurde. Sie wurde ursprünglich von InfluxData entwickelt und ist darauf ausgerichtet, große Mengen an Zeitreihendaten effizient zu speichern, abzurufen und zu analysieren. Zeitreihendaten sind Datenpunkte, die mit einem Zeitstempel versehen sind und in regelmäßigen Abständen erfasst werden, wie z.B. Sensordaten, Messungen oder Leistungsindikatoren.

Da wir ausschließlich Sensordaten und keine anderen Daten speichern, haben wir uns für diese Datenbank entschieden. Zusätzlich wird InfluxDB von Grafana standardmäßig als Datenquelle unterstützt.

## Grafana
Grafana ist eine Open-Source-Plattform für die Visualisierung und Analyse von Daten. Sie ermöglicht es, Daten aus verschiedenen Quellen zu erfassen, zu verarbeiten und in ansprechenden Dashboards darzustellen. Grafana bietet eine intuitive Benutzeroberfläche, mit der Benutzer ihre Daten in Form von Diagrammen, Grafiken, Tabellen und anderen visuellen Elementen präsentieren können.

Innerhalb von Grafana lassen sich Daten unter anderem aus den folgenden Datenquellen auswerten bzw. visualisieren:
- MySQL / PostgresQL / MS SQL Server
- Prometheus (Monitoring)
- Elasticsearch

## Docker
Alle Dienste werden isoliert als Docker-Container gestartet. Das Image des Webservices wird über ein eigenes Dockerfile gebaut. Alle anderen Dienste (Grafana und InfluxDB) verwenden die offiziellen Images der Anbieter. Die Einstellungen befinden sich dafür in der Datei "docker-compose.yml".

Docker Images:
- htwberlin/mdwvzaehlerstaende-server-ws
- grafana/grafana:10.0.1
- influxdb:2.7.1

### Docker-Compose
Damit innerhalb des Docker-Containers des Watcher-Dienstes auf den Kamera des Raspberry PI zugeriffen werden kann, muss der Zugriff erlaubt werden. Dazu werden Die Geräte "/dev/vchiq" und "/dev/vcsm", sowie das Verzeichnis "/opt/vc" in der docker-compose.yml gemapped werden. 

Damit auf Dateien, wie Einstellungen oder Bilddateien, von beiden Containern zugeriffen werden können, existiert das Volume "/var/shared_client_files".

Außerdem wurde mit dem Script "docker_compose_start.sh" die Möglichkeit geschaffen vor Ausführung des Docker-Compose-Befehls zu überprüfen, ob eine Kamera mit dem Raspberry PI verbunden ist. Dadurch lässt sich dieser mögliche Fehler vor Ausführung der einzelnen Docker-Container aufspüren.