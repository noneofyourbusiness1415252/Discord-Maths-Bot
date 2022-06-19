from http import server
import threading, os, time, logging, logging.handlers as handlers, urllib.request as request, glob


def keepAlive(bot):
    class Server(server.BaseHTTPRequestHandler):
        _bot = bot
        start = time.time()

        def log_request(self, code='', size=''):
            pass

        def do_GET(self):
            self.send_response(200)
            self.send_header(
                'Content-Type', 'font/woff2'
                if self.path == '/W.woff2' else 'text/html;charset=utf-8')
            self.send_header(
                'Cache-Control', 'max-age=31536000, immutable'
                if self.path == '/W.woff2' else 'no-cache')
            self.send_header('x-content-type-options', 'nosniff')
            self.send_header('server', 'discord-maths-bot')
            self.end_headers()
            bot = self._bot
            owner, user = bot.get_user(bot.owner_id), bot.user
            self.wfile.write(
                open(f"{os.path.dirname(__file__)}/W.woff2", 'rb').read(
                ) if self.path == '/W.woff2' else b'\n'.join(
                    [open(i, 'rb').read()
                     for i in glob.glob('logs*')]) if self.path == '/logs' else
                (f"<!DOCTYPE html><meta charset=utf-8><meta name=viewport content='width=device-width'><link rel='shortcut icon' href='{user.avatar.url}' alt=icon><html lang=en><script>window.onload=()=>setInterval(()=>{{let u=BigInt(Math.ceil(Date.now()/1000-{self.start}))\ndocument.getElementById('u').innerText=`${{u>86400n?`${{u/86400n}}d`:''}}${{u>3600n?`${{u/3600n%60n}}h`:''}}${{u>60n?`${{u/60n%24n}}m`:''}}${{`${{u%60n}}`}}s`}},1000)</script><style>@font-face{{font-family:W;src:url('W.woff2')}}*{{background-color:#FDF6E3;color:#657B83;font-family:W;text-align:center;margin:auto}}@media(prefers-color-scheme:dark){{*{{background-color:#002B36;color:#839496}}img{{height:1em}}</style><title>{user.name}</title><h1>{user.name}<img src='{user.avatar.url}'></h1><table><tr><td>Servers<td>{len(bot.guilds)}<tr><td>Latency<td>{round(bot.latency*1000 if bot.latency!=float('inf')else 0)}ms<tr><td>Uptime<td id=u>{f'<tr><td><a href=https://discord.com/users/{bot.owner_id}>DM owner</a><td>'if bot.owner_id else''}{f'<img src={owner.avatar.url}>{owner}'if owner else''}</table><br>"
                 +
                 '<div id=l></div><button type=button onclick="setInterval(()=>{let x=new XMLHttpRequest();x.onload=r=>document.getElementById(\'l\').innerText=r.srcElement.responseText;x.open(\'GET\',\'logs\');x.send()},1e3)">Show logs'
                 if os.path.isfile('logs') else '').encode())

    if os.environ['REPL_ID']:

        @bot.event
        async def on_ready():
            threading.Thread(
                target=server.HTTPServer(('',
                                          80), Server).serve_forever).start()
            owner = bot.get_user(bot.owner_id)
            print(f"Starting {bot.user}{f', made by {owner}'if owner else''}")

        intents = bot.intents
        if not (intents.presences or intents.members
                or intents.message_content):
            logger = logging.getLogger('discord')
            logger.setLevel(logging.DEBUG)
            handler = handlers.TimedRotatingFileHandler('./logs',
                                                        backupCount=1,
                                                        when='m',
                                                        interval=30)
            handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
            logger.addHandler(handler)
        owner, slug = (os.environ[x].lower()
                       for x in {'REPL_OWNER', 'REPL_SLUG'})
        try:
            request.urlopen(
                f"https://up.repl.link/add?author={owner}&repl={slug}")
        except:
            pass
    try:
        bot.run(os.environ['DISCORD_TOKEN'])
    except Exception as err:
        if hasattr(err, 'status') and err.status == 429:
            print('Rate-limit detected. Restarting repl')
            os.kill(1, 1)
        print(err)
