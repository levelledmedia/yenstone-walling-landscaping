#!/usr/bin/env python3
"""
Builds the inner pages of the Yenstone site from the homepage.

  services/*.html              the seven service pages (one shared design)
  about.html                   About us
  gallery.html                 Gallery (photo wall)
  service-versions/version-3.html   the kept "dark stone" layout, for later pages

The header, mobile menu, process, FAQ, quote section, footer and lightbox are
lifted straight from site/index.html, so they can never drift from the homepage.
Edit site/index.html (shared parts) or this file (page copy), then run:

    python3 tools/build-pages.py

The generated .html files are overwritten each time, so make copy changes here.
"""
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent.parent / 'site'
home = (SITE / 'index.html').read_text()

PHONE = '<svg class="icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'

# ------------------------------------------------------------------ shared chrome from the homepage
def between(start, end):
    i = home.index(start)
    return home[i:home.index(end, i)]


def rel(s, p):
    """Re-point relative page links and assets at the right folder depth (p is '' or '../')."""
    if not p:
        return s
    s = re.sub(r'href="(?!#|tel:|mailto:|https?:|\.\./)([^"]+)"', lambda m: f'href="{p}{m.group(1)}"', s)
    return s.replace('src="assets/', f'src="{p}assets/')


HEADER = between('<!-- HEADER -->', '<main id="main">')
PROCESS = between('<!-- PROCESS -->', '<!-- ALSO WE DO -->')
FAQ = between('<!-- FAQ -->', '<!-- QUOTE + CONTACT -->')
QUOTE = between('<!-- QUOTE + CONTACT -->', '</main>')
FOOTER = between('<!-- FOOTER -->', '<!-- LIGHTBOX -->')
LIGHTBOX = between('<!-- LIGHTBOX -->', '<script src=')


def header_for(p, current=None, slug=None):
    h = HEADER.replace('<a href="index.html" aria-current="page">Home</a>', '<a href="index.html">Home</a>')
    marks = {'home': 'index.html', 'about': 'about.html', 'services': 'index.html#services', 'gallery': 'gallery.html'}
    if current in marks and current != 'home':
        href = marks[current]
        h = re.sub(rf'<a href="{re.escape(href)}">', f'<a href="{href}" aria-current="page">', h)
    if slug:
        h = h.replace(f'<a href="services/{slug}.html">', f'<a href="services/{slug}.html" aria-current="page">')
    return rel(h, p)


# ------------------------------------------------------------------ photos (all real project photos used on the homepage)
PHOTOS = {
    'tree-relief-pool': (960, 750, 'A dry stone wall with a tree carved in relief behind a swimming pool'),
    'signpost-wall': (640, 750, 'A newly built dry stone wall beside a lane with a wooden signpost'),
    'curved-wall-field': (640, 375, 'A long curved dry stone wall across a field'),
    'oak-gate-paving': (640, 750, 'Stone paving leading to an oak gate set in a stone wall'),
    'lawn-curved-wall': (640, 375, 'A curved dry stone wall around a new lawn'),
    'broad-steps': (640, 375, 'Broad paved steps rising through a terraced garden'),
    'flint-wall': (640, 750, 'A flint wall running beside a gravel path'),
    'pond-wall-bench': (640, 375, 'A garden pond with a dry stone wall and bench behind it'),
    'wall-lane': (640, 375, 'A long dry stone wall beside a country lane'),
    'coursed-wall': (640, 750, 'Close view of a coursed dry stone wall under construction'),
    'formal-garden-steps': (640, 375, 'Broad stone steps rising between clipped lawns and low stone walls'),
    'retaining-wall-rose': (640, 375, 'A stone retaining wall with a climbing rose beside a drive'),
    'lawn-gate': (640, 750, 'A striped lawn running to a field gate in a hedged garden'),
    'wall-steps-deer': (640, 375, 'A dry stone wall with built-in stone steps and a deer grazing beside it'),
    'stone-bridge': (960, 750, 'A curved stone bridge over a stream in a planted garden'),
    'stone-house-glazing': (640, 750, 'A stone and oak house with a tall glazed gable and gravel drive'),
    'gravel-drive-wall': (640, 375, 'A gravel drive edged by a tall dry stone wall'),
    'retaining-wall-curve': (640, 375, 'A curved stone retaining wall in a planted garden'),
    'oak-barn-wall': (960, 750, 'An oak-clad building with a new dry stone wall and gravel forecourt'),
    'wall-oak-gate-lane': (640, 375, 'A dry stone wall with a new oak gate beside a lane'),
    'stone-detail-iris': (640, 375, 'Close view of cut stonework with iris leaves in front'),
}
GALLERY_ORDER = ['coursed-wall', 'stone-detail-iris', 'curved-wall-field', 'oak-gate-paving', 'lawn-curved-wall', 'broad-steps',
                 'flint-wall', 'pond-wall-bench', 'wall-lane', 'tree-relief-pool', 'oak-barn-wall', 'retaining-wall-rose',
                 'formal-garden-steps', 'wall-steps-deer', 'signpost-wall', 'stone-house-glazing', 'gravel-drive-wall',
                 'retaining-wall-curve', 'lawn-gate', 'wall-oak-gate-lane', 'stone-bridge']
# (order chosen so the justified rows pack evenly: three photos per row at common desktop widths)

# ------------------------------------------------------------------ service copy
EST = ('Established in 1991', 'One family, one yard, and a lot of walls.')
LOCAL = ('Local stone first', 'We match the stone of your house and your lane wherever we can.')

SERVICES = [
    dict(
        slug='dry-stone-walling', name='Dry stone walling',
        desc='Dry stone walling in South Somerset from Yenstone: boundary, retaining and garden walls, repairs and rebuilds, built by a certified waller. Call 01963 371123.',
        standfirst='Boundary, retaining and garden walls, built by hand in local stone by a certified waller.',
        hero=('curved-wall-field-cinematic', 1639, 960, 'A long curved dry stone wall across a field'),
        facts=[EST, ('DSWA certified', 'Qualified through the Dry Stone Walling Association.'), LOCAL],
        a_h='Built without mortar, made to last',
        a_p1='A dry stone wall holds together by weight and fit alone. Every stone is chosen, turned and set by hand so it locks against the stones around it. The wall drains freely, moves with the ground instead of cracking, and gets better with age.',
        a_p2='It is slow, skilled work, and it is the heart of what we do. We have been building walls across Somerset and Dorset since 1991, and everything else we build, from steps to terraces, is shaped by that way of working.',
        b_h='What we build and repair',
        b_intro='Whether it is a new wall or an old one that has come down, we start by looking at the stone you already have and the ground it stands on.',
        items=[
            ('Boundary and garden walls', 'Along a lane, around a field or enclosing a garden. We match the stone of your house and your lane, so a new wall looks as if it has always been there.'),
            ('Retaining walls', 'Walls that hold back sloping ground and give you level space to use. Built to drain freely, so water does not build up behind them.'),
            ('Repairs and rebuilds', 'We take down and rebuild walls that have leaned or collapsed, including lime-mortared walls, and reuse the original stone wherever we can. We also do insurance work and can give you a quote to pass to your insurer.'),
            ('Cladding and built-in details', 'Stone cladding for buildings, plus gateways, piers and steps set into the wall as it goes up.'),
        ],
        close='Not sure what your wall needs? Call us. We will come and look, talk through the options and send you a written quote.',
        w_p='Walls we have built in Somerset and Dorset. Select a photo to see it larger.',
        photos=['tree-relief-pool', 'signpost-wall', 'lawn-curved-wall', 'flint-wall', 'wall-lane', 'coursed-wall', 'wall-steps-deer', 'retaining-wall-rose'],
    ),
    dict(
        slug='paving', name='Paving, patios and drives',
        desc='Paving, patios and drives in South Somerset from Yenstone: stone and gravel surfaces laid on firm foundations. Call 01963 371123 for a free quote.',
        standfirst='Stone and gravel surfaces for terraces, paths and drives, laid on firm foundations.',
        hero=('hero-landscaping-driveway', 1672, 941, 'A gravel drive and a stone-flagged path leading to a stone cottage porch and a five-bar gate'),
        facts=[EST, ('Firm foundations', 'Laid on properly prepared ground, so surfaces stay level.'), LOCAL],
        a_h='Surfaces that last start below the surface',
        a_p1='Most paving problems start under the stone, not in it. A patio or drive that sinks, rocks or holds water has usually been laid on ground that was not prepared properly. We dig out, build up the base and set the levels so water runs where it should before any stone goes down.',
        a_p2='Because we build walls, steps and gardens as well, we think about how a surface meets everything around it: the edge of a lawn, the foot of a wall, the threshold of a door. The result looks like part of the garden rather than something added to it.',
        b_h='What we lay',
        b_intro='We work in natural stone and in gravel, and we will talk you through which suits your house, your budget and the way you use the space.',
        items=[
            ('Patios and terraces', 'Places to sit, eat and look at the garden, laid to fall gently away from the house and set in stone that suits it.'),
            ('Paths and walkways', 'Stone paths that link the house, the garden and the gate, wide enough to use and laid so they stay level.'),
            ('Drives and forecourts', 'Gravel and stone drives built on a proper sub-base, with edging that keeps everything in place.'),
            ('Repairs and relaying', 'Sunken, uneven or stained paving lifted, the base put right and the stone relaid, reusing what we can.'),
        ],
        close='Thinking about a patio or drive? Call us. We will visit, measure up and send you a written quote.',
        w_p='Recent work in Somerset and Dorset. Select a photo to see it larger.',
        photos=['oak-barn-wall', 'oak-gate-paving', 'gravel-drive-wall', 'flint-wall', 'wall-oak-gate-lane', 'stone-house-glazing', 'broad-steps', 'formal-garden-steps'],
    ),
    dict(
        slug='garden-design', name='Garden design and planning',
        desc='Garden design and planning in South Somerset from Yenstone: a clear plan for levels, paths, walls and planting before any ground is broken. Call 01963 371123.',
        standfirst='A clear plan for levels, paths, walls and planting before any ground is broken.',
        hero=('pond-wall-bench-cinematic', 1639, 960, 'A garden pond with a dry stone wall and bench behind it'),
        facts=[EST, ('One team', 'The people who plan your garden are the people who build it.'), LOCAL],
        a_h='Plan the whole garden, then build it in order',
        a_p1='Some gardens need a tidy-up. Others need a fresh start: new levels, a proper terrace, steps that make sense, borders that frame the view instead of hiding it. We look at how you use the space and how the land falls before we draw anything.',
        a_p2='We plan the walls, paving and planting together, so it feels like one garden rather than a set of separate jobs. Then we agree the order of work, so each stage leads naturally into the next.',
        b_h='What a plan covers',
        b_intro='A plan can be as simple as a sketch for one border or as full as a whole-garden scheme. It always starts with a visit.',
        items=[
            ('Levels and layout', 'How the garden falls, where it needs to be level, and how you move through it.'),
            ('Walls and boundaries', 'Stone walls that hold the ground, mark the edges and give the planting something to grow against.'),
            ('Paving and surfaces', 'Terraces, paths and drives chosen to suit the house and laid to match the plan.'),
            ('Planting and borders', 'Beds and borders that frame the view, planned alongside the hard landscaping so they sit together.'),
        ],
        close='Not sure where to start? Call us. We will come and look at the garden, talk through what you want and explain how we would approach it.',
        w_p='Recent work in Somerset and Dorset. Select a photo to see it larger.',
        photos=['stone-bridge', 'lawn-gate', 'pond-wall-bench', 'oak-gate-paving', 'retaining-wall-curve', 'stone-house-glazing', 'formal-garden-steps', 'lawn-curved-wall'],
    ),
    dict(
        slug='steps-and-terraces', name='Steps and terraces',
        desc='Steps and terraces in South Somerset from Yenstone: level changes in stone that look as if they were always there. Call 01963 371123 for a free quote.',
        standfirst='Level changes that look as if they were always there.',
        hero=('formal-garden-steps-cinematic', 1638, 960, 'Broad stone steps rising between clipped lawns and low stone walls'),
        facts=[EST, ('Built into the land', 'Steps and terraces shaped around the way your ground falls.'), LOCAL],
        a_h='Make a slope useful',
        a_p1='A sloping garden can be hard to use. Steps and terraces turn the fall of the land into usable levels, with comfortable, safe ways to move between them.',
        a_p2='We build them in stone, with retaining walls where the ground needs holding back, so the steps, terraces and walls are one piece of work and weather together.',
        b_h='What we build',
        b_intro='Every set of steps starts with the slope in front of it. We measure, work out the levels and build to suit.',
        items=[
            ('Garden steps', 'Stone steps with even risers and treads that are comfortable to use in all weathers.'),
            ('Terraces and level changes', 'Flat, usable areas cut into a slope and held by stone walls.'),
            ('Retaining walls', 'Dry stone walls that hold back the ground and drain freely.'),
            ('Steps built into walls', 'Stone steps set into a wall as it goes up, for gateways and changes of level.'),
        ],
        close='Got a slope that needs sorting? Call us. We will come and look, talk through the options and send you a written quote.',
        w_p='Recent work in Somerset and Dorset. Select a photo to see it larger.',
        photos=['formal-garden-steps', 'coursed-wall', 'broad-steps', 'oak-gate-paving', 'wall-steps-deer', 'lawn-gate', 'retaining-wall-curve', 'retaining-wall-rose'],
    ),
    dict(
        slug='lawns', name='Lawns and turfing',
        desc='Lawns and turfing in South Somerset from Yenstone: ground prepared properly, then seeded or turfed. Call 01963 371123 for a free quote.',
        standfirst='Ground prepared properly, then seeded or turfed.',
        hero=('hero-landscaping-family-garden', 1672, 941, 'A curved lawn beside a planted border, stone steps and a paved terrace'),
        facts=[EST, ('Prepared properly', 'Cleared, levelled and firmed before any seed or turf goes down.'), ('Family run', 'Run by one family from Perhams Farm, Yenston.')],
        a_h='A good lawn is made before it is laid',
        a_p1='Whether it is seed or turf, a lawn is only as good as the ground under it. We clear the site, level it, deal with drainage where it is needed and prepare a fine, firm seedbed before anything goes down.',
        a_p2='We can start from bare ground or from a tired old lawn, and we plan the edges, paths and borders around it so the lawn sits properly in the garden.',
        b_h='Seeded or turfed',
        b_intro='Both give you a good lawn. The right choice depends on how soon you want to use it, the size of the space and your budget.',
        items=[
            ('Turfing', 'Quality turf laid on prepared ground, for a lawn you can start to enjoy quickly.'),
            ('Seeding', 'Sown on a fine seedbed, a good option for larger areas and a more gradual start.'),
            ('Levelling and drainage', 'Uneven or boggy ground put right before the lawn goes down.'),
            ('Edges and borders', 'Clean edges, paths and planting beds that frame the lawn and keep it neat.'),
        ],
        close='Ready for a new lawn? Call us. We will come and look at the ground and send you a written quote.',
        w_p='Recent work in Somerset and Dorset. Select a photo to see it larger.',
        photos=['stone-bridge', 'lawn-gate', 'lawn-curved-wall', 'stone-house-glazing', 'formal-garden-steps', 'oak-gate-paving', 'pond-wall-bench', 'retaining-wall-curve'],
    ),
    dict(
        slug='groundworks', name='Groundworks',
        desc='Groundworks in South Somerset from Yenstone: excavation, levelling, foundations and drives, ready for what comes next. Call 01963 371123 for a free quote.',
        confirm='scope of groundworks (excavation, foundations, drives, drainage) is inferred; confirm with the client',
        standfirst='Excavation, levelling, foundations and drives, ready for what comes next.',
        hero=('hero-landscaping-wildlife-garden', 1774, 887, 'A wildlife pond with a gravel path, stone steps and a bench in a planted garden'),
        facts=[EST, ('Ready for what comes next', 'Ground prepared and finished so the next stage can start.'), ('Written quotes', 'The work and the price set out clearly before we start.')],
        a_h='The work you do not see afterwards',
        a_p1='Good groundworks are what everything else rests on: the levels, the drainage and the foundations. If they are right, walls, paving and gardens stay where they should. If they are not, nothing built on top will last.',
        a_p2='We dig, level and prepare the ground ourselves, so it is ready for what comes next, whether that is a wall, a terrace, a drive or a whole garden.',
        b_h='What we do',
        b_intro='From a small garden to a whole plot, we start by looking at the ground and what it needs to carry.',
        items=[
            ('Excavation and levelling', 'Digging out and levelling ground for terraces, paths, drives and building work.'),
            ('Foundations', 'Firm, correctly built bases for walls, steps and paved areas.'),
            ('Drives and hardstanding', 'Prepared and surfaced for vehicles, with drainage that keeps them dry.'),
            ('Drainage', 'Getting water away from where you do not want it.'),
        ],
        close='Need the ground sorting first? Call us. We will come and look and send you a written quote.',
        w_p='Recent work in Somerset and Dorset. Select a photo to see it larger.',
        photos=['oak-barn-wall', 'stone-house-glazing', 'gravel-drive-wall', 'coursed-wall', 'retaining-wall-curve', 'flint-wall', 'retaining-wall-rose', 'broad-steps'],
    ),
    dict(
        slug='septic-tanks', name='Septic tanks and drainage',
        desc='Septic tanks and drainage in South Somerset from Yenstone: installation and drainage for properties off mains sewers. Call 01963 371123 for a free quote.',
        confirm='scope of septic tank and drainage work, and any regulations to mention; confirm with the client. Real photos needed (see SHOT-LIST.md)',
        standfirst='Installation and drainage for properties off mains sewers.',
        hero=('stone-bridge-cinematic-overcast', 1639, 959, 'A low stone bridge over a stream in a planted garden'),
        facts=[EST, ('Local knowledge', 'Working across Somerset and Dorset from our base near Templecombe.'), ('Written quotes', 'The work and the price set out clearly before we start.')],
        a_h='Drainage for homes off the mains',
        a_p1='Many homes in our area are not connected to a mains sewer. A septic tank and its drainage need to be planned for the ground, the size of the household and the rules that apply.',
        a_p2='We install the tank and the drainage and put the ground back properly afterwards, so the work disappears into the garden.',
        b_h='What we do',
        b_intro='Every property is different. We start with a visit to look at the ground and what is already there.',
        items=[
            ('New installations', 'A tank and drainage fitted for a new build or a property that does not yet have a system.'),
            ('Replacing an old system', 'Taking out a failing or out-of-date tank and fitting a new one.'),
            ('Drainage and soakaways', 'The pipework and drainage that carry water away safely.'),
            ('Reinstating the ground', 'Levelling, turf and paths put back so the garden is usable again.'),
        ],
        close='Not sure what your property needs? Call us. We will come and look and send you a written quote.',
        w_p='Photos of our septic tank and drainage installations are coming soon.',
        photos=None,
        shots=['Septic tank installation, landscape 1400x900', 'Drainage and soakaway work, landscape 1400x900', 'Finished ground reinstated, landscape 1400x900'],
    ),
]
SLUG_ORDER = [s['slug'] for s in SERVICES]

# ------------------------------------------------------------------ small builders
def btns(kind, size='btn--lg'):
    first = {'dark': 'btn--call', 'light': 'btn--deep', 'split': 'btn--dark'}[kind]
    second = 'btn--ghost' if kind == 'dark' else 'btn--outline'
    call = f'<a class="btn {first} {size}" href="tel:01963371123">{PHONE}Call 01963 371123</a>'
    quote = f'<a class="btn {second} {size}" href="#quote">Get a free quote</a>'
    return call + quote


def img_tag(name, w, h, alt, p, cls='', lazy=True, extra=''):
    loading = ' loading="lazy"' if lazy else ''
    return f'<img{cls} src="{p}assets/img/{name}.webp" width="{w}" height="{h}" alt="{alt}"{loading}{extra}>'


def photo_buttons(names, p, anim=True):
    out = []
    for n in names:
        w, h, alt = PHOTOS[n]
        a = ' data-anim="settle"' if anim else ''
        out.append(f'<button type="button" class="svc-photo"{a}>{img_tag(n, w, h, alt, p)}</button>')
    return '\n          '.join(out)


def items_html(items):
    return '\n          '.join(f'<div class="svc-item" data-anim="settle"><h3>{h}</h3><p>{t}</p></div>' for h, t in items)


def shell(p, title, desc, body_class, main, current, slug=None, noindex=False):
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ''
    return f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <!-- CONFIRM: add the canonical URL once the final domain is set -->{robots}
  <meta name="theme-color" content="#2B1F1A">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:locale" content="en_GB">
  <script>document.documentElement.classList.add('js');</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400..600&display=swap">
  <link rel="stylesheet" href="{p}css/styles.css">
  <link rel="stylesheet" href="{p}css/pages.css">
</head>
<body class="{body_class}">
  <a class="skip" href="#main">Skip to content</a>

  {header_for(p, current, slug)}<main id="main">
{main}
    <!-- QUOTE (same as the homepage) -->
{rel(QUOTE, p)}  </main>

  {rel(FOOTER, p)}  {LIGHTBOX}<script src="{p}js/main.js" defer></script>
</body>
</html>
'''


def photo_hero(p, hero, h1, lede):
    n, w, h, alt = hero
    return f'''    <!-- HERO -->
    <section class="hero on-dark" aria-labelledby="hero-title">
      <div class="hero__media">{img_tag(n, w, h, alt, p, ' class="hero__img"', lazy=False, extra=' fetchpriority="high"')}</div>
      <div class="hero__shade" aria-hidden="true"></div>
      <div class="hero__content">
        <h1 id="hero-title" data-reveal>{h1}</h1>
        <p class="hero__lede" data-reveal>{lede}</p>
        <div class="hero__actions" data-reveal>
          {btns('dark')}
        </div>
      </div>
    </section>
'''


# ------------------------------------------------------------------ service page
def service_page(s):
    p = '../'
    confirm = f'    <!-- CONFIRM with client: {s["confirm"]} -->\n' if s.get('confirm') else '    <!-- CONFIRM with client: copy is drafted from the facts on the homepage; check before launch -->\n'
    facts = '\n        '.join(f'<li><strong>{a}</strong><span>{b}</span></li>' for a, b in s['facts'])
    if s['photos']:
        gallery = f'<div class="svc-mosaic" data-gallery data-stagger>\n          {photo_buttons(s["photos"], p)}\n        </div>'
    else:
        tiles = '\n          '.join(f'<div class="ph" data-shot="{t}"><span>{t.split(",")[0]}</span></div>' for t in s['shots'])
        gallery = f'<!-- SWAP: real photos of this work (SHOT-LIST.md) -->\n        <div class="svc-mosaic svc-mosaic--ph">\n          {tiles}\n        </div>'
    title = f'{s["name"]} in South Somerset'
    main = f'''{confirm}{photo_hero(p, s['hero'], title, s['standfirst'])}
    <section class="trust" aria-label="About our work">
      <ul class="trust__list">
        {facts}
      </ul>
    </section>

    <!-- INTRODUCTION -->
    <section class="svc-a" aria-labelledby="a-title">
      <div class="wrap svc-a__grid">
        <h2 id="a-title" data-anim="settle">{s['a_h']}</h2>
        <div class="svc-a__text">
          <p class="svc-lead">{s['a_p1']}</p>
          <p>{s['a_p2']}</p>
        </div>
      </div>
    </section>

    <!-- WHAT WE DO -->
    <section class="svc-b" aria-labelledby="b-title">
      <div class="wrap">
        <div class="svc-b__head" data-stagger>
          <h2 id="b-title" data-anim="settle">{s['b_h']}</h2>
          <p data-anim="settle">{s['b_intro']}</p>
        </div>
        <div class="svc-b__items" data-stagger>
          {items_html(s['items'])}
        </div>
        <div class="svc-b__close svc-close">
          <p>{s['close']}</p>
          <div class="svc-btns">{btns('light')}</div>
        </div>
      </div>
    </section>

    <!-- EXAMPLES -->
    <section class="svc-work" aria-labelledby="w-title">
      <div class="wrap">
        <div class="section-head" data-stagger>
          <h2 id="w-title" data-anim="settle">Examples of our work</h2>
          <p data-anim="settle">{s['w_p']}</p>
        </div>
        {gallery}
      </div>
    </section>
'''
    desc = s['desc']
    return shell(p, f'{title} | Yenstone Walling &amp; Landscaping', desc, 'service', main, 'services', slug=s['slug'])


# ------------------------------------------------------------------ about page
def about_page():
    p = ''
    why = items_html([
        ('A family firm', 'You deal with the same family from the first phone call to the final handover.'),
        ('A certified waller', 'Our walling is done by a waller qualified through the Dry Stone Walling Association.'),
        ('Local stone first', 'We match the stone of your house and your lane wherever we can, so new work sits naturally beside the old.'),
        ('Clear quotes, tidy sites', 'A written quote that sets out the work and the price, an agreed start date, and a site left tidy at the end of each day.'),
    ])
    hero = photo_hero(p, ('hero-concept-rural-wall', 1672, 941, 'A long dry stone wall running across a field towards a gate, with rolling Somerset countryside beyond'),
                      'About Yenstone Walling and Landscaping',
                      'A family firm from Yenston, near Templecombe, building walls, steps and gardens in stone since 1991.')
    process = rel(PROCESS, p)
    faq = rel(FAQ, p)
    main = f'''    <!-- CONFIRM with client: the story is drafted from the facts on the homepage. Replace with the family's own account (who started it, how it grew). -->
{hero}
    <!-- OUR STORY -->
    <section class="split" id="story" aria-labelledby="story-title">
      <figure class="split__img" data-anim="fade">
        {img_tag('tree-relief-pool', 960, 750, 'A dry stone wall with a tree carved in relief behind a swimming pool', p)}
      </figure>
      <div class="split__text">
        <div class="split__inner">
          <h2 id="story-title" data-anim="settle">Our story</h2>
          <p class="split__lead">Yenstone has been building in stone since 1991, and we are still doing it the same way: by hand, one stone at a time.</p>
          <p>We are a family firm, working from Perhams Farm at Yenston, near Templecombe. Dry stone walling is where we started and it is still the heart of what we do. It is slow, skilled work that rewards doing it properly.</p>
          <p>Everything else we build, from steps and terraces to paving and whole gardens, is shaped by that way of working. We plan the walls, the surfaces and the planting together, in local stone, so the finished garden feels settled from the first season.</p>
          <div class="split__actions">
            {btns('split', '')}
          </div>
        </div>
      </div>
    </section>

    <!-- WHY CHOOSE US -->
    <section class="svc-b svc-b--plain" aria-labelledby="why-title">
      <div class="wrap">
        <div class="svc-b__head" data-stagger>
          <h2 id="why-title" data-anim="settle">Why choose us</h2>
          <p data-anim="settle">Here is what you can expect when you call Yenstone.</p>
        </div>
        <div class="svc-b__items" data-stagger>
          {why}
        </div>
      </div>
    </section>

{process}
{faq}'''
    return shell(p, 'About us | Yenstone Walling &amp; Landscaping, Yenston, Templecombe',
                 'About Yenstone Walling and Landscaping, a family firm from Yenston near Templecombe building walls, steps and gardens in stone since 1991.',
                 'about', main, 'about')


# ------------------------------------------------------------------ gallery page
def gallery_page():
    p = ''
    items = []
    for i, n in enumerate(GALLERY_ORDER):
        w, h, alt = PHOTOS[n]
        lazy = i >= 4
        tag = img_tag(n, w, h, alt, p, lazy=lazy, extra=' decoding="async"')
        items.append(f'<li class="wall__item" style="--ar:{w / h:.4f}"><button type="button" class="svc-photo">{tag}</button></li>')
    wall = '\n        '.join(items)
    main = f'''    <!-- HERO -->
    <section class="v3-hero svc-hero on-dark" aria-labelledby="hero-title">
      <div class="v3-hero__bg" aria-hidden="true"></div>
      <div class="wrap">
        <div class="v3-hero__grid">
          <div class="v3-hero__text">
            <h1 id="hero-title" data-reveal>Gallery</h1>
            <p class="v3-hero__lede" data-reveal>Walls, steps, paving and gardens we have built across Somerset and Dorset. Select a photo to see it larger.</p>
            <div class="svc-btns" data-reveal>
              {btns('dark')}
            </div>
          </div>
          <img class="v3-hero__mark" src="{p}assets/img/logo-white.png" width="683" height="699" alt="Yenstone stone work trade mark, established 1991">
        </div>
      </div>
    </section>

    <!-- CONFIRM: add project names and locations when the client supplies them. SWAP: upgrade to 1600px+ originals (SHOT-LIST.md) -->
    <section class="wall-section" aria-label="Photographs of our work">
      <div class="wrap">
        <ul class="wall" data-gallery>
        {wall}
        </ul>
      </div>
    </section>
'''
    return shell(p, 'Gallery | Yenstone Walling &amp; Landscaping',
                 'Photographs of dry stone walls, steps, paving and gardens built by Yenstone across Somerset and Dorset.',
                 'gallery-page', main, 'gallery')


# ------------------------------------------------------------------ kept layout: version 3 (dry stone walling copy)
def version3_page():
    p = '../'
    s = SERVICES[0]
    facts = '\n          '.join(f'<li data-anim="settle"><strong>{a}</strong><span>{b}</span></li>' for a, b in s['facts'])
    main = f'''    <!-- HERO -->
    <section class="v3-hero svc-hero on-dark" aria-labelledby="hero-title">
      <div class="v3-hero__bg" aria-hidden="true"></div>
      <div class="wrap">
        <div class="v3-hero__grid">
          <div class="v3-hero__text">
            <h1 id="hero-title" data-reveal>{s['name']} in South Somerset</h1>
            <p class="v3-hero__lede" data-reveal>{s['standfirst']}</p>
            <div class="svc-btns" data-reveal>
              {btns('dark')}
            </div>
          </div>
          <img class="v3-hero__mark" src="{p}assets/img/logo-white.png" width="683" height="699" alt="Yenstone stone work trade mark, established 1991">
        </div>
        <ul class="facts" data-stagger>
          {facts}
        </ul>
      </div>
    </section>

    <!-- THE CRAFT -->
    <section class="v3-a" aria-labelledby="a-title">
      <div class="wrap">
        <h2 id="a-title" data-anim="settle">{s['a_h']}</h2>
        <div class="v3-a__cols">
          <p>{s['a_p1']}</p>
          <p>{s['a_p2']}</p>
        </div>
      </div>
    </section>

    <!-- WHAT WE BUILD -->
    <section class="v3-b on-dark" aria-labelledby="b-title">
      <div class="wrap">
        <div class="v3-b__head" data-stagger>
          <h2 id="b-title" data-anim="settle">{s['b_h']}</h2>
          <p data-anim="settle">{s['b_intro']}</p>
        </div>
        <div class="v3-b__items" data-stagger>
          {items_html(s['items'])}
        </div>
        <div class="v3-b__close svc-close">
          <p>{s['close']}</p>
          <div class="svc-btns">{btns('dark')}</div>
        </div>
      </div>
    </section>

    <!-- EXAMPLES -->
    <section class="v3-work" aria-labelledby="w-title">
      <div class="wrap">
        <div class="section-head" data-stagger>
          <h2 id="w-title" data-anim="settle">Examples of our work</h2>
          <p data-anim="settle">{s['w_p']}</p>
        </div>
        <div class="v3-gallery" data-gallery data-stagger>
          {photo_buttons(GALLERY_ORDER[:8], p)}
        </div>
      </div>
    </section>
'''
    return shell(p, 'Dry stone walling in South Somerset, layout 3 | Yenstone', s['desc'], 'v3', main, 'services', slug=s['slug'], noindex=True)


# ------------------------------------------------------------------ write everything
(SITE / 'services').mkdir(exist_ok=True)
(SITE / 'service-versions').mkdir(exist_ok=True)
for s in SERVICES:
    (SITE / 'services' / f'{s["slug"]}.html').write_text(service_page(s))
    print('wrote services/' + s['slug'] + '.html')
(SITE / 'about.html').write_text(about_page()); print('wrote about.html')
(SITE / 'gallery.html').write_text(gallery_page()); print('wrote gallery.html')
(SITE / 'service-versions' / 'version-3.html').write_text(version3_page()); print('wrote service-versions/version-3.html')
