"""Writes assets/cars.js from the traced outlines in polys.json."""
import json, sys
P = json.load(open(sys.argv[1]))
meta = {
    "sedan": dict(label="Sedan", model="Honda Accord", dir="left", credit="Photo: Unsplash",
                  zones=dict(bumper=[200, 270], partial=380, full=520), privacy=False),
    "coupe": dict(label="Coupe", model="BMW 4 Series", dir="right", credit="Photo: Unsplash",
                  zones=dict(bumper=[1460, 250], partial=1290, full=1040), privacy=False),
    "suv": dict(label="SUV", model="Cadillac Lyriq", dir="right", credit="Photo: Unsplash",
                zones=dict(bumper=[1470, 290], partial=1280, full=1060), privacy=True),
    "truck": dict(label="Truck", model="GMC Sierra", dir="left", credit="Photo: Unsplash",
                  zones=dict(bumper=[115, 200], partial=300, full=470), privacy=True),
}
cars = {k: {**meta[k], **{kk: v for kk, v in P[k].items()}} for k in meta}
data = json.dumps(cars, separators=(",", ":"))

js = r'''/* =========================================================
   SBN Studio — real vehicle photos with traced window + body outlines.
   Photos: assets/img/cars/<type>.jpg, 1600 x 615 (free under the Unsplash License).
   front / rear: window outlines in photo pixels. body: paint outline (used for PPF).
   zones: where each PPF package ends, measured from the nose (dir = way the car faces).
   To use your own photo: crop it to 1600 x 615 and re-trace these outlines.
   Exposes window.SBNCars = { types, render(type), setTint(el, front, rear) }.
   ========================================================= */
(function () {
  const W = 1600, H = 615;
  const TYPES = __DATA__;
  const pts = poly => "M" + poly.map(p => p.join(" ")).join(" L") + " Z";

  function render(type, opts = {}) {
    const c = TYPES[type] || TYPES.sedan;
    const id = opts.uid || "c" + Math.random().toString(36).slice(2, 7);
    const glass = [...c.front, ...c.rear];
    const base = (document.querySelector('script[src*="cars.js"]') || {}).src || "";
    const img = base.replace(/cars\.js.*$/, "img/cars/" + type + ".jpg");
    return `<div class="car-photo" data-type="${type}">
  <img src="${img}" alt="${c.model} side view" width="${W}" height="${H}"/>
  <svg class="car-svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true">
    <defs>
      <clipPath id="glass-${id}">${glass.map(g => `<path d="${pts(g)}"/>`).join("")}</clipPath>
      <clipPath id="body-${id}"><path clip-rule="evenodd" d="${pts(c.body)} ${glass.map(pts).join(" ")}"/></clipPath>
      <linearGradient id="refl-${id}" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".38" stop-color="#fff" stop-opacity="0"/>
        <stop offset=".46" stop-color="#fff" stop-opacity=".55"/><stop offset=".6" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
      </linearGradient>
      <filter id="soft-${id}"><feGaussianBlur stdDeviation="1.2"/></filter>
    </defs>
    <g class="tint" filter="url(#soft-${id})">
      ${c.front.map(g => `<path class="tint-front" d="${pts(g)}" fill="#020305" style="fill-opacity:0"/>`).join("")}
      ${c.rear.map(g => `<path class="tint-rear" d="${pts(g)}" fill="#020305" style="fill-opacity:0"/>`).join("")}
    </g>
    <g clip-path="url(#glass-${id})"><rect class="refl" x="0" y="0" width="${W}" height="${H}" fill="url(#refl-${id})" opacity=".08"/></g>
    <g class="ppf" clip-path="url(#body-${id})"></g>
  </svg>
</div>`;
  }

  /* Film darkness: a film passes VLT% of the light, so we lay black at (1 - VLT) over the glass. */
  function setTint(el, front, rear) {
    const a = v => (v ? 1 - v / 100 : 0);
    el.querySelectorAll(".tint-front").forEach(p => p.style.fillOpacity = a(front));
    el.querySelectorAll(".tint-rear").forEach(p => p.style.fillOpacity = a(rear));
    const r = el.querySelector(".refl");
    if (r) r.setAttribute("opacity", (0.05 + 0.18 * Math.max(a(front), a(rear))).toFixed(2));
  }

  window.SBNCars = { types: TYPES, render, setTint, W, H };
})();
'''
open(sys.argv[2], "w").write(js.replace("__DATA__", data))
print("wrote", sys.argv[2], len(js) + len(data))
