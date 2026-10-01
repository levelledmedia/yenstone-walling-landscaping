(() => {
  'use strict';

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /* Year */
  const year = $('#year');
  if (year) year.textContent = new Date().getFullYear();

  /* Header: transparent over the hero, solid once scrolled past it */
  const header = $('.site-header');
  const setHeader = () => {
    const solid = window.scrollY > 40;
    header.classList.toggle('is-solid', solid);
    header.classList.toggle('on-dark', !solid);
  };
  setHeader();
  window.addEventListener('scroll', setHeader, { passive: true });

  /* Mobile menu (native dialog gives focus trap + Esc) */
  const menu = $('#menu');
  const menuBtn = $('.menu-btn');
  if (menu && menuBtn) {
    menuBtn.addEventListener('click', () => menu.showModal());
    $('.menu__close', menu).addEventListener('click', () => menu.close());
    menu.addEventListener('click', (e) => {
      if (e.target.closest('a')) menu.close();
    });
  }

  /* Services dropdown (desktop nav): opens on hover or from the arrow button, closes on Esc, outside click or focus leaving */
  $$('.has-sub').forEach((item) => {
    const btn = $('.nav__toggle', item);
    let timer = 0;
    const set = (open) => {
      item.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
    };
    btn.addEventListener('click', () => {
      // a mouse user who hovered it open and then clicks the arrow keeps it open
      if (item.dataset.hover) { delete item.dataset.hover; set(true); return; }
      set(!item.classList.contains('is-open'));
    });
    item.addEventListener('pointerenter', (e) => {
      if (e.pointerType !== 'mouse') return;
      clearTimeout(timer);
      if (!item.classList.contains('is-open')) item.dataset.hover = '1';
      set(true);
    });
    item.addEventListener('pointerleave', (e) => {
      if (e.pointerType !== 'mouse') return;
      delete item.dataset.hover;
      timer = setTimeout(() => set(false), 160);
    });
    item.addEventListener('focusout', (e) => { if (!item.contains(e.relatedTarget)) set(false); });
    item.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && item.classList.contains('is-open')) { set(false); btn.focus(); }
    });
    document.addEventListener('pointerdown', (e) => { if (!item.contains(e.target)) set(false); });
  });

  /* Mobile menu: Services expands to show every service */
  $$('.menu__toggle').forEach((btn) => {
    const list = document.getElementById(btn.getAttribute('aria-controls'));
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', String(open));
      list.hidden = !open;
    });
  });

  /* Lightbox */
  const lb = $('#lightbox');
  const gallery = $('[data-gallery]');
  if (lb && gallery) {
    const lbImg = $('img', lb);
    const lbCap = $('figcaption', lb);
    const buttons = $$('button', gallery);
    let index = 0;

    const show = (i) => {
      index = (i + buttons.length) % buttons.length;
      const img = $('img', buttons[index]);
      lbImg.src = img.currentSrc || img.src;
      lbImg.alt = img.alt;
      lbCap.textContent = `${img.alt} (${index + 1} of ${buttons.length})`;
      lbImg.classList.remove('is-swapping');
      void lbImg.offsetWidth; // restart the fade
      lbImg.classList.add('is-swapping');
    };

    buttons.forEach((btn, i) => {
      btn.setAttribute('aria-label', `View larger: ${$('img', btn).alt}`);
      btn.addEventListener('click', () => { show(i); lb.showModal(); });
    });
    $('.lightbox__prev', lb).addEventListener('click', () => show(index - 1));
    $('.lightbox__next', lb).addEventListener('click', () => show(index + 1));
    $('.lightbox__close', lb).addEventListener('click', () => lb.close());
    lb.addEventListener('click', (e) => { if (e.target === lb || e.target.tagName === 'FIGURE') lb.close(); });
    lb.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });
  }

  /* Sliders (filmstrip, testimonials): arrows, keyboard, mouse drag, optional progress line,
     optional endless loop (data-loop) and slow auto-scroll (data-autoscroll). */
  const reducedForSlider = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  $$('[data-slider]').forEach((track) => {
    const name = track.dataset.slider;
    const prev = $(`[data-slider-btn="${name}:prev"]`);
    const next = $(`[data-slider-btn="${name}:next"]`);
    const bar = $(`[data-slider-bar="${name}"]`);

    /* Endless loop: one copy of the items before and after the originals. Whenever the track is
       idle, or on every frame while auto-scrolling, we jump by exactly one set width, which is invisible. */
    const looping = track.hasAttribute('data-loop');
    let originals = [];
    let before = [];
    const setWidth = () => (before.length ? originals[0].offsetLeft - before[0].offsetLeft : 0);
    const normalise = () => {
      const sw = setWidth();
      if (!sw) return 0;
      const l = track.scrollLeft;
      if (l < sw * 0.5) { track.scrollLeft = l + sw; return sw; }
      if (l > sw * 1.5) { track.scrollLeft = l - sw; return -sw; }
      return 0;
    };
    if (looping) {
      originals = Array.from(track.children);
      const makeClones = () => originals.map((el, i) => {
        const c = el.cloneNode(true);
        c.removeAttribute('data-anim');
        c.removeAttribute('id');
        c.setAttribute('aria-hidden', 'true');
        c.dataset.clone = '';
        if (c.matches('button, a')) c.tabIndex = -1;
        $$('button, a', c).forEach((x) => { x.tabIndex = -1; });
        // a clone of a photo opens the same photo in the viewer
        if (c.matches('button')) c.addEventListener('click', () => originals[i].click());
        return c;
      });
      before = makeClones();
      const after = makeClones();
      before.forEach((c) => track.insertBefore(c, originals[0]));
      after.forEach((c) => track.appendChild(c));
      const recentre = () => { track.scrollLeft = setWidth(); };
      recentre();
      window.addEventListener('resize', recentre);
    }

    const update = () => {
      const max = track.scrollWidth - track.clientWidth;
      if (looping) {
        const sw = setWidth() || 1;
        const frac = (((track.scrollLeft % sw) + sw) % sw) / sw;
        const visible = Math.min(1, track.clientWidth / sw);
        if (bar) bar.style.transform = `scaleX(${Math.max(visible, 0.08) + (1 - Math.max(visible, 0.08)) * frac})`;
        return;
      }
      const pos = max > 0 ? track.scrollLeft / max : 0;
      const visible = track.scrollWidth ? track.clientWidth / track.scrollWidth : 1;
      if (bar) bar.style.transform = `scaleX(${Math.max(visible, 0.08) + (1 - Math.max(visible, 0.08)) * pos})`;
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= max - 2;
    };
    const by = (dir) => track.scrollBy({ left: dir * track.clientWidth * 0.8, behavior: reducedForSlider ? 'auto' : 'smooth' });
    if (prev) prev.addEventListener('click', () => by(-1));
    if (next) next.addEventListener('click', () => by(1));

    let idleTimer = 0;
    let dragging = false;
    track.addEventListener('scroll', () => {
      update();
      if (looping) {
        clearTimeout(idleTimer);
        idleTimer = setTimeout(() => { if (!dragging) normalise(); }, 140);
      }
    }, { passive: true });
    window.addEventListener('resize', update);
    track.addEventListener('keydown', (e) => {
      if (e.target !== track) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); by(1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); by(-1); }
    });
    $$('img', track).forEach((img) => img.addEventListener('load', update));
    update();

    // Mouse drag (touch and trackpad already scroll natively)
    let startX = 0, startLeft = 0, down = false, moved = false;
    track.addEventListener('pointerdown', (e) => {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      down = true; moved = false; startX = e.clientX; startLeft = track.scrollLeft;
    });
    window.addEventListener('pointermove', (e) => {
      if (!down) return;
      const dx = e.clientX - startX;
      if (!moved && Math.abs(dx) > 5) { moved = true; dragging = true; track.classList.add('is-dragging'); }
      if (moved) track.scrollLeft = startLeft - dx;
    });
    window.addEventListener('pointerup', () => {
      if (!down) return;
      down = false;
      dragging = false;
      track.classList.remove('is-dragging');
      if (looping) normalise();
    });
    // A drag must not open the lightbox or follow a link
    track.addEventListener('click', (e) => {
      if (moved) { e.stopPropagation(); e.preventDefault(); moved = false; }
    }, true);

    // Optional slow auto-scroll. Pauses on hover and off-screen; any interaction stops it for good.
    if (track.hasAttribute('data-autoscroll') && !reducedForSlider) {
      const SPEED = 26; // px per second
      let stopped = false, onScreen = false, hovered = false, last = 0, pos = 0;
      const stop = () => {
        if (stopped) return;
        stopped = true;
        track.classList.remove('is-auto');
      };
      const frame = (t) => {
        if (stopped) return;
        requestAnimationFrame(frame);
        if (!onScreen || hovered || document.hidden) { last = 0; return; }
        if (!last) { last = t; pos = track.scrollLeft; return; }
        const dt = Math.min(t - last, 64);
        last = t;
        pos += (SPEED * dt) / 1000;
        if (!looping) {
          const max = track.scrollWidth - track.clientWidth;
          pos = Math.min(max, pos);
          track.scrollLeft = pos;
          if (pos >= max - 1) stop();
          return;
        }
        track.scrollLeft = pos;
        pos += normalise();
      };
      if ('IntersectionObserver' in window) {
        new IntersectionObserver((entries) => {
          onScreen = entries[0].isIntersecting;
          if (onScreen && !stopped) track.classList.add('is-auto');
        }, { threshold: 0.4 }).observe(track);
      }
      ['pointerdown', 'touchstart', 'keydown', 'focusin'].forEach((ev) => track.addEventListener(ev, stop, { passive: true }));
      track.addEventListener('wheel', (e) => { if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) stop(); }, { passive: true });
      track.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') hovered = true; });
      track.addEventListener('pointerleave', () => { hovered = false; last = 0; });
      [prev, next].forEach((b) => b && b.addEventListener('click', stop));
      setTimeout(() => requestAnimationFrame(frame), 1200);
    }
  });

  /* Reveal on scroll: one observer, each element animates once.
     Items revealed in the same batch inside a [data-stagger] parent arrive in order (--i).
     A [data-anim-group] (e.g. a slider) reveals all of its items together when the group scrolls
     into view, so cards that sit off-screen are already in place when you scroll to them. */
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const allAnim = $$('[data-anim]');
  const groups = $$('[data-anim-group]');
  const solo = allAnim.filter((el) => !el.closest('[data-anim-group]'));
  if (allAnim.length) {
    if (prefersReduced || !('IntersectionObserver' in window)) {
      allAnim.forEach((el) => el.classList.add('is-in'));
    } else {
      const whenLoaded = (el) => {
        // Wait for photos to load and decode first, so nothing pops in half-drawn
        const imgs = el.tagName === 'IMG' ? [el] : $$('img', el);
        return imgs.length
          ? Promise.race([
              Promise.all(imgs.map((img) => (img.decode ? img.decode().catch(() => {}) : Promise.resolve()))),
              new Promise((resolve) => setTimeout(resolve, 1500)),
            ])
          : Promise.resolve();
      };
      const reveal = new IntersectionObserver((entries) => {
        const counts = new Map();
        entries
          .filter((en) => en.isIntersecting)
          .sort((a, b) => (a.target.compareDocumentPosition(b.target) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1))
          .forEach((en) => {
            const el = en.target;
            reveal.unobserve(el);
            if (el.hasAttribute('data-anim-group')) {
              $$('[data-anim]', el).forEach((child, i) => {
                child.style.setProperty('--i', Math.min(i, 4));
                child.classList.add('is-in');
              });
              return;
            }
            const parent = el.closest('[data-stagger]');
            if (parent) {
              const n = counts.get(parent) || 0;
              el.style.setProperty('--i', n);
              counts.set(parent, n + 1);
            }
            whenLoaded(el).then(() => el.classList.add('is-in'));
          });
      }, { threshold: 0.18, rootMargin: '0px 0px -6% 0px' });
      solo.forEach((el) => reveal.observe(el));
      groups.forEach((el) => reveal.observe(el));
      document.documentElement.classList.add('anim-ready');
    }
  }

  /* Photo wall (gallery): each photo fades in once it has loaded, so lazy loading never pops */
  $$('.wall img').forEach((img) => {
    const done = () => img.classList.add('is-loaded');
    if (img.complete && img.naturalWidth) done();
    else { img.addEventListener('load', done, { once: true }); img.addEventListener('error', done, { once: true }); }
  });

  /* FAQ: smooth open and close */
  $$('.faq details').forEach((d) => {
    const summary = $('summary', d);
    summary.addEventListener('click', (e) => {
      if (prefersReduced || !d.animate) return;
      e.preventDefault();
      if (d._anim) d._anim.cancel();
      const cs = getComputedStyle(d);
      const borders = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth);
      const opts = { duration: 300, easing: 'cubic-bezier(.2,.7,.2,1)' };
      const start = d.offsetHeight;
      d.style.overflow = 'hidden';
      if (!d.open) {
        d.open = true;
        const end = d.offsetHeight;
        d._anim = d.animate({ height: [`${start}px`, `${end}px`] }, opts);
        $('p', d).animate({ opacity: [0, 1] }, { duration: 400, easing: opts.easing });
      } else {
        const end = summary.offsetHeight + borders;
        d._anim = d.animate({ height: [`${start}px`, `${end}px`] }, opts);
        d._anim.onfinish = () => { d.open = false; };
      }
      d._anim.onfinish = ((prev) => () => { if (prev) prev(); d.style.overflow = ''; d._anim = null; })(d._anim.onfinish);
      d._anim.oncancel = () => { d.style.overflow = ''; };
    });
  });

  /* Map: pan and zoom only after a click, so scrolling the page never gets caught by the map */
  $$('[data-map]').forEach((m) => {
    const veil = $('.area__veil', m);
    if (!veil) return;
    veil.addEventListener('click', () => m.classList.add('is-active'));
    m.addEventListener('mouseleave', () => m.classList.remove('is-active'));
    document.addEventListener('pointerdown', (e) => { if (!m.contains(e.target)) m.classList.remove('is-active'); });
  });

  /* Quote form: validation + success state.
     No backend yet. Set data-endpoint on the form (Formspree, Netlify, WordPress...) to send for real. */
  const form = $('#quote-form');
  const done = $('#form-done');
  if (form) {
    const rules = {
      name: (v) => (v.trim() ? '' : 'Enter your name so we know who to ask for.'),
      phone: (v) => {
        const digits = v.replace(/[^\d]/g, '');
        if (!v.trim()) return 'Enter a phone number so we can call you back.';
        return digits.length >= 10 && digits.length <= 13 && /^[\d\s()+\-]+$/.test(v)
          ? '' : 'Enter a UK phone number, for example 01963 371123.';
      },
      email: (v) => (!v.trim() || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? '' : 'Check the email address. It should look like name@example.com.'),
    };

    const check = (input) => {
      const rule = rules[input.name];
      if (!rule) return true;
      const msg = rule(input.value);
      const field = input.closest('.field');
      $('.field__error', field).textContent = msg;
      field.classList.toggle('has-error', !!msg);
      input.setAttribute('aria-invalid', msg ? 'true' : 'false');
      return !msg;
    };

    $$('input', form).forEach((input) => {
      input.addEventListener('blur', () => { if (input.value) check(input); });
      input.addEventListener('input', () => { if (input.closest('.field')?.classList.contains('has-error')) check(input); });
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const inputs = $$('input[name="name"], input[name="phone"], input[name="email"]', form);
      const results = inputs.map(check);
      const firstBad = inputs.find((_, i) => !results[i]);
      if (firstBad) { firstBad.focus(); return; }

      if ($('input[name="website"]', form).value) return; // honeypot

      const endpoint = form.dataset.endpoint;
      const btn = $('button[type="submit"]', form);
      if (endpoint) {
        btn.disabled = true;
        try {
          const res = await fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
          if (!res.ok) throw new Error(res.status);
        } catch (err) {
          btn.disabled = false;
          let msg = $('.form__error', form);
          if (!msg) {
            msg = document.createElement('p');
            msg.className = 'field__error form__error';
            msg.setAttribute('role', 'alert');
            btn.after(msg);
          }
          msg.textContent = 'That did not send. Please try again, or call us on 01963 371123.';
          return;
        }
      } else {
        console.warn('[quote form] No data-endpoint set: submission was NOT sent anywhere.');
      }

      form.hidden = true;
      done.hidden = false;
      done.focus();
    });
  }
})();
