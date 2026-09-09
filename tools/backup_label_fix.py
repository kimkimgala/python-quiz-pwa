from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='<button class="secondary" id="backupPrivateBtn">個人教材をバックアップ</button>'
new='<button class="secondary" id="backupPrivateBtn"><span>個人教材</span><br><span>バックアップ</span></button>'
if old not in s:
    raise SystemExit('target not found')
p.write_text(s.replace(old,new,1),encoding='utf-8')
