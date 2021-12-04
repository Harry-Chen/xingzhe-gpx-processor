#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import json
import gpxpy

def concat(gpx_input: list[str], gpx_output: str):

    print(f'Concatenating {gpx_input} to {gpx_output}...')

    if len(gpx_input) <= 1:
        print('No need to concatenate! No output file is generated.')
        return

    # parse and concat
    gpx_raw = [gpxpy.parse(open(f, 'r').read()) for f in gpx_input]
    segments = []
    for g, f in zip(gpx_raw, gpx_input):
        if len(g.tracks) != 1:
            print(f'ERROR: Input {f} has more than one track')
            exit(1)
        segments.extend(g.tracks[0].segments)
    
    # write to file
    print(f'Found {len(segments)} segments in total, write to {gpx_output}...')
    output_gpx = gpx_raw[0]
    output_gpx.tracks[0].segments = segments
    open(gpx_output, 'w').write(output_gpx.to_xml('1.1'))


if __name__ == '__main__':

    input_files = sys.argv[1:-1]
    output_file = sys.argv[-1]

    if any([not f.endswith('.gpx') for f in input_files]) or not output_file.endswith('.gpx'):
        print(f'Usage: {sys.argv[0]} gpx_file_1 ... gpx_file_n gpx_file_out', file=sys.stderr)
        exit(1)

    concat(input_files, output_file)
