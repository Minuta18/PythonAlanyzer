import fastapi
import datetime
from app import schemas
import asyncio
import runner
import base64

router = fastapi.APIRouter(prefix='/api/v1')

db = dict()

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

@router.get('/{task_id}')
async def view_task(task_id: str):
    task = db.get(task_id)
    if task is None:
        return fastapi.Response(status_code=404, content={
            'error': True,
            'message': 'This task not found',
        })
    
    task = task['task']
    if task.done():
        return {
            'error': False,
            'done': True,
            'result': task.result(),
        }
    else:
        return {
            'error': 'False',
            'done': False,
        }


