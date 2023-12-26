import fastapi
import datetime
from app import schemas
import asyncio
import runner
import base64

router = fastapi.APIRouter(prefix='/api/v1')

db = dict()
cache = dict()

@router.post('/')
async def create_task(create_task: schemas.CreateTaskSchema):
    global db
    filename = str(hash(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))) + '.py'
    code = base64.b64decode(create_task.code.encode('utf-8'))
    with open('./uploads/' + filename, 'w') as f:
        f.write(code.decode('utf-8'))

    ins = runner.inspect.Inspector('./uploads/' + filename)

    loop = asyncio.get_running_loop()
    task = loop.create_task(ins.inspect())    

    db[filename[:-3]] = {
        'done': False,
        'id': filename[-3],
        'task': task,
    }

    return {
        'id': filename[:-3],
        'done': False,
    }

# @router.options('/')
# async def create_task_options():
#     return fastapi.Response(headers={'Access-Control-Allow-Origin': '*'})

def render_dict(dct: dict):
    return f'''<ul class="ul">
    {[f'{key}: {value}' if type(value) != dict else f'{key}: ...<button class="opening-btn">show</button>{render_dict(value)}' for key, value in dct.items()]}
</ul>
'''

def render_html(result: dict):
    inner_html = '''<table class="res-table">
    <tbody>
        <tr>
            <td><b>Строка</b></td>
            <td><b>Переменные</b></td>
        </tr>
'''
    
    print(result)
    for line, value in result:
        inner_html += f'''<tr><td>{ line }</td><td>{ render_dict(value) }</td></tr>'''
    inner_html += '''</tbody></table>'''
    return inner_html

@router.get('/{task_id}')
async def view_task(task_id: str):
    global cache
    task = cache.get(task_id)
    if task is not None:
        return task

    task = db.get(task_id)
    if task is None:
        return fastapi.Response(status_code=404, content=str({
            'error': True,
            'message': 'This task not found',
        }))

    task = task['task']
    if task.done():
        cache.update({task_id: {
            'error': False,
            'done': True,
            'result': task.result(),
            'html': render_html(task.result()),
        }})
        return cache[task_id]
    else:
        return {
            'error': 'False',
            'done': False,
        }


