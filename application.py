# -*- coding: utf-8 -*-


from sanic import Sanic


app = Sanic("card_games")


app.static('/static', './static')


@app.listener('before_server_start')
async def before_server_start(app, loop):
    app.ctx.rooms = {}
    """
    # base no db
    app.ctx.rooms = {
        'room1': {
            'users': {
                'user1': {
                    'name': 'user1',
                    'ws': websocket,
                    'room': 'room1',
                    'ready': False,
                    'cards': [],
                    'landlord': False,
                    'score': 0,
                    'type': 'player',   # player, npc
                    'master': False,
                },
            },
            'status': 'waiting',    # waiting, playing, end
            'landlord': None,
            'last_cards': [],
            'last_user': None,
        }
    }
    """

@app.route('/')
async def index(request):
    return await app.send_file('./static/index.html')


@app.route('/ddz')
async def ddz(request):
    if not request.args.get('name'):
        # not login
        # TODO login(input name)
        return await app.send_file('./static/ddz.html')
    _room = request.args.get('room'):
    if not _room:
        # login but not in room
        # TODO create room or join room(input room)
        return await app.send_file('./static/ddz.html')
    if not app.ctx.rooms.get(room, None):
        # login but room not exist
        # TODO room list? or create room
        return await app.send_file('./static/ddz.html')

    return await app.send_file('./static/ddz.html', room=app.ctx.rooms[room])


@app.route('/ddz/create')
async def ddz_create(request):
    """create room"""
    # TODO to websocket?
    _user = request.args.get('name')
    if not _user:
        # TODO login
        return await app.send_file('./static/ddz.html')

    # TODO room configs
    _room = 'room1'     # TODO create room
    if app.ctx.rooms.get(_room, None):
        # TODO room exist random room
        _room = _room + '1'

    app.ctx.rooms[_room] = {
        'users': {
            _user: {
                'name': _user,
                'ws': None,
                'room': _room,
                'ready': False,
                'cards': [],
                'landlord': False,
                'score': 0,
                'type': 'player',
                'master': True,
            },
        },
        'status': 'waiting',
        'landlord': None,
        'last_cards': [],
        'last_user': None,
    }

    return await app.send_file('./static/ddz.html', room=app.ctx.rooms[_room])


@app.websocket('/ddz/ws')
async def ddz_ws(request, ws):
    _room = request.args.get('room')
    _user = request.args.get('name')
    if not _room or not _user:
        # TODO login
        return

    if not app.ctx.rooms.get(_room, None):
        # TODO room not exist
        return

    if not app.ctx.rooms[_room]['users'].get(_user, None):
        # TODO user not exist
        return

    app.ctx.rooms[_room]['users'][_user]['ws'] = ws

    while True:
        data = await ws.recv()
        # TODO parse data
        # TODO do something
        # TODO send data to other users
        # TODO send data to self


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
