from flask import send_file

from mindustry_server_stats.globals import app


@app.route('/favicon.ico')
def favicon():
    return send_file('static/icon.png')
