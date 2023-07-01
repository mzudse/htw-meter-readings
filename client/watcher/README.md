# Client: Watcher

Der Watcher läuft auf dem Raspberry PI und ist dabei verantwortlich für das das Erstellen eines Bildes mit der verbundenen Kamera. In diesem Fall wird die Kamera mithilfe des Moduls "PiCamera" angesprochen.


Das erfasste Bild wird in dem aktuellen Verzeichnis unter dem Namen "current_cam.png" abelegt. Durch die Docker-Compose-Konfiguration wird diesem Verzeichnis als Volume freigeben, sodass das Bild von dem "Client Webservice" verwendet werden kann.

## Aktivitätsdiagramm
![Client Watcher Activity Diagram](./doc/client_watcher_activity_diagram.png)