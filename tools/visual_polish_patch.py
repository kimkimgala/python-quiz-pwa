from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* UI polish: card compactness, icons, modal harmony */'
if marker in s:
    raise SystemExit('visual polish already applied')
css=r'''
/* UI polish: card compactness, icons, modal harmony */
.home-shell .coursecard{min-height:264px;padding:15px 16px}.course-card-top{gap:10px}.course-icon{width:44px;height:44px;flex-basis:44px;border-radius:14px;font-size:20px;box-shadow:inset 0 0 0 1px rgba(47,111,237,.06)}.home-shell .coursecard h2{font-size:17px;line-height:1.35;min-height:2.7em;margin-bottom:5px}.course-badge{font-size:10px;padding:3px 7px;letter-spacing:.02em}.course-desc{font-size:13px;line-height:1.45;height:2.9em;min-height:2.9em!important;margin-top:9px}.course-card-bottom{padding-top:10px}.course-progress-copy{min-height:2.5em;font-size:11px}.course-progress-track{height:6px;margin:5px 0 10px}.home-shell .cardactions{grid-template-columns:minmax(0,1fr) 72px}.home-shell .cardactions button{min-height:44px;font-size:13px;border-radius:12px}.modalback{background:rgba(15,23,42,.46);backdrop-filter:blur(2px)}.modal{border-radius:22px;padding:20px;box-shadow:0 24px 70px rgba(15,23,42,.2);border-color:#e2e8f0}.modal h2{font-size:21px;margin:0 0 6px}.course-manage-actions{gap:9px;margin:16px 0 14px}.course-manage-actions button{min-height:48px;border-radius:13px;padding:11px 13px;text-align:left}.course-manage-actions .secondary{background:#f8fafc;color:#344054;border-color:#e2e8f0}.course-manage-actions .secondary:hover{background:#f1f5f9}.course-manage-actions .danger{background:#fff7f6;border-color:#f3c5c2}.modalactions{gap:8px}.modalactions button{min-height:46px;border-radius:12px}
@media(max-width:700px){.home-shell .coursecard{min-height:250px;padding:14px}.course-icon{width:42px;height:42px;flex-basis:42px}.home-shell .coursecard h2{font-size:16px}.course-desc{font-size:13px}.home-shell .cardactions{grid-template-columns:minmax(0,1fr) 70px}.modal{padding:18px;border-radius:20px}}
'''
needle='</style>'
if needle not in s:
    raise SystemExit('style end not found')
s=s.replace(needle,css+'\n'+needle,1)
p.write_text(s,encoding='utf-8')
