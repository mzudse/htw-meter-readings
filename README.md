# Zählerstände auswerten und in Grafana anzeigen
Das Ziel dieses Projektes ist es, Zählerstände, z.B. einen Stromzählerstand automatisiert
abzulesen, zu verarbeiten und im Anschluss auszuwerten. Die erfassten Daten können so
verwendet werden, um Auswertungen zu erstellen oder um Korrelationen mit anderen Daten
darzustellen (z.B. Wetterdaten).


Die Dokumentation ist in mehrere Dateien aufgeteilt, welche in jede Ordner gefunden werden können. Außerdem werden alle verfügbaren README's im Folgenden aufgelistet:
- [Client README](./client/README.md)
    - [Client-Watcher README](./client/watcher/README.md)
    - [Client-Webservice README](./client/webservice/README.md)
- [Server README](./server/README.md)
    - [Client-Watcher README](./server/webservice/README.md)

### Verwendete Technologien
- [Python 3](https://www.python.org/about/)
- [Bash](https://www.gnu.org/software/bash/)
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Docker](https://www.docker.com/)
- [Grafana](https://grafana.com/)
- [Tesseract](https://github.com/tesseract-ocr/tesseract)
- [Ubuntu](https://ubuntu.com/)
- [Raspberry PI OS](https://www.raspberrypi.com/software/)

### Hardware
Im Folgenden wird die verwendetet Hardware aufgelistet. Anzumerken ist dabei, dass sich dieses System mit wenig Aufwand an andere Hardware angepasst werden kann.

- Raspberry PI 2 (https://www.raspberrypi.org/)
- Raspberry PI Camera, sofern unterstützt von dem jeweiligen Raspberry PI. (https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)