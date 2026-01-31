# Linienraster-Halftone

Erzeugt ein Linienraster-Halftone aus einem Graustufenbild mit kubischer Spline-Interpolation für glatte Linienmodulation.

## Features

- Linienraster im -30° Winkel
- 8 LPI (Lines Per Inch)
- Ausgabe: 150cm Breite bei 300 DPI (~17.700 Pixel)
- Kubische Spline-Interpolation für weiche Übergänge
- Optionale Tonwertspreizung und Gamma-Korrektur

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

### Beispiele

```bash
# Standard
python halftone.py foto.jpg

# Mit Autoscale
python halftone.py foto.jpg -a

# Mit Gamma-Korrektur (heller)
python halftone.py foto.jpg -g 0.8 -o output_hell.png

# Mit Gamma-Korrektur (dunkler)
python halftone.py foto.jpg -g 1.5 -o output_dunkel.png
```

## Ausgabe

- Format: PNG, 1-bit Schwarzweiß
- Größe: ~17.700 × proportionale Höhe Pixel
- Auflösung: 300 DPI bei 150cm Druckbreite
