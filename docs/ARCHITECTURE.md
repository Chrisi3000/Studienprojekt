# Architekturübersicht

## Systemgrenze

Die belegte Systemgrenze ist ein Python-Paket mit einer Kommandozeilenschnittstelle.
`setup.py` installiert das Paket `samplot` und registriert den Einstiegspunkt
`samplot = samplot.__main__:main`.

```text
CLI: samplot
  |
  +-- samplot plot
  |     +-- Argumentvalidierung in samplot/samplot.py
  |     +-- Alignment-/Referenzzugriff über pysam
  |     +-- Plotberechnung und Ausgabe über matplotlib
  |
  +-- samplot vcf
        +-- VCF-/PED-/Annotation-Lesen in samplot/samplot_vcf.py
        +-- Filterung und Kommandoerzeugung
        +-- Aufruf der Plotlogik
        +-- Bilddateien und HTML-Übersicht
```

## Komponenten

### CLI und Dispatch

`samplot/__main__.py` erstellt den globalen `argparse`-Parser, registriert die
Subcommands `plot` und `vcf` (über `add_plot()` und `add_vcf()`) und übergibt die Verarbeitung an die jeweiligen
Module. Die Versionsnummer kommt aus `samplot/__init__.py`.

### Plot-Komponente

`samplot/samplot.py` enthält sowohl die CLI-Definition (`add_plot()`) als auch die
fachliche Verarbeitung. Die Verarbeitung umfasst unter anderem:

- Ermittlung der darzustellenden Genomintervalle,
- Lesen und Aufbereitung von Coverage, Paired-End-, Split- und Long-Read-Daten,
- optionale Annotationen und Transkripte (für einen Standard-Plot nicht erforderlich),
- Darstellung von Varianten und Legenden,
- Schreiben des Plot-Ergebnisses.

Der aktuelle Code verwendet keine explizit getrennten Domain-, Service- und Infrastruktur-
Schichten. 

### VCF-Komponente

`samplot/samplot_vcf.py` liest VCF-Daten, optionale PED/FAM-Daten und optionale
Annotationen. Sie ordnet Samples den Alignment-Dateien zu, wendet die vorhandenen
Filter an, erzeugt Plot-Kommandos und führt diese aus. Für die HTML-Ausgabe wird das Template
`samplot/templates/samplot_vcf.html` verwendet.

### Laufzeit und Verpackung

`requirements.txt` definiert die direkten Python-Abhängigkeiten. Das
`Dockerfile` verwendet Python 3.10, installiert zusätzlich `samtools` und
installiert anschließend das Paket. `compose.yaml` startet einen interaktiven
Container und bindet `test/data` nach `/data`.

Die CircleCI-Konfiguration führt Unit- und funktionale Tests auf Linux und macOS
aus.

## Datenfluss

Beim `plot`-Subcommand werden CLI-Parameter validiert, Eingabedateien geöffnet,
Genomintervalle und Plotdimensionen berechnet, Read-Daten aufbereitet und das
Ergebnis als Bild geschrieben.

Beim `vcf`-Subcommand werden zuerst VCF-Samples und optionale Stammdaten gelesen.
Danach werden Varianten und Samples anhand der implementierten Regeln ausgewählt.
Für die verbleibenden Varianten entstehen Plot-Aufrufe; anschließend werden die
Plots ausgeführt oder als Kommandodatei abgelegt und die HTML-Seite geschrieben.

Testdaten bleiben vorerst im Repository, um die Reproduzierbarkeit der Entwicklung zu gewährleisten.
## Bewusste Grenzen und offene technische Fragen

- Es ist nicht bestätigt, ob die CLI-Kompatibilität langfristig stabil bleiben
  muss.
- Es ist nicht bestätigt, welche Python-Versionen außerhalb des Dockerfiles
  unterstützt werden.

