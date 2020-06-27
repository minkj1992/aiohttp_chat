from aiohttp import web
from aiohttp_session import get_session


async def db_handler(app, handler):
    async def middleware(request):
        if not all(*map(request.path.startswith, ('/static/', '/_debugtoolbar'))):
            request.db = app.db

        response = await handler(request)
        return response

    return middleware


async def authorize(app, handler):
    async def middleware(request):
        def _check_path(path):
            for r in ['/login', '/static/', '/signin', '/signout', '/_debugtoolbar/']:
                if path.startswith(r):
                    return False
            return True

        session = await get_session(request)
        if session.get('user'):
            return await handler(request)
        elif _check_path(request.path):
            url = request.app.router['login'].url()
            raise web.HTTPFound(url)  # ?
            return handler(request)  # TODO: 실행 될까?
        else:
            return await handler(request)

    return middleware
