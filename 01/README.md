# Übung 1 - Teil 2: Theoretische Grundlagen
(Matrikelnummer: 801005)

## Aufgabe 1 - Internetstandards, Internetorganisationen

### 1a - Internet-Standardisierungsprozess

Der Internet-Standardisierungsprozess erfolgt mittels *RFCs (Request for Comments)*, die Vorschläge für neue Internet-Standards oder zur Erweiterung bestehender enthalten. Ein solcher RFC beginnt nach der Einsendung durch eine Person oder Arbeitsgruppe als **Internet Draft**, also als vorläufige Version, die zur Stellungnahme und Diskussion gedacht ist. Wird dieser von der *Internet Engineering Steering Group (IESG)* oder der *Internet Engineering Task Force (IETF)* genehmigt, wird er zum **Proposed Standard**. Um schließlich zu einem richtigen **Internet Standard** zu werden, müssen nun mehrere unterschiedliche Implementierungen des Standards existieren und großflächig eingesetzt werden. Außerdem wird vom *Internet Architecture Board (IAB)* der Status bzw. die Bedeutung des Standards festgelegt.

### 1b - RFCs 1149, 2324

Bei *RFC 1149* handelt es sich um das **Internet Protocol over Avian Carriers**, das den Transport von Datenpaketen mittels Brieftauben erlaubt. *RFC 2324* dagegen ist das **Hyper Text Coffee Pot Control Protocol**, mit dem vernetzte Kaffeemaschinen gesteuert werden können. Gemeinsam ist diesen beiden Standards, dass es sich dabei um Aprilscherze handelt. Diese enthalten zwar interessante Ideen, sind aber eher nicht praktikabel umsetzbar. Beispielsweise benötigt mit IPoAC ein Ping rund 45 Minuten. Sie beweisen jedoch meiner Meinung nach den Humor von IAB, IETF und IRTF. ;)

## Aufgabe 2 - Schichtenmodell

### 2a - ASCII-Art

```
+---+-------------------+
| 4 | Application Layer |
+---+-------------------+
| 3 | Transport Layer   |
+---+-------------------+
| 2 | Internet Layer    |
+---+-------------------+
| 1 | Link Layer        |
+---+-------------------+
+---+-------------------+
| 0 | Hardware  Layer   |  <--- gehört nicht zum eigentlichen Schichtenmodell
+---+-------------------+
```

### 2b - Idee des Schichtenmodells

Die Idee des Schichtenmodells sagt aus, dass die Kommunikationsaufgaben eines Netzwerkbetriebssystems in mehrere Schichten aufgeteilt werden. Jede dieser Schichten löst ein Teilproblem, wobei sie dazu nur mit den ihr benachbarten Schichten kommunizieren kann. Ein solches Modell ist für das Internet sinnvoll, weil die zu lösenden Kommunikationsaufgaben zwar komplex sind, jedoch sehr gut hierarchisch in Teilprobleme aufgeteilt werden können. Dadurch kann die Kommunikationsaufgabe modular gelöst werden.

### 2c - Application Layer

Da jeder Layer nur mit den ihm benachbarten Layern kommuniziert, kennt der Application Layer ausschließlich den Transport Layer.