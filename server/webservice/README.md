# Server: Webservice

Der Webservice läuft auf dem Server und enthält die OCR-Logik, auf welche über die API zugegriffen werden kann.

## OCR-Prozess

Zur Umsetzung des OCR-Prozesses wurde Tesseract verwendet. Tesseract ist eine weit verbreitete Open-Source-Software zur optischen Zeichenerkennung (OCR), die es ermöglicht, Text aus Bildern und Dokumenten zu extrahieren und zu verstehen. Es wurde ursprünglich von Hewlett-Packard Laboratories entwickelt und später von Google weiterentwickelt.

1. Erhalte das Bild als base64-String.
2. Erstelle ein Bild mittels des base64-Strings.
3. Auf das Bild werden Graustufen angewendet, sodass der Kontrast besser ist.
4. Das Bild mit Graustuffen wir mittels Tesseract analysiert. Der Inhalt des Bildes wird von Tesseract als einzeiliger Text betrachtet, was über den Set Page Segmentation Mode 7 eingestellt werden.
5. Konvertierung und Validierung des Ergebnisses
6. Speicherung des Ergebnisses (Zählerstand) in der InfluxDB

## Quellen

https://github.com/tesseract-ocr/tesseract, abgerufen am 08.07.2023 um 23:50