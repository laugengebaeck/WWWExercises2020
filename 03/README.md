# WWW - Übung 3
(Matrikelnummer: 801005)
## Teil 1
### 2 - JSON-Ausgabe
Ja, die JSON-Ausgabe für die LZW-Komprimierung ist sinnvoll, da sie neben dem komprimierten String weitere wichtige Informationen enthält (die Länge eines Zeichens in Bits und das Anfangs-Wörterbuch), welche für die Dekodierung benötigt werden.

## Teil 2 - Grafik- und Audiokodierung
### 1 - Additive und subtraktive Farbmischung
Additive und subtraktive Farbmischung verwenden unterschiedliche Ansätze zur Mischung von Farben aus Grundfarben. 

Bei additiver Farbmischung werden zur Grundfarbe *Schwarz* andere Farben hinzugemischt (also addiert). Dieses Vorgehen findet man z. B. beim *RGB-Farbmodell*, bei dem Farben aus unterschiedlichen Anteilen der drei selbstleuchtenden Grundfarben Rot, Grün und Blau gemischt werden.

Bei subtraktiver Farbmischung dagegen werden von der Grundfarbe *Weiß* andere Farben abgezogen (also subtrahiert). Dieser Ansatz ist beim *CMY(K)-Farbmodell* zu finden, bei dem Farbpigmente der Grundfarben Cyan, Magenta, Yellow/Gelb und gegebenenfalls Schwarz auf eine weiße Oberfläche aufgetragen werden.
### 2 - YUV
Beim YUV-Farbmodell werden Farben nicht mittels anderer Farben gemischt, sondern in einen Helligkeitsanteil (Luminanz) und einen Farbanteil (Chrominanz) zerlegt. 

Alle drei Modelle haben ihre Daseinsberechtigung, da sie für unterschiedliche Zwecke verwendet werden. Das RGB-Modell wird zur Speicherung von Grafiken und zur Darstellung auf Bildschirmen benutzt, CMYK dagegen zum Druck, während YUV sich gut zur Farbübertragung bei Analogfernsehen bzw. als YCbCr für JPEG-Komprimierung benutzt wird eignet.
### 3 - HSV-Farbkodierung
Um umrechnen zu können, normieren wir zunächst die RGB-Kodierung auf [0,1] und erhalten ```(R, G, B) = (244/255, 10/17, 14/85)```. Nun können wir die in den Folien angegebenen Formeln anwenden und erhalten:
``` 
m1 = max(R, G, B) = 244/255
m2 = min(R, G, B) = 14/85
delta = m1 - m 2 = 202/255

S = delta/m1 = (202/255)/(244/255) 
  = 101/122 = 0,828 (rund)

V = m1 = 244/255 = 0,957 (rund)

H = 60° * ((G-B)/2)
  = 60° * 18/85
  = 12,706° (rund)
(da m1 = R)
```
### 4 - Chroma Subsampling
Chroma Subsampling wird verwendet, um die Datenmenge bei der Speicherung von Grafiken zu reduzieren, indem Farbinformationen (im Gegensatz zu Helligkeitsinformationen) mit reduzierter Auflösung gespeichert werden. Dies funktioniert, da das menschliche Auge Farbinformation nur mit reduzierter Auflösung im Vergleich zu Helligkeitsinformation wahrnimmt.
### 5 - Abtasttheorem

## Teil 3 - Multimediale Daten
### 1 - Datenmenge
### 2 - Schul-Cloud

## Teil 4 - Videokodierung
### 1 - Interlacing
### 2 - AV1
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE5NTQ2NjMzNTIsLTE5ODY0NTI1MDYsLT
UzNTc5OTk2NywxOTAzOTg5ODQ1LC0xMTE5MzYyOTQzLC0xODMx
MTU0Njc0XX0=
-->