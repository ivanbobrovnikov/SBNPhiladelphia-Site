"""Builds pixel-accurate window and paint masks for the SBN Studio car photos.

For each car we give a loose outline around the windows (and around the whole
body) plus a sample patch of the paint. Inside each loose outline, anything that
matches the paint colour is paint; everything else is glass. The result is
cleaned up and written as PNG masks the website uses with CSS mask-image.

Usage:  python make_masks.py <photos dir> <output dir>
Needs:  numpy, scipy, opencv-python-headless, pillow
"""
import json, os, sys
import cv2
import numpy as np
from scipy import ndimage

SRC, OUT = sys.argv[1], sys.argv[2]
CFG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "car-masks.json")))


def poly_mask(shape, polys, grow=0):
    m = np.zeros(shape[:2], np.uint8)
    for p in polys:
        cv2.fillPoly(m, [np.array(p, np.int32)], 255)
    if grow:
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (grow * 2 + 1,) * 2))
    return m > 0


def paint_mask(img, patch, thresh, l_weight):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    x0, y0, x1, y1 = patch
    ref = np.median(lab[y0:y1, x0:x1].reshape(-1, 3), axis=0)
    d = lab - ref
    dist = np.sqrt((d[..., 0] * l_weight) ** 2 + d[..., 1] ** 2 + d[..., 2] ** 2)
    return dist < thresh


def clean(m, open_px=2, close_px=6, min_area=400, max_hole=None):
    """Remove specks, close small gaps, fill holes (all of them, or only those under max_hole px)."""
    k = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r * 2 + 1,) * 2)
    m = cv2.morphologyEx(m.astype(np.uint8) * 255, cv2.MORPH_OPEN, k(open_px))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k(close_px)) > 0
    holes = ndimage.binary_fill_holes(m) & ~m
    if max_hole is not None:
        hl, hn = ndimage.label(holes)
        hs = ndimage.sum(holes, hl, range(1, hn + 1))
        holes = np.isin(hl, [i + 1 for i, s in enumerate(hs) if s <= max_hole])
    m = m | holes
    lbl, n = ndimage.label(m)
    sizes = ndimage.sum(m, lbl, range(1, n + 1))
    keep = np.isin(lbl, [i + 1 for i, s in enumerate(sizes) if s >= min_area])
    return keep


def save(m, path):
    a = (m.astype(np.float32) * 255)
    a = cv2.GaussianBlur(a, (0, 0), 0.8).astype(np.uint8)  # anti-alias the edge
    rgba = np.dstack([np.full_like(a, 255)] * 3 + [a])  # white, shape in the alpha channel (for CSS mask-image)
    cv2.imwrite(path, rgba, [cv2.IMWRITE_PNG_COMPRESSION, 9])


os.makedirs(OUT, exist_ok=True)
for name, c in CFG.items():
    img = cv2.imread(os.path.join(SRC, name + ".jpg"))
    paint = paint_mask(img, c["patch"], c["thresh"], c.get("lw", 0.35))
    excl = poly_mask(img.shape, c.get("exclude", []))
    for part in ("front", "rear"):
        rough = poly_mask(img.shape, c[part], c.get("grow", 6))
        glass = clean(rough & ~paint & ~excl, min_area=c.get("min_glass", 300))
        save(glass, os.path.join(OUT, f"{name}-{part}.png"))
    # Body: GrabCut separates the car from the background, seeded by the loose outline,
    # then the glass is cut out. PPF covers lights and trim too, so we don't colour-match paint here.
    inner = poly_mask(img.shape, [c["body"]])
    sure_fg = cv2.erode(inner.astype(np.uint8), np.ones((31, 31), np.uint8)) > 0
    maybe = poly_mask(img.shape, [c["body"]], 14)
    gc = np.full(img.shape[:2], cv2.GC_BGD, np.uint8)
    gc[maybe] = cv2.GC_PR_BGD
    gc[inner] = cv2.GC_PR_FGD
    gc[sure_fg] = cv2.GC_FGD
    bg, fg = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(img, gc, None, bg, fg, 6, cv2.GC_INIT_WITH_MASK)
    car = np.isin(gc, (cv2.GC_FGD, cv2.GC_PR_FGD)) & maybe
    glass_all = poly_mask(img.shape, c["front"] + c["rear"], c.get("grow", 6)) & ~paint
    body = clean(car & ~glass_all & ~excl, open_px=2, close_px=5, min_area=3000, max_hole=c.get("max_hole", 1500))
    save(body, os.path.join(OUT, f"{name}-paint.png"))
    print(name, "ok")
