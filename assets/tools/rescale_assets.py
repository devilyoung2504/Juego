from pathlib import Path
from PIL import Image

# Carpetas
ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "assets" / "raw"
OUT_DIR = ROOT / "assets" / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Config: cambia lo que necesites
CONFIG = {
    # Nombre del archivo (en raw) : (modo, target)
    # modo "fit" = ajusta a una resolución exacta (ej fondo 384x216)
    # modo "height" = ajusta por altura (ej personajes 96px de alto)
    "bg_arena.png": ("fit", (384, 216)),

    "PJ1_right.png": ("height", 96),
    "PJ2_left.png": ("height", 96),
}

# Para pixelart: usar NEAREST (no blur)
RESAMPLE = Image.Resampling.NEAREST

def resize_fit(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    return img.resize(size, RESAMPLE)

def resize_by_height(img: Image.Image, target_h: int) -> Image.Image:
    w, h = img.size
    scale = target_h / h
    new_w = max(1, int(w * scale))
    return img.resize((new_w, target_h), RESAMPLE)

def main():
    if not IN_DIR.exists():
        print(f"No existe: {IN_DIR}")
        return

    for src_name, (mode, target) in CONFIG.items():
        src_path = IN_DIR / src_name
        if not src_path.exists():
            print(f"[SKIP] No encontrado: {src_path}")
            continue

        img = Image.open(src_path).convert("RGBA")

        if mode == "fit":
            out_img = resize_fit(img, target)  # (W,H)
        elif mode == "height":
            out_img = resize_by_height(img, target)  # H
        else:
            print(f"[SKIP] modo desconocido para {src_name}: {mode}")
            continue

        out_path = OUT_DIR / src_name
        out_img.save(out_path, "PNG")
        print(f"[OK] {src_name} -> {out_path} size={out_img.size}")

if __name__ == "__main__":
    main()