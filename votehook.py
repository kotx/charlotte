from sanic import Sanic, response
import aioredis
import config
import asyncio

app = Sanic(__name__)
redis = None

async def start_db():
    global redis
    print('Connecting to redis...')
    redis = await aioredis.create_redis(address=config.redis['host'], password=config.redis['password'])
    print(f'Connected to redis!')

async def update(bot, user, data_type):
    global redis
    try:
        if not int(bot) == 431164137968500746:
            return 500
        await redis.set(user, 'upvoted', expire=2592000)
        return 200
    except:
        return 500

@app.route('/api/charlotte/votes', methods=['POST'])
async def on_push(request):
    if request.headers.get('Authorization') == config.votehookauth:
        data = request.json

        try:
            user = data['user']
            data_type = data['type']
            bot = data['bot']
        except:
            return response.json({'success': False}, status=500)
    
        status = await update(bot, user, data_type)

        return response.json({'success': status==200}, status=status)
    else:
        return response.json({'success': False}, status=500)

if __name__ == '__main__':
    app.add_task(start_db())
    app.run(port=3000)
