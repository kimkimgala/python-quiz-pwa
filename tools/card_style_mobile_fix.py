from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='.home-tools .managebar{grid-template-columns:1fr 1fr}.home-shell .cardactions{grid-template-columns:1fr auto}.home-bottom-nav'
new='.home-tools .managebar{grid-template-columns:1fr 1fr}.home-shell .cardactions{grid-template-columns:minmax(0,1fr) 76px}.home-bottom-nav'
if old not in s:
    raise SystemExit('mobile card action rule not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('mobile card action width fixed')
