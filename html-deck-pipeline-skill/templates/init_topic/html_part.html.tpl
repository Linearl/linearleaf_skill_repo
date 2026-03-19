<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{topic_code} {part_name} {version}</title>
  <style>
    :root{{--bg:#0b1020;--panel:#11182d;--panel-soft:#182443;--text:#e8eefc;--muted:#aeb8d6;--brand:#6ea8ff;--cyan:#5de4ff;--focus:#ffd166;--border:#2b3a64;--ratio-w:16;--ratio-h:9;}}
    *{{box-sizing:border-box}}
    body{{margin:0;min-height:100vh;background:radial-gradient(circle at top left,rgba(110,168,255,.18),transparent 24%),linear-gradient(180deg,#101936,#0b1020);color:var(--text);font-family:"Segoe UI","Microsoft YaHei",sans-serif}}
    body[data-ratio-mode="4:3"]{{--ratio-w:4;--ratio-h:3;}}
    body[data-ratio-mode="16:10"]{{--ratio-w:16;--ratio-h:10;}}
    body[data-ratio-mode="adaptive"] .frame{{width:min(96vw,calc(100vh - 32px));}}
    body[data-ratio-mode="adaptive"] .deck{{aspect-ratio:auto;height:calc(100vh - 32px);}}
    .sr-only:not(:focus):not(:active){{clip:rect(0 0 0 0);clip-path:inset(50%);height:1px;overflow:hidden;position:absolute;white-space:nowrap;width:1px}}
    .skip-link{{position:absolute;left:12px;top:12px;z-index:20;background:#fff;color:#000;padding:8px 10px;border-radius:999px;text-decoration:none;transform:translateY(-220%)}}
    .skip-link:focus-visible{{transform:translateY(0)}}
    .frame{{width:min(96vw,calc((100vh - 32px) * var(--ratio-w) / var(--ratio-h)));margin:16px auto}}
    .deck{{position:relative;aspect-ratio:var(--ratio-w) / var(--ratio-h);border:1px solid var(--border);border-radius:20px;overflow:hidden;background:linear-gradient(180deg,rgba(16,25,54,.98),rgba(11,16,32,.98));box-shadow:0 24px 56px rgba(0,0,0,.32)}}
    .deck-chrome{{position:absolute;left:0;right:0;z-index:5;pointer-events:none}}
    .deck-chrome.bottom{{bottom:0;padding:0 1rem 1rem}}
    .status-panel{{padding:.8rem 1rem;border:1px solid rgba(255,255,255,.1);border-radius:18px;background:rgba(7,12,24,.78);backdrop-filter:blur(12px);box-shadow:0 18px 34px rgba(0,0,0,.22)}}
    .statusline{{display:flex;justify-content:space-between;align-items:center;gap:1rem;color:var(--muted);font-size:.92rem}}
    .page-num{{color:var(--text);font-weight:700;letter-spacing:.06em;white-space:nowrap}}
    .nav-hint{{text-align:right}}
    .slide{{position:absolute;inset:0;display:none;height:100%;padding:28px 28px 108px;overflow:auto}}
    .slide.active{{display:grid;grid-template-rows:auto 1fr auto;gap:14px}}
    .header,.footer{{display:flex;justify-content:space-between;align-items:center;gap:1rem;color:var(--muted)}}
    .tag,.chip,.number{{display:inline-flex;align-items:center;gap:.38rem;border-radius:999px;line-height:1}}
    .tag,.chip{{padding:6px 12px;border:1px solid #355293;background:#1a2950;color:var(--brand);font-weight:700}}
    .tag::before{{content:"◉";color:var(--cyan)}}
    .chip::before{{content:"✦";color:var(--cyan)}}
    .number{{padding:6px 12px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.06);color:var(--text);font-weight:700;letter-spacing:.05em}}
    h2{{margin:.3rem 0 .7rem;font-size:clamp(1.8rem,2.8vw,2.8rem);line-height:1.18}}
    p,li{{color:var(--muted);line-height:1.65}}
    .tip-box{{margin-top:1rem;border-radius:16px;border:1px solid rgba(93,228,255,.38);background:linear-gradient(180deg,rgba(93,228,255,.12),rgba(18,26,48,.92));padding:.9rem 1rem;color:var(--text)}}
    .symbol-list{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;padding:0;list-style:none;margin:1rem 0 0}}
    .symbol-list li{{padding:.9rem 1rem;border-radius:16px;border:1px solid var(--border);background:rgba(24,36,67,.72)}}
    :focus-visible{{outline:3px solid var(--focus);outline-offset:2px}}
    @media (max-width:1100px){{
      .frame{{width:96vw}}
      .statusline,.header,.footer{{flex-direction:column;align-items:flex-start}}
      .nav-hint{{text-align:left}}
      .symbol-list{{grid-template-columns:1fr}}
    }}
  </style>
</head>
<body data-ratio-mode="16:9">
  <a class="skip-link" href="#maincontent">跳到主要内容</a>
  <p class="sr-only" aria-live="polite" aria-atomic="true" id="liveRegion">当前第 1 页，共 {page_count} 页</p>
  <main id="maincontent" class="frame" tabindex="-1">
    <h1 class="sr-only">{topic_code} {part_name}</h1>
    <div class="deck">
      <section class="slide active" data-index="0" aria-hidden="false">
        <div class="header"><span class="tag">{part_name}</span><span class="number">01 / {page_count:02d}</span></div>
        <div>
          <span class="chip">建议替换为章节标签</span>
          <h2>{part_name}（待填充）</h2>
          <p>请按分镜稿填充该分片的全部页面内容，并优先保留“结论、证据、动作”三类信息块。</p>
          <ul class="symbol-list" aria-label="Emoji/符号美化占位示例">
            <li><strong>🎯 结论先行</strong><p>把一句话判断放到最先被看到的位置。</p></li>
            <li><strong>🔍 证据补齐</strong><p>用来源、数据点或对比关系支撑判断。</p></li>
            <li><strong>✅ 动作收口</strong><p>最后落到下一步动作与验收信号。</p></li>
          </ul>
          <div class="tip-box" role="note" aria-label="填充提示">💡 提示：标题眉标、标签、步骤图标与提示符号应优先使用统一的 Emoji/符号风格。</div>
        </div>
        <div class="footer"><span>页眉主题：{part_name}</span><span>{version} · {style_id}</span></div>
      </section>
      <div class="deck-chrome bottom">
        <div class="status-panel">
          <div class="statusline"><span id="pageNum" class="page-num">01 / {page_count:02d}</span><span id="navHint" class="nav-hint">⌨ ←/→ 或 Space 翻页 · Home/End 跳转 · ⇆ 左右滑动切页</span></div>
        </div>
      </div>
    </div>
    <script>
      const slides = Array.from(document.querySelectorAll('.slide'));
      const liveRegion = document.getElementById('liveRegion');
      const pageNum = document.getElementById('pageNum');
      const deck = document.querySelector('.deck');
      const main = document.getElementById('maincontent');
      const total = slides.length;
      let idx = slides.findIndex((slide) => slide.classList.contains('active'));
      if (idx < 0) idx = 0;

      const getTitle = (slide) => {{
        const title = slide.querySelector('h2');
        return title ? title.textContent.trim() : '未命名页面';
      }};

      const sync = (announce = true) => {{
        const current = idx + 1;
        slides.forEach((slide, slideIndex) => {{
          const isActive = slideIndex === idx;
          slide.classList.toggle('active', isActive);
          slide.setAttribute('aria-hidden', isActive ? 'false' : 'true');
        }});
        if (pageNum) pageNum.textContent = `${{String(current).padStart(2, '0')}} / ${{String(total).padStart(2, '0')}}`;
        if (liveRegion && announce) liveRegion.textContent = `当前第 ${{current}} 页，共 ${{total}} 页 — ${{getTitle(slides[idx])}}`;
      }};

      const goTo = (nextIndex, announce = true) => {{
        idx = Math.max(0, Math.min(nextIndex, slides.length - 1));
        sync(announce);
      }};

      document.addEventListener('keydown', (event) => {{
        const nextKeys = ['ArrowRight', 'ArrowDown', ' ', 'Spacebar', 'PageDown'];
        const prevKeys = ['ArrowLeft', 'ArrowUp', 'PageUp'];
        if (nextKeys.includes(event.key)) {{ event.preventDefault(); goTo(idx + 1); return; }}
        if (prevKeys.includes(event.key)) {{ event.preventDefault(); goTo(idx - 1); return; }}
        if (event.key === 'Home') {{ event.preventDefault(); goTo(0); return; }}
        if (event.key === 'End') {{ event.preventDefault(); goTo(slides.length - 1); return; }}
      }});

      let touchStartX = 0;
      let touchStartY = 0;
      deck && deck.addEventListener('touchstart', (event) => {{
        const touch = event.changedTouches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
      }}, {{ passive: true }});

      deck && deck.addEventListener('touchend', (event) => {{
        const touch = event.changedTouches[0];
        const dx = touch.clientX - touchStartX;
        const dy = touch.clientY - touchStartY;
        if (Math.abs(dx) < 50 || Math.abs(dx) <= Math.abs(dy)) return;
        if (dx < 0) goTo(idx + 1); else goTo(idx - 1);
      }}, {{ passive: true }});

      window.addEventListener('hashchange', () => {{
        if (window.location.hash === '#maincontent' && main) main.focus();
      }});

      sync(false);
    </script>
  </main>
</body>
</html>
