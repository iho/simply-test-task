create_room_table_query = '''
CREATE TABLE IF NOT EXISTS public.room
(
    id SERIAL PRIMARY KEY NOT NULL,
	name VARCHAR(300),
	theme TEXT
)
'''

create_message_table_query = '''
CREATE TABLE IF NOT EXISTS public.message
(
   id SERIAL PRIMARY KEY,
   username VARCHAR(255),
   room_id INT NOT NULL REFERENCES room(id),
   text TEXT,
   ts TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc')
)'''
async def create_tables(pool):
    async with pool.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute(create_room_table_query)
        await cur.execute(create_message_table_query)


async def get_rooms(pool):
    async with pool.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute('SELECT * FROM public.room')
        return await cur.fetchall()


async def get_room_messages(pool, room_id):
    query = '''
    SELECT * FROM public.message WHERE room_id=%(id)s ORDER BY ts DESC LIMIT 100;
    '''
    async with pool.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute(query, {'id': room_id})
        messages = await cur.fetchall()
        return messages

create_room_query = '''
INSERT INTO public.room
(name, theme)
VALUES
  (%(name)s, %(theme)s)
RETURNING id;
'''

async def create_room(pool, data):
    async with pool.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute(create_room_query, data)
        return await cur.fetchone()


update_room_query = '''
UPDATE room
SET name = %(name)s, theme = %(theme)s
WHERE id = %(id)s;
'''
async def update_room(pool, data):
    async with pool.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute(update_room_query, data)

async def delete_room(pool, data):
    async with pool.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute('DELETE  FROM public.room WHERE id = %(id)s;', data)


create_message_query =  '''
INSERT INTO public.message
(room_id, username, text)
    VALUES
      (%(room_id)s, %(username)s, %(text)s)
RETURNING id, ts;
'''

async def create_message(pool, data):
    async with pool.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute(create_message_query, data)
        return await cur.fetchone()
