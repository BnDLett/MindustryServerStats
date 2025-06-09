from mindustry_server_stats.database.database import Database
from mindustry_server_stats.globals import app
from flask import render_template

@app.route("/")
def index():
    database = Database()

    query = database.cursor.execute("SELECT MAX(players), MAX(latency), MAX(wave) FROM datapoints;")
    players, latency, wave = query.fetchone()

    return render_template("index.html", player_max = players, latency_max = latency, wave_max = wave,
                           server = "mindustry.ddns.net")
