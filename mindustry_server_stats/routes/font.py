import gzip
from pathlib import Path

from flask import Response

from mindustry_server_stats.globals import app


CURRENT_FILE = Path(__file__)
CURRENT_PARENT = CURRENT_FILE.parent


@app.route('/font')
def font():
    font_data = Path(f"{CURRENT_PARENT.parent}/static/mindustry.woff2").read_bytes()
    # compressed_file = gzip.compress(font_file.read_bytes())
    # print(len(compressed_file))

    response = Response(
        font_data,
        200,
        # {"Content-Encoding": "gzip"},
        content_type="font/woff2"
    )

    return response
