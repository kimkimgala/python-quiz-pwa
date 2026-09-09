from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'course-card-bottom' in s and 'courseManageModal' in s:
    raise SystemExit('card style unification already applied')

css = r'''
/* 教材カセット：全カード共通レイアウト */
.home-shell .coursegrid{grid-template-columns:repeat(2,minmax(0,1fr));align-items:stretch}.home-shell .coursecard{display:flex;flex-direction:column;height:100%;min-width:0;min-height:280px}.course-card-top{display:flex;align-items:flex-start;gap:12px}.course-main{min-width:0;flex:1}.home-shell .coursecard h2{font-size:18px;line-height:1.35;min-height:2.7em;margin:0 0 6px;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-clamp:2;overflow:hidden;overflow-wrap:anywhere}.course-desc{font-size:14px;line-height:1.5;height:3em;min-height:3em!important;margin:11px 0 0;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-clamp:2;overflow:hidden}.course-card-bottom{margin-top:auto;padding-top:12px;border-top:1px solid #f1f3f7}.course-progress-copy{display:flex;justify-content:space-between;align-items:baseline;gap:8px;min-height:2.8em;margin-top:0;font-size:12px}.course-progress-copy>*{min-width:0}.course-progress-track{margin:6px 0 12px}.home-shell .cardactions{display:grid;grid-template-columns:minmax(0,1fr) 76px;gap:8px;align-items:stretch}.home-shell .cardactions button{width:100%;min-width:0;min-height:46px;font-size:14px;padding:9px 10px}.course-manage-actions{display:grid;gap:10px;margin:16px 0}.course-manage-actions button{min-height:50px;text-align:left}.course-manage-actions .danger{border-color:#f2b8b5;background:#fff7f6;color:var(--bad)}
@media(max-width:700px){.home-shell .coursegrid{grid-template-columns:1fr}}
'''

needle = '.course-progress-track.pending>div{width:0!important}\n'
if needle not in s:
    raise SystemExit('home css insertion point not found')
s = s.replace(needle, needle + css, 1)

modal = r'''
<div class="modalback hidden" id="courseManageModal">
<div class="modal" role="dialog" aria-modal="true" aria-labelledby="courseManageTitle">
<h2 id="courseManageTitle">教材の管理</h2>
<div id="courseManageName" class="small"></div>
<div id="courseManageActions" class="course-manage-actions"></div>
<div class="modalactions"><button type="button" class="secondary" id="closeCourseManageBtn">閉じる</button></div>
</div>
</div>
'''
modal_needle = '<div class="modalback hidden" id="deleteModal">'
if modal_needle not in s:
    raise SystemExit('modal insertion point not found')
s = s.replace(modal_needle, modal + modal_needle, 1)

new_render = r'''function renderCatalog(){$('catalogTitle').textContent='マイ教材';const g=$('courseGrid');g.innerHTML='';const mine=CATALOG.courses.filter(c=>isSubscribed(c.id));for(const c of mine){const card=document.createElement('div');card.className='coursecard';card.dataset.courseId=String(c.id);const top=document.createElement('div');top.className='course-card-top';const icon=document.createElement('div');icon.className='course-icon';icon.textContent=c.local?'✎':'▣';const main=document.createElement('div');main.className='course-main';const h=document.createElement('h2');h.textContent=c.title||c.id;const badge=document.createElement('span');badge.className='course-badge'+(c.local?' local':'');badge.textContent=c.local?'自作':'共有';main.append(h,badge);top.append(icon,main);const p=document.createElement('p');p.className='course-desc';p.textContent=c.description||'（説明はありません）';const bottom=document.createElement('div');bottom.className='course-card-bottom';const copy=document.createElement('div');copy.className='course-progress-copy';copy.innerHTML=`<span>学習済み ${progressFor(c.id)}問</span><span class="course-loading">読み込み中…</span>`;const track=document.createElement('div');track.className='course-progress-track pending';track.innerHTML='<div style="width:0%"></div>';const actions=document.createElement('div');actions.className='cardactions';const learn=document.createElement('button');learn.className='primary';learn.textContent='この教材を学ぶ';learn.onclick=()=>loadCourse(c);const manage=document.createElement('button');manage.className='secondary';manage.textContent='管理';manage.onclick=()=>openCourseManage(c);actions.append(learn,manage);bottom.append(copy,track,actions);card.append(top,p,bottom);g.append(card);enrichCourseCard(c,card)}if(!mine.length){const box=document.createElement('div');box.className='coursecard empty-card';const h=document.createElement('h2');h.textContent='マイ教材はまだありません';const p=document.createElement('p');p.textContent='「教材を追加」から使いたい教材を選んでください。';box.append(h,p);g.append(box)}const available=CATALOG.courses.filter(c=>!isSubscribed(c.id)).length;$('addCoursesBtn').textContent=available?`＋ 教材を追加（${available}）`:'＋ 教材を追加';renderResumeBanner()}
let managingCourse=null;
function closeCourseManage(){$('courseManageModal').classList.add('hidden');$('courseManageActions').replaceChildren();managingCourse=null}
function addManageAction(label,className,handler){const button=document.createElement('button');button.type='button';button.className=className;button.textContent=label;button.onclick=handler;$('courseManageActions').append(button)}
function openCourseManage(course){managingCourse=course;$('courseManageName').textContent=course.title||course.id;$('courseManageActions').replaceChildren();if(course.local){addManageAction('教材を編集する','secondary',()=>{location.href='./course-builder.html?edit='+encodeURIComponent(course.id)});addManageAction('共有用JSONを書き出す','secondary',()=>{const data=loadPrivateCourses()[course.id];if(!data){alert('教材データが見つかりません。');return}downloadText(data.course_id+'.json',JSON.stringify(data,null,2)+'\n')});addManageAction('この端末から削除する','danger',()=>{if(!confirm('個人教材「'+(course.title||course.id)+'」と学習成績をこの端末から完全に削除しますか？'))return;if(deletePrivateCourse(course.id))closeCourseManage()})}else{addManageAction('学習履歴をリセット','danger',()=>{if(!confirm('「'+(course.title||course.id)+'」の学習履歴をリセットしますか？'))return;localStorage.removeItem(progressKey(course.id));closeCourseManage();renderCatalog()});addManageAction('マイ教材から外す','secondary',()=>{closeCourseManage();openDelete(course)})}$('courseManageModal').classList.remove('hidden')}
'''

pattern = re.compile(r"function renderCatalog\(\)\{.*?\}\nfunction openDelete\(course\)", re.S)
m = pattern.search(s)
if not m:
    raise SystemExit('renderCatalog function block not found')
s = s[:m.start()] + new_render + 'function openDelete(course)' + s[m.end():]

bind_needle = "$ ('cancelDeleteBtn')"
# add close handler near existing modal handlers using a precise snippet
handler_needle = "$ ('confirmDeleteBtn')"

needle2 = "$('confirmDeleteBtn').onclick=confirmDelete;$('cancelDeleteBtn').onclick=closeDelete;$('closeAddBtn').onclick=()=>$('addModal').classList.add('hidden');"
if needle2 not in s:
    raise SystemExit('modal handler insertion point not found')
s = s.replace(needle2, "$('confirmDeleteBtn').onclick=confirmDelete;$('cancelDeleteBtn').onclick=closeDelete;$('closeCourseManageBtn').onclick=closeCourseManage;$('closeAddBtn').onclick=()=>$('addModal').classList.add('hidden');", 1)

# safety checks
required = [
    'className=\'course-card-bottom\'',
    "manage.textContent='管理'",
    "function openCourseManage(course)",
    'id="courseManageModal"',
    "addManageAction('教材を編集する'",
    "addManageAction('共有用JSONを書き出す'",
    "addManageAction('この端末から削除する'",
    "addManageAction('学習履歴をリセット'",
    "addManageAction('マイ教材から外す'",
]
for token in required:
    if token not in s:
        raise SystemExit('missing expected token: ' + token)
if "edit.textContent='編集'" in s or "erase.textContent='削除'" in s:
    raise SystemExit('legacy direct edit/delete buttons remain in renderCatalog')

p.write_text(s, encoding='utf-8')
print('card style unification applied')
