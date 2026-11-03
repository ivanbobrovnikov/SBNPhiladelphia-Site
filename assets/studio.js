/* =========================================================
   SBN Studio — interactive tools.
   Drop any of these into a page and this script builds it:
     <div data-studio="tint"></div>
     <div data-studio="ceramic"></div>
     <div data-studio="ppf"></div>
     <div data-studio-tabs></div>   (all three, tabbed)
   Needs cars.js loaded first. Booking uses window.SBN.book().
   ========================================================= */
(function () {
  const ic = (id, s = 16) => `<svg width="${s}" height="${s}"><use href="#${id}"/></svg>`;
  const book = key => window.SBN ? window.SBN.book(key) : (location.href = "tel:+12672637342");

  const VLTS = [70, 50, 35, 20, 15, 5];
  const PA_FRONT_MIN = 70; // PA: front side windows must let in 70%+ of light
  const FILMS = {
    ceramic: { name: "Ceramic Tint", desc: "Sides & rear · lifetime warranty", price: 299, was: 499, uv: 99, heat: 45, signal: 100 },
    nano: { name: "Nano Ceramic Tint", desc: "Max heat rejection · signal-safe", price: 399, was: 599, uv: 99, heat: 60, signal: 100 },
  };

  /* ---------------------------------------------------------- TINT */
  function tint(root) {
    const s = { type: "coupe", front: 70, rear: 20, film: "nano" };
    root.innerHTML = `
    <div class="studio">
      <div class="stage">
        <div class="stage-hud">
          <div class="readout"><div><small>Front</small><b data-o="front">70%</b></div><div><small>Rear</small><b data-o="rear">20%</b></div></div>
          <span class="legal" data-o="legal"></span>
        </div>
        <div class="stage-car" data-o="car"></div>
        <p class="stage-foot" data-o="foot"></p>
      </div>
      <div class="panel">
        <div><div class="ctl-label">Vehicle <em data-o="model"></em></div><div class="chips" data-c="type">
          ${Object.entries(SBNCars.types).map(([k, v]) => `<button class="chip-btn" data-v="${k}">${v.label}</button>`).join("")}</div></div>
        <div><div class="ctl-label">Front windows <em>VLT %</em></div><div class="vlt" data-c="front">
          ${VLTS.map(v => `<button class="chip-btn${v < PA_FRONT_MIN ? " illegal" : ""}" data-v="${v}">${v}</button>`).join("")}</div></div>
        <div><div class="ctl-label">Rear windows <em>VLT %</em></div><div class="vlt" data-c="rear">
          ${VLTS.map(v => `<button class="chip-btn" data-v="${v}">${v}</button>`).join("")}</div></div>
        <div><div class="ctl-label">Film</div><div class="film" data-c="film">
          ${Object.entries(FILMS).map(([k, f]) => `<button class="film-opt" data-v="${k}"><span><b>${f.name}</b><small>${f.desc}</small></span><span class="p">$${f.price}<s>$${f.was}</s></span></button>`).join("")}</div></div>
        <div class="bars" data-o="bars"></div>
        <div class="summary">
          <p class="note-sm" data-o="note"></p>
          <button class="btn btn-primary" data-o="book">Book this tint ${ic("i-arrow")}</button>
        </div>
      </div>
    </div>`;
    const $ = sel => root.querySelector(sel);
    let car;

    function drawCar() {
      $('[data-o="car"]').innerHTML = SBNCars.render(s.type);
      car = $('[data-o="car"] .car-photo');
      SBNCars.setTint(car, 0, 0);
      requestAnimationFrame(() => requestAnimationFrame(update)); // let tint fade in
      const c = SBNCars.types[s.type];
      $('[data-o="model"]').textContent = c.model;
      $('[data-o="foot"]').textContent = (c.privacy ? `This ${c.model} has factory privacy glass in the back, so film darkens it further. ` : "")
        + "Preview only: real film looks slightly different in person. Come see samples at the shop.";
    }
    function update() {
      SBNCars.setTint(car, s.front, s.rear);
      $('[data-o="front"]').textContent = s.front + "%";
      $('[data-o="rear"]').textContent = s.rear + "%";
      const legal = s.front >= PA_FRONT_MIN, L = $('[data-o="legal"]');
      L.className = "legal " + (legal ? "ok" : "bad");
      L.innerHTML = legal ? `${ic("i-check", 14)} PA street-legal` : `⚠ Front fails PA inspection`;
      const f = FILMS[s.film];
      $('[data-o="bars"]').innerHTML = [["UV blocked", f.uv], ["Heat rejection", f.heat], ["Signal-friendly", f.signal]]
        .map(([n, v]) => `<div class="bar-row"><span>${n}</span><span class="bar"><i style="width:${v}%"></i></span><b>${n === "Signal-friendly" ? "Yes" : (n === "Heat rejection" && s.film === "nano" ? "50–60%" : n === "Heat rejection" ? "40–45%" : v + "%")}</b></div>`).join("");
      const note = $('[data-o="note"]');
      note.className = "note-sm" + (legal ? "" : " warn");
      note.textContent = legal
        ? `${f.name}: front ${s.front}%, rear ${s.rear}%. Sides & rear windows, about 2–3 hours, lifetime warranty.`
        : `Pennsylvania requires 70% or lighter on the front side windows, so we'll install 70% up front. Your rear windows can be as dark as you want.`;
      $('[data-o="book"]').innerHTML = `Book ${f.name} · $${f.price} ${ic("i-arrow")}`;
      root.querySelectorAll("[data-c]").forEach(g => g.querySelectorAll("[data-v]").forEach(b => b.classList.toggle("active", String(s[g.dataset.c]) === b.dataset.v)));
    }
    root.addEventListener("click", e => {
      const b = e.target.closest("[data-v]"); if (!b) return;
      const key = b.parentElement.dataset.c; if (!key) return;
      s[key] = ["front", "rear"].includes(key) ? +b.dataset.v : b.dataset.v;
      key === "type" ? drawCar() : update();
    });
    $('[data-o="book"]').addEventListener("click", () => book("tint"));
    drawCar();
  }

  /* ---------------------------------------------------------- CERAMIC */
  function ceramic(root) {
    const img = "https://images.unsplash.com/photo-1553440569-bcc63803a83d?w=1600&q=80";
    root.innerHTML = `
    <div class="studio">
      <div>
        <div class="ba" style="--pos:50%">
          <div class="after"><img src="${img}" alt="Glossy red sports car after ceramic coating" loading="lazy"/></div>
          <div class="before"><img src="${img}" alt="" loading="lazy"/><div class="dust"></div><div class="swirls"></div><div class="spots"></div></div>
          <span class="tag l">Before</span><span class="tag r">After · Ceramic</span>
          <div class="handle"></div>
          <input type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after ceramic coating"/>
          <span class="hint">← Drag to compare →</span>
        </div>
        <p class="stage-foot" style="padding-top:.75rem">Simulated illustration of dull, swirled paint vs. corrected + coated paint. Your real before/afters go here.</p>
      </div>
      <div class="panel">
        <div><div class="ctl-label">10-Year Ceramic Coating</div>
          <div class="summary" style="border:0;padding:0"><div class="tot"><b>$499</b><small><s>$2,195</s> · limited sale</small></div></div></div>
        <div class="stat3"><div><b>10yr</b><small>Protection</small></div><div><b>110°</b><small>Water beading</small></div><div><b>99%</b><small>UV blocked</small></div></div>
        <div><div class="ctl-label">What's included</div>
          <ol class="steps-mini"><li>Exterior wash</li><li>Iron decontamination</li><li>Clay bar</li><li>Paint enhancement</li><li>10-year ceramic coating</li></ol></div>
        <div class="summary"><p class="note-sm">About 8–10 hours. Booking takes under a minute.</p>
          <button class="btn btn-primary" data-o="book">Book ceramic · $499 ${ic("i-arrow")}</button></div>
      </div>
    </div>`;
    const ba = root.querySelector(".ba"), input = ba.querySelector("input"), hint = ba.querySelector(".hint");
    input.addEventListener("input", () => { ba.style.setProperty("--pos", input.value + "%"); hint.style.opacity = 0; });
    root.querySelector('[data-o="book"]').addEventListener("click", () => book("ceramic"));
    // a short "teaser" wipe the first time it scrolls into view
    new IntersectionObserver((es, o) => es.forEach(e => {
      if (!e.isIntersecting) return; o.disconnect();
      let t0; const run = t => { t0 ??= t; const p = Math.min((t - t0) / 1600, 1); const v = 50 + Math.sin(p * Math.PI * 2) * 22; ba.style.setProperty("--pos", v + "%"); input.value = v; if (p < 1) requestAnimationFrame(run); };
      requestAnimationFrame(run);
    }), { threshold: .5 }).observe(ba);
  }

  /* ---------------------------------------------------------- PPF */
  const PPF = [
    { k: "bumper", name: "Front Bumper", desc: "The highest-impact zone. Stops daily stone chips." },
    { k: "partial", name: "Partial Front", desc: "Bumper + leading edge of hood & fenders, mirrors." },
    { k: "full", name: "Full Front End", desc: "Bumper, full hood, fenders, mirrors, headlights." },
    { k: "fullcer", name: "Full Front + Ceramic", desc: "Full front PPF + ceramic coating over the whole car." },
    { k: "body", name: "Full Body", desc: "Every painted panel. Show cars & collectors." },
  ];
  function ppf(root) {
    const s = { type: "sedan", pkg: "full" };
    root.innerHTML = `
    <div class="studio">
      <div class="stage">
        <div class="stage-hud">
          <div class="readout"><div><small>Coverage</small><b data-o="name">Full Front</b></div></div>
          <span class="legal ok">${ic("i-shield", 14)} Self-healing film</span>
        </div>
        <div class="stage-car" data-o="car"></div>
        <p class="stage-foot">Highlighted area = film coverage. Exact coverage is set at your free in-person estimate.</p>
      </div>
      <div class="panel">
        <div><div class="ctl-label">Vehicle</div><div class="chips" data-c="type">
          ${Object.entries(SBNCars.types).map(([k, v]) => `<button class="chip-btn" data-v="${k}">${v.label}</button>`).join("")}</div></div>
        <div><div class="ctl-label">Coverage package</div><div class="ppf-opts" data-c="pkg">
          ${PPF.map(p => `<button class="ppf-opt" data-v="${p.k}"><span class="dot"></span><b>${p.name}</b><small>${p.desc}</small></button>`).join("")}</div></div>
        <div class="summary"><div class="tot"><b>Free</b><small>in-person estimate · 20–30 min</small></div>
          <p class="note-sm">Every car is different, so PPF is priced in person: no guesswork, no obligation.</p>
          <a class="btn btn-primary" href="tel:+12672637342">${ic("i-phone")} Call to book estimate</a></div>
      </div>
    </div>`;
    const $ = sel => root.querySelector(sel);
    let svg;
    function draw() {
      $('[data-o="car"]').innerHTML = SBNCars.render(s.type);
      svg = $('[data-o="car"] svg');
      const c = SBNCars.types[s.type], { W, H } = SBNCars, z = c.zones, left = c.dir === "left";
      // each zone = [x where the film ends, y top]; film runs from that x to the nose
      const zones = { bumper: z.bumper, partial: [z.partial, 0], full: [z.full, 0], fullcer: [z.full, 0], body: [null, 0] };
      const rect = (x, y) => x === null ? `x="0" y="${y}" width="${W}" height="${H - y}"`
        : left ? `x="0" y="${y}" width="${x}" height="${H - y}"` : `x="${x}" y="${y}" width="${W - x}" height="${H - y}"`;
      const layer = svg.querySelector(".ppf"), u = Math.random().toString(36).slice(2, 7);
      layer.innerHTML = `<defs><linearGradient id="ppf-grad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#5ce1ff" stop-opacity=".55"/><stop offset=".5" stop-color="#bff3ff" stop-opacity=".35"/><stop offset="1" stop-color="#1a8cff" stop-opacity=".55"/></linearGradient>
          <linearGradient id="ppf-sheen-${u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
          ${Object.entries(zones).map(([k, [x, y]]) => `<clipPath id="ppfz-${k}-${u}"><rect ${rect(x, y)}/></clipPath>`).join("")}</defs>
        <rect class="ceramic-sheen" x="0" y="0" width="${W}" height="${H}" fill="#fff" opacity="0"/>` +
        Object.entries(zones).map(([k, [x, y]]) => `<g data-z="${k}"><g clip-path="url(#ppfz-${k}-${u})">
            <rect class="ppf-film" x="0" y="0" width="${W}" height="${H}"/>
            <rect class="ppf-film ppf-sheen" x="-260" y="0" width="220" height="${H}" style="fill:url(#ppf-sheen-${u})"/></g>
          ${x !== null ? `<line class="ppf-edge" x1="${x}" y1="${y}" x2="${x}" y2="${H}"/>` : ""}${y > 0 ? `<line class="ppf-edge" x1="${left ? 0 : x}" y1="${y}" x2="${left ? x : W}" y2="${y}"/>` : ""}</g>`).join("");
      update();
    }
    function update() {
      svg.querySelectorAll("[data-z]").forEach(g => g.querySelectorAll(".ppf-film,.ppf-edge").forEach(el => el.classList.toggle("on", g.dataset.z === s.pkg)));
      svg.querySelector(".ceramic-sheen").setAttribute("opacity", s.pkg === "fullcer" ? ".1" : "0");
      $('[data-o="name"]').textContent = PPF.find(p => p.k === s.pkg).name.replace(" End", "");
      root.querySelectorAll("[data-c]").forEach(g => g.querySelectorAll("[data-v]").forEach(b => b.classList.toggle("active", s[g.dataset.c] === b.dataset.v)));
    }
    root.addEventListener("click", e => {
      const b = e.target.closest("[data-v]"); if (!b) return;
      const key = b.parentElement.dataset.c; if (!key) return;
      s[key] = b.dataset.v; key === "type" ? draw() : update();
    });
    draw();
  }

  /* ---------------------------------------------------------- TABS */
  function tabs(root) {
    const T = [["tint", "i-eye", "Tint Visualizer"], ["ceramic", "i-sparkles", "Ceramic Before / After"], ["ppf", "i-shield", "PPF Coverage"]];
    root.innerHTML = `<div class="studio-tabs" role="tablist">${T.map(([k, i, n], j) => `<button class="studio-tab${j ? "" : " active"}" role="tab" data-t="${k}">${ic(i)}${n}</button>`).join("")}</div>
      ${T.map(([k], j) => `<div class="studio-pane${j ? "" : " active"}" data-p="${k}"><div data-studio="${k}"></div></div>`).join("")}`;
    root.querySelectorAll(".studio-tab").forEach(b => b.addEventListener("click", () => show(b.dataset.t)));
    function show(k) {
      root.querySelectorAll(".studio-tab").forEach(x => x.classList.toggle("active", x.dataset.t === k));
      root.querySelectorAll(".studio-pane").forEach(x => x.classList.toggle("active", x.dataset.p === k));
    }
    // links like href="#studio" data-studio-open="ppf" switch tabs
    document.querySelectorAll("[data-studio-open]").forEach(a => a.addEventListener("click", () => show(a.dataset.studioOpen)));
  }

  const TOOLS = { tint, ceramic, ppf };
  document.querySelectorAll("[data-studio-tabs]").forEach(tabs);
  document.querySelectorAll("[data-studio]").forEach(el => TOOLS[el.dataset.studio](el));
})();
