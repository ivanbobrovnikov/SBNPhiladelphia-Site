#!/usr/bin/env python3
"""Generates every page of the SBN Auto Styling site into /home/user/sbn-site."""
import os, re, html

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parts")
DOMAIN = "https://sbn-autostyling.com"
read = lambda n: open(os.path.join(PARTS, n)).read()
SPRITE, MODAL, CHAT = read("sprite.html"), read("modal.html"), read("chat.html")
IMGS = ["logo.png", "service-ppf.png", "service-ceramic.png", "service-window-tint.png", "about-hero.png"]
TEL = "tel:+12672637342"
e = html.escape


def fix_paths(s):
    """Turn root-relative paths from the original into {R}-relative ones."""
    for img in IMGS:
        s = s.replace(f'src="/{img}"', f'src="{{R}}assets/img/{img}"')
    s = re.sub(r'href="/([a-z0-9\-/]+)"', r'href="{R}\1/"', s)
    return s


def ic(name, size=16, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="{size}" height="{size}"><use href="#{name}"/></svg>'


def checks(items, size=16):
    return "".join(f'<li>{ic("i-check", size, "check")}{e(i)}</li>' for i in items)


def faq(items):
    return '<div class="faq">' + "".join(
        f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items) + "</div>"


# ---------------------------------------------------------------- chrome
def full_header(is_home):
    h = "" if is_home else "{ROOT}"
    links = [("Studio", f"{h}#studio"), ("Services", f"{h}#services"), ("Pricing", f"{h}#pricing"),
             ("Work", f"{h}#gallery"), ("Reviews", f"{h}#testimonials"), ("Visit", f"{h}#visit"), ("Blog", "{R}blog/")]
    nav = "".join(f'<a href="{u}">{t}</a>' for t, u in links)
    mob = "".join(f'<a class="link" href="{u}">{t}</a>' for t, u in links)
    return f'''<header class="header" id="header">
  <div class="header-inner">
    <a href="{h or '#hero'}" class="logo">
      <div class="logo-img"><img src="{{R}}assets/img/logo.png" alt="SBN Auto Styling" /></div>
      <span class="logo-text">SBN <span class="blue">Auto Styling</span></span>
    </a>
    <nav class="nav">{nav}
      <button class="btn btn-primary btn-sm" data-open-modal>Book now</button>
    </nav>
    <button class="burger" id="burger" aria-label="Open menu">{ic("i-menu", 22)}</button>
  </div>
  <div class="mobile-menu" id="mobileMenu">{mob}
    <button class="btn btn-primary btn-md" data-open-modal>Book now</button>
  </div>
</header>'''


def simple_header(*_):
    """Sub-pages now share the main floating nav."""
    return full_header(False)


FULL_FOOTER = '''<footer>
  <div class="container">
    <div class="foot">
      <div>
        <a href="{ROOT}" class="logo"><div class="logo-img"><img src="{R}assets/img/logo.png" alt="SBN"/></div><span class="logo-text" style="display:inline">SBN <span class="blue">Auto Styling</span></span></a>
        <p>Ceramic window tint, ceramic coating and paint protection film. Trusted by car enthusiasts across Philadelphia &amp; Bucks County.</p>
        <div class="socials">
          <a href="https://www.instagram.com/sbnautostyling" target="_blank" rel="noopener" aria-label="Instagram"><svg width="17" height="17"><use href="#i-insta"/></svg></a>
          <a href="https://www.facebook.com/profile.php?id=61586524292167" target="_blank" rel="noopener" aria-label="Facebook"><svg width="17" height="17"><use href="#i-fb"/></svg></a>
          <a href="tel:+12672637342" aria-label="Call"><svg width="17" height="17"><use href="#i-phone"/></svg></a>
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="{R}services/window-tinting/">Window Tinting</a></li>
          <li><a href="{R}services/ceramic-coating/">Ceramic Coating</a></li>
          <li><a href="{R}services/ppf/">Paint Protection Film</a></li>
          <li><a href="{ROOT}#studio">SBN Studio</a></li>
          <li><a href="{R}blog/">Blog</a></li>
        </ul>
      </div>
      <div>
        <h4>Areas</h4>
        <ul>
          <li><a href="{R}window-tinting-philadelphia/">Window Tinting Philadelphia</a></li>
          <li><a href="{R}ceramic-coating-philadelphia/">Ceramic Coating Philadelphia</a></li>
          <li><a href="{R}ppf-philadelphia/">PPF Philadelphia</a></li>
          <li><a href="{R}ppf-bucks-county/">PPF Bucks County</a></li>
          <li><a href="{R}ceramic-coating-northeast-philadelphia/">Ceramic NE Philadelphia</a></li>
          <li><a href="{R}window-tinting-bucks-county/">Window Tint Bucks County</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:+12672637342">267 263 7342</a></li>
          <li><a href="mailto:hello@sbnautostyling.com">hello@sbnautostyling.com</a></li>
          <li>100 Red Lion Rd, Unit 3<br/>Philadelphia, PA 19115</li>
          <li>Mon–Fri 8am–6pm · Sat 8am–5pm</li>
        </ul>
      </div>
    </div>
    <div class="foot-word" aria-hidden="true">SBN Auto Styling</div>
    <p class="nonref foot-nr">All deposits are non-refundable.</p>
    <div class="foot-bottom">
      <span>© <span class="yr">2026</span> SBN Auto Styling. All rights reserved.</span>
      <div><a href="{R}privacy-policy/">Privacy Policy</a><a href="{R}terms-of-service/">Terms of Service</a></div>
    </div>
  </div>
</footer>'''

SLIM_FOOTER = FULL_FOOTER


def render(path, title, desc, body, header, footer, auto_modal=False):
    depth = path.count("/") + 1 if path else 0
    R = "../" * depth
    root = R or "./"
    canonical = f"{DOMAIN}/{path}" if path else DOMAIN
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:title" content="{e(title)}" />
<meta property="og:description" content="{e(desc)}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:type" content="website" />
<link rel="icon" href="{{R}}assets/img/logo.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,500..900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="{{R}}assets/site.css" />
<!-- Tracking: paste your Google Tag Manager snippet here (GTM-N9CVL9ZD) -->
</head>
<body{' data-auto-modal="1"' if auto_modal else ''}>
{SPRITE}
{header}
<main>
{body}
</main>
{footer}
{fix_paths(MODAL)}
{CHAT}
<script src="{{R}}assets/vehicles.js"></script>
<script src="{{R}}assets/site.js"></script>
{'<script src="{R}assets/cars.js"></script><script src="{R}assets/studio.js"></script>' if 'data-studio' in body else ''}
</body>
</html>
'''
    doc = doc.replace("{ROOT}", root).replace("{R}", R)
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(doc)
    return path


PAGES = []

# ================================================================ HOME
home_body = read("home.html")
PAGES.append(render("", "SBN Auto Styling | Philadelphia's Premier Auto Customization",
                    "SBN Auto Styling — expert vehicle wraps, PPF, window tinting, ceramic coatings, and custom styling in Philadelphia, PA. Call 267 263 7342.",
                    home_body, full_header(True), FULL_FOOTER, auto_modal=True))

# ================================================================ SERVICE PAGES
PERKS = [("i-cal", "Fast Scheduling", "Same-week appointments available for most services. Quick turnaround without cutting corners."),
         ("i-check", "Clear Packages, No Guesswork", "Upfront pricing for ceramic coating, tint, and PPF — built for your car and your goals."),
         ("i-sparkles", "High-End Finish", "Paint prepped the right way so your coating bonds properly and looks insanely glossy."),
         ("i-zap", "100% Satisfaction", "Defense from UV, contamination, and daily wear — so your paint stays cleaner and easier to maintain.")]
OTHERS = {"ppf": ("i-shield", "Paint Protection Film", "Invisible shield against chips, scratches & UV.", "services/ppf/"),
          "ceramic": ("i-sparkles", "Ceramic Coating", "Glass-hard nano-ceramic layer for years of gloss.", "services/ceramic-coating/"),
          "tint": ("i-eye", "Window Tinting", "Block UV, slash heat, elevate your look.", "services/window-tinting/")}


def plan_card(name, was, now, feats, duration, book, featured, film=None, sub="Book today's price", pre="Sides &amp; rear"):
    top = '<div class="plan-top">★ MOST POPULAR</div>' if featured else ""
    btn = "btn-primary" if featured else "btn-white"
    head = '<span class="sale">Sale</span>' if was else ""
    was_html = f'<div class="was">{was}</div>' if was else f'<div class="was" style="text-decoration:none">{pre}</div>'
    return f'''<div class="plan{' featured' if featured else ''} reveal">{top}<div class="plan-body">
      <div class="plan-head"><span class="plan-name">{e(name)}</span>{head}</div>
      {was_html}<div class="price">{now}</div><div class="today"{"" if was else ' style="color:var(--muted)"'}>{sub}</div>
      <ul class="feat">{checks(feats)}</ul>
      <div class="duration">{ic("i-clock", 15)}{duration}</div>
      <button class="btn {btn}" data-book="{book}"{f' data-film="{film}"' if film else ""}>Book Now {ic("i-arrow", 16, "arrow")}</button>
    </div></div>'''


STUDIO_COPY = {
    "tint": ("Tint visualizer", "See it before<br/>you book.", "Pick your vehicle and paint, then flip between 70% and 5% to see exactly how dark each film looks."),
    "ceramic": ("Before / After", "Drag to see<br/>the difference.", "Dull, swirled paint vs. corrected and coated. That's what our 10-year package delivers."),
    "ppf": ("Coverage builder", "See what<br/>gets covered.", "Tap a package to see which panels the film protects. Exact coverage is set at your free estimate."),
}


def service_page(path, key, chip, h1, intro, img, middle):
    k, h, p = STUDIO_COPY[key]
    middle = f'''<section style="padding-top:3rem"><div class="container">
  <div class="sec-head"><div><span class="badge">{k}</span><h2 class="h-display h2">{h}</h2></div><p class="lead">{p}</p></div>
  <div data-studio="{key}"></div>
</div></section>''' + middle
    others = "".join(
        f'<a class="other" href="{{R}}{u}"><span class="ic">{ic(i, 18)}</span><span><b>{t}</b><small>{s}</small></span><span class="go">{ic("i-arrow", 16)}</span></a>'
        for k, (i, t, s, u) in OTHERS.items() if k != key)
    perks = "".join(f'<div class="perk reveal"><div class="ic">{ic(i, 18)}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in PERKS)
    body = f'''<section class="svc-hero">
  <div class="bgimg" style="background-image:url('{{R}}assets/img/{img}')"></div>
  <div class="container">
    <a class="crumb" href="{{ROOT}}#services">{ic("i-chevl", 14)} Our Services</a><br/>
    <span class="chip">{ic(OTHERS[key][0], 14)}{chip}</span>
    <h1 class="h-display">{h1}</h1>
    <p>{intro}</p>
  </div>
</section>
{middle}
<div class="perks"><div class="container perk-grid">{perks}</div></div>
<section style="padding-bottom:3rem"><div class="container">
  <h2 class="h-display" style="font-size:2.2rem">Explore Other Services</h2>
  <p class="lead" style="margin-top:.5rem">Combine services for maximum protection and value.</p>
  <div class="other-grid">{others}</div>
</div></section>
<section id="cta" style="padding-top:0"><div class="container"><div class="cta-band reveal">
  <div class="copy">
    <h2 class="h-display">Ready to protect<br/>your vehicle?</h2>
    <p>Get a free quote within 24 hours. No hard sell, just honest advice and top-tier results.</p>
    <div class="btns">
      <button class="btn btn-white btn-md" data-open-modal>Book now {ic("i-arrow", 16, "arrow")}</button>
      <a class="btn btn-ghost btn-md" href="{TEL}">{ic("i-phone", 16)}267 263 7342</a>
    </div>
  </div>
  <div class="img" style="background-image:url('{{R}}assets/img/{img}')"></div>
</div></div></section>'''
    PAGES.append(render(path, f"{h1.title()} Philadelphia | SBN Auto Styling", intro, body, full_header(False), FULL_FOOTER))


service_page("services/ppf", "ppf", "PPF", "Paint Protection Film",
             "Self-healing PPF creates a nearly invisible barrier that protects your paint from stone chips, scratches, bug acids, road grime, and UV fade — with zero impact on appearance.",
             "service-ppf.png", f'''<section><div class="container center">
  <span class="badge">Free In-Person Estimate</span>
  <h2 class="h-display h2">Every PPF Job Starts With<br/>A Free Estimate</h2>
  <p class="lead">PPF pricing depends on your exact vehicle, coverage zone, and film choice. We assess it in person — no guesswork, no hidden costs.</p>
  <div class="estimate" style="text-align:left">
    <div><div class="k">What to Expect</div><ul class="feat">{checks([
        "We measure and assess your vehicle in person — every car is different",
        "Get an exact price for front bumper, full front end, or full body coverage",
        "We walk you through film options, coverage zones, and self-healing tech",
        "No pressure, no obligation — just honest answers and a clear quote",
        "Most estimates take 20–30 minutes at our Philadelphia location"])}</ul></div>
    <div><div class="k">No Obligation · 100% Free</div><h3>Schedule Your Free PPF Estimate</h3>
      <div class="btns"><button class="btn btn-primary btn-md" data-book="ppf">Request free estimate {ic("i-arrow", 16, "arrow")}</button><a class="btn btn-dark btn-md" href="{TEL}">{ic("i-phone", 16)}Call us</a></div></div>
  </div>
  <p class="addr-line">Philadelphia, PA · 100 Red Lion Rd Unit 3 · 267 263 7342</p>
</div></section>''')

service_page("services/ceramic-coating", "ceramic", "CERAMIC", "Ceramic Coating",
             "Nano-ceramic technology chemically bonds to your clear coat, creating a glass-hard shield that repels water, blocks UV, resists chemicals, and makes every wash effortless.",
             "service-ceramic.png", f'''<section><div class="container center">
  <span class="badge">Pricing</span>
  <h2 class="h-display h2">Choose Your Package</h2>
  <p class="lead">Pricing varies by vehicle size and condition — contact us for an exact quote.</p>
  <div class="plans center-1" style="text-align:left">{plan_card("Ceramic Coating", "$1,295", "$499",
      ["Exterior wash", "Iron decontamination", "Clay bar", "Paint enhancement", "10 year ceramic coating"], "8 – 10 hours", "ceramic", True)}</div>
  <p class="note">Prices vary by vehicle make, model &amp; condition. Contact us for an exact quote — always free.</p>
</div></section>''')

service_page("services/window-tinting", "tint", "TINT", "Window Tinting",
             "Premium window films that block harmful UV rays, slash interior heat, and give your car a clean blacked-out look — while staying completely street-legal in Pennsylvania.",
             "service-window-tint.png", f'''<section><div class="container center">
  <span class="badge">Pricing</span>
  <h2 class="h-display h2">Choose Your Package</h2>
  <p class="lead">Pricing varies by vehicle size and condition — contact us for an exact quote.</p>
  <div class="plans center-3" style="text-align:left">
    {plan_card("Standard Ceramic", "", "$199", ["Sides & rear windows", "60% IR heat rejection", "Blocks 99% UV", "Lifetime warranty"], "2 – 3 hours", "tint", False, "standard", "Windshield +$195")}
    {plan_card("Premium Ceramic", "", "$299", ["Sides & rear windows", "75% IR heat rejection", "Blocks 99% UV", "Lifetime warranty"], "2 – 3 hours", "tint", True, "premium", "Windshield +$225")}
    {plan_card("Nano Ceramic", "", "$450", ["Sides & rear windows", "95%+ IR heat rejection", "Blocks 99% UV", "Lifetime warranty"], "2 – 3 hours", "tint", False, "nano", "Windshield +$250", "Starting at")}
  </div>
  <p class="note">Prices for coupes, sedans &amp; small SUVs. Larger SUVs &amp; trucks +$60 for any film.</p>
  <p class="note">Prices vary by vehicle make, model &amp; condition. Contact us for an exact quote — always free.</p>
</div></section>''')


# ================================================================ PHILADELPHIA LANDING PAGES (layout A)
def philly_page(path, title, desc, kicker, h1a, h1b, intro, btns, blocks):
    body = f'''<div class="local"><div class="narrow">
  <div class="kicker">{kicker}</div>
  <h1 class="h-display">{h1a}<br/><span class="blue">{h1b}</span></h1>
  <p class="intro">{intro}</p>
  <div class="btn-row">{btns}</div>
  {blocks}
</div></div>'''
    PAGES.append(render(path, title, desc, body, simple_header(), SLIM_FOOTER))


def boxes(items):
    return '<div class="cards2">' + "".join(f'<div class="box"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in items) + "</div>"


def pkg(k, now, was, feats, best=False):
    return f'<div class="pkg{" best" if best else ""}"><div class="k">{k}</div><div class="pr"><b>{now}</b><s>{was}</s></div><ul>{"".join(f"<li>✓ {e(f)}</li>" for f in feats)}</ul></div>'


coverage = [("Front Bumper", "Most popular entry point. Protects the highest-impact zone from stone chips and road debris."),
            ("Full Front End", "Bumper + hood + fenders + mirrors — complete highway protection for daily drivers."),
            ("Full Front End + Ceramic", "PPF combined with ceramic coating for hydrophobic gloss over the protected area."),
            ("Full Body", "Complete protection for show cars, collector vehicles, or anyone who wants total peace of mind.")]
form = f'''<div class="form-card">
  <div class="fh">{ic("i-shield", 16, "check")}Request Your Free PPF Estimate</div>
  <form id="estimateForm">
    <div class="frow">
      <div class="field"><label>First Name <span>*</span></label><input name="First name" required placeholder="John"/></div>
      <div class="field"><label>Last Name <span>*</span></label><input name="Last name" required placeholder="Smith"/></div>
    </div>
    <div class="frow">
      <div class="field"><label>Phone <span>*</span></label><input name="Phone" type="tel" required placeholder="(267) 555-0100"/></div>
      <div class="field"><label>Email <span>*</span></label><input name="Email" type="email" required placeholder="you@email.com"/></div>
    </div>
    <div class="field"><label>Vehicle (Year, Make, Model) <span>*</span></label><input name="Vehicle" required placeholder="e.g. 2023 Porsche 911 Carrera"/></div>
    <div class="field"><label>Coverage Interest <span>*</span></label><select name="Coverage" required>
      <option value="">Select coverage…</option><option>Front Bumper</option><option>Partial Front End</option><option>Full Front End</option>
      <option>Full Front + Ceramic Coating</option><option>Full Body PPF</option><option>Not Sure — I Need a Recommendation</option></select></div>
    <div class="field"><label>Notes <em>(optional)</em></label><textarea name="Notes" placeholder="Any details about your vehicle or preferences…"></textarea></div>
    <button type="submit" class="btn btn-primary">Request Free Estimate {ic("i-arrow", 16, "arrow")}</button>
    <p class="small-note" style="text-align:center;margin:0">No obligation. We'll be in touch within 1 business day.</p>
  </form>
  <div class="form-ok" id="formOk"><b>Thanks — request received!</b><span class="small-note">We'll be in touch within 1 business day. Need us sooner? Call 267 263 7342.</span></div>
</div>'''

philly_page("ppf-philadelphia", "Paint Protection Film Philadelphia PA | PPF Installation | SBN Auto Styling",
            "Professional PPF installation in Philadelphia, PA. Self-healing paint protection film for front bumpers, full front ends & full body. Free in-person estimates. Call 267 263 7342.",
            "Philadelphia, PA", "Paint Protection Film", "Philadelphia",
            "SBN Auto Styling installs professional-grade PPF on vehicles across Philadelphia and the surrounding area. Self-healing, virtually invisible, and built to last — starting with a free in-person estimate tailored to your specific car.",
            f'<a class="btn btn-primary btn-md" href="{TEL}">Call for Free Estimate</a><a class="btn btn-dark btn-md" href="{{R}}services/ppf/">View PPF Service Page →</a>',
            f'''<div class="block"><h2>Why Philadelphia Cars Need PPF</h2>{boxes([
    ("Rough Road Conditions", "Philadelphia's pothole-riddled roads throw debris at high speed. PPF creates a sacrificial barrier that absorbs impact without touching your paint."),
    ("Winter Salt Damage", "Road salt corrodes unprotected paint edges and chips. PPF seals vulnerable areas and is fully resistant to chemical damage from salt and de-icers."),
    ("Highway Stone Chips", "I-95, the turnpike, and Route 1 — all notorious for flying gravel from trucks. A full front-end PPF install is the most effective defense against chip damage."),
    ("Preserve Resale Value", "A car with clean, chip-free paint sells for significantly more. PPF is an investment that pays back when you sell or trade in.")])}</div>
<div class="block"><h2>PPF Coverage Options</h2><div class="stack">{"".join(f'<div class="box opt"><div><div class="t">{t}</div><p>{d}</p></div><span class="s">From free estimate</span></div>' for t, d in coverage)}</div>
<p class="small-note">All pricing is vehicle-specific and requires a free in-person assessment. No guesswork — just an honest quote.</p></div>
<div class="block"><h2>Frequently Asked Questions</h2>{faq([
    ("How much does PPF cost in Philadelphia?", "PPF pricing in Philadelphia varies by vehicle size and coverage zone. A front bumper typically starts around $400–$600, a full front end ranges from $1,200–$2,000, and full body coverage runs $4,000–$8,000+. We provide free in-person estimates so you get an exact price for your specific vehicle."),
    ("How long does paint protection film last?", "Quality PPF installed professionally typically lasts 7–10 years. Our self-healing films make minor scratches and swirl marks disappear with heat exposure. Proper maintenance extends the life significantly."),
    ("Is PPF worth it in Philadelphia?", "Absolutely. Philadelphia roads — potholes, highway gravel, salt in winter — are tough on paint. PPF prevents stone chips, road rash, and environmental damage that can cost thousands to repair. Most customers see it as protecting their investment."),
    ("Do you offer PPF near me in Philadelphia?", "Yes — SBN Auto Styling is located at 100 Red Lion Road Unit 3, Philadelphia PA 19115. We serve Northeast Philadelphia, Bucks County, Montgomery County, and the surrounding area."),
    ("What areas of the car can PPF protect?", "We install PPF on front bumpers, hoods, fenders, mirrors, door edges, rocker panels, and full body coverage. Every job starts with a free estimate where we walk you through exactly what makes sense for your vehicle and driving habits.")])}</div>
<div class="block"><h2>Ready to Protect Your Paint?</h2>
<p class="intro" style="margin-top:0">Fill out the form below and we'll reach out within 1 business day to schedule your free in-person estimate. Or call us directly at <a class="blue" href="{TEL}">267 263 7342</a>.</p>{form}</div>''')

philly_page("ceramic-coating-philadelphia", "Ceramic Coating Philadelphia PA | 10 Year Package $499 | SBN Auto Styling",
            "Professional ceramic coating in Philadelphia PA. 10-year ceramic coating just $499 (reg. $1,295). Includes wash, iron decontamination, clay bar, and paint enhancement. Book online today.",
            "Philadelphia, PA", "Ceramic Coating", "Philadelphia",
            "SBN Auto Styling provides professional ceramic coating for Philadelphia vehicles — a 10-year package starting with proper paint prep that most shops skip. Sale price: $499, regularly $1,295. Additional services available, just call.",
            f'<button class="btn btn-primary btn-md" data-book="ceramic">Book Online Now</button><a class="btn btn-dark btn-md" href="{{R}}services/ceramic-coating/">View Full Service Details →</a>',
            f'''<div class="block"><h2>Ceramic Coating Packages</h2>{pkg("10 Year Package — Best Value", "$499", "$1,295", ["Exterior wash", "Iron decontamination", "Clay bar", "Paint enhancement", "10 year ceramic coating"], True)}</div>
<div class="block"><h2>What Ceramic Coating Does for Your Car</h2>{boxes([
    ("Hydrophobic Protection", "Water, mud, and road grime bead off instantly. Your car stays cleaner longer and washing takes half the time."),
    ("UV & Fade Resistance", "Philadelphia summers fade unprotected paint. Ceramic coating blocks UV rays at the clear coat level, keeping your color deep and rich."),
    ("Chemical Resistance", "Bird droppings, tree sap, road salt — all repelled by the ceramic layer. No more etching or paint damage from common contaminants."),
    ("Deep Gloss Finish", "Ceramic coating enhances the depth of your paint like nothing else. The result looks better than the day you drove it off the lot.")])}</div>
<div class="block"><h2>FAQ — Ceramic Coating Philadelphia</h2>{faq([
    ("How much does ceramic coating cost in Philadelphia?", "SBN Auto Styling's 10-year ceramic coating package is currently $499 (regularly $1,295). It includes an exterior wash, iron decontamination, clay bar, and paint enhancement — not just the coating."),
    ("Is ceramic coating worth it in Philadelphia?", "Yes. Philadelphia's weather — harsh winters, road salt, summer UV — accelerates paint degradation. Ceramic coating creates a chemically bonded layer that repels water, resists UV fading, and makes washing dramatically easier. Most customers recoup the cost in reduced maintenance and better resale value."),
    ("How long does ceramic coating last?", "Our 10-year package uses a high-grade formulation that bonds deeply to the clear coat for a decade of protection. It requires basic maintenance — no waxing, just regular washing."),
    ("What's included in your ceramic coating package?", "The package includes an exterior wash, iron decontamination, clay bar, paint enhancement, and a 10-year ceramic coating. We never apply coating over dirty or contaminated paint.")])}</div>
<div class="block closer"><h2 class="h-display" style="font-size:2rem">Book Your Ceramic Coating Today</h2>
<p>Sale pricing available now. Book online or visit us at 100 Red Lion Road Unit 3, Philadelphia PA 19115.</p>
<button class="btn btn-primary btn-md" data-book="ceramic">Book Now — Sale Price</button></div>''')

philly_page("window-tinting-philadelphia", "Window Tinting Philadelphia PA | Ceramic & Nano Ceramic Tint | SBN Auto Styling",
            "Professional window tinting in Philadelphia PA. Ceramic tint from $199: Standard, Premium and Nano Ceramic films. PA legal tint. Lifetime warranty. Book online at SBN Auto Styling.",
            "Philadelphia, PA", "Window Tinting", "Philadelphia",
            "SBN Auto Styling provides ceramic and nano ceramic window tinting in Philadelphia — always PA-legal, bubble-free installs with a lifetime warranty. Sale pricing available on all packages.",
            f'<button class="btn btn-primary btn-md" data-book="tint">Book Online Now</button><a class="btn btn-dark btn-md" href="{{R}}services/window-tinting/">View Full Service Details →</a>',
            f'''<div class="block"><h2>Tint Packages</h2><div class="cards2">
{pkg("Standard Ceramic", "$199", "", ["Sides & rear windows", "60% IR heat rejection", "Blocks 99% UV", "Lifetime warranty"])}
{pkg("Premium Ceramic — Most Popular", "$299", "", ["Sides & rear windows", "75% IR heat rejection", "Blocks 99% UV", "Lifetime warranty"], True)}
{pkg("Nano Ceramic — Max Heat Rejection", "from $450", "", ["Sides & rear windows", "95%+ IR heat rejection", "Blocks 99% UV", "Lifetime warranty"])}</div>
<p class="small-note">Prices for coupes, sedans &amp; small SUVs; larger SUVs &amp; trucks +$60. Add the windshield: +$195 Standard, +$225 Premium, +$250 Nano.</p>
<p class="small-note">All tint is PA-legal. Front windows tinted to comply with Pennsylvania's 70% VLT requirement.</p></div>
<div class="block"><h2>Benefits of Window Tinting in Philadelphia</h2>{boxes([
    ("Beat Philadelphia Summers", "Ceramic tint dramatically reduces the solar heat that builds up inside your car — keeping it cooler without working the AC as hard."),
    ("UV Protection for You & Your Interior", "UV rays fade leather, crack dashboards, and damage skin. Our tint blocks 99% of UV — protecting your car's interior and your health."),
    ("Privacy & Security", "Tinted windows deter smash-and-grab theft by making valuables harder to see. A must for parking in Philadelphia neighborhoods."),
    ("Clean, Factory Look", "Our film is precision-cut to your vehicle. No razor blades on glass, no excess film — just clean edges that look like they came from the factory.")])}</div>
<div class="block"><h2>FAQ — Window Tinting Philadelphia</h2>{faq([
    ("What is the legal window tint percentage in Pennsylvania?", "In Pennsylvania, front side windows must allow more than 70% of light in (70% VLT). Rear side windows and the rear windshield can be any darkness. We always install PA-legal tint — you'll never fail inspection because of our work."),
    ("How much does window tinting cost in Philadelphia?", "Sides & rear windows on a coupe, sedan or small SUV: Standard Ceramic $199, Premium Ceramic $299, Nano Ceramic from $450. Larger SUVs and trucks are $60 more. Adding the windshield is $195 / $225 / $250 depending on film. All include a lifetime warranty."),
    ("What's the difference between Standard, Premium and Nano Ceramic?", "All three are ceramic films that block 99% of UV and don't interfere with GPS, Bluetooth or cell signal. The difference is infrared heat rejection: Standard 60%, Premium 75%, Nano 95%+."),
    ("How long does window tinting take in Philadelphia?", "Most vehicles are completed in 2–3 hours at our Philadelphia shop. We cut all film precisely to your vehicle's windows — no razor blades on the glass, clean edges every time."),
    ("Does window tint really reduce heat?", "Yes — significantly. Nano ceramic tint can reject up to 99% of UV rays and dramatically reduce infrared heat buildup. On a hot Philadelphia summer day, the difference inside the car is immediate and noticeable.")])}</div>
<div class="block closer"><h2 class="h-display" style="font-size:2rem">Book Your Tint Today</h2>
<p>2–3 hour install. Lifetime warranty. Sale pricing available now at 100 Red Lion Road Unit 3, Philadelphia PA 19115.</p>
<button class="btn btn-primary btn-md" data-book="tint">Book Now — Sale Price</button></div>''')


# ================================================================ REGION LANDING PAGES (layout B)
BUCKS = ["Warminster", "Langhorne", "Newtown", "Doylestown", "Levittown", "Bristol", "Bensalem", "Yardley", "Feasterville", "Southampton", "Horsham", "Willow Grove"]
NEPHL = ["Mayfair", "Fox Chase", "Bustleton", "Rhawnhurst", "Somerton", "Holme Circle", "Torresdale", "Pennypack", "Tacony", "Frankford", "Bridesburg", "Wissinoming", "Roxborough", "Manayunk", "Chestnut Hill", "Mount Airy"]


def region_page(path, title, desc, kicker, h1a, h1b, intro, hero_extra, btns, left_h, left_ps, right_h, right_html, areas_h, areas, faq_h, faqs, close_h, close_p, close_btn, close_addr):
    body = f'''<section class="region-hero"><div class="container" style="max-width:56rem">
  <div class="kicker">{kicker}</div>
  <h1 class="h-display">{h1a}<br/><span class="blue">{h1b}</span></h1>
  <p class="intro">{intro}</p>
  {hero_extra}
  <div class="btn-row">{btns}</div>
</div></section>
<section style="padding-top:3.5rem"><div class="container" style="max-width:56rem">
  <div class="two-col">
    <div class="block" style="margin-top:0"><h2>{left_h}</h2>{"".join(f'<p class="body">{e(p)}</p>' for p in left_ps)}</div>
    <div class="block" style="margin-top:0"><h2>{right_h}</h2>{right_html}</div>
  </div>
  <div class="block areas-box"><h2 style="font-size:1.5rem">{areas_h}</h2><ul>{"".join(f"<li>{a}</li>" for a in areas)}</ul></div>
  <div class="block"><h2>{faq_h}</h2>{faq(faqs)}</div>
  <div class="block closer"><h2 class="h-display" style="font-size:2.2rem">{close_h}</h2><p>{close_p}</p>{close_btn}<p class="addr">{close_addr}</p></div>
  <a class="home-back" href="{{ROOT}}">← Back to SBN Auto Styling Home</a>
</div></section>'''
    PAGES.append(render(path, title, desc, body, simple_header(), SLIM_FOOTER))


ADDR = "100 Red Lion Road Unit 3, Philadelphia, PA 19115 · 267 263 7342"
stack = lambda items: '<div class="stack">' + "".join(f'<div class="box"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in items) + "</div>"

region_page("ppf-bucks-county", "Paint Protection Film Bucks County PA | SBN Auto Styling",
            "Professional Paint Protection Film (PPF) installation serving Bucks County, PA — Warminster, Langhorne, Newtown, and surrounding areas. Self-healing, invisible protection. Call 267 263 7342.",
            "Bucks County, PA", "Paint Protection Film", "Bucks County",
            "SBN Auto Styling provides professional PPF installation to drivers across Bucks County, PA — Warminster, Langhorne, Newtown, Doylestown, and beyond. Preserve your vehicle's finish with self-healing, optically clear film.",
            "", f'<a class="btn btn-primary btn-md" href="{TEL}">Call 267 263 7342 for Free Estimate</a><a class="btn btn-dark btn-md" href="{{ROOT}}">View All Services</a>',
            "Why Bucks County Drivers Choose PPF", [
                "Bucks County roads — from Route 1 to I-95 — put your vehicle's paint at constant risk from gravel, road salt, construction debris, and highway stone chips. A single chip on a luxury vehicle can cost hundreds to repair.",
                "Paint Protection Film is the most effective way to shield your investment. The film absorbs impacts before they reach your clear coat, and self-healing technology means minor scratches disappear on their own with gentle heat.",
                "SBN Auto Styling is conveniently located just off the PA Turnpike in Philadelphia, making us the go-to PPF shop for Bucks County car owners."],
            "PPF Coverage Options", stack([
                ("Front Bumper", "The most common entry point — protects the highest-impact area from daily stone chips."),
                ("Full Front End", "Hood, fenders, mirrors, headlights, and bumper. Full coverage for highway driving."),
                ("Full Front End + Ceramic", "Physical protection plus hydrophobic ceramic coating for the ultimate combo."),
                ("Full Body PPF", "360° protection for concours, exotic, and collector vehicles.")]),
            "Bucks County Areas We Serve", BUCKS, "PPF Bucks County — FAQ", [
                ("Do you serve Bucks County for PPF installation?", "Yes. SBN Auto Styling serves all of Bucks County including Warminster, Langhorne, Newtown, Doylestown, Levittown, and surrounding areas. Our shop is located at 100 Red Lion Road Unit 3, Philadelphia, PA 19115 — a short drive from most of Bucks County."),
                ("How much does Paint Protection Film cost in Bucks County?", "PPF pricing depends on how much of your vehicle you want covered. Common options include front bumper only, full front end (hood, fenders, mirrors, bumper), or full body coverage. We provide free in-person estimates — call 267 263 7342 to schedule."),
                ("What brands of PPF do you use?", "We install industry-leading films including 3M and Avery Dennison. Both offer self-healing technology that erases minor scratches and swirl marks with heat."),
                ("Is PPF better than ceramic coating for rock chips?", "Yes. Ceramic coating protects against UV, water, and light scratches, but PPF provides physical impact protection against rock chips and road debris. Many Bucks County drivers choose to combine both for maximum protection."),
                ("How long does PPF installation take?", "Most installations take 1–3 days depending on coverage area. Full body PPF may require additional time. We'll give you a precise timeline at your free estimate.")],
            "Get Your Free PPF Estimate", "Book a free in-person assessment at our Philadelphia shop. We cover all PPF options and give you an honest quote — no pressure, no obligation.",
            f'<a class="btn btn-primary btn-md" href="{TEL}">Call 267 263 7342</a>', "100 Red Lion Road Unit 3, Philadelphia, PA 19115 · Mon–Fri 8am–6pm · Sat 8am–5pm")

region_page("ceramic-coating-northeast-philadelphia", "Ceramic Coating Northeast Philadelphia | SBN Auto Styling",
            "Professional ceramic coating in Northeast Philadelphia — 10-year package just $499 (reg. $1,295). Serving Mayfair, Fox Chase, Bustleton, Rhawnhurst, and surrounding areas. Call 267 263 7342.",
            "Northeast Philadelphia, PA", "Ceramic Coating", "Northeast Philadelphia",
            "SBN Auto Styling offers professional nano-ceramic coating to Northeast Philadelphia drivers — Mayfair, Fox Chase, Bustleton, Somerton, and beyond. Showroom shine and UV protection that lasts years, not months.",
            '<div class="mini-pkgs"><div class="mini"><div class="k">10-Year Package — Best Value</div><div class="pr"><b>$499</b><s>$1,295</s></div><small>Wash · Iron Decon · Clay Bar · Paint Enhancement · 10yr Coating</small></div></div>',
            f'<button class="btn btn-primary btn-md" data-book="ceramic">Book Online Now</button><a class="btn btn-dark btn-md" href="{TEL}">Call 267 263 7342</a>',
            "Why Northeast Philly Drivers Choose Ceramic", [
                "Northeast Philadelphia streets are tough on car paint. Salt-covered roads in winter, UV exposure in summer, and constant exposure to industrial fallout and road grime break down your clear coat faster than you might think.",
                "Ceramic coating creates a semi-permanent nano-ceramic layer that bonds directly to your paint, providing a hydrophobic surface that repels water, UV rays, bird droppings, tree sap, and brake dust.",
                "Unlike traditional wax that washes off in weeks, our 10-year formulation protects your investment for years with minimal maintenance."],
            "What's Included", pkg("10-Year Package", "$499", "$1,295", ["Exterior wash", "Iron decontamination", "Clay bar", "Paint enhancement", "10 year ceramic coating"], True),
            "Northeast Philadelphia Neighborhoods We Serve", NEPHL, "Ceramic Coating NE Philly — FAQ", [
                ("Where are you located relative to Northeast Philadelphia?", "SBN Auto Styling is at 100 Red Lion Road Unit 3, Philadelphia, PA 19115 — in the heart of Northeast Philadelphia near the Bucks County border. We're accessible from I-95, Route 1, and the PA Turnpike."),
                ("What's included in the 10-year ceramic coating package?", "Our 10-year package includes an exterior wash, iron decontamination, clay bar, paint enhancement, and a 10-year ceramic coating."),
                ("How long does ceramic coating take?", "Most ceramic coating installations take 1–2 days. The paint decontamination and correction steps require proper curing time for best adhesion and longevity."),
                ("Can ceramic coating be applied over PPF?", "Absolutely — and it's highly recommended. Ceramic coating over PPF adds hydrophobic properties that make the film easier to clean and maintain. SBN offers combined PPF + ceramic packages."),
                ("What maintenance does ceramic coating require?", "Ceramic coatings are low-maintenance. Avoid automated car washes with harsh brushes. Hand washes with a pH-neutral soap every 2–4 weeks keep the coating performing at its best. We provide full aftercare instructions with every install."),
                ("Do you serve neighborhoods throughout Northeast Philly?", "Yes. We serve Mayfair, Fox Chase, Bustleton, Rhawnhurst, Somerton, Holme Circle, Torresdale, Pennypack, Roxborough, and all surrounding Northeast Philadelphia neighborhoods.")],
            "Book Your Ceramic Coating", "Online booking available for same-week appointments. Sale pricing is available for a limited time.",
            '<button class="btn btn-primary btn-md" data-book="ceramic">Book Online Now</button>', ADDR)

region_page("window-tinting-bucks-county", "Window Tinting Bucks County PA | SBN Auto Styling",
            "Professional ceramic window tinting serving Bucks County PA — Warminster, Langhorne, Newtown, and surrounding areas. Ceramic tint from $199. PA legal. Call 267 263 7342.",
            "Bucks County, PA", "Window Tinting", "Bucks County",
            "SBN Auto Styling offers premium ceramic and nano ceramic window tinting to Bucks County drivers. Block UV, reduce heat, and protect your interior — all PA-legal compliant.",
            '<div class="mini-pkgs three"><div class="mini"><div class="k">Standard Ceramic</div><div class="pr"><b>$199</b></div><small>60% IR heat rejection</small></div><div class="mini"><div class="k">Premium Ceramic</div><div class="pr"><b>$299</b></div><small>75% IR heat rejection</small></div><div class="mini"><div class="k">Nano Ceramic</div><div class="pr"><b>$450+</b></div><small>95%+ IR heat rejection</small></div></div><p class="small-note" style="margin:-1rem 0 1.5rem">Sides &amp; rear, coupes/sedans/small SUVs. Larger SUVs &amp; trucks +$60.</p>',
            f'<button class="btn btn-primary btn-md" data-book="tint">Book Online Now</button><a class="btn btn-dark btn-md" href="{TEL}">Call 267 263 7342</a>',
            "Why Choose Ceramic Tint?", [
                "Not all window film is created equal. Cheap dyed tints fade, bubble, and turn purple within a few years. Ceramic tint uses metallic oxide particles that block heat and UV without degrading over time.",
                "Bucks County summers are intense. Ceramic tint can reduce interior cabin temperatures by 15–30°F, protecting your dashboard, seats, and leather while keeping every drive comfortable.",
                "Unlike metalized films, ceramic and nano ceramic tints don't interfere with GPS signals, satellite radio, E-ZPass, or cell phone reception — critical for daily commuters on the PA Turnpike and I-95."],
            "Tint Comparison", '<div class="stack">' +
            pkg("Standard Ceramic — $199", "", "", ["Blocks 99% of UV rays", "60% IR heat rejection", "No signal interference", "10+ year lifespan"]) +
            pkg("Premium Ceramic — $299", "", "", ["Blocks 99% of UV rays", "75% IR heat rejection", "No signal interference", "Noticeably cooler cabin"], True) +
            pkg("Nano Ceramic — from $450", "", "", ["Blocks 99% of UV rays", "95%+ IR heat rejection", "100% signal transparent", "Ideal for luxury vehicles"]) + "</div>",
            "Bucks County Areas We Serve", BUCKS, "Window Tinting Bucks County — FAQ", [
                ("Do you tint windows for Bucks County customers?", "Yes. We serve all of Bucks County including Warminster, Langhorne, Newtown, Doylestown, Bensalem, Levittown, and surrounding areas. Our shop is at 100 Red Lion Road Unit 3, Philadelphia, PA 19115 — just a short drive from most Bucks County towns."),
                ("What are the window tint laws in Pennsylvania?", "Pennsylvania law requires at least 70% Visible Light Transmission (VLT) on front side windows and the front windshield (above the AS-1 line). Rear side windows and the rear windshield have no VLT restriction. All our tint installations are PA-legal compliant."),
                ("What's the difference between Standard, Premium and Nano Ceramic tint?", "All three of our films are ceramic: they block 99% of UV and never interfere with GPS, phone signals or toll transponders. The difference is infrared heat rejection: Standard Ceramic 60%, Premium Ceramic 75%, Nano Ceramic 95%+."),
                ("How long does window tinting take?", "Most vehicles can be completed in 2–4 hours. We recommend avoiding rolling down windows for 3–5 days post-install to allow the adhesive to cure fully."),
                ("Does ceramic tint replace the need for sunshades?", "Ceramic tint significantly reduces interior heat buildup — in some cases by 15–30°F on a hot day. While it won't completely eliminate the need for a sunshade on extreme summer days, most customers find it dramatically more comfortable and rely on sunshades far less."),
                ("How long does window tint last?", "Quality ceramic and nano ceramic films last 10+ years without peeling, bubbling, or fading. Cheaper dyed films may begin to purple or bubble within 3–5 years. SBN only installs premium-grade film.")],
            "Book Your Window Tint Today", "Sale pricing available for a limited time. Book online in minutes or call us for same-week availability.",
            '<button class="btn btn-primary btn-md" data-book="tint">Book Online Now</button>', ADDR)


# ================================================================ BLOG
POSTS = [
    dict(slug="how-long-does-ppf-last", cat="PPF", read="5 min read", date="March 15, 2026",
         title="How Long Does PPF Last? (And Is It Worth It in Philadelphia?)",
         dek="Paint protection film can last 7–10 years with proper care. Here's what affects PPF lifespan and whether it makes sense for Philadelphia drivers.",
         body=[("p", "Paint protection film (PPF) is one of the best investments a Philadelphia driver can make — but how long does it actually last? The answer depends on the quality of the film, the quality of the install, and how well you maintain it."),
               ("h", "Typical PPF Lifespan: 7–10 Years"),
               ("p", "High-quality PPF installed by a professional shop typically lasts 7–10 years under normal driving conditions. Some premium films come with manufacturer warranties of up to 10 years against yellowing, cracking, and delamination."),
               ("p", "That said, PPF is a sacrificial layer — it does its job by taking damage instead of your paint. Heavy chip exposure on the front end may mean the film looks rough after 5–6 years, but it's done exactly what it was supposed to do."),
               ("h", "What Affects PPF Lifespan?"),
               ("ul", ["<b>Film quality</b> — entry-level films degrade faster than premium self-healing films", "<b>Installation quality</b> — poor installs with lifted edges collect dirt and fail early", "<b>Exposure</b> — highway miles and gravel roads wear the film faster than city driving", "<b>Maintenance</b> — regular washing and an occasional PPF sealant significantly extend life", "<b>Philadelphia winters</b> — road salt doesn't damage the film itself but can attack edges if not properly sealed"]),
               ("h", "Is PPF Worth It for Philadelphia Drivers?"),
               ("p", "Philadelphia is genuinely tough on paint. Between I-95 gravel, Route 1 trucks, Northeast Philly construction zones, and winter salt, an unprotected hood and bumper can be chip-covered within two years of ownership."),
               ("p", "A front bumper chip repair runs $300–$500. A hood respray is $800–$1,500. Full PPF on the front end costs less than one respray — and protects for a decade. The math usually works strongly in PPF's favor."),
               ("h", "When to Replace PPF"),
               ("ul", ["Visible yellowing or hazing that doesn't polish out", "Edges lifting and collecting dirt", "Deep scratches that haven't self-healed", "After a significant impact that dented or cracked the film", "When reselling — many buyers prefer fresh film over old discolored film"]),
               ("h", "Self-Healing PPF: Does It Really Work?"),
               ("p", "Yes — and it's impressive. Modern self-healing PPF contains a topcoat that flows back into shape when exposed to heat (sunlight or warm water). Light scratches and swirl marks from washing disappear within minutes in direct sunlight. It won't fix deep gouges, but for everyday wear it's genuinely functional.")],
         cta=("Ready to protect your paint? SBN Auto Styling offers free in-person PPF estimates at our Philadelphia shop.", "Book a Free Estimate", TEL)),
    dict(slug="ceramic-coating-vs-wax", cat="Ceramic Coating", read="6 min read", date="February 28, 2026",
         title="Ceramic Coating vs Wax: What Philadelphia Car Owners Need to Know",
         dek="Wax lasts weeks. Ceramic coating lasts years. Here's an honest comparison to help you decide which is right for your car and budget.",
         body=[("p", "If you care about your car's paint, you've probably asked this question: should I get ceramic coating or just wax? The honest answer depends on your budget, how long you plan to keep the car, and how much maintenance you want to do."),
               ("h", "The Core Difference"),
               ("p", "Wax sits on top of your paint as a temporary sacrificial layer. Ceramic coating chemically bonds to your clear coat, becoming part of the surface. That fundamental difference explains everything else."),
               ("h", "Durability"),
               ("ul", ["<b>Carnauba wax:</b> 4–8 weeks", "<b>Synthetic sealant:</b> 3–6 months", "<b>Entry-level ceramic:</b> 1–2 years", "<b>Professional ceramic (10yr):</b> 8–10 years"]),
               ("p", "If you're waxing your car every 6–8 weeks, the annual cost of products and labor quickly adds up to more than a one-time ceramic coating."),
               ("h", "Protection Level"),
               ("p", "Wax offers light protection against environmental fallout and gives a warm glow. Ceramic coating provides genuine protection against UV rays, bird droppings, tree sap, road salt, and light scratches — none of which wax can handle for more than a few days."),
               ("p", "In Philadelphia specifically, where winter road salt is relentless and summer UV is harsh, ceramic coating's chemical resistance is a genuine advantage."),
               ("h", "Hydrophobic Effect"),
               ("p", "Both wax and ceramic coating make water bead. But ceramic coating's hydrophobic effect is far more aggressive and long-lasting. After a professional ceramic coating, washing takes half the time and mud barely sticks. After waxing, the effect fades within weeks."),
               ("h", "Cost Comparison"),
               ("ul", ["<b>DIY waxing</b> (product + time annually): $200–$400/year", "<b>Professional wax/sealant:</b> $100–$250 every 6 months", "<b>SBN 10-year ceramic:</b> $499 one time (covers 10 years)"]),
               ("h", "Which Should You Choose?"),
               ("p", "If you're keeping your car 2+ years and want the best protection with minimal ongoing maintenance, ceramic coating wins easily. If you're leasing for 2 years or on a tight budget right now, a quality sealant is fine — but you'll be spending more per year over time.")],
         cta=("SBN Auto Styling's 10-year ceramic package is $499 (reg. $1,295) and includes full paint prep — not just the coating application.", "Book Ceramic Coating", "book:ceramic")),
    dict(slug="pennsylvania-window-tint-laws", cat="Window Tinting", read="4 min read", date="January 20, 2026",
         title="Pennsylvania Window Tint Laws: What's Legal in 2026?",
         dek="Pennsylvania has specific VLT requirements for window tint. Here's exactly what's legal, what'll fail inspection, and how SBN ensures compliance.",
         body=[("p", "Before tinting your car in Philadelphia, you need to know Pennsylvania's window tint laws. Get this wrong and you'll fail your annual inspection — or worse, get pulled over. Here's the complete breakdown."),
               ("h", "Pennsylvania Window Tint Legal Limits (2026)"),
               ("ul", ["<b>Front windshield:</b> Non-reflective tint only on the top 3 inches above the AS-1 line", "<b>Front side windows (driver &amp; passenger):</b> Must allow more than 70% of light in (70% VLT minimum)", "<b>Rear side windows:</b> Any darkness is legal", "<b>Rear windshield:</b> Any darkness is legal"]),
               ("p", "The critical number is 70% VLT (Visible Light Transmission) for front side windows. This means the glass must allow 70% or more of outside light through — which is quite light. Most factory glass already sits near this limit."),
               ("h", "What Does This Mean in Practice?"),
               ("p", "You can tint your rear windows (back doors and rear windshield) as dark as you want — full privacy tint, limo tint, whatever you like. The restriction only applies to the front two side windows and the windshield."),
               ("p", "At SBN Auto Styling, we always install PA-legal front window tint. We use a light ceramic film on front windows that adds UV protection and heat rejection while staying within the 70% VLT requirement. Your car will pass inspection every year."),
               ("h", "Will Tint Fail My PA Inspection?"),
               ("p", "Only if the front windows are too dark (below 70% VLT). Rear windows and the rear windshield are not tested. If you've had tint installed by another shop and are concerned about front window darkness, bring it in and we'll check the VLT with our meter."),
               ("h", "Reflectivity Rules"),
               ("p", "Pennsylvania also regulates reflectivity — tint cannot be mirrored or metallic in appearance. Our ceramic and nano ceramic films are non-reflective by design."),
               ("h", "Medical Exemptions"),
               ("p", "Pennsylvania does offer a medical exemption permit for individuals with certain skin conditions requiring reduced UV exposure. If you qualify, contact PennDOT — it allows darker front windows with a permit.")],
         cta=("All SBN window tint installs are Pennsylvania-legal with a lifetime warranty.", "Book Window Tint", "book:tint")),
    dict(slug="ppf-vs-ceramic-coating", cat="PPF", read="5 min read", date="December 10, 2025",
         title="PPF vs Ceramic Coating: Which Does Your Philadelphia Car Need?",
         dek="PPF and ceramic coating solve different problems. Here's how to choose — or why many Philadelphia drivers get both.",
         body=[("p", "PPF and ceramic coating are often confused, but they do fundamentally different things. Choosing between them — or combining them — depends on what you're trying to protect against."),
               ("h", "What Each Product Does"),
               ("p", "<b>PPF (Paint Protection Film)</b> is a physical barrier — a thick, clear polyurethane film that absorbs impact. It protects against stone chips, rock impacts, scratches, and physical damage. If a rock hits your hood, it hits the film, not your paint."),
               ("p", "<b>Ceramic coating</b> is a chemical bond — a nano-ceramic layer that bonds to your clear coat. It protects against chemical damage (bird droppings, sap, UV, salt), makes the surface hydrophobic, and enhances gloss. It will not stop a stone chip."),
               ("h", "Head-to-Head Comparison"),
               ("ul", ["Stone chip protection: PPF ✓ | Ceramic ✗", "UV &amp; fade protection: PPF ✓ | Ceramic ✓✓", "Chemical resistance: PPF ✓ | Ceramic ✓✓", "Hydrophobic beading: PPF partial | Ceramic ✓✓", "Self-healing minor scratches: PPF (premium films) ✓ | Ceramic ✗", "Gloss enhancement: PPF minimal | Ceramic ✓✓", "Durability: PPF 7–10yr | Ceramic 5–10yr"]),
               ("h", "Who Should Get PPF?"),
               ("p", "PPF is for drivers who do significant highway mileage, live near construction zones, or drive cars they want to preserve for resale. The front bumper and hood are the highest-priority areas — they take the most chip damage."),
               ("p", "In Philadelphia, if you regularly use I-95, the turnpike, or any suburban highways, PPF on the front end is a wise investment."),
               ("h", "Who Should Get Ceramic Coating?"),
               ("p", "Ceramic coating is for drivers who want easier maintenance, better gloss, and long-term protection from the environment. If you wash your car regularly and hate water spots, bird drop etching, and fading — ceramic coating solves all of that."),
               ("h", "The Best Combination: PPF + Ceramic"),
               ("p", "Many SBN customers get both — PPF on high-impact zones (front bumper, hood, fenders) and ceramic coating over the entire car including the PPF. The PPF handles physical damage, the ceramic handles everything else. SBN offers this as a combined package.")],
         cta=("Not sure which is right for your car? Call us and we'll give you an honest recommendation based on your vehicle and driving habits.", "Talk to Our Team", TEL)),
]


def cat_cls(c): return "cat ppf" if c == "PPF" else "cat"


cards = "".join(f'''<a class="post-card reveal" href="{{R}}blog/{p["slug"]}/">
  <div class="meta"><span class="{cat_cls(p["cat"])}">{p["cat"]}</span><span>{p["read"]}</span><span>{p["date"]}</span></div>
  <h2>{e(p["title"])}</h2><p>{e(p["dek"])}</p><span class="more">Read article →</span></a>''' for p in POSTS)
PAGES.append(render("blog", "Auto Styling Blog | PPF, Ceramic Coating & Window Tint Tips | SBN Auto Styling Philadelphia",
                    "Expert advice on paint protection film, ceramic coatings, and window tinting for Philadelphia car owners. Tips, guides, and honest answers from SBN Auto Styling.",
                    f'''<div class="local"><div class="narrow">
  <div class="kicker">From the Shop</div>
  <h1 class="h-display">Auto Styling<br/><span class="blue">Knowledge Base</span></h1>
  <p class="intro">Honest guides on PPF, ceramic coating, and window tinting — written for Philadelphia car owners by the team at SBN.</p>
  <div class="blog-list">{cards}</div>
</div></div>''', simple_header(), SLIM_FOOTER))

for p in POSTS:
    parts = []
    for kind, v in p["body"]:
        if kind == "p": parts.append(f"<p>{v}</p>")
        elif kind == "h": parts.append(f"<h2>{e(v)}</h2>")
        else: parts.append("<ul>" + "".join(f"<li><span>{i}</span></li>" for i in v) + "</ul>")
    text, label, target = p["cta"]
    btn = (f'<button class="btn btn-primary btn-md" data-book="{target[5:]}">{label}</button>' if target.startswith("book:")
           else f'<a class="btn btn-primary btn-md" href="{target}">{label}</a>')
    body = f'''<article class="article"><div class="narrow" style="max-width:44rem">
  <div class="meta"><span class="{cat_cls(p["cat"])}">{p["cat"]}</span><span>{p["read"]}</span><span>{p["date"]}</span></div>
  <h1>{e(p["title"])}</h1>
  <p class="dek">{e(p["dek"])}</p>
  <div class="prose">{"".join(parts)}</div>
  <div class="post-cta"><p>{e(text)}</p>{btn}</div>
  <div class="byline"><div>Written by<b>SBN Auto Styling Team</b>Philadelphia, PA · 267 263 7342</div><a class="back-link" href="{{R}}blog/">← More articles</a></div>
</div></article>'''
    PAGES.append(render(f"blog/{p['slug']}", f"{p['title']} | SBN Auto Styling", p["dek"], body,
                        simple_header("← All articles", "{R}blog/"), SLIM_FOOTER))


# ================================================================ LEGAL
def legal(path, title, desc, h1, alert, sections, other_label, other_href):
    out = []
    for h, items in sections:
        out.append(f"<h2>{h}</h2>")
        for it in items:
            out.append("<ul>" + "".join(f"<li><span>{x}</span></li>" for x in it) + "</ul>" if isinstance(it, list) else f"<p>{it}</p>")
    contact = '''<div class="contact-box"><b>SBN Auto Styling</b><br/>100 Red Lion Road, Unit 3<br/>Philadelphia, PA 19115<br/>Phone: <a href="tel:+12672637342">267 263 7342</a><br/>Email: <a href="mailto:hello@sbnautostyling.com">hello@sbnautostyling.com</a></div>'''
    body = f'''<div class="article legal-page"><div class="narrow" style="max-width:46rem">
  <div class="kicker">Legal</div>
  <h1 class="h-display">{h1}</h1>
  <p class="eff">Effective June 11, 2026</p>
  <div class="alert"><span class="i">!</span><div><b>ALL DEPOSITS ARE NON-REFUNDABLE.</b> {alert}</div></div>
  <div class="prose">{"".join(out)}{contact}</div>
  <div class="legal-foot"><a href="{{R}}{other_href}">{other_label}</a><a href="{{ROOT}}" style="color:var(--muted-fg)">← Back to Home</a></div>
</div></div>'''
    PAGES.append(render(path, title, desc, body, simple_header(), SLIM_FOOTER))


MAIL = '<a href="mailto:hello@sbnautostyling.com">hello@sbnautostyling.com</a>'
PHONE = '<a href="tel:+12672637342">267 263 7342</a>'
legal("privacy-policy", "Privacy Policy | SBN Auto Styling",
      "How SBN Auto Styling collects, uses, and protects information from visitors and customers on sbn-autostyling.com.",
      "Privacy Policy",
      "Any deposit paid to reserve an installation slot or secure materials will not be refunded for any reason, including cancellations, reschedules, or no-shows.", [
    ("1. Who We Are", [f'This Privacy Policy describes how <b>SBN Auto Styling</b> (“SBN”, “we”, “us”, or “our”) collects, uses, and shares information about you when you visit <a href="{DOMAIN}">sbn-autostyling.com</a> (the “Site”), contact us, or schedule services with us in Philadelphia, PA.',
                       f"Our shop is located at 100 Red Lion Road, Unit 3, Philadelphia, PA 19115. You can reach us at {PHONE} or {MAIL}."]),
    ("2. Information We Collect", ["We collect the following categories of information:", [
        "<b>Information you provide directly</b> — including your first and last name, phone number, email address, vehicle details (make, model, year), service preferences (PPF, ceramic coating, window tint, detailing, wraps), and any message or photos you submit through our quote forms, booking widgets, or live chat.",
        "<b>Booking &amp; communications data</b> — when you schedule an appointment through our embedded booking widgets, call, text, or chat with us, we receive your contact details and the content of your communication.",
        "<b>Automatically collected data</b> — IP address, browser type, device type (mobile/desktop), pages visited, the referring URL, approximate location, and a per-session identifier we store in your browser to understand traffic and improve the Site.",
        "<b>Cookies &amp; similar technologies</b> — first-party storage to keep your session alive and limited third-party scripts (described below) that may set their own cookies."]]),
    ("3. How We Use Your Information", ["We use the information we collect to:", [
        "Respond to your quote requests, calls, texts, chats, and bookings.",
        "Schedule, perform, and follow up on the services you requested (PPF, ceramic coating, window tinting, detailing, wraps, etc.).",
        "Send appointment reminders, status updates, and post-service follow-ups by phone, SMS, or email.",
        "Operate, secure, and improve the Site, including measuring traffic and fixing bugs.",
        "Comply with our legal obligations and enforce our Terms of Service."],
        "We do <b>not</b> sell your personal information, and we do not share it with third parties for their own marketing."]),
    ("4. Service Providers We Share Data With", ["We rely on a small number of trusted vendors to operate the Site and our business. These providers only receive the information they need to perform their service:", [
        "<b>LeadConnector / GoHighLevel</b> — powers our contact storage, booking widgets, and live chat widget on the Site.",
        "<b>Hosting &amp; database providers</b> — host the Site and securely store leads submitted through our forms.",
        "<b>Telephony &amp; messaging providers</b> — deliver SMS, calls, and email communications you initiate or that we send in response to your request."],
        "We may also disclose information if required by law, subpoena, or valid legal process, or to protect the rights, property, or safety of SBN Auto Styling, our customers, or others."]),
    ("5. SMS &amp; Phone Communications", [f"When you give us your phone number through a form, call, text, or chat, you agree that we may contact you at that number about your quote, appointment, or service. Message frequency varies. Message and data rates may apply. You can opt out of SMS at any time by replying <b>STOP</b>, reply <b>HELP</b> for help, or stop other communications by emailing us at {MAIL}.",
                                          "<b>No mobile information will be shared with third parties or affiliates for marketing or promotional purposes.</b> All of the categories of information described in this policy exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties. SMS opt-in consent is never sold, rented, or shared with anyone for any purpose other than delivering the messages you requested."]),
    ("6. Data Retention", ["We retain lead and customer information for as long as needed to provide our services, maintain business records, and comply with our legal obligations. You may request deletion of your information at any time (see “Your Rights” below)."]),
    ("7. Your Rights", [f"Depending on where you live, you may have the right to access, correct, delete, or restrict our use of your personal information, and to opt out of certain processing. To exercise any of these rights, email us at {MAIL} or call {PHONE}. We will respond within a reasonable timeframe and as required by applicable law."]),
    ("8. Children's Privacy", ["Our Site and services are intended for adults aged 18 and over. We do not knowingly collect personal information from children under 13. If you believe a child has provided us with personal information, please contact us and we will delete it."]),
    ("9. Security", ["We use reasonable administrative, technical, and physical safeguards designed to protect the information we collect. No method of transmission over the internet is 100% secure, so we cannot guarantee absolute security."]),
    ("10. Third-Party Links", ["The Site may contain links to third-party websites, including our social profiles on Instagram and Facebook. We are not responsible for the privacy practices of those sites; please review their policies before sharing your information."]),
    ("11. Changes to This Policy", ["We may update this Privacy Policy from time to time. When we do, we will revise the “Effective” date at the top of the page. Material changes will be communicated through the Site or by other reasonable means."]),
    ("12. Deposits (Non-Refundable)", ['<b>All deposits are non-refundable.</b> Any deposit collected to reserve an installation slot or secure materials will not be refunded for any reason, including cancellations, reschedules, or no-shows. Full payment and deposit terms are described in our <a href="{R}terms-of-service/">Terms of Service</a>.']),
    ("13. Contact Us", ["Questions about this Privacy Policy? Reach out:"]),
], "Read our Terms of Service →", "terms-of-service/")

legal("terms-of-service", "Terms of Service | SBN Auto Styling",
      "The terms and conditions that govern your use of sbn-autostyling.com and the services provided by SBN Auto Styling in Philadelphia, PA.",
      "Terms of Service",
      "Any deposit paid to reserve an installation slot or secure materials will not be refunded for any reason, including cancellations, reschedules, or no-shows. See Section 4 below for full details.", [
    ("1. Agreement", [f'These Terms of Service (the “Terms”) govern your access to and use of <a href="{DOMAIN}">sbn-autostyling.com</a> (the “Site”) and any related services, bookings, or communications offered by SBN Auto Styling (“SBN”, “we”, “us”, or “our”). By using the Site or scheduling work with us, you agree to these Terms. If you do not agree, please do not use the Site or our services.']),
    ("2. Eligibility", ["You must be at least 18 years old and legally able to enter into a binding contract to use the Site, submit a request, or schedule services. By using the Site you represent that you meet these requirements."]),
    ("3. Quotes, Estimates &amp; Bookings", [[
        "Online prices and package details are starting points only. Final pricing depends on your vehicle's make, model, size, condition, prep work required, and the specific film, coating, or tint chosen.",
        "PPF (paint protection film) is quoted in-person only. A free in-person estimate is required to confirm pricing.",
        "Appointments scheduled through our booking widgets are confirmed once we contact you to verify vehicle details and prep requirements.",
        "We reserve the right to refuse, reschedule, or modify service for any reason, including vehicle condition, safety, or scheduling capacity."]]),
    ("4. Payments, Deposits &amp; Cancellations", ["<b>ALL DEPOSITS ARE NON-REFUNDABLE.</b> Once a deposit is paid, it will not be refunded for any reason.", [
        "<b>All deposits are non-refundable.</b> A deposit may be required to reserve installation slots or secure materials for ceramic coating, tint, PPF, wraps, or detailing. Once paid, a deposit will not be refunded under any circumstances, including cancellations, reschedules, or no-shows.",
        "Final payment is due upon completion of work unless otherwise agreed in writing.",
        "We accept the payment methods displayed at our shop. Returned payments or chargebacks may incur additional fees.",
        "Cancellations or reschedules must be made at least 48 hours before your appointment. Late cancellations or no-shows forfeit the non-refundable deposit and may be subject to a rescheduling fee."]]),
    ("5. Customer Responsibilities", [[
        "Provide accurate vehicle information and disclose any prior repairs, repaint, body filler, rust, or aftermarket modifications that may affect installation.",
        "Remove personal belongings before drop-off. SBN is not responsible for items left in the vehicle.",
        "Ensure the vehicle has sufficient fuel and is in safe, drivable condition.",
        "Follow our post-install care instructions (e.g., curing time for ceramic coating, no car washes for window tint, etc.). Failure to follow care instructions may void coverage."]]),
    ("6. Workmanship &amp; Warranty", ["We stand behind the quality of our work. Specific warranties (for example, the multi-year ceramic coating warranty or the lifetime tint warranty) are described on the relevant service page or in your service receipt. Warranty terms cover defects in workmanship and product performance only; they do not cover:", [
        "Damage from accidents, collisions, abrasive washing, or improper care.",
        "Pre-existing paint defects, rust, chips, scratches, or contaminated paint identified before or during prep.",
        "Acts of nature, vandalism, road debris, chemical exposure outside normal driving conditions, or modifications made by third parties.",
        "Vehicles that have been repainted, polished, or modified by another shop after our service."],
        "Warranty claims must be brought to our shop for inspection. Our remedy at our sole discretion is repair or re-installation of the affected area."]),
    ("7. Vehicle Drop-Off &amp; Storage", ["Vehicles left at our shop are stored at the customer's own risk. While we take reasonable measures to secure customer vehicles, SBN is not liable for theft, vandalism, weather damage, or other loss occurring while your vehicle is on our property. We recommend you maintain comprehensive insurance on your vehicle at all times."]),
    ("8. Acceptable Use of the Site", ["You agree not to:", [
        "Use the Site for any unlawful purpose or in violation of any applicable laws or regulations.",
        "Attempt to interfere with, disrupt, or gain unauthorized access to the Site, its servers, or related systems.",
        "Submit false, misleading, or fraudulent information through any form, booking, or chat.",
        "Scrape, copy, frame, or reproduce content from the Site without our prior written permission."]]),
    ("9. Intellectual Property", ["All content on the Site — including text, photos, logos, video, graphics, and the SBN Auto Styling name and marks — is owned by or licensed to SBN Auto Styling and is protected by copyright, trademark, and other intellectual property laws. You may not use our content without our prior written permission, except for your own personal, non-commercial reference."]),
    ("10. Photos &amp; Marketing", ["We may photograph vehicles before, during, and after service for quality control and marketing purposes (social media, our website, advertising). If you do not want your vehicle featured in marketing materials, let us know in writing before your appointment and we will respect your request."]),
    ("11. Disclaimers", ["The Site and our services are provided on an “as is” and “as available” basis. To the maximum extent permitted by law, we disclaim all warranties, express or implied, including implied warranties of merchantability, fitness for a particular purpose, and non-infringement, except for any express written warranty we provide with a specific service."]),
    ("12. Limitation of Liability", ["To the maximum extent permitted by law, SBN Auto Styling and its owners, employees, and contractors will not be liable for any indirect, incidental, special, consequential, or punitive damages arising out of or in connection with your use of the Site or our services. Our total liability for any claim relating to a service is limited to the amount you paid us for that specific service."]),
    ("13. Indemnification", ["You agree to indemnify and hold harmless SBN Auto Styling and its personnel from any claims, damages, losses, or expenses (including reasonable attorneys' fees) arising out of your breach of these Terms, your misuse of the Site, or your violation of any third-party rights."]),
    ("14. Governing Law &amp; Disputes", ["These Terms are governed by the laws of the Commonwealth of Pennsylvania, without regard to its conflict-of-law principles. Any dispute that cannot be resolved informally will be brought exclusively in the state or federal courts located in Philadelphia, Pennsylvania, and you consent to their personal jurisdiction."]),
    ("15. Changes to These Terms", ["We may update these Terms from time to time. When we do, we will update the “Effective” date at the top of the page. Your continued use of the Site or our services after a change takes effect constitutes acceptance of the revised Terms."]),
    ("16. SMS / Text Messaging Program", ["By providing your mobile number to SBN Auto Styling — through a form, our booking widgets, live chat, a phone call, or a text — you consent to receive SMS text messages from us. Consent to receive marketing text messages is not a condition of purchasing any product or service.", [
        "<b>Program description &amp; use cases:</b> We send text messages related to appointment scheduling and reminders, quote and estimate follow-ups, service and status updates, responses to your inquiries, and occasional promotions or offers.",
        "<b>Message frequency:</b> Message frequency varies based on your interactions with us.",
        "<b>Message &amp; data rates:</b> Message and data rates may apply. Charges are billed by and payable to your mobile service provider.",
        "<b>How to opt out:</b> Reply <b>STOP</b> to any message to unsubscribe at any time. After you send STOP, we will send one final message confirming you have been opted out.",
        f"<b>How to get help:</b> Reply <b>HELP</b> for assistance, or contact us at {PHONE} or {MAIL}.",
        "<b>Carrier liability:</b> Wireless carriers (such as AT&amp;T, T-Mobile, Verizon, and others) are not liable for delayed or undelivered messages.",
        '<b>Privacy:</b> Mobile opt-in information and consent are never shared with third parties or affiliates for marketing purposes. See our <a href="{R}privacy-policy/">Privacy Policy</a> for details.']]),
    ("17. Contact Us", ["Questions about these Terms? Get in touch:"]),
], "Read our Privacy Policy →", "privacy-policy/")

# ================================================================ 404 + sitemap + robots
render("404", "Page Not Found | SBN Auto Styling", "This page could not be found.",
       '<div class="notfound"><div><h1 class="h-display blue">404</h1><p class="lead" style="margin:1rem auto 2rem">This page could not be found.</p><a class="btn btn-primary btn-md" href="/">Back to Home</a></div></div>',
       simple_header(), SLIM_FOOTER)
# Most hosts look for /404.html at the root
os.replace(os.path.join(OUT, "404", "index.html"), os.path.join(OUT, "404.html")); os.rmdir(os.path.join(OUT, "404"))
open(os.path.join(OUT, "404.html"), "w").write(open(os.path.join(OUT, "404.html")).read().replace('href="../', 'href="/').replace('src="../', 'src="/'))

urls = "".join(f"  <url><loc>{DOMAIN}/{p}</loc></url>\n" if p else f"  <url><loc>{DOMAIN}</loc></url>\n" for p in PAGES)
open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
print(len(PAGES), "pages:", *PAGES, sep="\n  ")
