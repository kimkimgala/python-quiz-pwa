from pathlib import Path

src = Path('tools/v111_patch.py').read_text(encoding='utf-8')
src = src.replace(
    'wire = "$(\'courseBuilderBtn\').onclick=()=>location.href=\'./course-builder.html\';"',
    'wire = "$(\'courseBuilderBtn\').onclick=()=>{location.href=\'./course-builder.html\'};"'
)
exec(compile(src, 'tools/v111_patch.py', 'exec'))
