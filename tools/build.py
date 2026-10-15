import sys, json
out = sys.argv[1]
SITE = "https://www.koldaltax.com"
# Add your business phone here (e.g. "(954) 555-0123") to show call buttons across the site.
PHONE = ""
CITIES = ["Coral Springs", "Margate", "Parkland", "Coconut Creek", "Tamarac", "Pompano Beach"]
NAV = [("/bookkeeping/", "Bookkeeping"), ("/tax/", "Tax"), ("/advisory/", "Planning"), ("/services/irs-notice-help/", "IRS Help"), ("/about/", "About")]
SCHEMA = {"@context": "https://schema.org", "@type": "AccountingService", "name": "Koldal Tax & Advisory",
          "url": SITE, "email": "alek@koldaltax.com", "founder": {"@type": "Person", "name": "Alek Koldal, EA"},
          "address": {"@type": "PostalAddress", "addressLocality": "Coral Springs", "addressRegion": "FL", "addressCountry": "US"},
          "areaServed": [{"@type": "City", "name": c + ", FL"} for c in CITIES]}
if PHONE: SCHEMA["telephone"] = PHONE
TEL = "tel:" + "".join(ch for ch in PHONE if ch.isdigit() or ch == "+")

def page(path, title, desc, body):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a>' for h, t in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Koldal Tax &amp; Advisory">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,300;6..72,400&family=Hanken+Grotesk:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{json.dumps(SCHEMA)}</script>
</head>
<body>
<header><div class="wrap"><a class="brand" href="/"><b>Koldal</b><small>Tax &amp; Advisory</small></a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button><nav id="site-nav">{nav}{f'<a class="btn ghost" href="{TEL}">Call {PHONE}</a>' if PHONE else ""}<a class="btn" href="/contact/">Contact</a></nav></div><script>{{const b=document.querySelector(".menu-btn"),h=b.closest("header");b.addEventListener("click",()=>{{const o=h.classList.toggle("open");b.setAttribute("aria-expanded",o);b.textContent=o?"Close":"Menu"}})}}</script></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div><a class="brand" href="/"><b>Koldal</b><small>Tax &amp; Advisory</small></a><p class="small">Alek Koldal, EA<br>Coral Springs, Florida<br>{f'<a href="{TEL}">{PHONE}</a><br>' if PHONE else ""}<a href="mailto:alek@koldaltax.com">alek@koldaltax.com</a></p></div>
<div><strong>Services</strong><a href="/bookkeeping/">Bookkeeping</a><a href="/tax/">Tax preparation</a><a href="/advisory/">Tax planning</a><a href="/services/irs-notice-help/">IRS help</a><a href="/pricing/">Pricing</a></div>
<div><strong>Resources</strong><a href="/irs-notices/">IRS notice lookup</a><a href="/quickbooks-help/">QuickBooks help</a><a href="/about/">About</a><a href="/contact/">Contact</a></div>
<div><strong>Connect</strong><a href="https://g.page/r/CTKng70qwgj_EBM/review" rel="noopener">Google reviews</a><a href="https://www.linkedin.com/in/aleksander-koldal" rel="noopener">LinkedIn</a><a href="https://members.csccrchamber.com/list/member/koldal-tax-advisory-margate-7305" rel="noopener">Chamber of Commerce</a></div>
<p class="legal">&copy; 2026 Koldal Tax &amp; Advisory · Serving {", ".join(CITIES[:-1])} and {CITIES[-1]}</p>
</div></footer>
{f'<a class="callbar" href="{TEL}">Call {PHONE}</a>' if PHONE else ""}
<script src="/assets/config.js"></script><script src="/assets/forms.js"></script>
</body>
</html>
"""

def quick_form(topic, heading, blurb):
    t = topic.replace('"', "&quot;")
    return f"""<div class="card quick" style="margin-top:30px"><h3>{heading}</h3><p>{blurb}</p>
<form data-kind="contact" style="margin-top:14px"><input type="hidden" name="service" value="{t}">
<div class="row"><label>First name<input name="first_name" required autocomplete="given-name"></label><label>Last name<input name="last_name" required autocomplete="family-name"></label></div>
<div class="row"><label>Email<input type="email" name="email" required autocomplete="email"></label><label>Phone<input type="tel" name="phone" autocomplete="tel"></label></div>
<label>Anything I should know? (optional)<textarea name="message" style="min-height:80px"></textarea></label>
<label class="hp">Leave empty<input name="website" tabindex="-1" autocomplete="off"></label>
<button class="btn" type="submit">Request help</button><div class="msg" role="status"></div></form>
{f'<p class="small" style="margin-top:12px">Or call <a href="{TEL}">{PHONE}</a>.</p>' if PHONE else ""}</div>"""

CTA = """<section><div class="wrap"><div class="cta"><div><h2>Let&#39;s talk about what you need.</h2><p>The first consultation is free.</p></div><a class="btn" href="/contact/">Book a consultation</a></div></div></section>"""

EA_BADGE = '<span class="ea">EA</span>'

# Monthly bookkeeping starts at $300. Higher tiers are quoted after the free review.
PLANS = [
 ("Essentials", "From $300<span>/month</span>", "For a newer or simpler business.", "Up to 2 bank or card accounts, roughly 100 transactions a month",
  ["Monthly bank and credit card reconciliations", "Every transaction categorized", "Monthly profit &amp; loss and balance sheet", "Email support during the year", "Books ready for your tax return"]),
 ("Growth", "Custom quote", "For an established business with more moving parts.", "Up to 5 accounts, roughly 300 transactions a month",
  ["Everything in Essentials", "Loan and merchant account reconciliations", "Customer invoices and unpaid bills tracked", "Quarterly review call", "Quarterly estimated tax payments calculated"]),
 ("Advisory", "Custom quote", "For owners who want a numbers partner, not just clean books.", "Larger volume, quoted after your review",
  ["Everything in Growth", "Monthly review call", "Cash-flow forecast", "Year-end review of your numbers"]),
]
ADDONS = [
 ("QuickBooks setup &amp; cleanup (one time)", "$800 to $2,500", "/services/quickbooks-cleanup/"),
 ("Payroll setup &amp; review with Gusto", "Monthly add-on", "/services/payroll-with-gusto/"),
 ("1099 preparation &amp; filing", "Per form, each January", "/quickbooks-help/1099-contractors/"),
]

TAX_SERVICES = [
 ("Individual tax returns (1040)", "Federal and state returns for individuals, families and business owners.", "From $650"),
 ("Business tax returns", "Schedule C, partnerships (1065) and S corporations (1120-S), prepared from your books.", "Quoted"),
 ("Tax planning &amp; projections", "Year-end planning and quarterly estimated payments, so April has no surprises.", "Quoted"),
 ("Unfiled &amp; prior-year returns", "Behind on filing? I&#39;ll get missing years filed and you back in good standing.", "Quoted"),
 ("IRS notices &amp; representation", "CP2000s, balance-due notices, payment plans and audits by mail, answered for you.", "Quoted"),
 ("IRS transcript review", "Your wage &amp; income and account transcripts pulled and explained: what the IRS has on file, what you owe and what&#39;s missing.", "Quoted"),
 ("Penalty relief", "First-time abatement and reasonable-cause requests. Free penalty review.", "Small upfront fee plus a percentage of penalties removed"),
]
TAX_LINKS = {"IRS transcript review": "/services/irs-notice-help/#irs", "IRS notices &amp; representation": "/services/irs-notice-help/", "Penalty relief": "/services/irs-notice-help/#penalty"}

def tax_cards(prices=True):
    h = ""
    for n, d, pr in TAX_SERVICES:
        u = TAX_LINKS.get(n)
        tag, end = (f'<a class="card notice" href="{u}">', "</a>") if u else ('<div class="card">', "</div>")
        price = f'<p class="small" style="margin-top:10px"><strong>{pr}</strong></p>' if prices else ""
        h += f'{tag}<h3>{n}{" &rarr;" if u else ""}</h3><p>{d}</p>{price}{end}'
    return f'<div class="grid">{h}</div>'

def tax_rows():
    rows = "".join(f"<tr><td>{n}</td><td>{pr}</td></tr>" for n, _, pr in TAX_SERVICES)
    return f'<div class="tablewrap"><table class="addons"><thead><tr><th>Tax service</th><th>Pricing</th></tr></thead><tbody>{rows}</tbody></table></div>'

def plan_cards(full=True):
    h = ""
    for i, (name, price, who, size, items) in enumerate(PLANS):
        ul = "".join(f"<li>{x}</li>" for x in (items if full else items[:3]))
        pop = ''
        h += f'''<div class="card plan{' featured' if i == 1 else ''}">{pop}<h3>{name}</h3>
<p class="price">{price}</p><p>{who}</p><p class="small">{size}</p><ul class="checks">{ul}</ul>
<a class="btn{'' if i == 1 else ' ghost'}" href="/contact/">Start with a free review</a></div>'''
    return f'<div class="plans">{h}</div>'

def addon_rows():
    rows = ""
    for n, p, u in ADDONS:
        cell = f'<a href="{u}">{n}</a>' if u else n
        rows += f"<tr><td>{cell}</td><td>{p}</td></tr>"
    return f'<div class="tablewrap"><table class="addons"><thead><tr><th>Add-on</th><th>Pricing</th></tr></thead><tbody>{rows}</tbody></table></div>'

STEPS = """<ol class="steps">
<li><h3>Free QuickBooks review</h3><p>Give me view access to your QuickBooks Online file. I&#39;ll tell you what&#39;s right, what&#39;s off, and which plan fits.</p></li>
<li><h3>Catch up, if needed</h3><p>If you&#39;re behind, I clean up and reconcile the past months first, for a quoted price.</p></li>
<li><h3>Monthly bookkeeping</h3><p>Every month your accounts are reconciled and your reports land in your inbox. At tax time, your Enrolled Agent already knows your numbers.</p></li></ol>"""

EA_SECTION = """<section class="band-dark"><div class="wrap split"><div><p class="eyebrow">Enrolled Agent</p><h2>Your bookkeeper is also a federally licensed tax professional</h2>
<p>Enrolled Agents are licensed by the U.S. Department of the Treasury and have unlimited rights to represent taxpayers before the IRS, for any tax matter, in all 50 states. It&#39;s the highest credential the IRS awards.</p>
<p>That means your books are kept with your tax return in mind, and if the IRS ever sends a letter, the person who knows your numbers is the one who can answer it.</p>
<p><a class="btn light" href="/tax/">Tax &amp; IRS services</a></p></div>
<ul class="ea-list"><li><strong>Business tax returns</strong><span>Schedule C, partnerships and S corporations, prepared from books I keep.</span></li>
<li><strong>Individual returns</strong><span>Federal and state returns for owners and families.</span></li>
<li><strong>Tax planning</strong><span>Quarterly estimates and year-end planning, so April has no surprises.</span></li>
<li><strong>IRS representation</strong><span>Notices, payment plans and penalty relief, handled for you.</span></li></ul></div></section>"""

REVIEW_FORM = """<form data-kind="contact" class="card"><input type="hidden" name="service" value="Free QuickBooks review">
<div class="row"><label>First name<input id="f-first" name="first_name" required autocomplete="given-name"></label><label>Last name<input id="f-last" name="last_name" required autocomplete="family-name"></label></div>
<div class="row"><label>Email<input id="f-email" type="email" name="email" required autocomplete="email"></label><label>Phone<input id="f-phone" type="tel" name="phone" autocomplete="tel"></label></div>
<div class="row"><label>Business name<input id="f-biz" name="x_business" autocomplete="organization"></label><label>Type of business<input id="f-type" name="x_type" placeholder="e.g. contractor, salon"></label></div>
<div class="row"><label>Are your books up to date<select id="f-current" name="x_current"><option>Yes, mostly</option><option>A few months behind</option><option>More than a year behind</option><option>Not sure</option></select></label>
<label>Using QuickBooks Online<select id="f-qbo" name="x_qbo"><option>Yes</option><option>QuickBooks Desktop</option><option>Another program</option><option>Spreadsheets or nothing yet</option></select></label></div>
<label>What do you need help with<select id="f-need" name="x_need"><option>Monthly bookkeeping</option><option>Cleanup &amp; catch-up</option><option>Payroll with Gusto</option><option>Tax return</option><option>IRS notice or penalty</option><option>Something else</option></select></label>
<label>Anything else? (optional)<textarea id="f-msg" name="message" style="min-height:90px"></textarea></label>
<label class="hp">Leave empty<input name="website" tabindex="-1" autocomplete="off"></label>
<button class="btn" type="submit">Request my free review</button><div class="msg" role="status"></div></form>"""

PILLARS = [
 ("Bookkeeping", "Monthly QuickBooks Online bookkeeping", "Reconciled accounts and clear monthly reports, plus cleanup, catch-up and Gusto payroll.", "From $300/month", "/bookkeeping/"),
 ("Tax preparation", "Individual &amp; business returns", "Returns for individuals, sole proprietors, partnerships and S corporations, including prior years.", "1040s from $650", "/tax/"),
 ("Tax planning", "Planning &amp; advisory", "Year-end planning, quarterly estimates, business structure and a monthly review of your numbers.", "Quoted for your situation", "/advisory/"),
 ("IRS help", "Notices &amp; representation", "IRS letters, payment plans, audits by mail and penalty relief, handled by your Enrolled Agent.", "Free notice review", "/services/irs-notice-help/"),
]
PORTRAIT = """<figure class="portrait"><div class="portrait-frame"><img src="/assets/headshot.jpg" alt="Alek Koldal, EA" width="420" height="520" onerror="this.remove()"><span class="portrait-ph" aria-hidden="true">AK</span></div>
<figcaption><strong>Alek Koldal, EA</strong><span>IRS Enrolled Agent · Founder</span></figcaption></figure>"""
CONTACT_FORM = REVIEW_FORM.replace('''<div class="row"><label>Are your books up to date<select id="f-current" name="x_current"><option>Yes, mostly</option><option>A few months behind</option><option>More than a year behind</option><option>Not sure</option></select></label>
<label>Using QuickBooks Online<select id="f-qbo" name="x_qbo"><option>Yes</option><option>QuickBooks Desktop</option><option>Another program</option><option>Spreadsheets or nothing yet</option></select></label></div>
''', '').replace('value="Free QuickBooks review"', 'value="Consultation request"').replace('<option>Monthly bookkeeping</option><option>Cleanup &amp; catch-up</option><option>Payroll with Gusto</option><option>Tax return</option><option>IRS notice or penalty</option><option>Something else</option>', '<option>Bookkeeping</option><option>Tax return</option><option>Tax planning &amp; advisory</option><option>IRS notice or penalty</option><option>Payroll with Gusto</option><option>Something else</option>').replace('Request my free review', 'Request a consultation').replace('<label>Business name<input id="f-biz" name="x_business" autocomplete="organization"></label><label>Type of business<input id="f-type" name="x_type" placeholder="e.g. contractor, salon"></label>', '<label>Business name (if any)<input id="f-biz" name="x_business" autocomplete="organization"></label><label>Type of business<input id="f-type" name="x_type" placeholder="e.g. contractor, salon"></label>')
SERVICES = [
 ("Individual Tax Returns", "Federal and state tax preparation and filing for individuals and families.", []),
 ("Business Tax Returns", "Tax preparation for sole proprietors, partnerships, and S corporations.", []),
 ("Tax Planning & Projections", "Proactive planning to help reduce surprises and make informed financial decisions.", []),
 ("Monthly Bookkeeping", "Reliable, organized bookkeeping to help you understand your business, stay tax-ready, and make better decisions throughout the year.",
  ["Bank and credit card reconciliations", "Income and expense categorization", "Monthly profit and loss reports", "QuickBooks Online support", "Loan account reconciliations", "Help with business questions throughout the year", "Coordination with your tax preparation"]),
 ("QuickBooks Cleanup & Catch-Up", "Behind on your bookkeeping? I'll organize past transactions, reconcile accounts, and bring your QuickBooks file up to date.", []),
 ("IRS Help", "Questions about an IRS notice or letter? As an Enrolled Agent I can help you understand it and respond.", []),
]
def cards(items):
    h = ""
    for t, d, li in items:
        t = t.replace("&", "&amp;")
        ul = ("<ul>" + "".join(f"<li>{x}</li>" for x in li) + "</ul>") if li else ""
        h += f'<div class="card"><h3>{t}</h3><p>{d}</p>{ul}</div>'
    return h

pages = {
"index.html": page("/", "Bookkeeping, Tax &amp; IRS Help in Coral Springs, FL | Koldal Tax &amp; Advisory",
 "Bookkeeping, tax preparation, tax planning and IRS representation for small businesses and individuals, from Alek Koldal, EA, an IRS Enrolled Agent in Coral Springs, FL.",
 f"""<div class="hero"><div class="wrap hero-grid"><div>
<p class="eyebrow">Enrolled Agent · Coral Springs, FL</p>
<h1>Clear books. Confident taxes.</h1>
<p>Bookkeeping, tax preparation, planning and IRS help for small businesses and individuals, from one Enrolled Agent.</p>
<div class="actions"><a class="btn" href="/contact/">Book a consultation</a><a class="textlink" href="#services">Our services</a></div></div>
{PORTRAIT}</div></div>
<div class="trust"><div class="wrap"><ul><li>IRS Enrolled Agent</li><li>5.0 on Google</li><li>QuickBooks Online</li><li>Chamber of Commerce member</li></ul></div></div>
<section id="services"><div class="wrap"><p class="eyebrow">Services</p><h2>Everything in one place</h2>
<div class="pillars">{"".join(f'<a class="pillar" href="{u}"><span class="pillar-k">{k}</span><h3>{t}</h3><p>{d}</p><span class="pillar-f">{f}</span></a>' for k, t, d, f, u in PILLARS)}</div></div></section>
<section class="band-dark"><div class="wrap split"><div><p class="eyebrow">Why an Enrolled Agent</p>
<p class="statement">The highest credential the IRS awards, working on your books all year.</p></div>
<ul class="ea-list"><li><strong>Federally licensed</strong><span>Licensed by the U.S. Treasury to represent taxpayers before the IRS, in every state.</span></li>
<li><strong>One point of contact</strong><span>The person who keeps your books prepares your return and answers the IRS.</span></li>
<li><strong>Local</strong><span>Based in Coral Springs, serving South Florida in person or remotely.</span></li></ul></div></section>
<section><div class="wrap"><p class="eyebrow">How it works</p><h2>Simple from the first call</h2>
<ol class="steps"><li><h3>Consultation</h3><p>Tell me what you need. It&#39;s free.</p></li>
<li><h3>Clear quote</h3><p>A plan and a price before any work starts.</p></li>
<li><h3>Ongoing support</h3><p>Books, returns and planning handled all year.</p></li></ol></div></section>
{CTA}"""),
"bookkeeping/index.html": page("/bookkeeping/", "QuickBooks Online Bookkeeping in Coral Springs, FL | Koldal Tax &amp; Advisory",
 "Monthly QuickBooks Online bookkeeping, cleanup and catch-up, and payroll with Gusto for small businesses in Coral Springs and South Florida. From $300 a month.",
 f"""<div class="hero"><div class="wrap"><p class="eyebrow">Bookkeeping</p><h1>Monthly QuickBooks Online bookkeeping</h1>
<p>Accounts reconciled every month, reports you can trust, and books that are ready for your tax return. From $300 a month.</p>
<div class="actions"><a class="btn" href="/contact/">Book a free consultation</a><a class="btn ghost" href="/pricing/">See plans &amp; pricing</a></div></div></div>
<section><div class="wrap"><h2>How it works</h2>{STEPS}</div></section>
<section style="background:var(--soft)"><div class="wrap"><h2>Plans</h2><p class="lede">Your exact price is set after a free review of your books, so there are no surprise bills.</p>{plan_cards(full=False)}
<p style="margin-top:18px"><a href="/pricing/">Compare plans and add-ons &rarr;</a></p></div></section>
<section><div class="wrap split"><div><h2>For any small business</h2>
<p>Whatever your business does, if it runs on QuickBooks Online I can keep its books: contractors and trades, real estate agents, salons, cleaning and landscaping companies, restaurants, online sellers, professional services and more.</p></div>
<div class="linklist"><a href="/services/quickbooks-cleanup/"><strong>Setup &amp; cleanup</strong><span>A one-time start: prior months cleaned up and your books tied to your tax return</span></a><a href="/services/payroll-with-gusto/"><strong>Payroll with Gusto</strong><span>Setup, QuickBooks connection and a review of every payroll</span></a><a href="/quickbooks-help/1099-contractors/"><strong>1099 preparation</strong><span>1099-NECs for your contractors, filed each January</span></a></div></div></section>
{CTA}"""),
"tax/index.html": page("/tax/", "Tax Preparation by an Enrolled Agent in Coral Springs, FL | Koldal Tax &amp; Advisory",
 "Individual and business tax return preparation from Alek Koldal, EA, an IRS Enrolled Agent in Coral Springs, FL. Individual returns from $650.",
 f"""<div class="hero"><div class="wrap"><p class="eyebrow">{EA_BADGE} Tax preparation</p><h1>Tax returns prepared by an Enrolled Agent</h1>
<p>Individual and business returns prepared by a federally licensed tax professional. For bookkeeping clients, your return comes straight from books I already keep.</p>
<div class="actions"><a class="btn" href="/contact/">Book a free consultation</a><a class="btn ghost" href="/pricing/#tax-pricing">See tax pricing</a></div></div></div>
<section><div class="wrap"><div class="grid">
<div class="card"><h3>Individual returns (1040)</h3><p>Federal and state returns for individuals, families and business owners, including self-employment, rental and investment income.</p><p class="small" style="margin-top:10px"><strong>From $650</strong></p></div>
<div class="card"><h3>Business returns</h3><p>Sole proprietors (Schedule C), partnerships (1065) and S corporations (1120-S).</p><p class="small" style="margin-top:10px"><strong>Quoted</strong></p></div>
<div class="card"><h3>Unfiled &amp; prior-year returns</h3><p>Behind on filing? I&#39;ll get missing years filed and you back in good standing with the IRS.</p><p class="small" style="margin-top:10px"><strong>Quoted</strong></p></div></div>
<p class="small" style="margin-top:22px">Planning ahead for next year? See <a href="/advisory/">tax planning &amp; advisory</a>. Got a letter from the IRS? See <a href="/services/irs-notice-help/">IRS help</a>.</p></div></section>
{CTA}"""),
"advisory/index.html": page("/advisory/", "Tax Planning &amp; Advisory in Coral Springs, FL | Koldal Tax &amp; Advisory",
 "Tax planning, quarterly estimates, year-end planning and business advisory from Alek Koldal, EA, an IRS Enrolled Agent in Coral Springs, FL.",
 f"""<div class="hero"><div class="wrap"><p class="eyebrow">Tax planning &amp; advisory</p><h1>Plan your taxes before the year ends, not after</h1>
<p>Most tax savings happen during the year. I use your actual numbers to plan ahead, so April brings no surprises and your business decisions come with the tax answer built in.</p>
<div class="actions"><a class="btn" href="/contact/">Book a free consultation</a></div></div></div>
<section><div class="wrap"><div class="grid">
<div class="card"><h3>Year-end tax planning</h3><p>A review before December 31 of what you&#39;ll owe and the moves that can still lower it.</p></div>
<div class="card"><h3>Quarterly estimated taxes</h3><p>Estimated payments calculated from your real income, so you pay the right amount on time.</p></div>
<div class="card"><h3>Business structure</h3><p>Whether an LLC, S corporation election or a change in owner pay makes sense for you, with the numbers to back it.</p></div>
<div class="card"><h3>Monthly review &amp; cash flow</h3><p>A regular call on your numbers and a cash-flow forecast, so you can plan hires, purchases and taxes.</p></div></div>
<p class="lede" style="margin-top:28px">Planning is quoted for your situation, on its own or alongside <a href="/bookkeeping/">monthly bookkeeping</a>.</p></div></section>
{CTA}"""),
"services/index.html": page("/services/", "Services | Koldal Tax &amp; Advisory",
 "Bookkeeping, tax preparation, tax planning and IRS representation from an Enrolled Agent in Coral Springs, FL.",
 f"""<section><div class="wrap"><h1>Services</h1><p class="lede">Everything your business and your taxes need, from one Enrolled Agent.</p>
<div class="pillars">{"".join(f'<a class="pillar" href="{u}"><span class="pillar-k">{k}</span><h3>{t}</h3><p>{d}</p><span class="pillar-f">{f}</span></a>' for k, t, d, f, u in PILLARS)}</div>
<h2 style="margin-top:44px">Also available</h2><div class="linklist">
<a href="/services/quickbooks-cleanup/"><strong>QuickBooks cleanup &amp; catch-up</strong><span>Get caught up, then stay caught up</span></a>
<a href="/services/payroll-with-gusto/"><strong>Payroll with Gusto</strong><span>Setup, QuickBooks connection and review of every payroll</span></a>
<a href="/quickbooks-help/1099-contractors/"><strong>1099 preparation</strong><span>1099-NECs for your contractors, filed each January</span></a></div></div></section>{CTA}"""),
"contact/index.html": page("/contact/", "Book a Free Consultation | Koldal Tax &amp; Advisory",
 "Book a free consultation with Alek Koldal, EA about bookkeeping, tax preparation, tax planning or IRS help.",
 f"""<section><div class="wrap split"><div><h1>Book a free consultation</h1>
<p>Tell me a little about what you need and I&#39;ll get back to you to set up a time to talk. The consultation is free and there&#39;s no obligation.</p>
<p>For bookkeeping, I&#39;ll also ask for view access to your QuickBooks Online file so I can see where things stand.</p>
<p>Prefer email? <a href="mailto:alek@koldaltax.com?subject=Consultation">alek@koldaltax.com</a></p></div>
{CONTACT_FORM}</div></section>"""),
"pricing/index.html": page("/pricing/", "Bookkeeping Plans &amp; Pricing | Koldal Tax &amp; Advisory",
 "Monthly QuickBooks Online bookkeeping plans from an Enrolled Agent in South Florida, plus add-ons for tax returns, payroll and 1099s.",
 f"""<section><div class="wrap"><h1>Plans &amp; pricing</h1><p class="lede">Every plan starts with a free QuickBooks review, so the price is set by your actual books, not a guess.</p>{plan_cards()}</div></section>
<section style="background:var(--soft)"><div class="wrap"><h2>Add-ons</h2><p class="lede">Add what you need to any plan.</p>{addon_rows()}</div></section>
<section id="tax-pricing"><div class="wrap"><h2>Tax services</h2><p class="lede">Available on their own or with a bookkeeping plan.</p>{tax_rows()}</div></section>
<section><div class="wrap" style="max-width:780px"><h2>Common questions</h2>
<details><summary>What counts as a transaction?</summary><p>Each line in your bank or credit card feed: a deposit, a purchase, a transfer. Your free review gives me the real count.</p></details>
<details><summary>Do I need my own QuickBooks Online subscription?</summary><p>Yes. You own your file and your data. If you don&#39;t have QuickBooks Online yet, I&#39;ll help you pick the right version and set it up.</p></details>
<details><summary>I&#39;m behind. Can I still start?</summary><p>Yes. We start with a one-time setup and cleanup ($800 to $2,500 depending on the work), then move you onto a monthly plan.</p></details>
<details><summary>Do you run payroll?</summary><p>Payroll runs through Gusto. I set up your Gusto account, connect it to QuickBooks, and review every payroll so it&#39;s recorded correctly.</p></details>
<details><summary>Can you do my taxes too?</summary><p>Yes. I&#39;m an IRS Enrolled Agent. I prepare business returns from the books I keep, and individual returns starting at $650.</p></details>
<details><summary>Is there a long-term contract?</summary><p>No. Plans are month to month.</p></details>
</div></section>{CTA}"""),
"about/index.html": page("/about/", "About Alek Koldal, EA | Koldal Tax &amp; Advisory",
 "Alek Koldal is an IRS Enrolled Agent providing QuickBooks Online bookkeeping and tax services for small businesses in Coral Springs and South Florida.",
 f"""<section><div class="wrap split"><div><h1>About Alek Koldal, EA</h1>
<p>Koldal Tax &amp; Advisory helps small business owners keep accurate books, make informed decisions, and stop dreading tax season.</p>
<p>I&#39;m an IRS Enrolled Agent, licensed by the U.S. Department of the Treasury to prepare returns and represent taxpayers before the IRS. Day to day I work mainly in QuickBooks Online, handling monthly bookkeeping, cleanups and catch-ups, so your books and your taxes are handled by the same person.</p>
<p>Based in Coral Springs, Florida, I believe responsive communication, personalized service, and practical solutions are the foundation of every good client relationship. My goal is to be more than your bookkeeper: a trusted advisor and long-term partner in your business.</p>
<p><strong>Alek Koldal, EA</strong><br><a href="mailto:alek@koldaltax.com">alek@koldaltax.com</a></p>
<p><a class="btn" href="/contact/">Get a free QuickBooks review</a></p></div>
<div><img class="headshot" src="/assets/headshot.jpg" alt="Alek Koldal, EA" width="380" height="475" onerror="this.remove()"></div></div></section>"""),
"resources/index.html": page("/resources/", "Free QuickBooks &amp; IRS Help | Koldal Tax &amp; Advisory", "Free guides from an Enrolled Agent: look up your IRS notice or fix common QuickBooks Online problems.", f"""<section><div class="wrap"><h1>Free help</h1><p class="lede">Plain-English guides from an Enrolled Agent who works in QuickBooks Online every day.</p><div class="grid" style="margin-top:20px"><a class="card notice" href="/irs-notices/"><h3>IRS notice lookup &rarr;</h3><p>Find your notice number (CP2000, CP14, CP504, 5071C and more) and see what it means, what to do and your deadline.</p></a><a class="card notice" href="/quickbooks-help/"><h3>QuickBooks Online help &rarr;</h3><p>Step-by-step fixes for bank feeds, reconciliations, uncategorized transactions, 1099s and more.</p></a></div></div></section>{CTA}"""),
"404.html": page("/404.html", "Page not found | Koldal Tax &amp; Advisory", "Page not found.",
 """<section><div class="wrap"><h1>Page not found</h1><p>That page doesn't exist. <a href="/">Go to the homepage</a> or <a href="/contact/">get in touch</a>.</p></div></section>"""),
}
import os, html as H
NOTICES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "notices.json")))
URG = {"low": "Low: informational", "medium": "Medium: action needed", "high": "High: respond by the deadline", "urgent": "Urgent: time-sensitive rights"}
DISCLAIMER = '<p class="small" style="margin-top:28px">This is general information, not tax advice for your situation. Always go by the dates and instructions printed on your own notice. Official IRS explanation: <a href="https://www.irs.gov/individuals/understanding-your-irs-notice-or-letter" rel="noopener">Understanding your IRS notice or letter</a>.</p>'
rows = ""
for n in NOTICES:
    e = lambda x: H.escape(x)
    rows += f'<a class="card notice" href="/irs-notices/{n["id"]}/" data-q="{e((n["name"]+" "+n["title"]+" "+n["what"]).lower())}"><h3>{e(n["name"])}</h3><p>{e(n["title"])}</p><span class="badge {n["urgency"]}">{n["urgency"].title()}</span></a>'
    li = lambda xs: "<ul>" + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ul>"
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f"What is IRS notice {n['name']}?", "acceptedAnswer": {"@type": "Answer", "text": n["what"]}},
        {"@type": "Question", "name": f"What should I do if I get a {n['name']}?", "acceptedAnswer": {"@type": "Answer", "text": " ".join(n["todo"])}},
        {"@type": "Question", "name": f"How long do I have to respond to a {n['name']}?", "acceptedAnswer": {"@type": "Answer", "text": n["deadline"]}}]}
    body = f"""<section><div class="wrap" style="max-width:780px"><p class="small"><a href="/irs-notices/">IRS notices</a> &rsaquo; {e(n["name"])}</p>
<h1>IRS {e(n["name"])}: {e(n["title"])}</h1><p><span class="badge {n["urgency"]}">{URG[n["urgency"]]}</span> <span class="small">For: {e(n["who"])}</span></p>
<h2>What this notice means</h2><p>{e(n["what"])}</p>
<h2>Common reasons you got it</h2>{li(n["common"])}
<h2>What to do</h2>{li(n["todo"])}
<h2>Deadline</h2><p><strong>{e(n["deadline"])}</strong></p>
{quick_form("IRS notice: " + n["name"], "Get help with your " + e(n["name"]), "As an IRS Enrolled Agent, I can review your notice, explain what it means for you, and respond to the IRS on your behalf. Send your details and I&#39;ll get back to you.")}
{DISCLAIMER}</div></section><script type="application/ld+json">{json.dumps(faq)}</script>"""
    pages[f"irs-notices/{n['id']}/index.html"] = page(f"/irs-notices/{n['id']}/", f"IRS {e(n['name'])} Notice Explained: {e(n['title'])} | Koldal Tax &amp; Advisory", e(f"Got an IRS {n['name']}? What it means, common reasons, what to do, and your deadline. Plain-English guide from Alek Koldal, EA."), body)
pages["irs-notices/index.html"] = page("/irs-notices/", "IRS Notice Lookup: What Your IRS Letter Means | Koldal Tax &amp; Advisory",
 "Look up your IRS notice or letter (CP2000, CP14, CP504, LT11, 5071C and more) and get a plain-English explanation, what to do, and your deadline.",
 f"""<section><div class="wrap"><h1>IRS notice lookup</h1><p style="color:var(--muted);max-width:680px">Find the notice number in the top or bottom right corner of your IRS letter (for example CP2000 or LTR 5071C), then search for it below.</p>
<input id="nq" type="search" placeholder="Search, e.g. CP2000, levy, identity" aria-label="Search IRS notices" style="max-width:520px;margin:10px 0 24px">
<div class="grid" id="nl">{rows}</div><p id="none" style="display:none">No match. <a href="/contact/">Send me your notice</a> and I'll explain it.</p>{DISCLAIMER}</div></section>
<script>const q=document.getElementById('nq'),cs=[...document.querySelectorAll('#nl .notice')];q.addEventListener('input',()=>{{const v=q.value.toLowerCase().replace(/ /g,'');let n=0;cs.forEach(c=>{{const m=c.dataset.q.replace(/ /g,'').includes(v);c.style.display=m?'':'none';n+=m}});document.getElementById('none').style.display=n?'none':''}});</script>""")
QBO = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "quickbooks.json")))
qrows = ""
for a in QBO:
    e = lambda x: H.escape(x)
    qrows += f'<a class="card notice" href="/quickbooks-help/{a["id"]}/" data-q="{e((a["title"]+" "+a["why"]).lower())}"><h3>{e(a["title"])}</h3><p>{e(a["q"])}</p></a>'
    steps = "<ol>" + "".join(f"<li>{e(x)}</li>" for x in a["fix"]) + "</ol>"
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": a["q"], "acceptedAnswer": {"@type": "Answer", "text": a["why"] + " " + " ".join(a["fix"])}}]}
    body = f"""<section><div class="wrap" style="max-width:780px"><p class="small"><a href="/quickbooks-help/">QuickBooks Online help</a> &rsaquo; {e(a["title"])}</p>
<h1>{e(a["title"])}</h1>
<h2>Why it happens</h2><p>{e(a["why"])}</p>
<h2>How to fix it</h2>{steps}
<h2>When to get help</h2><p>{e(a["pro"])}</p>
{quick_form("QuickBooks: " + a["title"], "Want me to fix it for you?", "I work in QuickBooks Online every day doing bookkeeping, cleanup and catch-up for small businesses. Send your details and I&#39;ll get back to you.")}
<p class="small" style="margin-top:28px">Menu names in QuickBooks Online change from time to time. If a step doesn&#39;t match what you see, the same option is usually nearby.</p></div></section><script type="application/ld+json">{json.dumps(faq)}</script>"""
    pages[f"quickbooks-help/{a['id']}/index.html"] = page(f"/quickbooks-help/{a['id']}/", f"{e(a['title'])} | QuickBooks Online Help | Koldal Tax &amp; Advisory", e(a["q"] + " Causes and step-by-step fixes from a QuickBooks Online bookkeeper in Coral Springs, FL."), body)
pages["quickbooks-help/index.html"] = page("/quickbooks-help/", "QuickBooks Online Help: Common Problems and Fixes | Koldal Tax &amp; Advisory",
 "Fix common QuickBooks Online problems: bank feeds, reconciliations, uncategorized transactions, Undeposited Funds, 1099s and more. From a Coral Springs bookkeeper.",
 f"""<section><div class="wrap"><h1>QuickBooks Online help</h1><p style="color:var(--muted);max-width:680px">Plain-English fixes for the QuickBooks Online problems I see most often. If you&#39;d rather have it done for you, every page has a quick way to reach me.</p>
<input id="nq" type="search" placeholder="Search, e.g. bank feed, reconcile, 1099" aria-label="Search QuickBooks help" style="max-width:520px;margin:10px 0 24px">
<div class="grid" id="nl">{qrows}</div><p id="none" style="display:none">No match. <a href="/contact/">Ask me directly</a>.</p></div></section>
<script>const q=document.getElementById('nq'),cs=[...document.querySelectorAll('#nl .notice')];q.addEventListener('input',()=>{{const v=q.value.toLowerCase();let n=0;cs.forEach(c=>{{const m=c.dataset.q.includes(v);c.style.display=m?'':'none';n+=m}});document.getElementById('none').style.display=n?'none':''}});</script>""")

def service_page(slug, title, desc, h1, intro, sections, topic, links):
    secs = "".join(f"<h2 id=\"{h.split()[0].lower().strip(',')}\">{h}</h2>" + ("<ul>" + "".join(f"<li>{x}</li>" for x in body) + "</ul>" if isinstance(body, list) else f"<p>{body}</p>") for h, body in sections)
    lk = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in links)
    pages[f"services/{slug}/index.html"] = page(f"/services/{slug}/", title, desc,
     f"""<section><div class="wrap" style="max-width:780px"><p class="small"><a href="/services/">Services</a></p><h1>{h1}</h1><p style="font-size:19px;color:var(--muted)">{intro}</p>{secs}
<h2>Helpful guides</h2><ul>{lk}</ul>{quick_form(topic, "Get started", "Tell me a bit about your situation and I&#39;ll get back to you.")}</div></section>""")

AREA = f"Based in Coral Springs and working with clients in {', '.join(CITIES[1:-1])} and {CITIES[-1]}, as well as remotely across Florida."
service_page("irs-notice-help", "IRS Notice &amp; Letter Help in Coral Springs, FL | Koldal Tax &amp; Advisory",
 "Got a letter from the IRS? An Enrolled Agent in Coral Springs, FL can explain your notice, respond for you, and set up payment plans.",
 "Help with IRS notices and letters",
 "An IRS letter doesn't have to be stressful. As an Enrolled Agent, I'm federally licensed to represent taxpayers before the IRS. " + AREA,
 [("What I can do", ["Explain what your notice means and what it will cost","Pull and review your IRS transcripts","Respond to proposed changes such as a CP2000","Set up payment plans for balances due","Respond to identity verification and missing information letters","Protect your appeal rights when time limits apply"]),
  ("Penalty relief", "Many penalties can be reduced or removed, through first-time abatement or reasonable cause. I charge a small upfront fee plus a percentage of the penalties the IRS actually removes, so you mostly pay when it works. The first penalty review is free."),
  ("IRS transcripts", "Not sure what the IRS has on file? I pull your wage &amp; income and account transcripts and walk you through them: the W-2s and 1099s reported under your name, payments, balances and any missing returns. It&#39;s the fastest way to see where you stand before filing or answering a notice."),
  ("What to send me", "A copy of every page of the notice, and the tax return for that year if you have it.")],
 "IRS notice help",
 [(f"/irs-notices/{n['id']}/", "IRS " + H.escape(n["name"]) + ": " + H.escape(n["title"])) for n in NOTICES[:6]] + [("/irs-notices/", "Look up any IRS notice")])
service_page("quickbooks-cleanup", "QuickBooks Cleanup &amp; Catch-Up in Coral Springs, FL | Koldal Tax &amp; Advisory",
 "Months or years behind in QuickBooks Online? Cleanup and catch-up bookkeeping from an Enrolled Agent in Coral Springs, FL, quoted after a free review.",
 "QuickBooks cleanup &amp; catch-up",
 "Get caught up, then stay caught up. I bring your QuickBooks Online file current, reconcile every account, and leave you with books ready for your tax return. " + AREA,
 [("What&#39;s included", ["Bank and credit card accounts reconciled month by month", "Uncategorized and Ask My Accountant transactions sorted", "Duplicates, Undeposited Funds and opening balances fixed", "Loan and owner draw entries corrected", "A clean profit &amp; loss and balance sheet at the end"]),
  ("How pricing works", "Getting started is a one-time setup fee, usually $800 to $2,500 depending on the work. It covers cleaning up prior months, reviewing your bank accounts, setting up bank rules, getting to know your accounts, and making sure your books tie to your tax return. I quote the exact amount after reviewing your file, then you move onto a monthly plan so it never piles up again."),
  ("Taxes behind too?", "As an Enrolled Agent I can also file missing returns and deal with any IRS notices that came while you were catching up.")],
 "QuickBooks cleanup",
 [(f"/quickbooks-help/{a['id']}/", H.escape(a["title"])) for a in QBO if a["id"] in ("catch-up-bookkeeping", "reconciliation-discrepancy", "uncategorized-transactions", "undeposited-funds", "duplicate-transactions")])
service_page("payroll-with-gusto", "Payroll Setup &amp; Review with Gusto | Koldal Tax &amp; Advisory",
 "Payroll setup with Gusto, connected to QuickBooks Online and reviewed every pay run by an Enrolled Agent in Coral Springs, FL.",
 "Payroll with Gusto, set up and checked",
 "Payroll runs through Gusto, which files payroll taxes and W-2s. I set it up right, connect it to QuickBooks Online, and review every payroll so your books and your payroll match. " + AREA,
 [("What I do", ["Set up your Gusto account, employees and contractors", "Connect Gusto to QuickBooks Online with the right accounts", "Review each payroll as it posts to your books", "Make sure owner pay is handled correctly for S corporations", "Reconcile payroll liabilities at year end"]),
  ("Contractors", "Paying contractors through Gusto? I make sure their W-9s are collected and their 1099s are right.")],
 "Payroll with Gusto",
 [("/quickbooks-help/1099-contractors/", "Preparing 1099s in QuickBooks Online"), ("/quickbooks-help/owner-draws/", "Personal expenses paid from the business account")])

for name, html in pages.items():
    p = os.path.join(out, name); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(html)
open(os.path.join(out, "CNAME"), "w").write("www.koldaltax.com\n")
open(os.path.join(out, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
urls = "".join(f"<url><loc>{SITE}/{n[:-len('index.html')]}</loc></url>" for n in pages if n.endswith("index.html"))
open(os.path.join(out, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
print("built", list(pages))
