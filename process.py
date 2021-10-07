#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from datetime import datetime, timezone
import sys
import json
import gpxpy
from lxml import etree

def process(gpx_f, json_f):

    print(f'Merging data from {json_f} into {gpx_f}...')

    # index data by time
    json_data = {}
    for p in json.load(open(json_f, 'r'))["points"]:
        # Xingzhe uses strange timestamp (neither local nor UTC) in GPX file
        t = datetime.fromtimestamp(p['time'] // 1000 + 8 * 3600).astimezone(timezone.utc)
        json_data[t] = p
    print(f'Loaded {len(json_data)} points from JSON')

    # change GPX schema from 1.0 to 1.1 because gpxpy discards extensions on 1.0
    gpx_raw = open(gpx_f, 'r').read()
    gpx_raw = gpx_raw.replace('www.topografix.com/GPX/1/0', 'www.topografix.com/GPX/1/1')
    gpx_raw = gpx_raw.replace('version="1.0"', 'version="1.1"')

    match_count = 0
    inserted_count = 0
    gpx = gpxpy.parse(gpx_raw)
    
    # process each point in GPX
    for track in gpx.tracks:
        for seg in track.segments:
            for p in seg.points:
                if p.time in json_data:
                    match_count += 1
                    d = json_data[p.time]

                    # helper function
                    def try_add_attribute(name: str):
                        nonlocal inserted_count
                        if name in d and d[name] != 0.0:
                            # check all extensions, remove existing ones
                            exts = [e for e in p.extensions if e.tag != name]
                            e = etree.Element(name)
                            e.text = str(d[name])
                            exts.append(e)
                            p.extensions = exts
                            inserted_count += 1

                    # try to insert attributes from JSON data
                    try_add_attribute('speed')
                    try_add_attribute('cadence')
                    try_add_attribute('heartrate')
                    try_add_attribute('power')
 
    # check match
    if match_count == 0:
        print('No points are matched between GPX and JSON files, please double-check!')
        exit(1)
   
    # output GPX file in version 1.1
    print(f'Modifed {match_count} points in GPX, inserted {inserted_count} attributes')
    open(gpx_f, 'w').write(gpx.to_xml('1.1'))


if __name__ == '__main__':

    if len(sys.argv) != 3 or not sys.argv[1].endswith('.gpx') or not sys.argv[2].endswith('.json'):
        print(f'Usage: {sys.argv[0]} gpx_file json_file', file=sys.stderr)
        exit(1)

    process(sys.argv[1], sys.argv[2])
