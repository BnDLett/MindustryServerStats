from flask import request

from mindustry_server_stats.database.database import Database
from mindustry_server_stats.globals import app


@app.route("/sitemap")
def sitemap():
    database = Database()

    base_domain = request.args.get("base_domain", default="mindustry-stats.lettsn.org")
    base_protocol = request.args.get("base_protocol", default="https")
    index_url = f"{base_protocol}://{base_domain}/"

    links: list[str] = [index_url]

    server_ids = database.get_server_ids()
    for server_id in server_ids:
        links.append(f"{index_url}server/{server_id[0]}")

    return "\n".join(links)
