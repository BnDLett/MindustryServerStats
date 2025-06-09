from flask import render_template

from mindustry_server_stats.database.database import Database
from mindustry_server_stats.database.popos.server import Server
from mindustry_server_stats.globals import app
from mindustry_server_stats.utils import get_server_display


@app.route('/')
def index():
    database = Database()
    servers = database.get_servers()

    menu_html = ''
    server: Server
    for server in servers:
        menu_html += (f'<li><button class="server" onclick=\'window.location.href = "/server/{server.id}"\'>'
                      f'{get_server_display(server)}'
                      f'</button></li>')

    query = database.cursor.execute("SELECT COUNT(*) FROM servers;")
    count = query.fetchone()[0]

    return render_template('index.html', servers=menu_html, count=count)
