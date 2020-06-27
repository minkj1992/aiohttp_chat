import asyncio
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from middlewares import db_handler, authorize
from settings import *
from routes import routes


async def init(loop):
    app = web.Application(loop=loop, middlewares=[
        session_middleware(EncryptedCookieStorage(SECRET_KEY)),
        authorize,
        db_handler,
    ])

    # route part
    for route in routes:
        method, path, handler, name = route
        app.router.add_route(method=method, path=path, handler=handler, name=name)
    app.router.add_static('/static', 'static', name='static')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
