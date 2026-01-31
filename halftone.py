#!/usr/bin/env python3
"""Linienraster-Halftone mit kubischer Spline-Interpolation."""

import argparse
import numpy as np
from PIL import Image, ImageDraw
from scipy.interpolate import CubicSpline
import math

def main():
    parser = argparse.ArgumentParser(description='Erzeugt ein Linienraster-Halftone aus einem Graustufenbild.')
    parser.add_argument('input', help='Eingabebild (JPEG, PNG, etc.)')
    parser.add_argument('-o', '--output', default='output.png', help='Ausgabedatei (default: output.png)')
    parser.add_argument('-a', '--autoscale', action='store_true', help='Tonwerte auf 0..255 normalisieren')
    parser.add_argument('-g', '--gamma', type=float, default=1.0, help='Gamma-Korrektur (default: 1.0)')
    parser.add_argument('-d', '--dpi', type=int, default=300, help='Ausgabeauflösung (default: 300)')
    parser.add_argument('-w', '--width', type=float, default=1500, help='Kleinere Ausdehnung in mm (default: 1500)')
    parser.add_argument('--min-gray', type=int, default=0, help='Minimaler Grauwert (default: 0)')
    parser.add_argument('--max-gray', type=int, default=255, help='Maximaler Grauwert (default: 255)')
    args = parser.parse_args()

    LPI = 8
    ANGLE = -30

    img = Image.open(args.input).convert('L')
    
    # Ausgabegröße berechnen: width ist die kleinere Dimension
    width_px = int(args.width / 25.4 * args.dpi)
    if img.width < img.height:
        OUTPUT_WIDTH_PX = width_px
        new_height = int(img.height * OUTPUT_WIDTH_PX / img.width)
    else:
        new_height = width_px
        OUTPUT_WIDTH_PX = int(img.width * new_height / img.height)
    
    LINE_SPACING = args.dpi / LPI
    MAX_WIDTH = LINE_SPACING

    img = img.resize((OUTPUT_WIDTH_PX, new_height), Image.Resampling.LANCZOS)
    pixels = np.array(img, dtype=np.float32)

    # 1. Autoscale
    if args.autoscale:
        pmin, pmax = pixels.min(), pixels.max()
        print(f"Autoscale: {pmin:.0f}..{pmax:.0f} -> 0..255")
        if pmax > pmin:
            pixels = (pixels - pmin) / (pmax - pmin) * 255

    # 2. Gamma
    if args.gamma != 1.0:
        print(f"Gamma: {args.gamma}")
        pixels = 255 * (pixels / 255) ** args.gamma

    # 3. Min/Max Skalierung
    if args.min_gray != 0 or args.max_gray != 255:
        print(f"Grauwert-Bereich: {args.min_gray}..{args.max_gray}")
        pixels = args.min_gray + pixels / 255 * (args.max_gray - args.min_gray)

    print(f"Bildgröße: {OUTPUT_WIDTH_PX}x{new_height} ({OUTPUT_WIDTH_PX/args.dpi*25.4:.0f}x{new_height/args.dpi*25.4:.0f} mm)")

    canvas = Image.new('1', (OUTPUT_WIDTH_PX, new_height), 1)
    draw = ImageDraw.Draw(canvas)

    angle_rad = math.radians(ANGLE)
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    diag = math.sqrt(OUTPUT_WIDTH_PX**2 + new_height**2)
    num_lines = int(diag / LINE_SPACING) + 1
    cx, cy = OUTPUT_WIDTH_PX / 2, new_height / 2
    coarse_step = LINE_SPACING
    fine_step = LINE_SPACING / 4
    nx, ny = -sin_a, cos_a

    print(f"Zeichne {num_lines} Linien...")

    for i in range(num_lines):
        d = -diag/2 + i * LINE_SPACING
        px = cx + d * sin_a
        py = cy - d * cos_a
        x1, y1 = px - diag * cos_a, py - diag * sin_a
        x2, y2 = px + diag * cos_a, py + diag * sin_a

        line_len = 2 * diag
        num_coarse = int(line_len / coarse_step) + 1
        t_coarse = np.linspace(0, 1, num_coarse)
        widths_coarse = []

        for t in t_coarse:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            ix, iy = int(x), int(y)
            if 0 <= ix < OUTPUT_WIDTH_PX and 0 <= iy < new_height:
                brightness = pixels[iy, ix]
                widths_coarse.append((255 - brightness) / 255 * MAX_WIDTH)
            else:
                widths_coarse.append(0)

        if len(t_coarse) >= 4:
            spline = CubicSpline(t_coarse, widths_coarse)
            num_fine = int(line_len / fine_step) + 1
            t_fine = np.linspace(0, 1, num_fine)
            widths_fine = np.clip(spline(t_fine), 0, MAX_WIDTH)

            upper, lower = [], []
            for j, t in enumerate(t_fine):
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                half_w = widths_fine[j] / 2
                upper.append((x + nx * half_w, y + ny * half_w))
                lower.append((x - nx * half_w, y - ny * half_w))

            polygon = upper + lower[::-1]
            if len(polygon) >= 3:
                draw.polygon(polygon, fill=0)

        if i % 100 == 0:
            print(f"  Linie {i}/{num_lines}")

    canvas.save(args.output)
    print(f"Gespeichert: {args.output}")

if __name__ == '__main__':
    main()
