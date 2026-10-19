# Projektziel

## Zweck

Dieses Repository stellt mit `samplot` ein Kommandozeilenwerkzeug zur visuellen
Prüfung struktureller Varianten (Structural Variants, SVs) in genomischen
Alignments bereit. 

Das Projektziel in der aktuell belegbaren Form ist:

1. Einen einzelnen Genomabschnitt aus SAM-, BAM- oder CRAM-Dateien als Plot
   darzustellen (`samplot plot`).
2. Varianten aus einer VCF-Datei zu lesen, zu filtern und für passende Varianten
   Plots zu erzeugen (`samplot vcf`).
3. Die Ergebnisse als Bilddateien und beim VCF-Modus zusätzlich als
   HTML-Übersicht bereitzustellen.
4. Die Logik für die SVs Deletionen, Duplikationen, Inversionen und Translokationen
   existierten bereits in der Erstversion, zugänglich über folgenden Link in GitHub:
   https://github.com/ryanlayer/samplot/tree/master. Die Aufgabe dieses Projekts ist es, 
   die bereits existierende Logik um die Darstellung von Insertions (in long und short reads)
    zu erweitern.

## Eingaben und Ergebnisse

**Belegt durch den Code:**

- `samplot plot` erwartet mindestens eine indizierte Alignment-Datei (`-b`),
  Koordinaten (`-c`, `-s`, `-e`) und optional einen SV-Typ.
- CRAM-Eingaben benötigen eine Referenzdatei (`-r`).
- `samplot vcf` verarbeitet eine VCF-Datei, ordnet deren Samples BAM/CRAM-Dateien
  zu und kann optional eine PED/FAM-Datei sowie Annotationen verwenden.
- Die Plotlogik liest Alignments mit `pysam` und erzeugt Grafiken mit
  `matplotlib`.
- Die CLI wird über den installierten Einstiegspunkt `samplot` gestartet.

Die genaue Auswahl von Varianten und Samples wird über vorhandene
CLI-Optionen wie `--filter`, `--min_call_rate`, `--max_hets`, `--dn_only`,
`--min_entries` und `--max_entries` gesteuert. Diese Datei legt keine neuen
Filterregeln fest.

## Scope

Es soll keine Webanwendung oder API-Schnittstelle oder Datenbank implementiert werden.
Das Tool soll nur um die Logik zur Darstellung von Insertions erweitert werden.

## Annahmen dieser Erstversion

- **Annahme A1:** Das Repository ist primär ein eigenständiges Python-CLI-Paket
  und nicht nur eine Sammlung von Testskripten. Das folgt aus `setup.py`, dem
  Console-Entry-Point und `samplot/__main__.py`.
- **Annahme A2:** Bilddateien und die HTML-Übersicht sind die fachlichen
  Ergebnisse. Das folgt aus der Plot-Ausgabe in `samplot.py`, `write_site()` in
  `samplot_vcf.py` und den Testdaten.
- **Annahme A3:** Die vorhandenen Testdaten dienen der reproduzierbaren
  Entwicklung und nicht als produktiver Datenspeicher. Ihre Dateiformate und
  Nutzung in `test/` belegen die Testrolle; eine weitergehende
  Betriebsanforderung ist nicht dokumentiert.

Diese Annahmen sind Arbeitsannahmen für die Dokumentation und keine
Architekturentscheidungen. Sie müssen bei neuen fachlichen Anforderungen
bestätigt oder ersetzt werden.
