#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from influxdb import InfluxDBClient
import sys
import json
from pathlib import Path
import gpxpy

if __name__ == '__main__':

    if len(sys.argv) != 3 or not sys.argv[1].endswith('.json') or not sys.argv[2].endswith('.gpx'):
        print(f'Usage: {sys.argv[0]} config.json my_track.gpx', file=sys.stderr)
        exit(1)

    config_f, gpx_f = sys.argv[1:]

    # create client
    influx_config = json.load(open(config_f, 'r'))
    db = influx_config['database']
    client = InfluxDBClient(
        host=influx_config['host'],
        port=influx_config['port'],
        username=influx_config['username'],
        password=influx_config['password'],
        database=db
    )    

    # avoid duplication
    track_name = Path(gpx_f).stem
    tags = [r[1] for r in client.query(f'SHOW TAG VALUES ON "{db}" WITH KEY = "name"').raw['series'][0]['values']]
    if track_name in tags:
        print(f'{track_name} already in database, ignored.', file=sys.stderr)
        exit(0)

    # construct points
    gpx = gpxpy.parse(open(gpx_f, 'r'))
    points = []
    for track in gpx.tracks:
        for seg in track.segments:
            for p in seg.points:
                # add fields from attributes and extension
                fields = {
                    'latitude': p.latitude,
                    'longtitude': p.longitude,
                    'elevation': p.elevation,
                }
                for e in p.extensions:
                    fields[e.tag] = float(e.text)
                points.append({
                    'measurement': 'gpx',
                    'fields': fields,
                    'time': p.time.isoformat()
                })

    # write to database and exit
    client.write_points(points, tags={ 'name': track_name })
    print(f'Successfully wrote {len(points)} points to InfluxDB with name {track_name}', file=sys.stderr)
