from aiohttp import web

import db
from utils import get_admin_logins, is_admin

async def create_room(request):
    data = await request.json()
    assert 'theme' in data
    assert 'name' in data
    if not is_admin(data):
        return web.json_response({
            'status': 'Access denied',
        }, status=403)
    res = await db.create_room(request.app['db_pool'], data)
    return web.json_response({
        'status': 'Succesfuly created',
        'room_id': res['id']
    })

async def rooms(request):
    data = await db.get_rooms(request.app['db_pool'])
    return web.json_response(data)

async def room_ud(request):
    id = int(request.match_info['id'])
    data = await request.json()
    status = 'Unknow'
    if not is_admin(data):
        return web.json_response({
            'status': 'Access denied',
        }, status=403)
    if request.method == 'DELETE':
        await db.delete_room(request.app['db_pool'], {'id': id})
        status = 'Succesfuly deleted'
    if request.method == 'PATCH':
        assert 'theme' in data
        assert 'name' in data
        data['id'] = id
        await db.update_room(request.app['db_pool'], data)
        status = 'Succesfuly updated'
    return web.json_response({'status': status})

async def admins(request):
    return web.json_response(get_admin_logins())


def add_routers(app):
    app.router.add_get('/admins', admins)
    app.router.add_post('/room', create_room)
    app.router.add_get('/room', rooms)
    app.router.add_route('patch', '/room/{id}', room_ud)
    app.router.add_route('delete', '/room/{id}', room_ud)
    app.router.add_static('/static', './static')
