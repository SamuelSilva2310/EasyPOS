import os
import cairosvg

# === SETTINGS ===
INPUT_DIR = "svg_icons"         # Folder containing your SVG files
OUTPUT_DIR = "images/icons"    # Output folder for PNGs
SIZES = [24, 48, 64]        # You can change/add sizes here

# =================

def convert_all_svgs(input_dir, output_dir, sizes):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    svg_files = [f for f in os.listdir(input_dir) if f.endswith(".svg")]
    if not svg_files:
        print("⚠️ No SVG files found in", input_dir)
        return

    for svg_file in svg_files:
        svg_path = os.path.join(input_dir, svg_file)
        name = os.path.splitext(svg_file)[0]

        for size in sizes:
            out_dir = os.path.join(output_dir, str(size))
            os.makedirs(out_dir, exist_ok=True)
            png_path = os.path.join(out_dir, f"{name}.png")

            cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=size, output_height=size)
            print(f"✅ {svg_file} → {png_path}")

    print("\n🎉 Done! Converted", len(svg_files), "icons into PNGs at sizes:", sizes)


if __name__ == "__main__":
    convert_all_svgs(INPUT_DIR, OUTPUT_DIR, SIZES)