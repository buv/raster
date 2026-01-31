# Linienraster-Halftone

Erzeugt ein Linienraster-Halftone aus einem Graustufenbild mit kubischer Spline-Interpolation für glatte Linienmodulation.

## Features

- Linienraster im -30° Winkel
- 8 LPI (Lines Per Inch)
- Ausgabe: 150cm Breite bei 300 DPI (~17.700 Pixel)
- Kubische Spline-Interpolation für weiche Übergänge
- Optionale Tonwertspreizung und Gamma-Korrektur
- Rot- und Blaufilter für analoge SW-Fotografie-Effekte

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Verwendung

```bash
source venv/bin/activate
python halftone.py <eingabebild> [optionen]
```

### Optionen

| Option | Beschreibung |
|--------|--------------|
| `-o, --output` | Ausgabedatei (default: output.png) |
| `-a, --autoscale` | Tonwerte auf 0..255 normalisieren |
| `-g, --gamma` | Gamma-Korrektur (default: 1.0) |
| `-d, --dpi` | Ausgabeauflösung (default: 300) |
| `-w, --width` | Kleinere Ausdehnung in mm (default: 1500) |
| `--min-gray` | Minimaler Grauwert (default: 0) |
| `--max-gray` | Maximaler Grauwert (default: 255) |
| `--red` | Rotfilter-Intensität 0..1 (default: 0) |
| `--blue` | Blaufilter-Intensität 0..1 (default: 0) |

### Farbfilter

Die Filter simulieren analoge SW-Fotografie-Filter:

- `--red 1.0`: Reiner Rotkanal – Himmel wird dunkler, Hauttöne heller
- `--blue 1.0`: Reiner Blaukanal – Himmel wird heller, Hauttöne dunkler
- Werte zwischen 0 und 1 interpolieren linear zwischen Standard-Luminanz (0.299R, 0.587G, 0.114B) und dem reinen Kanal

### Beispiele

```bash
# Standard
python halftone.py foto.jpg

# Mit Autoscale
python halftone.py foto.jpg -a

# Mit Gamma-Korrektur (heller)
python halftone.py foto.jpg -g 0.8 -o output_hell.png

# Mit Rotfilter (dramatischer Himmel)
python halftone.py foto.jpg --red 0.7 -a

# Kleinere Ausgabe für Plotter
python halftone.py foto.jpg -w 500 -d 150
```

## Verarbeitungsreihenfolge

1. Farbfilter (RGB-Gewichtung)
2. Autoscale (Tonwertspreizung)
3. Gamma-Korrektur
4. Min/Max Grauwert-Skalierung

## Ausgabe

- Format: PNG, 1-bit Schwarzweiß
- Größe: Abhängig von `-w` und `-d`
- Default: ~17.700 × proportionale Höhe Pixel (150cm bei 300 DPI)
