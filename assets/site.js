/* =========================================================
   SBN Auto Styling — shared site script (every page loads this)
   ========================================================= */

/* ---------- config: edit these ---------- */
const BOOKING = {
  ceramic: { title: "Book Ceramic Coating", url: "https://api.leadconnectorhq.com/widget/booking/BF04Qi6NL2P9ruo4J4i5" },
  tint:    { title: "Book Window Tinting",  url: "https://api.leadconnectorhq.com/widget/booking/uhIOYDDNgCicw61MKhm8" }
};
// Where the PPF estimate form sends leads. Leave empty to fall back to opening an email.
// Works with Formspree, Getform, a LeadConnector/GoHighLevel inbound webhook, etc.
const FORM_ENDPOINT = "";
const LEAD_EMAIL = "hello@sbnautostyling.com";

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* ---------- header: solid on scroll + mobile menu ---------- */
const header = $("#header");
if (header) {
  const onScroll = () => header.classList.toggle("scrolled", scrollY > 20);
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
}
const menu = $("#mobileMenu"), burger = $("#burger");
if (menu && burger) {
  const icon = open => `<svg width="26" height="26"><use href="#${open ? "i-x" : "i-menu"}"/></svg>`;
  burger.addEventListener("click", () => { burger.innerHTML = icon(menu.classList.toggle("open")); });
  $$("a,button", menu).forEach(el => el.addEventListener("click", () => { menu.classList.remove("open"); burger.innerHTML = icon(false); }));
}

/* ---------- hero parallax (home) ---------- */
const heroBg = $("#heroBg");
if (heroBg) addEventListener("scroll", () => { if (scrollY < innerHeight) heroBg.style.transform = `scale(1.05) translateY(${scrollY * 0.3}px)`; }, { passive: true });

/* ---------- reveal on scroll + counters ---------- */
function countUp(el) {
  const end = +el.dataset.count, suf = el.dataset.suffix || "", t0 = performance.now();
  const tick = t => { const p = Math.min((t - t0) / 1600, 1); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + suf; if (p < 1) requestAnimationFrame(tick); };
  requestAnimationFrame(tick);
}
const io = new IntersectionObserver(entries => entries.forEach(e => {
  if (!e.isIntersecting) return;
  e.target.classList.add("in");
  $$("[data-count]", e.target).forEach(countUp);
  io.unobserve(e.target);
}), { threshold: 0.15 });

/* ---------- testimonials (home) ---------- */
const tgrid = $("#tgrid");
if (tgrid) {
  const TESTIMONIALS = [
    { name: "James M.", text: "Absolutely blown away by the finish. The team at SBN took my brief and executed it perfectly. The ceramic coating is flawless and they detailed the car before handing it back." },
    { name: "Sarah K.", text: "Had PPF fitted on my new Range Rover and the peace of mind is worth every penny. Professional team, clean workshop. 10/10." },
    { name: "Tom B.",   text: "The ceramic coating has made washing the car so much easier — water just beads off. The gloss depth is incredible. SBN are the real deal." },
    { name: "Priya S.", text: "Amazing service from start to finish. The tints look factory-fitted, perfect edges, no bubbles. Great value for money." }
  ];
  const star = '<svg width="16" height="16"><use href="#i-star"/></svg>';
  tgrid.innerHTML = TESTIMONIALS.map((t, i) => `
    <div class="tcard reveal d${i % 2}">
      <span class="qmark">&ldquo;</span>
      <div class="stars">${star.repeat(5)}</div>
      <blockquote>&ldquo;${t.text}&rdquo;</blockquote>
      <div class="who"><span class="avatar">${t.name[0]}</span>${t.name}</div>
    </div>`).join("");
}
$$(".reveal").forEach(el => io.observe(el));

/* ---------- pricing tabs (home) ---------- */
function setTab(key) {
  $$("[data-tab-btn]").forEach(b => b.classList.toggle("active", b.dataset.tabBtn === key));
  $$("[data-panel]").forEach(p => p.classList.toggle("active", p.dataset.panel === key));
  const note = $("#pricingNote"); if (note) note.style.display = key === "ppf" ? "none" : "";
}
if ($("[data-tab-btn]")) {
  $$("[data-tab-btn]").forEach(b => b.addEventListener("click", () => setTab(b.dataset.tabBtn)));
  $$("[data-tab]").forEach(a => a.addEventListener("click", () => setTab(a.dataset.tab)));
  setTab("ceramic");
}

/* ---------- gallery lightbox (home) ---------- */
const lb = $("#lightbox");
if (lb) {
  $$(".gal-item img").forEach(img => img.addEventListener("click", () => {
    $("img", lb).src = img.src.replace("w=800", "w=1600"); lb.classList.add("open");
  }));
  lb.addEventListener("click", () => lb.classList.remove("open"));
}

/* ---------- service picker / booking modal (every page) ---------- */
const frame = $("#bookingFrame");
function goStep(name) { $$(".m-step").forEach(s => s.classList.toggle("active", s.dataset.step === name)); }
function openModal(step = "pick") { goStep(step); document.body.classList.add("modal-open"); document.documentElement.style.overflow = "hidden"; }
function closeModal() { document.body.classList.remove("modal-open"); document.documentElement.style.overflow = ""; if (frame) frame.removeAttribute("src"); }
function book(key) { const b = BOOKING[key]; $("#bookTitle").textContent = b.title; frame.src = b.url; openModal("book"); }

$$("[data-open-modal]").forEach(b => b.addEventListener("click", () => openModal(b.dataset.openModal || "pick")));
$$("[data-go]").forEach(b => b.addEventListener("click", () => goStep(b.dataset.go)));
$$("[data-book]").forEach(b => b.addEventListener("click", () => book(b.dataset.book)));
$$("[data-close-modal]").forEach(b => b.addEventListener("click", closeModal));
const overlay = $("#overlay"); if (overlay) overlay.addEventListener("click", closeModal);
addEventListener("keydown", e => { if (e.key === "Escape") { closeModal(); if (lb) lb.classList.remove("open"); } });

/* auto-open the picker once per browser session, after the visitor scrolls past the first screen (home only) */
if (document.body.dataset.autoModal === "1") {
  let shown = false;
  try { shown = sessionStorage.getItem("sbn_modal_seen") === "1"; } catch (e) {}
  addEventListener("scroll", function auto() {
    if (shown || scrollY < innerHeight * 0.8) return;
    shown = true; removeEventListener("scroll", auto);
    try { sessionStorage.setItem("sbn_modal_seen", "1"); } catch (e) {}
    setTimeout(() => { if (!document.body.classList.contains("modal-open")) openModal(); }, 1500);
  }, { passive: true });
}

/* ---------- PPF estimate form ---------- */
const form = $("#estimateForm");
if (form) form.addEventListener("submit", async e => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  const done = () => { form.style.display = "none"; $("#formOk").style.display = "block"; };
  if (FORM_ENDPOINT) {
    const btn = $("button[type=submit]", form); btn.disabled = true; btn.textContent = "Sending…";
    try {
      const r = await fetch(FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) });
      if (!r.ok) throw new Error(r.status);
      done();
    } catch (err) {
      btn.disabled = false; btn.textContent = "Request Free Estimate";
      alert("Sorry, that didn't go through. Please call us at 267 263 7342.");
    }
  } else {
    const body = Object.entries(data).map(([k, v]) => `${k}: ${v}`).join("\n");
    location.href = `mailto:${LEAD_EMAIL}?subject=${encodeURIComponent("Free PPF Estimate Request")}&body=${encodeURIComponent(body)}`;
    done();
  }
});

/* ---------- chat bubble placeholder ---------- */
const chatX = $("#chatPopX"); if (chatX) chatX.addEventListener("click", () => $("#chatPop").remove());
$$(".yr").forEach(el => el.textContent = new Date().getFullYear());
