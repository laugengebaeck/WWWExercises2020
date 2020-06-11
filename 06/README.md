# WWW - Übungsblatt 6

(Matrikelnummer: 801005)

## Teil I - Routing-Tabellen

### 1 - Dijkstra-Algorithmus

### 2 - Distanzvektor-Routing

## Teil II - Recherche-Aufgaben

### 1 - DHCP

### 2 - Informationsaustausch bei DHCPv4

### 3 - DHCPv6 und Router Advertisement

### 4 - Neighbor Discovery

#### a - Neighbor Discovery Protocol

NDP übernimmt die Funktion des Address Resolution Protocol (ARP) bei IPv6. Es ist also für die Auflösung von IPv6-Adressen zu MAC-Adressen verantwortlich.

#### b - Unterschiede IPv4 und NDP

* NDP führt die Adressauflösung mittels ICMP auf dem Internet Layer statt wie ARP auf dem Link Layer durch. Dadurch ist es weniger vom Medium abhängig.
* IPv6-Router können über NDP eine für den gesamten Link (also alle Hosts) geltende MTU bekanntgeben. Bei ARP ist das nicht möglich.
* Mittels Router-Advertisement-Nachrichten kann NDP eine automatische Adresskonfiguration durchführen (ähnlich wie DHCP bei IPv4).

### 5 - Netzmaske und IP-Adressen

Die Netzmaske ist hier 255.255.192.0. Das Netz 249.151.128.0/18 umfasst alle IP-Adressen, bei denen die ersten 18 Bits genau den ersten 18 Bits von 249.151.128.0 entsprechen. Die ersten 16 Bit (also 249.151) stimmen bei 249.151.101.89 und 249.151.201.83 offensichtlich jeweils überein. Nun schreiben wir das dritte Byte der IPs jeweils in binär:

```python
128 = 10000000
101 = 01100101
201 = 11001001
```

Wie man sieht, unterscheiden sich bei beiden IPs jeweils die ersten zwei Bit des dritten Bytes vom Netz. Folglich ist keine der beiden IP-Adressen in diesem Netz enthalten.

### 6 - IP-ID

Eine IP-ID wird zum Zusammensetzen von zuvor fragmentierten IP-Datenpaketen beim Empfänger benötigt. Mithilfe dieses Feldes und der Source Address kann er die Zusammengehörigkeit von Fragmenten feststellen und sie mithilfe des Headerfelds *Fragment Offset* wieder zusammensetzen.

RFC 791 definiert das Identification-Headerfeld als
> An identifying value assigned by the sender to aid in assembling the fragments of a datagram.

Damit wird explizit nicht vorgeschrieben, dass die ID fortlaufend sein muss. Sie muss lediglich pro Paket eindeutig sein, um die Zusammengehörigkeit der Fragmente feststellen können. Die Reihenfolge der Fragmente wiederum wird durch den Fragment Offset festgelegt und nicht durch die IP-ID.

### 7 - traceroute

Traceroute arbeitet mithilfe von ICMP-Echo-Requests, welche an den Zielhost gesendet werden. Solche Echo-Requests entsprechen dabei der Aufforderung, das erhaltene Paket unverändert zurückzusenden. Dabei kann eine Time To Live (TTL), also die maximale Anzahl an Hops, mitgesendet werden. Traceroute sendet zunächst ein Paket mit einer TTL von 1 an den Zielhost. Der erste Router dekrementiert nun die TTL und sendet, da die TTL nun 0 ist, eine ICMP-Antwort "Time Exceeded" an den Sender, wobei er als Source seine eigene IP-Adresse angibt. Nun wird das ganze mit immer um eins höheren TTLs wiederholt, wodurch auch die IP-Adressen aller weiteren Hops bekannt werden. Dies geht so lange, bis der Ziel-Host erreicht wird (der dann mit einer ICMP Echo Reply antwortet) oder die von Traceroute bestimmte Maximalanzahl an Hops erreicht ist.

Der von Traceroute ermittelte Weg muss nicht immer der tatsächliche sein. Dies kann zum Beispiel durch Firewalls, NAT, IP-Tunnel oder die Wahl einer anderen Route bei Überlastung beeinflusst werden.

(Eigentlich verwendet nur Windows-Traceroute ICMP. Linux-Traceroute benutzt UDP, erhält aber als Antwort auch ICMP-Pakete.)

### 8 - Fragmentierung und MTU Path Discovery

TODO

### 9 - Verkürzung IP-Adresse

Gekürzt erhalten wir 0:0:500::400a:9999.

## Teil III - Routing in der Praxis

### 3 - Flag fd60:XX::2

### 6 - Bonus-Flags
