from mindustry_server_stats.database.database import Database
from mindustry_server_stats.database.popos.server import Server
from mindustry_server_stats.globals import app
from flask import render_template, abort, request

from mindustry_server_stats.utils import server_exists, get_server_display


@app.route("/server/<server_id>")
def server(server_id: str):
    database = Database()

    if not server_exists(database, server_id):
        abort(400, "The specified server couldn't be found.")

    query = database.cursor.execute("SELECT MAX(players), MAX(latency), MAX(wave) FROM datapoints "
                                    "INNER JOIN servers ON datapoints.server_id = servers.id "
                                    "WHERE servers.id = ?;", [server_id])
    players, latency, wave = query.fetchone()
    requested_server: Server | type[Server] = database.get_server(server_id)

    # Experimental mobile device detection code
    # mobile_css = '<link href="/static/mobile.css" rel="stylesheet">'
    # user_platform = request.user_agent.string
    # if (user_platform is not None) and (user_platform.lower() in "windows linux"):
    #     mobile_css = ''

    mobile_css = ''

    return render_template("server.html", player_max = players, latency_max = latency, wave_max = wave,
                           server_display = get_server_display(requested_server), mobile_css = mobile_css,
                           server_id = requested_server.id)
