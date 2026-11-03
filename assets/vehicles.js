/* =========================================================
   Year / Make / Model picker backed by the free NHTSA vPIC database
   (https://vpic.nhtsa.dot.gov/api/), which lists every make and model sold in the US.
   Each model is mapped to a preview body style: sedan, coupe, sports, suv or truck.
   Exposes window.SBNVehicles = { mount(el, onChange), bodyStyle(make, model, nhtsaType) }.
   ========================================================= */
(function () {
  const API = "https://vpic.nhtsa.dot.gov/api/vehicles";
  const MAKES = ["Acura", "Alfa Romeo", "Aston Martin", "Audi", "Bentley", "BMW", "Buick", "Cadillac", "Chevrolet", "Chrysler",
    "Dodge", "Ferrari", "Fiat", "Ford", "Genesis", "GMC", "Honda", "Hyundai", "Infiniti", "Jaguar", "Jeep", "Kia",
    "Lamborghini", "Land Rover", "Lexus", "Lincoln", "Lotus", "Lucid", "Maserati", "Mazda", "McLaren", "Mercedes-Benz",
    "Mini", "Mitsubishi", "Nissan", "Polestar", "Porsche", "Ram", "Rivian", "Rolls-Royce", "Subaru", "Tesla", "Toyota",
    "Volkswagen", "Volvo"];
  const SPORTS_MAKES = /^(ferrari|lamborghini|mclaren|lotus)$/i;
  const SPORTS = /\b(911|718|cayman|boxster|carrera|corvette|viper|gt-?r|nsx|r8|amg gt|sls|slr|i8|f-?type|nissan z|370z|350z|gt500|ford gt|acura nsx|vantage|db1[12]|dbs|huracan|aventador|revuelto)\b/i;
  const COUPE = /\b(mustang|camaro|challenger|charger daytona|[248] series|m[248]\b|z4|supra|brz|gr86|86|miata|mx-5|rc\b|lc\b|tt\b|a5|s5|rs ?5|q?60 coupe|q60|c-class coupe|e-class coupe|cle|clk|sl\b|slk|slc|genesis coupe|veloster|wrx|civic si|type r|golf r|gti|elantra n|integra|solara|cts-v coupe|xk|f-type|ghibli|granturismo|wraith|dawn|continental gt)\b/i;

  /* NHTSA vehicle type → preview body style (with name-based overrides for coupes and sports cars). */
  function bodyStyle(make, model, type) {
    if (type === "truck") return "truck";
    if (type === "mpv") return "suv";
    const name = `${make} ${model}`;
    if (SPORTS_MAKES.test(make) || SPORTS.test(name)) return "sports";
    if (COUPE.test(name)) return "coupe";
    return "sedan";
  }

  /* Pricing size: every truck/van, plus full-size and 3-row SUVs and minivans, is "large" (+$60 on tint).
     Everything else (cars, compact & mid-size 2-row SUVs) is "std". Edit LARGE to change what counts as big. */
  const LARGE = /\b(tahoe|suburban|yukon|escalade|expedition|navigator|sequoia|land cruiser|lx ?\d*|gx ?\d*|qx80|armada|wagoneer|grand cherokee l|durango|traverse|enclave|acadia|explorer|aviator|pilot|mdx|telluride|palisade|atlas\b(?! cross)|ascent|highlander|grand highlander|pathfinder|qx60|cx-9\d?|x7|gls|gle|q7|q8|xc90|range rover(?! (evoque|velar|sport))|defender 1[13]0|discovery\b(?! sport)|model x|r1s|ex90|ev9|ioniq 9|vistiq|sienna|odyssey|pacifica|carnival|voyager|sprinter|transit|promaster|express|savana|metris|cullinan)\b/i;
  function sizeOf(make, model, style) {
    if (style === "truck") return "large";
    return LARGE.test(`${make} ${model}`) ? "large" : "std";
  }

  const cache = {};
  async function models(make, year) {
    const key = make + year;
    if (cache[key]) return cache[key];
    // Some models (e.g. the Porsche 911) are only listed without a vehicle type, so fetch the full list too,
    // then drop anything NHTSA files as a motorcycle, trailer, bus, off-road or low-speed vehicle.
    const get = t => fetch(`${API}/GetModelsForMakeYear/make/${encodeURIComponent(make)}/modelyear/${year}${t ? "/vehicletype/" + t : ""}?format=json`)
      .then(r => r.json()).then(d => d.Results.map(x => ({ name: x.Model_Name.trim(), type: t }))).catch(() => []);
    const SKIP = ["motorcycle", "trailer", "bus", "off road vehicle", "low speed vehicle"];
    const [typed, skipped, every] = await Promise.all([
      Promise.all(["car", "mpv", "truck"].map(get)).then(a => a.flat()),
      Promise.all(SKIP.map(get)).then(a => new Set(a.flat().map(m => m.name.toLowerCase()))),
      get(""),
    ]);
    const seen = new Set();
    const list = [...typed, ...every.map(m => ({ ...m, type: null }))]
      .filter(m => m.name && !/^'\d/.test(m.name) && !skipped.has(m.name.toLowerCase()) && !seen.has(m.name.toLowerCase()) && seen.add(m.name.toLowerCase()))
      .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));
    return (cache[key] = list);
  }

  /* Renders three selects into el. onChange({ year, make, model, style, label }) fires when a model is picked. */
  function mount(el, onChange, initial = {}) {
    const now = new Date().getFullYear() + 1;
    const years = Array.from({ length: now - 1989 }, (_, i) => now - i);
    el.innerHTML = `<div class="veh">
      <select data-k="year" aria-label="Year"><option value="">Year</option>${years.map(y => `<option>${y}</option>`).join("")}</select>
      <select data-k="make" aria-label="Make"><option value="">Make</option>${MAKES.map(m => `<option>${m}</option>`).join("")}<option value="__other">Other…</option></select>
      <select data-k="model" aria-label="Model" disabled><option value="">Model</option></select>
      <input data-k="other" class="veh-other" placeholder="Make & model" hidden/>
    </div>`;
    const $ = k => el.querySelector(`[data-k="${k}"]`);
    const s = { year: initial.year || "", make: initial.make || "", model: initial.model || "" };
    let list = [];
    const emit = () => {
      if (!s.year || !s.make || !s.model) return onChange(null);
      const m = list.find(x => x.name === s.model);
      const style = s.make === "__other" ? null : bodyStyle(s.make, s.model, m && m.type);
      const label = s.make === "__other" ? `${s.year} ${s.model}` : `${s.year} ${s.make} ${s.model}`;
      onChange({ year: s.year, make: s.make === "__other" ? "" : s.make, model: s.model, style, label, size: sizeOf(s.make, s.model, style) });
    };
    async function loadModels() {
      const sel = $("model");
      sel.disabled = true; s.model = "";
      if (!s.year || !s.make || s.make === "__other") { sel.innerHTML = `<option value="">Model</option>`; emit(); return; }
      sel.innerHTML = `<option value="">Loading…</option>`;
      list = await models(s.make, s.year);
      sel.innerHTML = `<option value="">Model</option>${list.map(m => `<option>${m.name}</option>`).join("")}<option value="__type">Not listed — I'll type it</option>`;
      sel.disabled = false;
      emit();
    }
    $("year").addEventListener("change", e => { s.year = e.target.value; loadModels(); });
    $("make").addEventListener("change", e => {
      s.make = e.target.value;
      const other = s.make === "__other";
      $("other").hidden = !other; $("model").hidden = other;
      loadModels();
    });
    $("model").addEventListener("change", e => {
      if (e.target.value === "__type") { $("other").hidden = false; $("other").focus(); s.model = ""; return emit(); }
      $("other").hidden = s.make !== "__other"; s.model = e.target.value; emit();
    });
    $("other").addEventListener("input", e => { s.model = e.target.value.trim(); emit(); });
    if (s.year) $("year").value = s.year;
    if (s.make) { $("make").value = s.make; }
    if (s.year && s.make) loadModels().then(() => { if (initial.model) { $("model").value = initial.model; s.model = initial.model; emit(); } });
  }

  window.SBNVehicles = { mount, bodyStyle, sizeOf, models };
})();
