/* =========================================================
   SBN Auto Styling — shared site script (every page loads this)
   ========================================================= */

/* ---------- config: edit these ---------- */
// GoHighLevel booking calendars (Calendars → your calendar → Share → booking link).
// Turn on payments in each calendar's settings to collect the deposit.
const BOOKING = {
  ceramic: { title: "Book Ceramic Coating", url: "https://api.leadconnectorhq.com/widget/booking/BF04Qi6NL2P9ruo4J4i5" },
  tint:    { title: "Book Window Tinting",  url: "https://api.leadconnectorhq.com/widget/booking/uhIOYDDNgCicw61MKhm8" }
};
// GoHighLevel inbound webhook (Automation → Workflow → trigger "Inbound Webhook" → copy URL).
// Every checkout and estimate request is posted here with the vehicle, service, film and tint %.
const GHL_WEBHOOK = "";
// Fallback for the PPF estimate form if no webhook is set: opens an email.
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

/* ---------- reviews marquee (home) ---------- */
const track = $("#reviewsTrack");
if (track) {
  const REVIEWS = [
    { name: "James M.", tag: "Ceramic Coating", text: "Absolutely blown away by the finish. The team at SBN took my brief and executed it perfectly. The ceramic coating is flawless and they detailed the car before handing it back." },
    { name: "Sarah K.", tag: "PPF · Range Rover", text: "Had PPF fitted on my new Range Rover and the peace of mind is worth every penny. Professional team, clean workshop. 10/10." },
    { name: "Tom B.",   tag: "Ceramic Coating", text: "The ceramic coating has made washing the car so much easier — water just beads off. The gloss depth is incredible. SBN are the real deal." },
    { name: "Priya S.", tag: "Window Tint", text: "Amazing service from start to finish. The tints look factory-fitted, perfect edges, no bubbles. Great value for money." }
  ];
  const star = '<svg width="15" height="15"><use href="#i-star"/></svg>';
  const card = r => `<div class="tcard"><div class="stars">${star.repeat(5)}</div><blockquote>&ldquo;${r.text}&rdquo;</blockquote>
    <div class="who"><span class="avatar">${r.name[0]}</span><span>${r.name}<small>${r.tag}</small></span></div></div>`;
  // repeated so the marquee loops seamlessly (the track scrolls by half its width)
  track.innerHTML = [...REVIEWS, ...REVIEWS, ...REVIEWS, ...REVIEWS].map(card).join("");
}

/* ---------- gallery strip: arrows + drag to scroll ---------- */
const strip = $("#strip");
if (strip) {
  $$("[data-strip]").forEach(b => b.addEventListener("click", () => strip.scrollBy({ left: +b.dataset.strip * strip.clientWidth * 0.8, behavior: "smooth" })));
  let down = false, x0 = 0, s0 = 0;
  strip.addEventListener("pointerdown", e => { if (e.pointerType !== "mouse") return; down = true; x0 = e.clientX; s0 = strip.scrollLeft; strip.classList.add("drag"); });
  addEventListener("pointermove", e => { if (down) strip.scrollLeft = s0 - (e.clientX - x0); });
  addEventListener("pointerup", () => { down = false; strip.classList.remove("drag"); });
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
function goStep(name) { $$(".m-step").forEach(s => s.classList.toggle("active", s.dataset.step === name)); const m = $(".modal"); if (m) m.scrollTop = 0; }
function openModal(step = "pick") { goStep(step); document.body.classList.add("modal-open"); document.documentElement.style.overflow = "hidden"; }
function closeModal() { document.body.classList.remove("modal-open"); document.documentElement.style.overflow = ""; if (frame) frame.removeAttribute("src"); }
/* ---------- checkout: vehicle + service details + contact → GoHighLevel ---------- */
const FILMS = { ceramic: { name: "Ceramic Tint", price: 299 }, nano: { name: "Nano Ceramic Tint", price: 399 } };
const SERVICES = {
  tint: { title: "Window Tinting", next: "Next: pick a time and pay your deposit." },
  ceramic: { title: "10-Year Ceramic Coating", next: "Next: pick a time and pay your deposit." },
  ppf: { title: "Paint Protection Film", next: "We'll call you to set up your free in-person estimate." },
};
const state = window.SBNState = window.SBNState || { vehicle: null };
try { state.vehicle = state.vehicle || JSON.parse(sessionStorage.getItem("sbn_vehicle") || "null"); } catch (e) {}
let order = null;

function orderSummary(o) {
  if (o.service === "tint") {
    const f = FILMS[o.film], installed = Math.max(o.front, 70);
    return { lines: [f.name + " · sides & rear", `Front ${o.front}%${installed !== o.front ? " → installed at 70% (PA law)" : ""} · Rear ${o.rear}%`], price: "$" + f.price, installed };
  }
  if (o.service === "ceramic") return { lines: ["10-year package: wash, iron decon, clay bar, paint enhancement, coating", "About 8–10 hours"], price: "$499" };
  return { lines: [(o.pkg || "PPF coverage to be decided") + " · free in-person estimate", "20–30 minutes at our shop"], price: "Free" };
}
function renderSummary(el) {
  const s = orderSummary(order), v = state.vehicle;
  el.innerHTML = `<div><b>${SERVICES[order.service].title}</b>${s.lines.map(l => `<small>${l}</small>`).join("")}${v ? `<small>Vehicle: ${v.label}</small>` : ""}</div><span>${s.price}</span>`;
}

function checkout(o) {
  order = { film: "nano", front: 70, rear: 20, ...o };
  const form = $("#checkoutForm");
  $("#coTitle").textContent = SERVICES[order.service].title;
  $("#coNext").textContent = SERVICES[order.service].next;
  $("#coSubmit").innerHTML = (order.service === "ppf" ? "Request my free estimate" : "Continue to calendar & deposit") + ' <svg class="arrow" width="16" height="16"><use href="#i-arrow"/></svg>';
  $("#coTint").hidden = order.service !== "tint";
  form.film.value = order.film; form.front.value = order.front; form.rear.value = order.rear;
  $("#coLegal").hidden = order.front >= 70;
  if (window.SBNVehicles) SBNVehicles.mount($("#coVehicle"), v => { state.vehicle = v; $("#coVehErr").hidden = true; renderSummary($("#coSummary")); }, state.vehicle || {});
  renderSummary($("#coSummary"));
  openModal("checkout");
}
const coForm = $("#checkoutForm");
if (coForm) {
  coForm.addEventListener("change", e => {
    if (!["film", "front", "rear"].includes(e.target.name)) return;
    order[e.target.name] = e.target.name === "film" ? e.target.value : +e.target.value;
    $("#coLegal").hidden = order.front >= 70;
    renderSummary($("#coSummary"));
  });
  coForm.addEventListener("submit", e => {
    e.preventDefault();
    const v = state.vehicle;
    $("#coVehErr").hidden = !!v;
    if (!v || !coForm.reportValidity()) return;
    try { sessionStorage.setItem("sbn_vehicle", JSON.stringify(v)); } catch (err) {}
    const c = Object.fromEntries(new FormData(coForm));
    const s = orderSummary(order);
    const lead = {
      first_name: c.first_name, last_name: c.last_name, phone: c.phone, email: c.email,
      vehicle: v.label, vehicle_year: v.year, vehicle_make: v.make, vehicle_model: v.model,
      service: SERVICES[order.service].title, price: s.price,
      package: order.service === "tint" ? FILMS[order.film].name : order.service === "ppf" ? (order.pkg || "") : "10-Year Ceramic",
      tint_front_requested: order.service === "tint" ? order.front + "%" : "",
      tint_front_install: order.service === "tint" ? s.installed + "%" : "",
      tint_rear: order.service === "tint" ? order.rear + "%" : "",
      notes: c.notes || "", sms_consent: c.consent ? "yes" : "no",
      summary: [SERVICES[order.service].title, ...s.lines, "Vehicle: " + v.label, s.price].join(" | "),
      source: "website checkout", page: location.href,
    };
    sendLead(lead);
    if (order.service === "ppf") return goStep("done");
    const cal = BOOKING[order.service];
    const q = new URLSearchParams({ first_name: c.first_name, last_name: c.last_name, email: c.email, phone: c.phone });
    $("#bookTitle").textContent = "Pick a time & pay deposit";
    renderSummary($("#bookSummary"));
    frame.src = cal.url + (cal.url.includes("?") ? "&" : "?") + q;
    goStep("book");
  });
}
/* Posts a lead to the GoHighLevel inbound webhook. Form-encoded + no-cors so the browser sends it without a preflight. */
function sendLead(lead) {
  if (!GHL_WEBHOOK) { console.warn("SBN: GHL_WEBHOOK not set, lead not sent", lead); return Promise.resolve(false); }
  return fetch(GHL_WEBHOOK, { method: "POST", mode: "no-cors", body: new URLSearchParams(lead) }).then(() => true, () => false);
}
function book(key, film) { checkout({ service: key, film: film || "nano" }); }
window.SBN = { book, checkout, openModal, closeModal, sendLead };

$$("[data-open-modal]").forEach(b => b.addEventListener("click", () => openModal(b.dataset.openModal || "pick")));
$$("[data-go]").forEach(b => b.addEventListener("click", () => goStep(b.dataset.go)));
$$("[data-book]").forEach(b => b.addEventListener("click", () => book(b.dataset.book, b.dataset.film)));
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
  if (GHL_WEBHOOK) {
    const btn = $("button[type=submit]", form); btn.disabled = true; btn.textContent = "Sending…";
    const ok = await sendLead({ ...data, service: "Paint Protection Film", source: "PPF estimate form", page: location.href });
    if (ok) return done();
    btn.disabled = false; btn.textContent = "Request Free Estimate";
    alert("Sorry, that didn't go through. Please call us at 267 263 7342.");
  } else {
    const body = Object.entries(data).map(([k, v]) => `${k}: ${v}`).join("\n");
    location.href = `mailto:${LEAD_EMAIL}?subject=${encodeURIComponent("Free PPF Estimate Request")}&body=${encodeURIComponent(body)}`;
    done();
  }
});

/* ---------- chat bubble placeholder ---------- */
const chatX = $("#chatPopX"); if (chatX) chatX.addEventListener("click", () => $("#chatPop").remove());
$$(".yr").forEach(el => el.textContent = new Date().getFullYear());
