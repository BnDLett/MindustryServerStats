import gzip
import json
from datetime import timedelta, datetime
from time import time_ns

from flask import request, abort, make_response

from mindustry_server_stats.database.database import Database
from mindustry_server_stats.globals import app, log, MAX_DELAY
from mindustry_server_stats.utils import get_data, server_exists


@app.route('/raw_datapoints/<server_id>')
def raw_datapoints(server_id: str):
    maximum_data_time = 2_592_000  # aka 30 days
    lower_limit = request.args.get('seconds_of_data')

    if lower_limit is None:
        abort(400, "Missing lower limit for the range.")
    elif not server_exists(Database(), server_id):
        abort(400, f"Couldn't find server: {server_id}.")

    try:
        range_minimum = timedelta(seconds=float(lower_limit))
    except ValueError:
        abort(400, "Malformed lower limit.")

    if float(lower_limit) > maximum_data_time:
        abort(403, "A client is only allowed to request 60 seconds worth of data.")

    start = time_ns()
    fields = get_data(server_id, datetime.now() - range_minimum, MAX_DELAY)
    content = gzip.compress(json.dumps(fields).encode('utf-8'), 5)
    end = time_ns()
    log.info(f"Get data: {(end - start) * 0.000001} ms | {(end - start)} ns")

    response = make_response(content)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = 'application/json'

    return response
