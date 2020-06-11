# WWW Übung 4 - Kommunikationsnetze

## Teil I - Vermittlung

### 1 - Übertragungszeiten

#### a - Compute Cluster -> CS35

Wir berechnen zunächst ``` 18 MiB = 151 Mbit (rund)```.

Bei nachrichtenvermittelter Übertragung können wir einfach die Übertragungszeiten der einzelnen Verbindungsteile sowie die Latenzen addieren und erhalten:
```
0,001 s + 151 Mbit / 4000 Mbit/s + 151 Mbit / 40 Mbit/s + 
0,020 s + 151 Mbit / 1000 Mbit/s + 151 Mbit / 100 Mbit/s 
= 5,47475 s
```

Bei paketvermittelter Übertragung rechen wir zunächst die MTU in Bit um und erhalten ``` 8 * 1500 Byte = 12000 Bit ```

Nun können wir 151 Mbit auf das nächste Vielfache von 12000 Bit aufrunden und erhalten ```151 008 000 Bit```

Führen wir nun obige Berechnung mit dieser Datenmenge durch, erhalten wir
```
0,001 s + 151 008 000 Bit / 4000 Mbit/s + 151 008 000 Bit / 40 Mbit/s + 
0,020 s + 151 008 000 Bit / 1000 Mbit/s + 151 008 000 Bit / 100 Mbit/s 
= 5,49504 s
```

#### b - Jued30 -> Moench

Bei nachrichtenvermittelter Übertragung gehen wir wieder ähnlich wie in a vor.
```
0,001 s + 151 Mbit / 500 Mbit/s + 0,001 s + 151 Mbit / 400 Mbit/s
= 0,6815 s
```

Bei paketvermittelter Übertragung gehen wir auch hier ähnlich wie in a vor.Dabei erhalten wir
```
0,001 s + 151 008 000 Bit / 500 Mbit/s + 0,001 s +
151 008 000 Bit / 400 Mbit/s
= 0,681536 s
```

### 2 - Parallele Telefonate

Laut [Wikipedia](https://de.wikipedia.org/wiki/IP-Telefonie#Durchsatz) wird bei einem IP-Telefonat eine Datenrate von ```64 Kbit/s``` rein für die Payload und von ```100 Kbit/s``` mitsamt dem Overhead durch Protokolle und Header benötigt.

In diesem Fall begrenzt das AirFiber zwischen Jued30 und Stack Ref2 die maximale Geschwindigkeit auf der Verbindung. Da Telefonate symmetrisch sind und somit in beide Richtungen gleich viele Daten übertragen werden, steht uns auch nur die geringere der beiden Geschwindigkeiten des AirFiber zur Verfügung, also ```300 Mbit/s```. Damit können wir nun einfach die Anzahl der möglichen parallelen Telefonate berechnen:
```
(300 Mbit/s) / (100 Kbit/s) = 3000 Telefonate
```

### 3 - Backup Compute Cluster

#### a - Geschwindigkeit ohne Compute Cluster

Wir runden 2 TB auf das nächste Vielfache von 1500 Byte auf und erhalten ```2 000 000 001 000 Byte bzw. 16 000 000 008 000 Bit```. Nun können wir wieder wie in Aufgabe 1 verfahren und erhalten:
```
16 000 000 008 000 Bit / 400 Mbit/s + 0,001 s + 
16 000 000 008 000 Bit / 600 Mbit/s + 0,001 s +
16 000 000 008 000 Bit / 1000 Mbit/s
= 82666,669 s  
```

Praktisch ist der Durchsatz jedoch geringer, unter anderem aufgrund des Overheads durch Paketheader, Latenzen und die Geschwindigkeit des Backup-Systems.

#### b - Geschwindigkeit mit Compute Cluster
Nun berücksichtigen wir zusätzlich die Geschwindigkeit der Verbindung Stack Ref2 - Compute Cluster. Damit erhöht sich die Zeit um
```
16 000 000 008 000 Bit / 16000 Mbit/s = 1000 s 
```

Außerdem wird nun die Geschwindigkeit des Backup-Systems mit einberechnet. Da dieses ein RAID 5 mit 3 Festplatten benutzt, muss effektiv das 1,5-fache der eigentlichen Nutzdaten gespeichert werden. Dafür stehen summiert 60 MB/s zur Verfügung. Somit erhalten wir als benötigte Zeit für das Speichern:
```
1,5 * 2 TB / 60 Mbit/s = 50000 s
```
Insgesamt erhalten wir also jetzt als Zeit 133 666 s.

### 4 - Daten "in der Luft"
Dies können wir recht einfach berechnen, indem wir zunächst die Übertragungszeit aus der Länge der Verbindung und der Lichtgeschwindigkeit berechnen und dann mit der Datendurchsatzrate multiplizieren. Wir erhalten:
```
(200 m / 300 000 000 m/s) * (300 Mbit/s + 500 Mbit/s) = 533 Bit
```

## Teil II - Klassifikation

### 1 - Lasten-/Sicherheitsverbund

Ein Lastenverbund ist ein Verbund von Rechnern/Systemen, bei dem zwischen den verbundenen Rechnern ein Lastausgleich stattfindet. Dies kann für Serversysteme sinnvoll sein, um Anfragen möglichst schnell bearbeiten zu können (z.B. bei Content Delivery Networks), indem die Auslastung der einzelnen Systeme ausgeglichen wird, sodass kein System überlastet wird

Ein Sicherheitsverbund ist ein Verbund von Systemen, bei dem beim Ausfall eines Systems andere Systeme dessen Funktionen übernehmen. Dies kann sinnvoll sein, um Redundanz und damit hohe Verfügbarkeit zu gewährleisten, beispielsweise bei der Datenspeicherung mittels RAID.

### 2 - HPI-Netz

Beim HPI-Netz handelt es sich bezüglich der räumlichen Ausdehnung um ein Local Area Network, da sich sämtliche Systeme im Umkreis von 1 km auf den drei Campus befinden (wenn man von den per VPN verbundenen Geräten absieht). Weiterhin handelt es sich beim HPI-Netz um ein inhomogenes Rechnernetz, da zu ihm Rechner vieler unterschiedlicher Typen gehören (z.B. PCs mit verschiedenen Betriebssystemen, Server, Access Points, Drucker, ...).

## Teil III - Sicherheit

### 1 - Geschlossen vs. offen

Geschlossene Netze sind meist sicherer als offene Netze, da ein Angreifer bei ihnen physikalischen Zugang benötigt, um einen Angriff zu starten. Es ist jedoch trotz allem für Angreifer nicht unmöglich, physikalischen Zugang zu erlangen, weshalb auch geschlossene Netze durchaus angreifbar sind. Bei offenen Netzen ist es dagegen durch geeignete Sicherheitsmaßnahmen möglich, die Angriffsgefahr zu verringern.

### 2 - Angriff

a) Folgende Sicherheitsziele können verletzt werden:
* Confidentiality - Dem Angreifer ist es offensichtlich möglich, die Kommunikation des Switches mitzuhören.
* Integrity - Da der Angreifer Zugriff auf den Switch hat, kann er dessen Kommunikation auch verändern (sofern sie nicht verschlüsselt ist).
* Authenticity - Wenn der Angreifer die Kommunikation verändern kann, ist es ihm auch möglich, die Absenderinformationen zu verändern.
* Availability - Der Angreifer könnte z. B. die Source Address Table des Switches so verändern, dass alle Pakete an einen einzigen Rechner gesendet werden, der so überlastet wird.

Folgende Sicherheitsziele können eher nicht verletzt werden:
* Non-Repudiation - Da die Verbindlichkeit meist mittels elektronischer Signaturen o.ä. gewährleistet wird, wird es dem Angreifer vermutlich nicht möglich sein, die Kommunikation zu verändern, ohne dass solche Signaturen ungültig werden.

b) Da der Angreifer Zugriff auf ein Gerät innerhalb des Netzwerks hat, ist es ihm möglich, passiv die Kommunikation des Switches aufzuzeichnen, ohne diese zu verändern.

### 3 - Kryptosysteme

Es handelt sich dabei um symmetrische (Secret Key) und asymmetrische (Public Key) Kryptosysteme.