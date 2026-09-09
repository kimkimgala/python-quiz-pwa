from pathlib import Path

p = Path('course-builder.html')
s = p.read_text(encoding='utf-8')

if 'wizard-progress-card' in s:
    raise SystemExit('Phase UI-4 already applied')

css = r'''
.wizard-progress-card{background:transparent;border:0;padding:0;margin:0 0 14px}.wizard-progress{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.wizard-progress button{display:flex;align-items:center;gap:9px;min-height:54px;text-align:left;border:1px solid var(--border);border-radius:16px;background:#fff;color:var(--muted);padding:10px 12px;font-size:13px}.wizard-progress button[aria-current="step"]{border-color:var(--accent);background:var(--soft);color:#1849a9;box-shadow:0 0 0 2px rgba(47,111,237,.08)}.step-num{width:30px;height:30px;flex:0 0 30px;border-radius:10px;background:#f2f4f7;display:flex;align-items:center;justify-content:center;font-weight:900}.wizard-progress button[aria-current="step"] .step-num{background:var(--accent);color:#fff}.step-copy strong{display:block;font-size:14px;color:var(--text)}.wizard-progress button[aria-current="step"] .step-copy strong{color:#1849a9}.step-eyebrow{font-size:12px;font-weight:900;color:var(--accent);letter-spacing:.06em;margin-bottom:5px}.wizard-step{scroll-margin-top:12px}.wizard-step.hidden-step{display:none}.wizard-footer{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:18px;padding-top:14px;border-top:1px solid #e7ebf1}.wizard-footer .next{grid-column:2}.wizard-footer.single .next{grid-column:1/-1}.wizard-footer button{min-height:52px}.step-intro{margin:-6px 0 14px;color:var(--muted);font-size:14px;line-height:1.55}.builder-hero{border-radius:24px;padding:20px}.builder-hero h1{font-size:clamp(26px,4vw,36px)}
'''
needle = '@media(max-width:720px){'
assert needle in s
s = s.replace(needle, css + '@media(max-width:720px){.wizard-progress{grid-template-columns:1fr}.wizard-progress button{min-height:48px}.wizard-footer{grid-template-columns:1fr}.wizard-footer .next{grid-column:auto}', 1)

s = s.replace('<title>教材作成アシスタント v1.11</title>', '<title>教材作成 | スタディカード</title>', 1)
s = s.replace('<a href="./">← 学習アプリへ戻る</a><span class="pill">v1.11</span>', '<a href="./">← マイ教材へ戻る</a><span class="pill">教材作成</span>', 1)
s = s.replace('<section class="card"><h1>教材作成アシスタント</h1><div class="sub">作成した教材は原則としてこの端末だけに保存します。v1.11では編集・上書き・ID衝突チェック・保存容量エラー対応を強化しました。共有したい場合だけ共有用JSONを書き出します。</div></section>', '<section class="card builder-hero"><h1>教材作成アシスタント</h1><div class="sub">基本情報 → 問題入力 → 保存・書き出しの3ステップで教材を作成します。作成途中の入力内容は、ステップを移動してもそのまま保持されます。</div></section>', 1)

intro_end = '</section><section class="card"><h2>1. 教材情報</h2>'
assert intro_end in s
progress = '''</section><section class="wizard-progress-card" aria-label="教材作成ステップ"><div class="wizard-progress"><button type="button" data-step-go="1" aria-current="step"><span class="step-num">1</span><span class="step-copy"><strong>基本情報</strong><span>教材名・分類</span></span></button><button type="button" data-step-go="2"><span class="step-num">2</span><span class="step-copy"><strong>問題入力</strong><span>手入力・CSV</span></span></button><button type="button" data-step-go="3"><span class="step-num">3</span><span class="step-copy"><strong>保存</strong><span>保存・共有</span></span></button></div></section><section class="card wizard-step" data-step="1"><div class="step-eyebrow">STEP 1 / 3</div><h2>基本情報</h2><div class="step-intro">まず教材の名前や分類を設定します。分類情報などの任意項目は、必要なものだけ入力してください。</div>'''
s = s.replace(intro_end, progress, 1)

step1_to_2 = '</div></div></section><section class="card"><h2>2. CSV / Excelから一括読込</h2>'
assert step1_to_2 in s
s = s.replace(step1_to_2, '</div></div><div class="wizard-footer single"><button type="button" class="primary next" data-step-go="2">次へ：問題入力</button></div></section><section class="card wizard-step hidden-step" data-step="2"><div class="step-eyebrow">STEP 2 / 3</div><h2>CSV / Excelから一括読込</h2><div class="step-intro">CSVを使わない場合は、このまま下の「問題を追加」から1問ずつ入力できます。</div>', 1)

qhead = '<section class="card"><div class="question-head"><h2>3. 問題</h2>'
assert qhead in s
s = s.replace(qhead, '<section class="card wizard-step hidden-step" data-step="2"><div class="question-head"><div><div class="step-eyebrow">STEP 2 / 3</div><h2>問題入力</h2></div>', 1)

q_to_save = '<div id="questions"></div></section><section class="card"><h2>4. 保存・共有</h2>'
assert q_to_save in s
s = s.replace(q_to_save, '<div id="questions"></div><div class="wizard-footer"><button type="button" class="secondary" data-step-go="1">← 基本情報へ</button><button type="button" class="primary next" data-step-go="3">次へ：保存・書き出し</button></div></section><section class="card wizard-step hidden-step" data-step="3"><div class="step-eyebrow">STEP 3 / 3</div><h2>保存・書き出し</h2><div class="step-intro">内容を確認して、この端末へ保存するか、共有用JSONを書き出します。</div>', 1)

end_save = '</section></main><script>(function(){'
assert end_save in s
s = s.replace(end_save, '<div class="wizard-footer"><button type="button" class="secondary" data-step-go="2">← 問題入力へ</button><button type="button" class="secondary next" data-step-go="1">基本情報を見直す</button></div></section></main><script>(function(){', 1)

wizard_js = r'''<script>(function(){'use strict';var currentStep=1;function showStep(step){step=Number(step);if(step<1||step>3)return;currentStep=step;document.querySelectorAll('.wizard-step').forEach(function(el){el.classList.toggle('hidden-step',Number(el.getAttribute('data-step'))!==step)});document.querySelectorAll('[data-step-go]').forEach(function(btn){if(btn.closest('.wizard-progress')){if(Number(btn.getAttribute('data-step-go'))===step)btn.setAttribute('aria-current','step');else btn.removeAttribute('aria-current')}});var target=document.querySelector('.wizard-step[data-step="'+step+'"]');if(target)requestAnimationFrame(function(){target.scrollIntoView({behavior:'smooth',block:'start'})})}document.querySelectorAll('[data-step-go]').forEach(function(btn){btn.addEventListener('click',function(){showStep(btn.getAttribute('data-step-go'))})});window.addEventListener('builder-edit-loaded',function(){showStep(1)});showStep(1)})();</script>'''
assert '</body>' in s
s = s.replace('</body>', wizard_js + '</body>', 1)

# Safety checks: preserve all existing functional controls and exactly three visual steps.
for token in ['id="courseId"','id="csvFile"','id="importCsvBtn"','id="addQuestionBtn"','id="saveLocalBtn"','id="downloadBtn"','id="validateBtn"','id="previewBtn"']:
    if token not in s:
        raise SystemExit('missing preserved control: '+token)
if s.count('data-step="1"') != 1 or s.count('data-step="3"') != 1 or s.count('data-step="2"') != 2:
    raise SystemExit('unexpected wizard step structure')
if 'AI' in wizard_js:
    raise SystemExit('AI feature must not be added')

p.write_text(s, encoding='utf-8')
print('Phase UI-4 patch applied')
