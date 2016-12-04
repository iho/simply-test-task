from aiohttp import web
from aiohttp.web import Response, WebSocketResponse, WSMsgType
import db 
import json

async def send_message(request):
    id = int(request.match_info['id'])
    data = await request.json()
    data = {field: data[field] for field in ['username', 'text']}
    data['room_id'] = id
    resp = await db.create_message(request.app['db_pool'], data)
    resp['ts'] = resp['ts'].isoformat()
    data.update(resp)
    for ws in request.app['sockets']:
        if ws is not resp:
            ws.send_str(json.dumps(data))
    return web.json_response(data)

async def get_messages(request):
    id = int(request.match_info['id']) 
    messages = await db.get_room_messages(request.app['db_pool'], id)
    for message  in messages:
        message['ts'] = message['ts'].isoformat()
    messages.reverse()
    return web.json_response(messages)

async def wshandler(request):
    resp = WebSocketResponse()
    ok, protocol = resp.can_prepare(request)
    if not ok:
        return Response(text='Only websockets', content_type='text/html')
    await resp.prepare(request)

    try:
        print('Someone joined.')
        for ws in request.app['sockets']:
            ws.send_str('Someone joined')
        request.app['sockets'].append(resp)

        async for msg in resp:
            if msg.type == WSMsgType.TEXT:
                for ws in request.app['sockets']:
                    if ws is not resp:
                        ws.send_str(msg.data)
            else:
                return resp
        return resp

    finally:
        request.app['sockets'].remove(resp)
        print('Someone disconnected.')
        for ws in request.app['sockets']:
            ws.send_str('Someone disconnected.')

def add_routers(app):
    app.router.add_post('/message/{id}', send_message)
    app.router.add_get('/message/{id}', get_messages)
    app.router.add_get('/ws', wshandler)
