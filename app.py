import os

import aiopg
import psycopg2
from aiohttp import web

import asyncio
import db
import message_handlers
import room_handlers

async def init(app):
    app['sockets'] = []

    dsn = 'dbname=aiopg_db user=aiopg_user password=password host=127.0.0.1'

    pool = await aiopg.create_pool(dsn,
                                   cursor_factory=psycopg2.extras.RealDictCursor,
                                   echo=True)
    app['db_pool'] = pool


async def finish(app):
    for ws in app['sockets']:
        ws.close()

INDEX_FILE = os.path.join(os.path.dirname(__file__), 'index.html')
async def index(request):
    with open(INDEX_FILE, 'rb') as fp:
        return web.Response(body=fp.read(), content_type='text/html')

loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
app.router.add_get('/', index)
room_handlers.add_routers(app)
message_handlers.add_routers(app)
app.on_startup.append(init)
app.on_cleanup.append(finish)
web.run_app(app)
