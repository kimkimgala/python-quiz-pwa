from pathlib import Path
import re

# ---------- course-builder.html ----------
p = Path('course-builder.html')
s = p.read_text(encoding='utf-8')
s = s.replace('教材作成アシスタント v1.10', '教材作成アシスタント v1.11')
s = s.replace('<span class="pill">v1.10</span>', '<span class="pill">v1.11</span>')
s = s.replace(
    '作成した教材は原則としてこの端末だけに保存します。共有したい場合だけ、共有用JSONを書き出してGitHubへ登録します。入力内容はブラウザ内だけで処理します。',
    '作成した教材は原則としてこの端末だけに保存します。v1.11では編集・上書き・ID衝突チェック・保存容量エラー対応を強化しました。共有したい場合だけ共有用JSONを書き出します。'
)

if 'id="v111-builder-stability"' not in s:
    addon = r'''<script id="v111-builder-stability">
(function(){'use strict';
var PRIVATE_KEY='private_courses_v1',SUB_KEY='subscribed_courses_v1',SHARED_IDS_KEY='shared_course_ids_v1';
function $(id){return document.getElementById(id)}function tv(v){return String(v==null?'':v).trim()}
function loadMap(){try{var x=JSON.parse(localStorage.getItem(PRIVATE_KEY));return x&&typeof x==='object'&&!Array.isArray(x)?x:{}}catch(e){return{}}}
function showError(msg){var b=$('message');if(!b){alert(msg);return}b.className='notice error';b.textContent=msg}
function showOk(msg){var b=$('message');if(!b){alert(msg);return}b.className='notice ok';b.textContent=msg}
function buildCourse(){var cards=document.querySelectorAll('.question-card'),qs=[];for(var i=0;i<cards.length;i++){var e=cards[i],rows=e.querySelectorAll('.option-row'),ops=[];for(var j=0;j<rows.length;j++){var k=tv(rows[j].querySelector('.optkey').value),v=tv(rows[j].querySelector('.opttext').value);if(k&&v)ops.push([k,v])}qs.push({day:tv(e.querySelector('.day').value),number:Number(e.querySelector('.number').value),type:e.querySelector('.type').value,question:tv(e.querySelector('.question').value),options:ops,answer:tv(e.querySelector('.answer').value),explanation:tv(e.querySelector('.explanation').value)})}return{course_id:tv($('courseId').value),title:tv($('title').value),description:tv($('description').value),category:tv($('category').value),difficulty:tv($('difficulty').value),audience:tv($('audience').value),author:tv($('author').value),version:tv($('courseVersion').value),updated_at:tv($('updatedAt').value),study_time:tv($('studyTime').value),tags:tv($('tags').value).split(',').map(tv).filter(Boolean),subtitle:tv($('subtitle').value),section_label:tv($('sectionLabel').value)||'章',clear_count:Number($('clearCount').value),questions:qs}}
function validate(d){if(!/^[A-Za-z0-9][A-Za-z0-9_-]*$/.test(d.course_id))return'教材IDが不正です。';if(!d.title)return'教材名を入力してください。';if(!Number.isInteger(d.clear_count)||d.clear_count<1)return'クリア回数は1以上の整数にしてください。';if(!d.questions.length)return'問題を1問以上追加してください。';var nums={};for(var i=0;i<d.questions.length;i++){var q=d.questions[i];if(!q.day)return'問題'+(i+1)+': 章・区分を入力してください。';if(!Number.isInteger(q.number))return'問題'+(i+1)+': 問題番号は整数にしてください。';if(nums[q.number])return'問題番号が重複しています。';nums[q.number]=1;if(!q.question)return'問題'+(i+1)+': 問題文を入力してください。';if(q.options.length<2)return'問題'+(i+1)+': 選択肢を2個以上入力してください。';if(!q.options.some(function(o){return o[0]===q.answer}))return'問題'+(i+1)+': 正解に対応する選択肢がありません。';if(!q.explanation)return'問題'+(i+1)+': 解説を入力してください。'}return''}
function editId(){try{return new URLSearchParams(location.search).get('edit')||''}catch(e){return''}}
async function sharedIds(){try{var r=await fetch('./catalog.json',{cache:'no-store'});if(r.ok){var d=await r.json(),a=(d.courses||[]).map(function(c){return String(c.id)});try{localStorage.setItem(SHARED_IDS_KEY,JSON.stringify(a))}catch(e){}return new Set(a)}}catch(e){}try{return new Set(JSON.parse(localStorage.getItem(SHARED_IDS_KEY))||[])}catch(e){return new Set()}}
function quotaMsg(e){return e&&((e.name==='QuotaExceededError')||(e.code===22)||(e.code===1014))?'端末の保存容量が不足しています。先に個人教材をバックアップし、不要な教材を削除してください。':'個人教材を保存できませんでした。 '+String(e&&e.message?e.message:e)}
function setFields(d){$('courseId').value=d.course_id||'';$('title').value=d.title||'';$('description').value=d.description||'';$('category').value=d.category||'';$('difficulty').value=d.difficulty||'';$('audience').value=d.audience||'';$('author').value=d.author||'';$('courseVersion').value=d.version||'';$('updatedAt').value=d.updated_at||'';$('studyTime').value=d.study_time||'';$('tags').value=Array.isArray(d.tags)?d.tags.join(','):'';$('subtitle').value=d.subtitle||'';$('sectionLabel').value=d.section_label||'章';$('clearCount').value=d.clear_count||3;var box=$('questions');box.innerHTML='';(d.questions||[]).forEach(function(q){$('addQuestionBtn').click();var cards=document.querySelectorAll('.question-card'),c=cards[cards.length-1];c.querySelector('.day').value=q.day;c.querySelector('.number').value=q.number;c.querySelector('.type').value=q.type||'四者択一';c.querySelector('.question').value=q.question||'';c.querySelector('.explanation').value=q.explanation||'';var rows=c.querySelectorAll('.option-row');for(var i=0;i<rows.length;i++){rows[i].querySelector('.opttext').value=''}(q.options||[]).forEach(function(o,i){if(i<rows.length){rows[i].querySelector('.optkey').value=o[0];rows[i].querySelector('.opttext').value=o[1]}});c.querySelector('.answer').value=q.answer||'A'})}
async function saveLocal(){var d=buildCourse(),err=validate(d);if(err){showError(err);return}var remote=await sharedIds();if(remote.has(d.course_id)){showError('教材ID「'+d.course_id+'」は共有教材で使用されています。別の教材IDにしてください。');return}var map=loadMap(),editing=editId(),exists=!!map[d.course_id];if(exists&&editing!==d.course_id&&!confirm('同じ教材IDの個人教材があります。上書きしますか？'))return;if(editing&&editing!==d.course_id&&map[editing]){if(!confirm('教材IDを変更すると旧IDの個人教材は削除されます。続けますか？'))return;delete map[editing]}map[d.course_id]=d;try{localStorage.setItem(PRIVATE_KEY,JSON.stringify(map));var ids=[];try{ids=JSON.parse(localStorage.getItem(SUB_KEY))||[]}catch(e){}if(ids.indexOf(d.course_id)<0)ids.push(d.course_id);if(editing&&editing!==d.course_id)ids=ids.filter(function(x){return x!==editing});localStorage.setItem(SUB_KEY,JSON.stringify(ids));showOk(exists||editing?'個人教材を更新しました。':'個人教材として保存しました。GitHubには送信されません。');setTimeout(function(){location.href='./'},700)}catch(e){showError(quotaMsg(e))}}
function install(){var old=$('saveLocalBtn');if(old){var btn=old.cloneNode(true);old.parentNode.replaceChild(btn,old);btn.addEventListener('click',saveLocal)}var id=editId();if(id){var d=loadMap()[id];if(!d){showError('編集対象の個人教材が見つかりません。');return}setTimeout(function(){setFields(d);$('courseId').focus()},0)}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(install,0)});else setTimeout(install,0);
})();
</script>'''
    s = s.replace('</body>', addon + '</body>', 1)
p.write_text(s, encoding='utf-8')

# ---------- index.html ----------
p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = s.replace('PWA版 v1.10・個人教材・共有教材・カテゴリ・検索・教材作成・オフライン対応', 'PWA版 v1.11・安定化・個人教材編集・バックアップ・共有教材・オフライン対応')
old = '<div class="managebar" style="gap:10px;flex-wrap:wrap"><button class="secondary" id="addCoursesBtn">教材を追加</button><button class="secondary" id="courseBuilderBtn">教材を作成</button></div>'
new = '<div class="managebar" style="gap:10px;flex-wrap:wrap"><button class="secondary" id="addCoursesBtn">教材を追加</button><button class="secondary" id="courseBuilderBtn">教材を作成</button><button class="secondary" id="backupPrivateBtn">個人教材をバックアップ</button><button class="secondary" id="restorePrivateBtn">個人教材を復元</button><input id="restorePrivateFile" type="file" accept="application/json,.json" class="hidden"></div>'
if old not in s:
    raise SystemExit('managebar target missing')
s = s.replace(old, new, 1)
marker = 'function privateCourseEntries(){'
helper = r'''function savePrivateCourses(map){try{localStorage.setItem(PRIVATE_COURSES_KEY,JSON.stringify(map));return true}catch(e){alert(e&&e.name==='QuotaExceededError'?'端末の保存容量が不足しています。バックアップ後に不要な個人教材を削除してください。':'個人教材を保存できませんでした。\n'+String(e));return false}}
function remoteCourseIds(){const ids=new Set();for(const c of CATALOG.courses||[]){if(!c.local)ids.add(String(c.id))}return ids}
function refreshCatalogWithPrivate(){const remote=(CATALOG.courses||[]).filter(c=>!c.local);CATALOG.courses=mergePrivateCourses(remote);renderCatalog()}
function deletePrivateCourse(id){const map=loadPrivateCourses();if(!map[id])return false;delete map[id];if(!savePrivateCourses(map))return false;unsubscribeCourse(id);localStorage.removeItem(progressKey(id));refreshCatalogWithPrivate();return true}
function downloadText(name,text){const blob=new Blob([text],{type:'application/json;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000)}
function backupPrivateCourses(){const map=loadPrivateCourses();const pkg={format:'python-quiz-private-backup',version:1,exported_at:new Date().toISOString(),courses:Object.values(map)};downloadText('private-courses-backup.json',JSON.stringify(pkg,null,2))}
async function restorePrivateCourses(file){let pkg;try{pkg=JSON.parse(await file.text())}catch(e){alert('バックアップJSONを読み込めませんでした。');return}if(!pkg||pkg.format!=='python-quiz-private-backup'||!Array.isArray(pkg.courses)){alert('このファイルは個人教材バックアップではありません。');return}const remote=remoteCourseIds(),map=loadPrivateCourses();for(const d of pkg.courses){if(!d||!d.course_id||!Array.isArray(d.questions)||!d.questions.length){alert('不正な教材データが含まれています。復元を中止しました。');return}if(remote.has(String(d.course_id))){alert('共有教材と同じID「'+d.course_id+'」が含まれるため復元できません。');return}}const dup=pkg.courses.filter(d=>map[d.course_id]).map(d=>d.course_id);if(dup.length&&!confirm('既存の個人教材 '+dup.join(', ')+' を上書きして復元しますか？'))return;for(const d of pkg.courses)map[d.course_id]=d;if(!savePrivateCourses(map))return;for(const d of pkg.courses)subscribeCourse(d.course_id);refreshCatalogWithPrivate();alert('個人教材を復元しました。')}
'''
if 'function backupPrivateCourses()' not in s:
    if marker not in s:
        raise SystemExit('private entry marker missing')
    s = s.replace(marker, helper + marker, 1)
oldmerge = 'data.courses=mergePrivateCourses(data.courses);CATALOG=data;initializeSubscriptions();renderCatalog();'
newmerge = "try{localStorage.setItem('shared_course_ids_v1',JSON.stringify(data.courses.map(c=>String(c.id))))}catch(e){}data.courses=mergePrivateCourses(data.courses);CATALOG=data;initializeSubscriptions();renderCatalog();"
if oldmerge in s:
    s = s.replace(oldmerge, newmerge, 1)
oldcatch = "}catch(e){$('catalogTitle').textContent='教材一覧を読み込めません';$('courseGrid').textContent=String(e)}"
newcatch = "}catch(e){CATALOG={title:'マイ教材',courses:privateCourseEntries()};initializeSubscriptions();renderCatalog();if(!CATALOG.courses.length){$('catalogTitle').textContent='オフライン：共有教材一覧を取得できません';$('courseGrid').textContent='個人教材もありません。オンライン時に再度開いてください。'}}"
if oldcatch in s:
    s = s.replace(oldcatch, newcatch, 1)
old_actions = "const del=document.createElement('button');del.className='danger';del.textContent='教材管理';del.onclick=()=>openDelete(c);\nactions.append(learn,del);card.append(h,p,meta,actions);g.append(card);"
new_actions = "if(c.local){const edit=document.createElement('button');edit.className='secondary';edit.textContent='編集';edit.onclick=()=>{location.href='./course-builder.html?edit='+encodeURIComponent(c.id)};const erase=document.createElement('button');erase.className='danger';erase.textContent='完全削除';erase.onclick=()=>{if(confirm('個人教材「'+(c.title||c.id)+'」と学習成績をこの端末から完全に削除しますか？'))deletePrivateCourse(c.id)};actions.append(learn,edit,erase)}else{const del=document.createElement('button');del.className='danger';del.textContent='教材管理';del.onclick=()=>openDelete(c);actions.append(learn,del)}card.append(h,p,meta,actions);g.append(card);"
if old_actions not in s:
    raise SystemExit('course card actions target missing')
s = s.replace(old_actions, new_actions, 1)
wire = "$('courseBuilderBtn').onclick=()=>location.href='./course-builder.html';"
if wire not in s:
    raise SystemExit('builder wire missing')
s = s.replace(wire, wire + "\n$('backupPrivateBtn').onclick=backupPrivateCourses;\n$('restorePrivateBtn').onclick=()=>$('restorePrivateFile').click();\n$('restorePrivateFile').addEventListener('change',async e=>{const f=e.target.files&&e.target.files[0];if(f)await restorePrivateCourses(f);e.target.value=''});", 1)
p.write_text(s, encoding='utf-8')

# ---------- service-worker.js ----------
p = Path('service-worker.js')
s = p.read_text(encoding='utf-8')
s = re.sub(r"const CACHE_NAME='python-quiz-pwa-v1-[^']+';", "const CACHE_NAME='python-quiz-pwa-v1-11';", s, count=1)
old = "  if(u.origin===location.origin&&u.pathname.endsWith('.json')){"
new = "  if(e.request.mode==='navigate'||(u.origin===location.origin&&u.pathname.endsWith('.html'))){e.respondWith(fetch(e.request).then(r=>{if(r.ok){const copy=r.clone();caches.open(CACHE_NAME).then(c=>c.put(e.request,copy));}return r}).catch(()=>caches.match(e.request).then(x=>x||caches.match('./index.html'))));return;}\n  if(u.origin===location.origin&&u.pathname.endsWith('.json')){"
if old not in s:
    raise SystemExit('service worker target missing')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')

# ---------- README.md ----------
p = Path('README.md')
s = p.read_text(encoding='utf-8')
s = re.sub(r'^# Python Quiz PWA v1\.\d+', '# Python Quiz PWA v1.11', s, count=1, flags=re.M)
note = '''
## v1.11 v2.0前安定化

- 個人教材の編集・上書き保存・完全削除
- 共有教材との教材ID衝突を保存時に拒否
- 個人教材の一括バックアップ／復元
- localStorage容量不足時の明示エラー
- オフラインで共有カタログが取得できない場合も個人教材を利用可能
- HTMLナビゲーションをネットワーク優先にして旧版画面の残留を抑制

'''
if '## v1.11 v2.0前安定化' not in s:
    pos = s.find('\n', s.find('\n') + 1)
    s = s[:pos+1] + note + s[pos+1:]
p.write_text(s, encoding='utf-8')
