# AGENTS.md

Arbeitsgrundlage und Anlaufstelle für KI-Coding-Agents in diesem Repository.

## Projektziel

Das Projekt erweitert das bestehende Python-CLI-Tool `samplot` um die Darstellung
von Insertions in Short- und Long-Read-Daten.

Der aktuelle Funktionsumfang umfasst insbesondere:

- `samplot plot` zur Darstellung eines Genomabschnitts
- `samplot vcf` zur Verarbeitung und Filterung von Varianten aus VCF-Dateien
- Unterstützung für SAM-, BAM- und CRAM-Dateien
- Visualisierung struktureller Varianten und Alignment-Daten
- Ausgabe von Plot-Bildern und beim VCF-Modus einer HTML-Übersicht

Es soll keine Webanwendung, API oder Datenbank entwickelt werden, sofern dies
nicht ausdrücklich neu bestätigt wird.

## Arbeitsprinzipien

- Bevorzuge einfache, nachvollziehbare Lösungen.
- Verstehe zuerst den bestehenden Code, bevor du ihn änderst.
- Halte Änderungen klein und auf eine logische Aufgabe begrenzt.
- Bewahre das bestehende CLI-Verhalten, sofern eine Änderung nicht ausdrücklich
  gewünscht ist.
- Triff keine unbestätigten Architekturentscheidungen.
- Kennzeichne Annahmen sehr ausdrücklich.
- Erkläre komplexe oder wissenschaftliche Logik so, dass sie auch zum Lernen
  geeignet ist.
- Vermeide neue Abhängigkeiten, wenn die bestehende Lösung ausreicht.
- Ändere keine fremden oder nicht zur Aufgabe gehörenden Änderungen im
  Arbeitsverzeichnis.
- Versuche, Lösungen nicht zu overengineeren.

## Architektur

Die Architektur ist in `docs/ARCHITECTURE.md` beschrieben.

Wichtige Einstiegspunkte:

- `samplot/__main__.py`
  - erstellt den globalen CLI-Parser
  - registriert die Subcommands `plot` und `vcf`
  - ruft die jeweils hinterlegte Verarbeitungsfunktion auf
- `samplot/samplot.py`
  - definiert und verarbeitet `samplot plot`
  - liest Alignment-Daten
  - berechnet und erzeugt Plots
- `samplot/samplot_vcf.py`
  - definiert und verarbeitet `samplot vcf`
  - liest und filtert VCF-Varianten
  - ordnet Samples Alignment-Dateien zu
  - erzeugt Plot-Aufrufe und die HTML-Übersicht
- `samplot/templates/samplot_vcf.html`
  - Template für die VCF-Ergebnisübersicht
- `samplot/__init__.py`
  - enthält die Paketversion

Der aktuelle Code verwendet keine explizit getrennten Domain-, Service- und
Infrastruktur-Schichten. Führe eine solche Aufteilung nicht ohne bestätigte
Anforderung ein.

## Technologien

Bevorzugte und bereits verwendete Technologien:

- Python
- `argparse`
- `pysam`
- `matplotlib`
- `numpy`
- `Jinja2`
- Docker und Docker Compose
- Shell-Skripte für funktionale Tests

Die direkten Python-Abhängigkeiten stehen in `requirements.txt`.
Das Dockerfile verwendet Python 3.10 und installiert zusätzlich `samtools`.

Neue Bibliotheken dürfen nur eingeführt werden, wenn sie für die Aufgabe
wirklich erforderlich sind. Die Notwendigkeit und der Einfluss auf Setup und
Dokumentation müssen erklärt werden.

## Änderungsablauf

1. Lies die relevanten Dateien und die zugehörige Dokumentation.
2. Suche nach bestehender Logik, die wiederverwendet werden kann.
3. Beschreibe bei größeren Änderungen kurz:
   - Ziel der Änderung
   - betroffene Dateien
   - Annahmen
   - geplante Tests
4. Implementiere die kleinste sinnvolle Lösung.
5. Ergänze oder aktualisiere Tests für verändertes Verhalten.
6. Aktualisiere die direkt betroffene Dokumentation.
7. Führe geeignete Tests aus.
8. Prüfe den Diff auf unbeabsichtigte Änderungen.

Bei neuen oder geänderten fachlichen Regeln müssen insbesondere
`docs/GOAL.md`, `docs/ARCHITECTURE.md`, `docs/decisions.md` und
`docs/progress.md` auf Aktualisierungsbedarf geprüft werden.

```bash
bash runtests.sh