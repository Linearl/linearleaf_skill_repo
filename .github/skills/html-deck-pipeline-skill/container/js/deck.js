/* deck.js — HTML Deck website skeleton (config-driven) */
(() => {
  let SLIDES = [];
  let PART_LABELS = {};
  let PART_ORDER = [];

  let currentIdx = 0;
  let currentPart = 'ch01';
  let loadedPartCss = new Set();

  const deck = document.getElementById('deck');
  const progressBar = document.querySelector('#deck-progress .bar');
  const partNav = document.getElementById('part-nav');
  const deckShell = document.getElementById('deck-shell');

  /* ── Part CSS loading ── */
  function loadPartCss(part) {
    if (loadedPartCss.has(part)) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `style/${part}.css`;
    link.id = `css-${part}`;
    document.head.appendChild(link);
    loadedPartCss.add(part);
  }

  /* ── Set part class on shell ── */
  function setPart(part) {
    loadPartCss(part);
    if (currentPart === part) return;
    PART_ORDER.forEach(p => deckShell.classList.remove(`part-${p}`));
    deckShell.classList.add(`part-${part}`);
    currentPart = part;
  }

  /* ── Auto-scale current slide to fit deck vertically (no layout change) ── */
  let _scaleRAF = 0;
  function applyAutoScale() {
    cancelAnimationFrame(_scaleRAF);
    _scaleRAF = requestAnimationFrame(() => {
      const slideEl = deck.querySelector('.slide.active');
      if (!slideEl) return;
      slideEl.style.transform = '';
      slideEl.style.transformOrigin = '';
      const scrollH = slideEl.scrollHeight;
      const clientH = slideEl.clientHeight;
      if (scrollH > clientH) {
        // Scale factor driven purely by vertical space; -1px safety margin prevents rounding scrollbar
        const scale = (clientH - 1) / scrollH;
        slideEl.style.transform = `scale(${scale})`;
        slideEl.style.transformOrigin = 'top center';
      }
    });
  }

  /* ── Load a slide ── */
  async function loadSlide(idx) {
    const s = SLIDES[idx];
    if (!s) return;

    setPart(s.part);
    const url = `slides/${s.part}/${s.file}`;

    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const html = await res.text();

      deck.innerHTML = html;
      const slideEl = deck.querySelector('.slide');
      if (slideEl) {
        slideEl.classList.add('active');
        slideEl.dataset.slideKey = s.part + '/' + s.file;
        applyAutoScale();
      }

      currentIdx = idx;
      updateProgress();
      updatePartNav();
      updateHash();
      // Editor hook: notify editor that a new slide has loaded
      if (window.__deckAPI && typeof window.__deckAPI.onSlideLoaded === 'function') {
        window.__deckAPI.onSlideLoaded();
      }
    } catch (err) {
      deck.innerHTML = `<div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--risk);"><p>加载失败: ${url} — ${err.message}</p></div>`;
    }
  }

  /* ── Navigate ── */
  function next() { if (currentIdx < SLIDES.length - 1) loadSlide(currentIdx + 1); }
  function prev() { if (currentIdx > 0) loadSlide(currentIdx - 1); }

  function goToPart(part) {
    const idx = SLIDES.findIndex(s => s.part === part);
    if (idx >= 0) loadSlide(idx);
  }

  /* ── Progress bar ── */
  function updateProgress() {
    const pct = ((currentIdx + 1) / SLIDES.length * 100).toFixed(1);
    if (progressBar) progressBar.style.width = pct + '%';
  }

  /* ── Part nav buttons ── */
  function buildPartNav() {
    if (!partNav) return;
    PART_ORDER.forEach(part => {
      const btn = document.createElement('button');
      btn.textContent = PART_LABELS[part];
      btn.addEventListener('click', () => goToPart(part));
      btn.dataset.part = part;
      partNav.appendChild(btn);
    });
  }

  function updatePartNav() {
    if (!partNav) return;
    partNav.querySelectorAll('button').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.part === currentPart);
    });
  }

  /* ── Hash routing ── */
  function updateHash() {
    const s = SLIDES[currentIdx];
    history.replaceState(null, '', `#${s.part}/${s.file.replace('.html','')}`);
  }

  function resolveHash() {
    const hash = window.location.hash.slice(1);
    if (!hash) return 0;
    // Match: ch03/02-feedback or ch03/2
    const parts = hash.split('/');
    if (parts.length < 2) return 0;

    const [part, slug] = parts;
    // Try by file slug first
    let idx = SLIDES.findIndex(s => s.part === part && s.file.replace('.html','') === slug);
    // Try by index within part
    if (idx < 0 && /^\d+$/.test(slug)) {
      const n = parseInt(slug, 10) - 1;
      const partSlides = SLIDES.reduce((acc, s, i) => { if (s.part === part) acc.push(i); return acc; }, []);
      if (n >= 0 && n < partSlides.length) idx = partSlides[n];
    }
    return idx >= 0 ? idx : 0;
  }

  /* ── Keyboard ── */
  function onKey(e) {
    // Don't trap if user is in an input (allow Ctrl+E regardless)
    if (e.ctrlKey && e.key === 'e') {
      e.preventDefault();
      if (window.__editor && window.__editor.toggle) window.__editor.toggle();
      return;
    }
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
      e.preventDefault();
      next();
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      prev();
    }
  }

  /* ── Config ── */
  let deckConfig = null;  // { themes: [...], fontsizes: [...] }

  async function loadConfig() {
    try {
      const res = await fetch('css/config.yaml');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const text = await res.text();
      // Minimal YAML parser for our simple structure
      deckConfig = parseSimpleYaml(text);
    } catch(e) {
      console.warn('Failed to load config.yaml, using defaults', e);
      deckConfig = {
        themes: [{ id: 'dark-theme-2', label: '暗色2', default: true }],
        fontsizes: [{ id: 'standard', label: '标准', default: true }]
      };
    }
  }

  function parseSimpleYaml(text) {
    // Parse a simple two-level YAML with list items
    const result = {};
    let section = null;
    for (const line of text.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      if (!line.startsWith(' ')) {
        section = trimmed.replace(/:.*$/, '');
        result[section] = [];
      } else if (section && trimmed.startsWith('- id:')) {
        const item = {};
        item.id = trimmed.replace(/- id:\s*/, '').trim();
        result[section].push(item);
      } else if (section && trimmed.startsWith('label:')) {
        const last = result[section][result[section].length - 1];
        if (last) last.label = trimmed.replace(/label:\s*/, '').trim();
      } else if (section && trimmed.startsWith('default:')) {
        const last = result[section][result[section].length - 1];
        if (last) last.default = trimmed.replace(/default:\s*/, '').trim() === 'true';
      }
    }
    return result;
  }

  function themeIds() { return (deckConfig?.themes || []).map(t => t.id); }
  function fontsizeIds() { return (deckConfig?.fontsizes || []).map(f => f.id); }
  function themeLabel(id) { const t = (deckConfig?.themes || []).find(t => t.id === id); return t ? t.label : id; }
  function defaultThemeId() { const t = (deckConfig?.themes || []).find(t => t.default); return t ? t.id : (deckConfig?.themes || [])[0]?.id || 'dark-theme-2'; }
  function defaultFontsizeId() { const f = (deckConfig?.fontsizes || []).find(f => f.default); return f ? f.id : (deckConfig?.fontsizes || [])[0]?.id || 'standard'; }

  /* ── Theme switching ── */
  const THEME_KEY = 'deck-theme';
  const THEME_CSS = ['tokens.css'];
  const SHARED_CSS = ['css/common/base.css', 'css/common/components.css'];

  function getTheme() {
    try {
      const stored = localStorage.getItem(THEME_KEY);
      const ids = themeIds();
      if (stored && ids.includes(stored)) return stored;
    } catch(e) {}
    return defaultThemeId();
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    // Swap CSS link hrefs to point to the selected theme directory
    const links = document.querySelectorAll('link[rel="stylesheet"][href^="css/"]');
    links.forEach(link => {
      // Extract filename from current href (e.g. "css/dark-theme-2/tokens.css" → "tokens.css")
      const parts = link.href.split('/');
      const file = parts[parts.length - 1];
      if (THEME_CSS.includes(file)) {
        link.href = `css/theme/${theme}/${file}`;
      }
    });
    const sel = document.getElementById('theme-select');
    if (sel) sel.value = theme;
  }

  function onThemeChange() {
    const sel = document.getElementById('theme-select');
    if (!sel) return;
    const theme = sel.value;
    try { localStorage.setItem(THEME_KEY, theme); } catch(e) {}
    applyTheme(theme);
  }

  function initTheme() {
    applyTheme(getTheme());
  }

  /* ── Font-size switching ── */
  const FONTSIZE_KEY = 'deck-fontsize';

  function getFontSize() {
    try {
      const stored = localStorage.getItem(FONTSIZE_KEY);
      const ids = fontsizeIds();
      if (stored && ids.includes(stored)) return stored;
    } catch(e) {}
    return defaultFontsizeId();
  }

  function applyFontSize(fontsize) {
    document.documentElement.setAttribute('data-font-size', fontsize);
    const links = document.querySelectorAll('link[rel="stylesheet"][href^="css/fontsize/"]');
    links.forEach(link => {
      link.href = `css/fontsize/${fontsize}.css`;
    });
    const sel = document.getElementById('fontsize-select');
    if (sel) sel.value = fontsize;
  }

  function onFontSizeChange() {
    const sel = document.getElementById('fontsize-select');
    if (!sel) return;
    const fontsize = sel.value;
    try { localStorage.setItem(FONTSIZE_KEY, fontsize); } catch(e) {}
    applyFontSize(fontsize);
  }

  function initFontSize() {
    applyFontSize(getFontSize());
  }

  function buildSelectors() {
    const themeSel = document.getElementById('theme-select');
    if (themeSel && deckConfig?.themes) {
      themeSel.innerHTML = '';
      for (const t of deckConfig.themes) {
        const opt = document.createElement('option');
        opt.value = t.id;
        opt.textContent = t.label;
        themeSel.appendChild(opt);
      }
    }
    const fontsizeSel = document.getElementById('fontsize-select');
    if (fontsizeSel && deckConfig?.fontsizes) {
      fontsizeSel.innerHTML = '';
      for (const f of deckConfig.fontsizes) {
        const opt = document.createElement('option');
        opt.value = f.id;
        opt.textContent = f.label;
        fontsizeSel.appendChild(opt);
      }
    }
  }

  /* ── Export single static HTML ── */

  async function exportToSingleHTML() {
    const exportBtn = document.getElementById('export-btn');
    if (exportBtn) {
      exportBtn.textContent = '导出中…';
      exportBtn.disabled = true;
    }

    try {
      // 1. Fetch all CSS
      const theme = getTheme();
      const fontsize = getFontSize();
      const themeCssPaths = THEME_CSS.map(f => `css/theme/${theme}/${f}`);
      const fontsizeCssPath = `css/fontsize/${fontsize}.css`;
      const allCssParts = PART_ORDER.map(p => `style/${p}.css`);
      const cssPaths = [...SHARED_CSS, ...themeCssPaths, fontsizeCssPath, ...allCssParts];
      const cssTexts = await Promise.all(cssPaths.map(async path => {
        try {
          const res = await fetch(path);
          return res.ok ? await res.text() : `/* ${path} not found */`;
        } catch { return `/* ${path} failed */`; }
      }));
      const allCss = cssTexts.join('\n');

      // Inject editor customizations if available
      let editorOverrides = '';
      if (window.__editor && typeof window.__editor.getCSSOverrides === 'function') {
        editorOverrides = window.__editor.getCSSOverrides();
      }

      // 2. Fetch all slides
      const slideHtmls = await Promise.all(SLIDES.map(async s => {
        try {
          const res = await fetch(`slides/${s.part}/${s.file}`);
          return res.ok ? await res.text() : `<!-- ${s.file} load failed -->`;
        } catch { return `<!-- ${s.file} load failed -->`; }
      }));

      // 3. Build the exported document
      const slidesHtml = slideHtmls.map((html, i) => {
        const s = SLIDES[i];
        // Make first slide active, rest hidden
        return html.replace(
          /class="slide\s+active"/,
          'class="slide active"'
        ).replace(
          /class="slide"/,
          i === 0 ? 'class="slide active"' : 'class="slide"'
        ).replace(
          /<section class="slide">/,
          i === 0 ? '<section class="slide active">' : '<section class="slide">'
        );
      }).join('\n');

      const title = document.title || 'HTML Deck';

      const themeOpts = (deckConfig?.themes || []).map(t =>
        `<option value="${t.id}">${t.label}</option>`
      ).join('\n            ');
      const fontsizeOpts = (deckConfig?.fontsizes || []).map(f =>
        `<option value="${f.id}">${f.label}</option>`
      ).join('\n            ');
      const themeNamesJson = JSON.stringify((deckConfig?.themes || []).map(t => t.id));
      const fontsizeNamesJson = JSON.stringify((deckConfig?.fontsizes || []).map(f => f.id));
      const defaultTheme = defaultThemeId();
      const defaultFontsize = defaultFontsizeId();
      const currentTheme = getTheme();
      const currentFontsize = getFontSize();

      const exportedHtml = `<!doctype html>
<html lang="zh-CN" data-theme="${currentTheme}" data-font-size="${currentFontsize}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${title}</title>
  <style>
${allCss}
${editorOverrides}
  </style>
  <style>
    /* Export mode: hide shell chrome, show all slides as stack */
    #part-nav, #deck-progress, #kbd-hint, #export-btn, #theme-select, #pptx-btn, #fontsize-select, #editor-toggle-btn { display: none; }
    #deck-shell { display: block; height: 100vh; overflow: hidden; padding: 0; }
    .deck { max-width: none; border-radius: 0; box-shadow: none; }
    .slide { display: none; }
    .slide.active { display: flex; flex-direction: column; }
    /* Export selects: fixed position bottom-right */
    #export-theme-select, #export-fontsize-select {
      position: fixed; bottom: 1rem; z-index: 999;
      padding: 0.35rem 0.6rem;
      border: 1px solid var(--accent);
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-size: 0.82rem; font-weight: 700;
      cursor: pointer;
      font-family: var(--font-main);
      appearance: none; -webkit-appearance: none;
      outline: none;
    }
    #export-theme-select { right: 1rem; }
    #export-fontsize-select { right: 6.5rem; }
    #export-theme-select option, #export-fontsize-select option { background: var(--bg); color: var(--text); }
  </style>
</head>
<body>
  <select id="export-theme-select" title="切换主题">
            ${themeOpts}
  </select>
  <select id="export-fontsize-select" title="切换字号">
            ${fontsizeOpts}
  </select>
  <main id="deck-shell" class="part-ch01" aria-label="${title}">
    <div class="deck" id="deck" role="region" aria-label="幻灯片">
${slidesHtml}
    </div>
  </main>
  <script>
    (() => {
      /* Theme & Fontsize */
      const THEME_KEY = 'deck-theme';
      const FONTSIZE_KEY = 'deck-fontsize';
      const THEME_NAMES = ${themeNamesJson};
      const FONTSIZE_NAMES = ${fontsizeNamesJson};
      const DEFAULT_THEME = '${defaultTheme}';
      const DEFAULT_FONTSIZE = '${defaultFontsize}';

      const themeSel = document.getElementById('export-theme-select');
      const fontsizeSel = document.getElementById('export-fontsize-select');

      function getTheme() {
        try { const v = localStorage.getItem(THEME_KEY); if (v && THEME_NAMES.includes(v)) return v; } catch(e) {}
        return DEFAULT_THEME;
      }
      function getFontsize() {
        try { const v = localStorage.getItem(FONTSIZE_KEY); if (v && FONTSIZE_NAMES.includes(v)) return v; } catch(e) {}
        return DEFAULT_FONTSIZE;
      }
      function applyTheme(t) { document.documentElement.setAttribute('data-theme', t); if (themeSel) themeSel.value = t; }
      function applyFontsize(fs) { document.documentElement.setAttribute('data-font-size', fs); if (fontsizeSel) fontsizeSel.value = fs; }
      applyTheme(getTheme());
      applyFontsize(getFontsize());
      if (themeSel) themeSel.addEventListener('change', () => { try { localStorage.setItem(THEME_KEY, themeSel.value); } catch(e) {} applyTheme(themeSel.value); });
      if (fontsizeSel) fontsizeSel.addEventListener('change', () => { try { localStorage.setItem(FONTSIZE_KEY, fontsizeSel.value); } catch(e) {} applyFontsize(fontsizeSel.value); });

      /* Slides */
      const slides = Array.from(document.querySelectorAll('.slide'));
      let idx = 0;
      function show(i) {
        slides.forEach((el, j) => el.classList.toggle('active', j === i));
        slides[i]?.classList.add('active');
        // Auto-scale
        const el = slides[i];
        if (!el) return;
        el.style.transform = '';
        el.style.transformOrigin = '';
        const sh = el.scrollHeight;
        const ch = el.clientHeight;
        if (sh > ch) {
          el.style.transform = 'scale(' + ((ch - 1) / sh) + ')';
          el.style.transformOrigin = 'top center';
        }
        idx = i;
      }
      function next() { if (idx < slides.length - 1) show(idx + 1); }
      function prev() { if (idx > 0) show(idx - 1); }
      document.addEventListener('keydown', e => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) return;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') { e.preventDefault(); next(); }
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); prev(); }
      });
      window.addEventListener('resize', () => {
        const el = slides[idx];
        if (!el) return;
        el.style.transform = '';
        const sh = el.scrollHeight;
        const ch = el.clientHeight;
        if (sh > ch) {
          el.style.transform = 'scale(' + ((ch - 1) / sh) + ')';
          el.style.transformOrigin = 'top center';
        }
      });
      show(0);
    })();
  <\/script>
</body>
</html>`;

      // 4. Trigger download (with save dialog when available)
      const blob = new Blob([exportedHtml], { type: 'text/html;charset=utf-8' });
      const defaultName = `${title.replace(/[\/\\:*?"<>|]/g, '-')}-export.html`;

      if (typeof window.showSaveFilePicker === 'function') {
        try {
          const handle = await window.showSaveFilePicker({
            suggestedName: defaultName,
            types: [{ description: 'HTML 文件', accept: { 'text/html': ['.html'] } }],
          });
          const writable = await handle.createWritable();
          await writable.write(blob);
          await writable.close();
        } catch (e) {
          if (e.name !== 'AbortError') throw e; // user cancelled, silently ignore
        }
      } else {
        // Fallback: blob download to default folder
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = defaultName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }

      if (exportBtn) {
        exportBtn.textContent = '导出 HTML';
        exportBtn.disabled = false;
      }
    } catch (err) {
      if (exportBtn) {
        exportBtn.textContent = '导出失败';
        exportBtn.disabled = false;
      }
      console.error('Export failed:', err);
    }
  }

  /* ── Export PPTX (client-side: html2canvas + pptxgenjs) ── */
  let _pptxLibsReady = false;

  async function ensurePptxLibs() {
    if (_pptxLibsReady) return;
    if (typeof html2canvas === 'undefined') {
      await new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
        s.onload = resolve;
        s.onerror = () => reject(new Error('html2canvas load failed'));
        document.head.appendChild(s);
      });
    }
    if (typeof PptxGenJS === 'undefined') {
      await new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = 'https://cdn.jsdelivr.net/npm/pptxgenjs@3.12.0/dist/pptxgen.bundle.js';
        s.onload = resolve;
        s.onerror = () => reject(new Error('pptxgenjs load failed'));
        document.head.appendChild(s);
      });
    }
    _pptxLibsReady = true;
  }

  async function exportToPPTX() {
    const pptxBtn = document.getElementById('pptx-btn');
    if (pptxBtn) {
      pptxBtn.textContent = '导出中…';
      pptxBtn.disabled = true;
    }

    try {
      await ensurePptxLibs();

      const savedIdx = currentIdx;
      const slideEls = [];
      const slideImages = [];

      // Capture each slide
      for (let i = 0; i < SLIDES.length; i++) {
        await loadSlide(i);
        // Wait briefly for layout/auto-scale to settle
        await new Promise(r => setTimeout(r, 200));

        const slideEl = deck.querySelector('.slide.active');
        if (!slideEl) continue;

        const canvas = await html2canvas(slideEl, {
          backgroundColor: null,
          scale: 2,
          useCORS: true,
          logging: false,
        });
        slideImages.push(canvas.toDataURL('image/png'));
        slideEls.push(slideEl);
      }

      // Restore original slide
      await loadSlide(savedIdx);

      // Build PPTX
      const pptx = new PptxGenJS();
      pptx.defineLayout({ name:'CUSTOM', width:'13.333', height:'7.5' });
      pptx.layout = 'CUSTOM';

      slideImages.forEach((dataUrl, i) => {
        const s = pptx.addSlide();
        s.addImage({ data: dataUrl, x: 0, y: 0, w: '13.333', h: '7.5' });
      });

      const title = document.title || 'HTML Deck';
      const defaultName = `${title.replace(/[\/\\:*?"<>|]/g, '-')}.pptx`;

      const pptxBlob = await pptx.write({ outputType: 'blob' });

      // Try save dialog, fallback to download
      if (typeof window.showSaveFilePicker === 'function') {
        try {
          const handle = await window.showSaveFilePicker({
            suggestedName: defaultName,
            types: [{ description: 'PowerPoint 文件', accept: { 'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'] } }],
          });
          const writable = await handle.createWritable();
          await writable.write(pptxBlob);
          await writable.close();
        } catch (e) {
          if (e.name !== 'AbortError') throw e;
        }
      } else {
        const url = URL.createObjectURL(pptxBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = defaultName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }

      if (pptxBtn) {
        pptxBtn.textContent = '导出 PPTX';
        pptxBtn.disabled = false;
      }
    } catch (err) {
      if (pptxBtn) {
        pptxBtn.textContent = '导出失败';
        pptxBtn.disabled = false;
      }
      console.error('PPTX export failed:', err);
    }
  }

  /* ── Init ── */
  async function init() {
    // Load config.yaml first (themes + fontsizes)
    await loadConfig();
    buildSelectors();

    // Fetch slides-config.json
    try {
      const res = await fetch('slides-config.json');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const config = await res.json();
      SLIDES = config.slides || [];
      PART_LABELS = config.parts || {};
      PART_ORDER = config.partOrder || Object.keys(config.parts || {});
      if (config.title) document.title = config.title;
    } catch (err) {
      console.error('Failed to load slides-config.json:', err);
      return;
    }

    if (!SLIDES.length) {
      deck.innerHTML = `<div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--text-faint);"><p>slides-config.json 中未配置幻灯片</p></div>`;
      return;
    }

    initTheme();
    initFontSize();
    buildPartNav();
    const startIdx = resolveHash();
    loadSlide(startIdx);
    document.addEventListener('keydown', onKey);
    window.addEventListener('hashchange', () => {
      const idx = resolveHash();
      if (idx !== currentIdx) loadSlide(idx);
    });
    window.addEventListener('resize', applyAutoScale);
    const exportBtn = document.getElementById('export-btn');
    if (exportBtn) exportBtn.addEventListener('click', exportToSingleHTML);
    const themeSel = document.getElementById('theme-select');
    if (themeSel) themeSel.addEventListener('change', onThemeChange);
    const fontsizeSel = document.getElementById('fontsize-select');
    if (fontsizeSel) fontsizeSel.addEventListener('change', onFontSizeChange);
    const pptxBtn = document.getElementById('pptx-btn');
    if (pptxBtn) pptxBtn.addEventListener('click', exportToPPTX);

    // Expose API for editor
    window.__deckAPI = {
      getCurrentSlideKey: function() {
        const s = SLIDES[currentIdx];
        return s ? s.part + '/' + s.file : null;
      },
      getCurrentSlideEl: function() {
        return deck.querySelector('.slide.active');
      },
      applyAutoScale: applyAutoScale,
      onSlideLoaded: null  // editor sets this
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
