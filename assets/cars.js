/* =========================================================
   SBN Studio — real vehicle photos with traced window + body outlines.
   Photos: assets/img/cars/<type>.jpg, 1600 x 615 (free under the Unsplash License).
   front / rear: window outlines in photo pixels. body: paint outline (used for PPF).
   zones: where each PPF package ends, measured from the nose (dir = way the car faces).
   To use your own photo: crop it to 1600 x 615 and re-trace these outlines.
   Exposes window.SBNCars = { types, render(type), setTint(el, front, rear) }.
   ========================================================= */
(function () {
  const W = 1600, H = 615;
  const TYPES = {"sedan":{"label":"Sedan","model":"Honda Accord","dir":"left","credit":"Photo: Unsplash","zones":{"bumper":[200,270],"partial":380,"full":520},"privacy":false,"front":[[[505,250],[560,205],[620,155],[695,108],[862,105],[860,244]]],"rear":[[[896,104],[1082,106],[1132,128],[1170,168],[1197,222],[1194,235],[897,240]],[[1143,100],[1205,113],[1275,152],[1346,203],[1312,210],[1255,182],[1200,142]]],"body":[[75,455],[62,400],[65,330],[85,300],[110,280],[200,255],[330,235],[430,215],[560,140],[700,80],[1100,78],[1150,100],[1350,205],[1500,225],[1530,260],[1545,330],[1555,400],[1550,450],[1530,465],[1340,460],[1335,420],[1300,370],[1240,345],[1170,350],[1120,395],[1105,460],[450,470],[450,440],[430,370],[380,330],[320,318],[255,330],[210,375],[195,450]]},"coupe":{"label":"Coupe","model":"BMW 4 Series","dir":"right","credit":"Photo: Unsplash","zones":{"bumper":[1460,250],"partial":1290,"full":1040},"privacy":false,"front":[[[634,77],[760,74],[850,88],[920,113],[965,138],[980,155],[980,189],[656,182]]],"rear":[[[350,152],[385,127],[450,100],[540,83],[623,77],[648,181],[380,176],[356,166]]],"body":[[55,420],[45,350],[55,290],[70,230],[80,190],[95,180],[250,170],[345,150],[420,100],[520,70],[620,58],[760,58],[870,75],[960,115],[1050,175],[1130,180],[1300,210],[1440,240],[1520,262],[1545,300],[1560,360],[1555,430],[1530,445],[1470,440],[1465,360],[1430,310],[1360,290],[1290,300],[1235,345],[1225,440],[520,440],[490,420],[480,340],[430,300],[360,285],[290,295],[240,340],[225,420]]},"suv":{"label":"SUV","model":"Cadillac Lyriq","dir":"right","credit":"Photo: Unsplash","zones":{"bumper":[1470,290],"partial":1280,"full":1060},"privacy":true,"front":[[[760,82],[880,86],[960,110],[1030,150],[1065,180],[995,182],[990,196],[765,196]]],"rear":[[[500,88],[715,80],[720,196],[500,196]],[[365,190],[405,140],[440,103],[497,90],[500,195]]],"body":[[40,460],[30,380],[45,300],[55,230],[60,190],[200,80],[350,55],[500,55],[900,62],[960,100],[1050,160],[1110,200],[1250,225],[1400,250],[1520,285],[1555,320],[1570,400],[1560,470],[1510,480],[1475,470],[1470,380],[1420,320],[1350,300],[1270,310],[1215,360],[1200,470],[490,470],[480,370],[430,310],[350,290],[270,305],[215,360],[205,470]]},"truck":{"label":"Truck","model":"GMC Sierra","dir":"left","credit":"Photo: Unsplash","zones":{"bumper":[115,200],"partial":300,"full":470},"privacy":true,"front":[[[488,195],[520,160],[560,118],[600,88],[625,77],[710,75],[712,193]]],"rear":[[[745,75],[950,75],[965,95],[970,165],[945,190],[740,192]]],"body":[[45,440],[40,370],[55,300],[60,220],[110,200],[250,180],[400,160],[440,150],[520,95],[600,58],[1000,58],[1025,70],[1035,185],[1530,185],[1545,200],[1550,330],[1560,370],[1555,430],[1480,440],[1420,440],[1415,340],[1370,295],[1265,280],[1170,295],[1125,340],[1115,445],[450,445],[390,440],[385,330],[340,290],[250,280],[160,295],[110,345],[105,440]]}};
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
