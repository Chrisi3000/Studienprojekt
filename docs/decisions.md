# Architekturentscheidungen

Dieses Dokument hält nur Entscheidungen fest, die aus dem aktuellen Repository
belegt sind. Es werden keine neuen Zielarchitekturen beschlossen. Vor jeder 
Änderung der Architektur muss der/die User*in die Entscheidung bestätigen. 

- Das Programm ist eine Kommandozeilenanwendung. 
- Die Plot-Erzeugung erfolgt lokal in Python mit den Paketen `pysam` und `matplotlib`.
- Wir verwenden Docker für die Ausführung des Programms. 

## Scope
- Es wird keine Webanwendung oder API-Schnittstelle oder Datenbank implementiert.
- Die Plot-Erzeugung bleibt synchron. 
- Zum Testen werden die vorhandenen Testdaten genutzt.

## Umgang mit Annahmen

Die Erstversion nimmt nur an, dass die vorhandenen Entrypoints, Datenflüsse und
Ausgabearten aktuell relevant sind. Diese Annahme wird durch den vorhandenen
Code gestützt, ersetzt aber keine Produktentscheidung. Nicht belegte
Technologie- oder Betriebsentscheidungen dürfen nicht ergänzt werden.
