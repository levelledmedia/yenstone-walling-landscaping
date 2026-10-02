#!/usr/bin/env python3
"""
Builds the inner pages of the Yenstone site from the homepage.

  services/*.html              the eight service pages (one shared design)
  about.html                   About us
  our-work.html                Our work (photo wall)
  contact.html                 Contact
  privacy-policy.html          Privacy policy
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

PLACEHOLDER = '<div class="ph" data-anim="settle"><span>Photo coming soon</span></div>'
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
AREA = between('<!-- SERVICE AREA -->', '<!-- FAQ -->')
QUOTE_FORM = re.search(r'(        <!-- TODO before launch.*?)\n      </div>\n    </section>', QUOTE, re.S).group(1)
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Perhams+Farm,+Sally+Lovells+Lane,+Yenston,+Templecombe,+BA8+0NE'


def header_for(p, current=None, slug=None):
    h = HEADER.replace('<a href="index.html" aria-current="page">Home</a>', '<a href="index.html">Home</a>')
    marks = {'home': 'index.html', 'about': 'about.html', 'work': 'our-work.html', 'contact': 'contact.html'}
    if current == 'services':
        h = h.replace('<button class="nav__toggle"', '<button class="nav__toggle" aria-current="page"').replace('<button class="menu__toggle"', '<button class="menu__toggle" aria-current="page"')
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
# Newer photos supplied as originals (jpg/png), named for what they show so each page can pick the right ones
EXT = {n: 'jpg' for n in ['landscaping-brick-path-flower-borders', 'stone-paved-passage', 'sandstone-patio-dining', 'rustic-stone-terrace', 'stone-flag-doorway', 'paved-courtyard-white-house',
                          'terraced-stone-steps', 'terraced-patio-walls', 'orchard-garden-wall', 'pond-garden-wall', 'roadside-dry-stone-wall',
                          'stone-cottage-boundary-wall', 'terraced-dry-stone-walls', 'courtyard-low-stone-wall', 'excavator-retaining-wall',
                          'excavator-stepped-groundworks', 'dumper-garden-work', 'leaf-motif-garden-gate', 'wrought-iron-railing-welding',
                          'bridge-railing-clematis', 'brick-footbridge-railings']}
EXT['spear-top-house-railings'] = 'png'
PHOTOS.update({
    'landscaping-brick-path-flower-borders': (1138, 1138, 'A brick path running between deep flower borders in a landscaped garden'),
    'stone-walling-flower-border-wall': (1440, 1440, 'A dry stone wall running beside a planted border and a paved path'),
    'stone-walling-gated-lane-wall': (1440, 1440, 'A long dry stone wall beside a narrow lane'),
    'stone-walling-new-boundary-wall': (1440, 1440, 'A newly built dry stone boundary wall with young trees planted beside it'),
    'stone-walling-tall-lane-wall': (1440, 1440, 'A tall dry stone wall rising beside a lane'),
    'stone-paved-passage': (960, 750, 'Irregular sandstone paving laid as a path beside a stone wall'),
    'sandstone-patio-dining': (640, 750, 'A sandstone patio with a metal table and chairs against a stone wall'),
    'rustic-stone-terrace': (640, 750, 'A terrace of random stone flags outside a stone house'),
    'stone-flag-doorway': (960, 750, 'Grey stone flags and gravel in front of a white front door'),
    'paved-courtyard-white-house': (640, 750, 'A large paved courtyard with seating beside a white-painted cottage'),
    'terraced-stone-steps': (640, 750, 'Stone steps and low retaining walls rising through a garden, with terracotta pots'),
    'terraced-patio-walls': (640, 750, 'A new stone terrace held by low dry stone walls'),
    'orchard-garden-wall': (640, 750, 'A dry stone wall beside a lawn and planted border, with fields beyond'),
    'pond-garden-wall': (640, 750, 'A dry stone wall behind a garden border and pond planting'),
    'roadside-dry-stone-wall': (640, 750, 'A tall coursed dry stone wall beside a road'),
    'stone-cottage-boundary-wall': (640, 750, 'A stone cottage with a new dry stone boundary wall along the lane'),
    'terraced-dry-stone-walls': (640, 750, 'A dry stone wall running along a gravel path with fields beyond'),
    'courtyard-low-stone-wall': (960, 750, 'A low dry stone wall beside a cottage doorway'),
    'excavator-retaining-wall': (960, 750, 'A mini excavator above a newly built dry stone retaining wall'),
    'excavator-stepped-groundworks': (960, 750, 'A mini excavator beside newly shuttered and concreted steps in a garden'),
    'dumper-garden-work': (640, 750, 'A tracked dumper on site in a garden during groundworks'),
    'leaf-motif-garden-gate': (533, 625, 'A wrought iron garden gate with leaf motifs between stone gate piers'),
    'wrought-iron-railing-welding': (960, 750, 'New wrought iron railings being welded on site beside a stone building'),
    'bridge-railing-clematis': (533, 625, 'A wrought iron railing with clematis beside a stone path'),
    'brick-footbridge-railings': (533, 625, 'A cobbled path between stone walls with curled wrought iron handrails'),
    'spear-top-house-railings': (960, 750, 'Black iron spear-top railings above a low stone wall in front of a stone house'),
})
GALLERY_ORDER = ['coursed-wall', 'stone-detail-iris', 'curved-wall-field', 'landscaping-brick-path-flower-borders', 'oak-gate-paving', 'lawn-curved-wall',
                 'broad-steps', 'stone-walling-flower-border-wall', 'flint-wall', 'pond-wall-bench', 'wall-lane', 'stone-walling-new-boundary-wall',
                 'tree-relief-pool', 'oak-barn-wall', 'retaining-wall-rose', 'stone-walling-gated-lane-wall', 'formal-garden-steps', 'wall-steps-deer',
                 'signpost-wall', 'stone-walling-tall-lane-wall', 'stone-house-glazing', 'gravel-drive-wall', 'retaining-wall-curve', 'lawn-gate',
                 'wall-oak-gate-lane', 'stone-bridge']
# (order chosen so the justified rows pack evenly: three photos per row at common desktop widths)

# ------------------------------------------------------------------ service copy
EST = ('Established in 1991', 'Over thirty years of landscaping and building in stone across Somerset and Dorset.')
LOCAL = ('Local stone first', 'We match the stone of your house and your lane wherever we can.')
QUOTES = ('Written quotes', 'The work and the price set out clearly before we start.')

# Order here is the order of the homepage cards and the Services dropdown:
# landscaping leads, dry stone walling second, then the rest.
SERVICES = [
    dict(
        slug='landscaping-somerset', name='Landscaping',
        desc='Landscaping in Somerset and Dorset from Yenstone: hard landscaping, garden features, outdoor improvements and bespoke projects. Call 01963 371123 for a free quote.',
        confirm='garden features and bespoke project examples are inferred from the client\'s one-line description and photos; confirm',
        standfirst='Hard landscaping, garden features, outdoor improvements and bespoke projects, planned and built as one.',
        hero=('hero-landscaping-terraced-patio', 1672, 941, 'A stone terrace and patio with low dry stone walls in a garden'),
        facts=[EST, ('One team', 'The people who plan your garden are the people who build it.'), LOCAL],
        a_h='Plan the whole garden, then build it in order',
        a_p1='Some gardens need a tidy-up. Others need a fresh start: new levels, a proper terrace, steps that make sense, borders that frame the view instead of hiding it. We look at how you use the space and how the land falls before we start.',
        a_p2='We plan the paving, steps, walls and planting together, so it feels like one garden rather than a set of separate jobs. Then we agree the order of work, so each stage leads naturally into the next.',
        b_h='What we landscape',
        b_intro='A landscaping job can be as simple as a new path or as full as a whole-garden scheme. It always starts with a visit.',
        items=[
            ('Hard landscaping', 'Terraces, paths, steps, walls and surfaces that give the garden its structure, built in stone that suits the house.'),
            ('Garden features', 'Seating areas, raised beds, water features and focal points that give a garden character and somewhere to look.'),
            ('Outdoor improvements', 'Lawns, borders and awkward levels put right, so the space you have works better for the way you use it.'),
            ('Bespoke projects', 'Something particular in mind? We work from your ideas and the site to design and build something made for your garden.'),
        ],
        close='Not sure where to start? Call us. We will come and look at the garden, talk through what you want and explain how we would approach it.',
        w_p='Recent work in Somerset and Dorset. Select a photo to see it larger.',
        photos=['stone-bridge', 'landscaping-brick-path-flower-borders', 'pond-wall-bench', 'lawn-gate', 'orchard-garden-wall', 'retaining-wall-curve', 'pond-garden-wall', 'terraced-patio-walls'],
    ),
    dict(
        slug='dry-stone-walling-somerset', name='Dry stone walling',
        desc='Dry stone walling in Somerset and Dorset from Yenstone: boundary and retaining walls, repairs and restoration, built by a certified waller. Call 01963 371123.',
        standfirst='Traditional dry stone walls, including boundary walls, retaining walls, repairs and restoration, built by hand in local stone by a certified waller.',
        hero=('hero-walling-urn-garden', 1672, 941, 'A dry stone wall with a stone urn on the pier, looking over open fields'),
        facts=[EST, ('DSWA certified', 'Qualified through the Dry Stone Walling Association.'), LOCAL],
        a_h='Built without mortar, made to last',
        a_p1='A dry stone wall holds together by weight and fit alone. Every stone is chosen, turned and set by hand so it locks against the stones around it. The wall drains freely, moves with the ground instead of cracking, and gets better with age.',
        a_p2='It is slow, skilled work, and it is where Yenstone began. We have been building walls across Somerset and Dorset since 1991, and the same care goes into everything else we build.',
        b_h='What we build and repair',
        b_intro='Whether it is a new wall or an old one that has come down, we start by looking at the stone you already have and the ground it stands on.',
        items=[
            ('Boundary and garden walls', 'Along a lane, around a field or enclosing a garden. We match the stone of your house and your lane, so a new wall looks as if it has always been there.'),
            ('Retaining walls', 'Walls that hold back sloping ground and give you level space to use. Built to drain freely, so water does not build up behind them.'),
            ('Repairs and restoration', 'We take down and rebuild walls that have leaned or collapsed, including lime-mortared walls, and reuse the original stone wherever we can. We also do insurance work and can give you a quote to pass to your insurer.'),
            ('Gateways, piers and built-in steps', 'Gateways, piers and steps set into the wall as it goes up, so they are part of the wall rather than added to it.'),
        ],
        close='Not sure what your wall needs? Call us. We will come and look, talk through the options and send you a written quote.',
        w_p='Walls we have built in Somerset and Dorset. Select a photo to see it larger.',
        photos=['tree-relief-pool', 'stone-walling-flower-border-wall', 'stone-walling-gated-lane-wall', 'stone-walling-new-boundary-wall', 'wall-lane', 'stone-walling-tall-lane-wall', 'curved-wall-field', 'stone-cottage-boundary-wall'],
    ),
    dict(
        slug='steps-and-terraces-somerset', name='Steps and terraces',
        desc='Steps and terraces in Somerset and Dorset from Yenstone: bespoke stone steps, terracing and raised landscape features designed to suit the surrounding garden. Call 01963 371123.',
        standfirst='Bespoke stone steps, terracing and raised landscape features designed to suit the surrounding garden.',
        hero=('formal-garden-steps-cinematic', 1638, 960, 'Broad stone steps rising between clipped lawns and low stone walls'),
        facts=[EST, ('Built into the land', 'Steps and terraces shaped around the way your ground falls.'), LOCAL],
        a_h='Make a slope useful',
        a_p1='A sloping garden can be hard to use. Steps and terraces turn the fall of the land into usable levels, with comfortable, safe ways to move between them.',
        a_p2='We build them in stone, with retaining walls where the ground needs holding back, so the steps, terraces and walls are one piece of work and weather together.',
        b_h='What we build',
        b_intro='Every set of steps starts with the slope in front of it. We measure, work out the levels and build to suit.',
        items=[
            ('Garden steps', 'Stone steps with even risers and treads that are comfortable to use in all weathers.'),
            ('Terraces and raised features', 'Flat, usable areas and raised landscape features, cut into a slope or built up from it and held by stone walls.'),
            ('Retaining walls', 'Dry stone walls that hold back the ground and drain freely.'),
            ('Steps built into walls', 'Stone steps set into a wall as it goes up, for gateways and changes of level.'),
        ],
        close='Got a slope that needs sorting? Call us. We will come and look, talk through the options and send you a written quote.',
        w_p='Recent work in Somerset and Dorset. Select a photo to see it larger.',
        photos=['terraced-stone-steps', 'formal-garden-steps', 'broad-steps', 'wall-steps-deer', 'retaining-wall-rose', 'terraced-patio-walls'],
    ),
    dict(
        slug='paving-and-patios-somerset', name='Paving and patios',
        desc='Paving and patios in Somerset and Dorset from Yenstone: patios, paths and paved areas in durable stone finishes for gardens and outdoor spaces. Call 01963 371123.',
        standfirst='Patios, paths and paved areas using durable stone finishes for gardens and outdoor spaces.',
        hero=('hero-paving-courtyard', 1672, 941, 'A large sandstone paved courtyard with seating beside a white-painted cottage'),
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
        photos=['sandstone-patio-dining', 'rustic-stone-terrace', 'stone-flag-doorway', 'paved-courtyard-white-house', 'stone-paved-passage', 'oak-gate-paving', 'gravel-drive-wall', 'stone-house-glazing'],
    ),
    dict(
        slug='groundworks-somerset', name='Groundworks',
        desc='Groundworks in Somerset and Dorset from Yenstone: site preparation, excavation, foundations and associated groundwork for landscaping and construction projects. Call 01963 371123.',
        confirm='scope of groundworks (excavation, foundations, drives, drainage) is inferred; confirm with the client',
        standfirst='Site preparation, excavation, foundations and associated groundwork for landscaping and construction projects.',
        hero=('excavator-stepped-groundworks', 960, 750, 'A mini excavator beside newly shuttered and concreted steps in a garden'),
        facts=[EST, ('Ready for what comes next', 'Ground prepared and finished so the next stage can start.'), QUOTES],
        a_h='The work you do not see afterwards',
        a_p1='Good groundworks are what everything else rests on: the levels, the drainage and the foundations. If they are right, walls, paving and gardens stay where they should. If they are not, nothing built on top will last.',
        a_p2='We dig, level and prepare the ground ourselves, so it is ready for what comes next, whether that is a terrace, a drive, a wall or a whole garden.',
        b_h='What we do',
        b_intro='From a small garden to a whole plot, we start by looking at the ground and what it needs to carry.',
        items=[
            ('Site preparation and excavation', 'Clearing, digging out and levelling ground for terraces, paths, drives and building work.'),
            ('Foundations', 'Firm, correctly built bases for walls, steps and paved areas.'),
            ('Drives and hardstanding', 'Prepared and surfaced for vehicles, with drainage that keeps them dry.'),
            ('Drainage', 'Getting water away from where you do not want it.'),
        ],
        close='Need the ground sorting first? Call us. We will come and look and send you a written quote.',
        w_p='Groundworks in progress. Select a photo to see it larger.',
        photos=['dumper-garden-work', 'excavator-retaining-wall'],
    ),
    dict(
        slug='septic-tanks-somerset', name='Septic tanks',
        desc='Septic tanks in Somerset and Dorset from Yenstone: installation, including the excavation, groundworks and drainage the system needs. Call 01963 371123 for a free quote.',
        confirm='scope of septic tank and drainage work, and any regulations to mention; confirm with the client. Real photos needed (see SHOT-LIST.md)',
        standfirst='Septic tank installation, including associated excavation, groundworks and drainage requirements.',
        hero=('stone-bridge-cinematic-overcast', 1639, 959, 'A low stone bridge over a stream in a planted garden'),
        facts=[EST, ('Local knowledge', 'Working across Somerset and Dorset from our base near Templecombe.'), QUOTES],
        a_h='Drainage for homes off the mains',
        a_p1='Many homes in our area are not connected to a mains sewer. A septic tank and its drainage need to be planned for the ground, the size of the household and the rules that apply.',
        a_p2='We install the tank and the drainage and put the ground back properly afterwards, so the work disappears into the garden.',
        b_h='What we do',
        b_intro='Every property is different. We start with a visit to look at the ground and what is already there.',
        items=[
            ('New installations', 'A tank and drainage fitted for a new build or a property that does not yet have a system.'),
            ('Replacing an old system', 'Taking out a failing or out-of-date tank and fitting a new one.'),
            ('Excavation and groundworks', 'The digging, bedding and backfilling the tank needs, done as part of the installation.'),
            ('Drainage and soakaways', 'The pipework and drainage that carry water away safely, and the ground put back afterwards.'),
        ],
        close='Not sure what your property needs? Call us. We will come and look and send you a written quote.',
        w_p='Photos of our septic tank installations are coming soon.',
        photos=None,
    ),
    dict(
        slug='bespoke-ironmongery-somerset', name='Bespoke ironmongery',
        desc='Bespoke ironmongery in Somerset and Dorset from Yenstone: custom-made ironwork and metal features for gardens, gates, landscaping and stonework. Call 01963 371123.',
        confirm='scope of ironmongery is inferred from the client\'s one-line description; confirm what they make.',
        standfirst='Custom-made ironwork and metal features designed to complement gardens, gates, landscaping and stonework.',
        hero=('hero-ironmongery-bridge', 1672, 941, 'A cobbled path between stone walls with curled wrought iron handrails'),
        facts=[EST, ('Made to measure', 'Ironwork designed for the place it is going, not taken off a shelf.'), QUOTES],
        a_h='Ironwork made for the place it is going',
        a_p1='The right metalwork finishes a garden: a gate that closes properly, a feature that picks up the style of the house, details that match the stone around them. Because it is custom-made, it can be designed around your garden rather than adapted to fit it.',
        a_p2='We build the landscaping and stonework as well, so the ironwork, the walls and the surfaces can be planned together and fit as one piece.',
        b_h='What we make',
        b_intro='Every piece starts with a conversation about where it is going and how it will be used.',
        items=[
            ('Gates and gate furniture', 'Custom-made gates, hinges and latches designed to suit the opening, the wall or hedge around it and the style of the property.'),
            ('Garden metalwork', 'Features and supports for the garden that suit the planting and the stonework around them.'),
            ('Fittings and details', 'Brackets, fixings and other small pieces made to match the rest of the job.'),
            ('Made to match', 'Ironwork designed alongside new landscaping and stonework, or to complement a garden that already exists.'),
        ],
        close='Have a piece in mind? Call us. We will talk through what you want and send you a written quote.',
        w_p='Ironwork we have made and fitted. Select a photo to see it larger.',
        photos=['spear-top-house-railings', 'leaf-motif-garden-gate', 'wrought-iron-railing-welding', 'bridge-railing-clematis', 'brick-footbridge-railings'],
    ),
    dict(
        slug='stone-cladding-somerset', name='Stone cladding',
        desc='Stone cladding in Somerset and Dorset from Yenstone: traditional and contemporary stone cladding, including lime and mortared walling. Call 01963 371123 for a free quote.',
        confirm='scope of cladding is inferred from the client\'s one-line description; confirm. SWAP: hero is a stand-in texture, use a real cladding photo (SHOT-LIST.md)',
        standfirst='Traditional and contemporary stone cladding, including lime and mortared walling.',
        hero=('stone-texture', 1920, 1080, 'Close view of natural stonework'),
        facts=[EST, ('Traditional and contemporary', 'Stone finishes to suit an old farmhouse or a new build.'), LOCAL],
        a_h='Stone that suits the building',
        a_p1='Stone cladding changes how a building sits in its setting. Whether the look is traditional or contemporary, the result depends on choosing the right stone and fixing it properly.',
        a_p2='We also build in lime and mortared walling, and we match the stone of your house and your lane wherever we can, so the new work belongs with the old.',
        b_h='What we do',
        b_intro='Every building is different. We start with a visit to look at the structure, the stone around it and the finish you want.',
        items=[
            ('Traditional stone cladding', 'Natural stone laid to suit older buildings and the character of the area.'),
            ('Contemporary cladding', 'Cleaner, more modern stone finishes for new builds, extensions and feature walls.'),
            ('Lime and mortared walling', 'Walls built and pointed in lime or mortar, where the job calls for it.'),
            ('Matching existing stonework', 'Stone chosen to sit beside what is already there, so new work and old read as one.'),
        ],
        close='Thinking about cladding? Call us. We will come and look and send you a written quote.',
        w_p='Photos of our stone cladding are coming soon.',
        photos=None,
    ),
]
SLUG_ORDER = [s['slug'] for s in SERVICES]

# ------------------------------------------------------------------ small builders
def btns(kind, size='btn--lg'):
    first = {'dark': 'btn--call', 'light': 'btn--dark', 'split': 'btn--dark'}[kind]
    second = 'btn--ghost' if kind == 'dark' else 'btn--outline'
    call = f'<a class="btn {first} {size}" href="tel:01963371123">{PHONE}Call 01963 371123</a>'
    quote = f'<a class="btn {second} {size}" href="#quote">Get a free quote</a>'
    return call + quote


def img_tag(name, w, h, alt, p, cls='', lazy=True, extra=''):
    loading = ' loading="lazy"' if lazy else ''
    ext = EXT.get(name, 'webp')
    return f'<img{cls} src="{p}assets/img/{name}.{ext}" width="{w}" height="{h}" alt="{alt}"{loading}{extra}>'


def photo_buttons(names, p, anim=True):
    out = []
    for n in names:
        w, h, alt = PHOTOS[n]
        a = ' data-anim="settle"' if anim else ''
        out.append(f'<button type="button" class="svc-photo"{a}>{img_tag(n, w, h, alt, p)}</button>')
    return '\n          '.join(out)


def items_html(items):
    return '\n          '.join(f'<div class="svc-item" data-anim="settle"><h3>{h}</h3><p>{t}</p></div>' for h, t in items)


def quote_block(quote, p):
    return f'    <!-- QUOTE (same as the homepage) -->\n{rel(QUOTE, p)}' if quote else ''


def shell(p, title, desc, body_class, main, current, slug=None, noindex=False, quote=True):
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
{quote_block(quote, p)}  </main>

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
    # The mosaic is laid out for 5, 6 or 8 tiles. Real photos come first; any gap is filled with plain placeholders,
    # so a page with no photos yet already looks like it will once they arrive.
    photos = s.get('photos') or []
    total = len(photos) if len(photos) in (5, 6, 8) else (8 if len(photos) > 6 else 6)
    mod = ' svc-mosaic--5' if total == 5 else ''
    tiles = photo_buttons(photos, p).split('\n          ') if photos else []
    tiles += [PLACEHOLDER] * (total - len(photos))
    swap = '<!-- SWAP: real photos of this work, replace each placeholder with a photo button (see the others) -->\n        ' if len(photos) < total else ''
    gdata = ' data-gallery' if photos else ''
    gallery = swap + f'<div class="svc-mosaic{mod}"{gdata} data-stagger>\n          ' + '\n          '.join(tiles) + '\n        </div>'
    title = f'{s["name"]} in Somerset and Dorset'
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
        ('Hands-on, start to finish', 'You deal with the people who plan and build the work, from the first phone call to the final handover.'),
        ('A certified waller', 'Our walling is done by a waller qualified through the Dry Stone Walling Association.'),
        ('Local stone first', 'We match the stone of your house and your lane wherever we can, so new work sits naturally beside the old.'),
        ('Clear quotes, tidy sites', 'A written quote that sets out the work and the price, an agreed start date, and a site left tidy at the end of each day.'),
    ])
    hero = photo_hero(p, ('hero-concept-rural-wall', 1672, 941, 'A long dry stone wall running across a field towards a gate, with rolling Somerset countryside beyond'),
                      'About Yenstone Walling and Landscaping',
                      'Landscapers and dry stone wallers from Yenston, near Templecombe, building gardens, steps and walls in stone since 1991.')
    process = rel(PROCESS, p)
    faq = rel(FAQ, p)
    main = f'''    <!-- CONFIRM with client: the story is drafted from the facts on the homepage. Replace with the firm's own account (who started it, how it grew). -->
{hero}
    <!-- OUR STORY -->
    <section class="split" id="story" aria-labelledby="story-title">
      <figure class="split__img" data-anim="fade">
        {img_tag('stone-bridge-cinematic-morning', 1536, 1024, 'A curved stone bridge over a stream in a planted garden, Somerset', p)}
      </figure>
      <div class="split__text">
        <div class="split__inner">
          <h2 id="story-title" data-anim="settle">Our story</h2>
          <p class="split__lead">Yenstone has been building in stone since 1991, and we are still doing it the same way: by hand, one stone at a time.</p>
          <p>We work from Perhams Farm at Yenston, near Templecombe. Dry stone walling is where we started, and the same patience and care go into all of the landscaping we do today. It is slow, skilled work that rewards doing it properly.</p>
          <p>Everything else we build, from steps and terraces to paving and whole gardens, is shaped by that way of working. We plan the surfaces, the walls and the planting together, in local stone, so the finished garden feels settled from the first season.</p>
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
                 'About Yenstone Walling and Landscaping, landscapers and dry stone wallers from Yenston near Templecombe, building gardens, steps and walls in stone since 1991.',
                 'about', main, 'about')


# ------------------------------------------------------------------ our work page
WORK_BATCH = 12   # photos shown at first, and added per press of "Show more"


def work_page():
    p = ''
    items = []
    for i, n in enumerate(GALLERY_ORDER):
        w, h, alt = PHOTOS[n]
        lazy = i >= 4
        tag = img_tag(n, w, h, alt, p, lazy=lazy, extra=' decoding="async"')
        items.append(f'<li class="wall__item" style="--ar:{w / h:.4f}"><button type="button" class="svc-photo">{tag}</button></li>')
    # First batch is in the page. Later batches sit in <template> elements: not rendered and not downloaded until
    # "Show more" is pressed (js/main.js). To add photos: add them to PHOTOS and GALLERY_ORDER, then rebuild.
    first, rest = items[:WORK_BATCH], items[WORK_BATCH:]
    wall = '\n        '.join(first)
    batches = '\n'.join('        <template data-wall-batch>\n          ' + '\n          '.join(rest[k:k + WORK_BATCH]) + '\n        </template>'
                        for k in range(0, len(rest), WORK_BATCH))
    main = f'''    <!-- HERO -->
    <section class="v3-hero svc-hero on-dark" aria-labelledby="hero-title">
      <div class="v3-hero__bg" aria-hidden="true"></div>
      <div class="wrap">
        <div class="v3-hero__grid">
          <div class="v3-hero__text">
            <h1 id="hero-title" data-reveal>Our work</h1>
            <p class="v3-hero__lede" data-reveal>Gardens, steps, paving and walls we have built across Somerset and Dorset. Select a photo to see it larger.</p>
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
        <div class="wall__more" hidden>
          <button class="btn btn--outline btn--lg" type="button">Show more photos</button>
          <p class="wall__status" role="status" aria-live="polite"></p>
        </div>
{batches}
      </div>
    </section>
'''
    return shell(p, 'Our work | Yenstone Walling &amp; Landscaping',
                 'Photographs of landscaping, steps, paving and dry stone walls built by Yenstone across Somerset and Dorset.',
                 'gallery-page', main, 'work')


# ------------------------------------------------------------------ contact page
def contact_page():
    p = ''
    hero = photo_hero(p, ('stone-bridge-cinematic-evening', 1536, 1024, 'A low stone bridge over a stream in a planted garden at dusk'),
                      'Contact us',
                      'Call, email or send us a few details about your garden. We will arrange a visit and send you a written quote.')
    ways = f"""    <!-- WAYS TO REACH US -->
    <section class="also" aria-labelledby="ways-title">
      <div class="wrap">
        <h2 id="ways-title" data-anim="settle">Get in touch</h2>
        <ul class="also__list" data-anim="draw" data-stagger>
          <li data-anim="settle">
            <div class="also__item">
              <h3>Call us</h3>
              <p>The quickest way. We will answer if we can, and call you back if we are on site.</p>
              <a class="also__big" href="tel:01963371123">01963 371123</a>
              <a class="tile__link" href="tel:07751278363">Mobile: 07751 278363</a>
            </div>
          </li>
          <li data-anim="settle">
            <div class="also__item">
              <h3>Email us</h3>
              <p>Tell us about the job and, if you have them, send a few photos of the site.</p>
              <a class="also__big also__big--sm" href="mailto:info@yenstonewalling.co.uk">info@yenstonewalling.co.uk</a>
            </div>
          </li>
          <li data-anim="settle">
            <div class="also__item">
              <h3>Our base</h3>
              <p>Perhams Farm, Sally Lovells Lane,<br>Yenston, Templecombe, Somerset BA8 0NE</p>
              <a class="tile__link" href="{MAPS}" target="_blank" rel="noopener">View on map</a>
            </div>
          </li>
        </ul>
      </div>
    </section>
"""
    quote = f"""    <!-- MESSAGE FORM (the form itself is shared with the homepage) -->
    <section class="quote on-dark" id="quote" aria-labelledby="quote-title">
      <div class="quote__bg" aria-hidden="true"></div>
      <div class="wrap quote__grid">
        <div class="quote__info">
          <h2 id="quote-title" data-anim="settle">Prefer to write it down?</h2>
          <p>Tell us a little about your property and what you have in mind. We will call you back to arrange a visit and send you a written quote.</p>
          <dl class="contact">
            <div><dt>Where</dt><dd>The town or postcode of the job</dd></div>
            <div><dt>What</dt><dd>What you would like done, in a sentence or two</dd></div>
            <div><dt>Photos</dt><dd>They help, but they are not essential</dd></div>
          </dl>
        </div>

{QUOTE_FORM}
      </div>
    </section>
"""
    main = f"""{hero}
{ways}
    {rel(AREA, p)}{rel(FAQ, p)}{quote}"""
    return shell(p, 'Contact us | Yenstone Walling &amp; Landscaping, Yenston, Templecombe',
                 'Contact Yenstone Walling and Landscaping at Yenston, near Templecombe: call 01963 371123, email or send a message for a free quote in Somerset and Dorset.',
                 'contact-page', main, 'contact', quote=False)


# ------------------------------------------------------------------ privacy policy (copy lives in policy_copy.py)
def policy_page():
    from policy_copy import INTRO, SECTIONS
    p = ''
    body = '\n'.join(
        f'        <div class="policy__sec">\n          <h2>{t}</h2>\n          <div class="policy__body">{x}\n          </div>\n        </div>'
        for t, x in SECTIONS)
    main = f'''    <!-- CONFIRM with client: see the note at the top of tools/policy_copy.py -->
    <!-- HERO -->
    <section class="v3-hero svc-hero on-dark" aria-labelledby="hero-title">
      <div class="v3-hero__bg" aria-hidden="true"></div>
      <div class="wrap">
        <div class="v3-hero__grid">
          <div class="v3-hero__text">
            <h1 id="hero-title" data-reveal>Privacy policy</h1>
            <p class="v3-hero__lede" data-reveal>How we look after the personal information you share with us.</p>
          </div>
          <img class="v3-hero__mark" src="{p}assets/img/logo-white.png" width="683" height="699" alt="Yenstone stone work trade mark, established 1991">
        </div>
      </div>
    </section>

    <section class="policy" aria-label="Privacy policy">
      <div class="wrap">
        <p class="policy__intro">{INTRO}</p>
{body}
      </div>
    </section>
'''
    return shell(p, 'Privacy policy | Yenstone Walling &amp; Landscaping',
                 'How Yenstone Walling and Landscaping collects, uses and protects the personal information you share with us.',
                 'policy-page', main, 'policy', quote=False)


# ------------------------------------------------------------------ kept layout: version 3 (dry stone walling copy)
def version3_page():
    p = '../'
    s = next(x for x in SERVICES if x['slug'] == 'dry-stone-walling-somerset')
    facts = '\n          '.join(f'<li data-anim="settle"><strong>{a}</strong><span>{b}</span></li>' for a, b in s['facts'])
    main = f'''    <!-- HERO -->
    <section class="v3-hero svc-hero on-dark" aria-labelledby="hero-title">
      <div class="v3-hero__bg" aria-hidden="true"></div>
      <div class="wrap">
        <div class="v3-hero__grid">
          <div class="v3-hero__text">
            <h1 id="hero-title" data-reveal>{s['name']} in Somerset and Dorset</h1>
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
    return shell(p, 'Dry stone walling in Somerset and Dorset, layout 3 | Yenstone', s['desc'], 'v3', main, 'services', slug=s['slug'], noindex=True)


# ------------------------------------------------------------------ write everything
(SITE / 'services').mkdir(exist_ok=True)
(SITE / 'service-versions').mkdir(exist_ok=True)
for s in SERVICES:
    (SITE / 'services' / f'{s["slug"]}.html').write_text(service_page(s))
    print('wrote services/' + s['slug'] + '.html')
(SITE / 'about.html').write_text(about_page()); print('wrote about.html')
(SITE / 'our-work.html').write_text(work_page()); print('wrote our-work.html')
(SITE / 'contact.html').write_text(contact_page()); print('wrote contact.html')
(SITE / 'privacy-policy.html').write_text(policy_page()); print('wrote privacy-policy.html')
(SITE / 'service-versions' / 'version-3.html').write_text(version3_page()); print('wrote service-versions/version-3.html')
