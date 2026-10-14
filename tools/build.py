import sys, json
out = sys.argv[1]
SITE = "https://www.koldaltax.com"
# Add your business phone here (e.g. "(954) 555-0123") to show call buttons across the site.
PHONE = ""
CITIES = ["Coral Springs", "Margate", "Parkland", "Coconut Creek", "Tamarac", "Pompano Beach"]
NAV = [("/", "Home"), ("/services/", "Services"), ("/irs-notices/", "IRS Notices"), ("/quickbooks-help/", "QuickBooks Help"), ("/about/", "About"), ("/contact/", "Contact")]
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
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{json.dumps(SCHEMA)}</script>
</head>
<body>
<header><div class="wrap"><a class="brand" href="/">Koldal Tax &amp; Advisory</a><nav>{nav}{f'<a class="btn ghost" href="{TEL}">Call {PHONE}</a>' if PHONE else ""}<a class="btn" href="/contact/">Book a consultation</a></nav></div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div><strong>Koldal Tax &amp; Advisory</strong><br>Alek Koldal, EA (Enrolled Agent)<br>Coral Springs, Florida<br>{f'<a href="{TEL}">{PHONE}</a><br>' if PHONE else ""}<a href="mailto:alek@koldaltax.com">alek@koldaltax.com</a><br>Serving {", ".join(CITIES[:-1])} and {CITIES[-1]}<br>
<a href="https://members.csccrchamber.com/list/member/koldal-tax-advisory-margate-7305" rel="noopener">Chamber of Commerce member</a> · <a href="https://www.linkedin.com/in/aleksander-koldal" rel="noopener">LinkedIn</a> · <a href="https://g.page/r/CTKng70qwgj_EBM/review" rel="noopener">Leave a Google review</a>
<p class="small">&copy; 2026 Koldal Tax &amp; Advisory</p></div>
<div><strong>Newsletter</strong><p class="small">Tax deadlines and tips, a few times a year.</p>
<form data-kind="newsletter"><label class="hp">Leave empty<input name="website" tabindex="-1" autocomplete="off"></label>
<input type="email" name="email" required placeholder="Email address" aria-label="Email address"><button class="btn" type="submit">Sign up</button>
<div class="msg" role="status" style="grid-column:1/-1"></div></form></div>
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

CTA = """<section><div class="wrap"><div class="cta"><div><h2>Ready to get organized?</h2><p style="margin:6px 0 0;opacity:.85">Book a consultation and we can talk through what you need.</p></div><a class="btn" href="/contact/">Book a consultation</a></div></div></section>"""

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
"index.html": page("/", "Koldal Tax &amp; Advisory | Bookkeeping &amp; Tax Services in Coral Springs, FL",
 "Accounting, bookkeeping and tax services for individuals and small businesses in Coral Springs and South Florida, from Alek Koldal, EA.",
 f"""<div class="hero"><div class="wrap"><h1>Accounting, bookkeeping &amp; tax services for individuals and small businesses</h1>
<p>Helping clients in Coral Springs and across South Florida stay organized, tax-ready, and focused on growth.</p>
<div class="actions"><a class="btn" href="/contact/">Book a consultation</a><a class="btn ghost" href="/services/">See services</a></div></div></div>
<section><div class="wrap"><h2>How I can help</h2><div class="grid">{cards(SERVICES[:3] + SERVICES[4:5] + [(SERVICES[3][0], SERVICES[3][1], [])])}</div>
<p style="margin-top:20px"><a href="/services/">All services &rarr;</a></p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="card"><h3>Got a letter from the IRS?</h3><p>Look up your notice number (CP2000, CP14, CP504, 5071C and more) for a plain-English explanation and your deadline.</p><p style="margin-top:14px"><a class="btn ghost" href="/irs-notices/">Look up your IRS notice</a></p></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="card"><h3>Stuck in QuickBooks Online?</h3><p>Bank feeds not updating, reconciliations that won&#39;t balance, a pile of uncategorized transactions: step-by-step fixes for common problems.</p><p style="margin-top:14px"><a class="btn ghost" href="/quickbooks-help/">QuickBooks Online help</a></p></div></div></section>
<section style="background:var(--soft)"><div class="wrap split"><div><h2>Work with an Enrolled Agent</h2>
<p>I'm Alek Koldal, an IRS Enrolled Agent. Enrolled Agents are federally licensed tax practitioners who can represent taxpayers before the IRS.</p>
<p>You'll work with me directly, with responsive communication and practical answers year-round, not just at tax time.</p>
<p><a href="/about/">More about me &rarr;</a></p></div>
<div class="card"><h3>&#9733;&#9733;&#9733;&#9733;&#9733; 5.0 on Google</h3><p>Read what clients say, or leave a review.</p><p style="margin-top:12px"><a href="https://g.page/r/CTKng70qwgj_EBM/review" rel="noopener">Google reviews &rarr;</a></p></div></div></section>
{CTA}"""),
"about/index.html": page("/about/", "About Alek Koldal, EA | Koldal Tax &amp; Advisory",
 "Koldal Tax &amp; Advisory in Coral Springs, FL offers personalized accounting, bookkeeping and tax services for individuals and small businesses.",
 f"""<section><div class="wrap split"><div><h1>About Koldal Tax &amp; Advisory</h1>
<p>Koldal Tax &amp; Advisory helps individuals and small business owners stay organized, make informed financial decisions, and reach their long-term goals.</p>
<p>Based in Coral Springs, Florida, I help clients keep accurate financial records throughout the year. I believe responsive communication, personalized service, and practical solutions are the foundation of every good client relationship.</p>
<p>Whether you need help catching up on bookkeeping, ongoing monthly accounting, or tax preparation, my goal is to simplify the financial side of your business so you can focus on running it with confidence.</p>
<p>I want to be more than your accountant: a trusted advisor and long-term partner in your financial success.</p>
<p><strong>Alek Koldal, EA</strong><br><a href="mailto:alek@koldaltax.com">alek@koldaltax.com</a></p>
<p><a class="btn" href="/contact/">Book a consultation</a></p></div>
<div><img class="headshot" src="/assets/headshot.jpg" alt="Alek Koldal, EA" width="380" height="475" onerror="this.remove()"></div></div></section>"""),
"services/index.html": page("/services/", "Tax, Bookkeeping &amp; QuickBooks Services | Koldal Tax &amp; Advisory",
 "Individual and business tax returns, tax planning, monthly bookkeeping, QuickBooks cleanup and IRS help for clients in Coral Springs and South Florida.",
 f"""<section><div class="wrap"><h1>Services</h1><p style="color:var(--muted);max-width:640px">Every engagement starts with a consultation so I can understand your situation.</p>
<div class="grid" style="margin-top:24px"><a class="card notice" href="/services/quickbooks-online-bookkeeping/"><h3>QuickBooks Online bookkeeping &rarr;</h3><p>Monthly bookkeeping, cleanup and catch-up.</p></a><a class="card notice" href="/services/tax-preparation/"><h3>Tax preparation &rarr;</h3><p>Individual and small business returns.</p></a><a class="card notice" href="/services/irs-notice-help/"><h3>IRS notice help &rarr;</h3><p>Got a letter from the IRS? I can respond for you.</p></a></div>
<h2 style="margin-top:34px">Tax services</h2><div class="grid">{cards([SERVICES[0], SERVICES[1], SERVICES[2], SERVICES[5]])}</div>
<h2 style="margin-top:40px">Accounting services</h2><div class="grid">{cards([SERVICES[3], SERVICES[4]])}</div></div></section>
{CTA}"""),
"contact/index.html": page("/contact/", "Contact &amp; Book a Consultation | Koldal Tax &amp; Advisory",
 "Contact Koldal Tax &amp; Advisory for bookkeeping, tax preparation and IRS help. Send a message to book a consultation.",
 """<section><div class="wrap split"><div><h1>Book a consultation</h1>
<p>Whether you need help with bookkeeping, taxes, or getting your books back on track, I'm here to help. Send a message and I'll get back to you soon.</p>
<p>Prefer email? <a href="mailto:alek@koldaltax.com?subject=Consultation">alek@koldaltax.com</a></p></div>
<form data-kind="contact"><div class="row"><label>First name<input name="first_name" required autocomplete="given-name"></label><label>Last name<input name="last_name" required autocomplete="family-name"></label></div>
<label>Email<input type="email" name="email" required autocomplete="email"></label>
<label>Phone (optional)<input type="tel" name="phone" autocomplete="tel"></label>
<label>What do you need help with?<select name="service"><option>Individual tax return</option><option>Business tax return</option><option>Tax planning</option><option>Monthly bookkeeping</option><option>QuickBooks cleanup</option><option>IRS notice or letter</option><option>Something else</option></select></label>
<label>Message<textarea name="message" required></textarea></label>
<label class="hp">Leave empty<input name="website" tabindex="-1" autocomplete="off"></label>
<button class="btn" type="submit">Send message</button><div class="msg" role="status"></div></form></div></section>"""),
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
    pages[f"irs-notices/{n['id']}/index.html"] = page(f"/irs-notices/{n['id']}/", f"IRS {e(n['name'])} Notice Explained: {e(n['title'])} | Koldal Tax", e(f"Got an IRS {n['name']}? What it means, common reasons, what to do, and your deadline. Plain-English guide from Alek Koldal, EA."), body)
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
    pages[f"quickbooks-help/{a['id']}/index.html"] = page(f"/quickbooks-help/{a['id']}/", f"{e(a['title'])} | QuickBooks Online Help | Koldal Tax", e(a["q"] + " Causes and step-by-step fixes from a QuickBooks Online bookkeeper in Coral Springs, FL."), body)
pages["quickbooks-help/index.html"] = page("/quickbooks-help/", "QuickBooks Online Help: Common Problems and Fixes | Koldal Tax &amp; Advisory",
 "Fix common QuickBooks Online problems: bank feeds, reconciliations, uncategorized transactions, Undeposited Funds, 1099s and more. From a Coral Springs bookkeeper.",
 f"""<section><div class="wrap"><h1>QuickBooks Online help</h1><p style="color:var(--muted);max-width:680px">Plain-English fixes for the QuickBooks Online problems I see most often. If you&#39;d rather have it done for you, every page has a quick way to reach me.</p>
<input id="nq" type="search" placeholder="Search, e.g. bank feed, reconcile, 1099" aria-label="Search QuickBooks help" style="max-width:520px;margin:10px 0 24px">
<div class="grid" id="nl">{qrows}</div><p id="none" style="display:none">No match. <a href="/contact/">Ask me directly</a>.</p></div></section>
<script>const q=document.getElementById('nq'),cs=[...document.querySelectorAll('#nl .notice')];q.addEventListener('input',()=>{{const v=q.value.toLowerCase();let n=0;cs.forEach(c=>{{const m=c.dataset.q.includes(v);c.style.display=m?'':'none';n+=m}});document.getElementById('none').style.display=n?'none':''}});</script>""")

def service_page(slug, title, desc, h1, intro, sections, topic, links):
    secs = "".join(f"<h2>{h}</h2>" + ("<ul>" + "".join(f"<li>{x}</li>" for x in body) + "</ul>" if isinstance(body, list) else f"<p>{body}</p>") for h, body in sections)
    lk = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in links)
    pages[f"services/{slug}/index.html"] = page(f"/services/{slug}/", title, desc,
     f"""<section><div class="wrap" style="max-width:780px"><p class="small"><a href="/services/">Services</a></p><h1>{h1}</h1><p style="font-size:19px;color:var(--muted)">{intro}</p>{secs}
<h2>Helpful guides</h2><ul>{lk}</ul>{quick_form(topic, "Get started", "Tell me a bit about your situation and I&#39;ll get back to you.")}</div></section>""")

AREA = f"Based in Coral Springs and working with clients in {', '.join(CITIES[1:-1])} and {CITIES[-1]}, as well as remotely across Florida."
service_page("quickbooks-online-bookkeeping", "QuickBooks Online Bookkeeping in Coral Springs, FL | Koldal Tax &amp; Advisory",
 "Monthly QuickBooks Online bookkeeping, cleanup and catch-up for small businesses in Coral Springs, Margate, Parkland and South Florida.",
 "QuickBooks Online bookkeeping for small businesses",
 "Monthly bookkeeping, cleanup and catch-up in QuickBooks Online, done by an Enrolled Agent who also prepares your taxes. " + AREA,
 [("Monthly bookkeeping", SERVICES[3][2]),
  ("Cleanup &amp; catch-up", "Behind by a few months or a few years? I'll bring your QuickBooks Online file up to date, reconcile every account, and leave you with books you can trust at tax time."),
  ("Why it helps to have your bookkeeper do your taxes", "Your books and your return are done by the same person, so nothing gets lost between them, and questions get answered once.")],
 "QuickBooks Online bookkeeping",
 [(f"/quickbooks-help/{a['id']}/", H.escape(a["title"])) for a in QBO[:6]] + [("/quickbooks-help/", "All QuickBooks Online help")])
service_page("irs-notice-help", "IRS Notice &amp; Letter Help in Coral Springs, FL | Enrolled Agent | Koldal Tax",
 "Got a letter from the IRS? An Enrolled Agent in Coral Springs, FL can explain your notice, respond for you, and set up payment plans.",
 "Help with IRS notices and letters",
 "An IRS letter doesn't have to be stressful. As an Enrolled Agent, I'm federally licensed to represent taxpayers before the IRS. " + AREA,
 [("What I can do", ["Explain what your notice means and what it will cost","Respond to proposed changes such as a CP2000","Set up payment plans for balances due","Respond to identity verification and missing information letters","Protect your appeal rights when time limits apply"]),
  ("What to send me", "A copy of every page of the notice, and the tax return for that year if you have it.")],
 "IRS notice help",
 [(f"/irs-notices/{n['id']}/", "IRS " + H.escape(n["name"]) + ": " + H.escape(n["title"])) for n in NOTICES[:6]] + [("/irs-notices/", "Look up any IRS notice")])
service_page("tax-preparation", "Tax Preparation in Coral Springs, FL | Individual &amp; Small Business | Koldal Tax",
 "Individual and small business tax preparation by an Enrolled Agent in Coral Springs, FL: 1040s, Schedule C, partnerships and S corporations.",
 "Tax preparation for individuals and small businesses",
 "Straightforward tax preparation from an Enrolled Agent, with year-round answers when you need them. " + AREA,
 [("Individuals", SERVICES[0][1]), ("Small businesses", SERVICES[1][1]), ("Planning", SERVICES[2][1])],
 "Tax preparation",
 [("/irs-notices/", "Got a letter from the IRS? Look it up"), ("/quickbooks-help/1099-contractors/", "Preparing 1099s in QuickBooks Online")])

for name, html in pages.items():
    p = os.path.join(out, name); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(html)
open(os.path.join(out, "CNAME"), "w").write("www.koldaltax.com\n")
open(os.path.join(out, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
urls = "".join(f"<url><loc>{SITE}/{n[:-len('index.html')]}</loc></url>" for n in pages if n.endswith("index.html"))
open(os.path.join(out, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
print("built", list(pages))
