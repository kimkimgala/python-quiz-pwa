from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label):
    global s
    c=s.count(old)
    if c!=1: raise SystemExit(f'{label}: {c} matches')
    s=s.replace(old,new,1)

rep("let studyStyle='continue';","let studyStyle='continue',shuffleBeforeMock=false;",'state')
rep("questionLimit.value='all';reviewTarget.value='combined';shuffle.checked=false;studyStyle='continue';","questionLimit.value='all';reviewTarget.value='combined';shuffle.checked=false;shuffleBeforeMock=false;studyStyle='continue';",'configure')
rep("function setStudyStyle(style){studyStyle=style;syncStudyStyleUI()}","function setStudyStyle(style){studyStyle=style;$('setupMessage').textContent='';syncStudyStyleUI()}",'setStudyStyle')
old="function syncStudyStyleUI(){document.querySelectorAll('[data-study-style]').forEach(b=>b.classList.toggle('selected',b.dataset.studyStyle===studyStyle));const review=studyStyle==='review',mock=studyStyle==='mock';$('reviewTargetField').classList.toggle('hidden',!review);shuffle.disabled=mock;if(mock)shuffle.checked=true;else if(shuffle.dataset.forcedMock==='1'){shuffle.checked=false}shuffle.dataset.forcedMock=mock?'1':'0';$('styleHint').innerHTML=studyStyle==='continue'?'前回の学習位置を優先して再開します。':review?'間違えた問題・未クリア問題を既存履歴から抽出します。詳細設定で対象を絞れます。':'<span class=\"mock-note\">模試では問題順を自動でランダム化します。</span>';$('setupMessage').textContent=''}"
new="function syncStudyStyleUI(){document.querySelectorAll('[data-study-style]').forEach(b=>b.classList.toggle('selected',b.dataset.studyStyle===studyStyle));const review=studyStyle==='review',mock=studyStyle==='mock',wasMock=shuffle.dataset.forcedMock==='1';$('reviewTargetField').classList.toggle('hidden',!review);if(mock){if(!wasMock)shuffleBeforeMock=shuffle.checked;shuffle.checked=true;shuffle.disabled=true}else{shuffle.disabled=false;if(wasMock)shuffle.checked=shuffleBeforeMock}shuffle.dataset.forcedMock=mock?'1':'0';$('styleHint').innerHTML=studyStyle==='continue'?'前回の学習位置を優先して再開します。':review?'間違えた問題・未クリア問題を既存履歴から抽出します。詳細設定で対象を絞れます。':'<span class=\"mock-note\">模試では問題順を自動でランダム化します。</span>'}"
rep(old,new,'sync')
p.write_text(s,encoding='utf-8')
print('Phase UI-3 follow-up fix applied')
