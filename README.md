# Xingzhe GPX Processor 行者轨迹处理工具

[Xingzhe](https://imxingzhe.com) sells cheap GPS bike meters with sensor support including cadence, heart rate and power. But the GPX files exported from its website does not contain any sensor metrics.

## Requirements

Python 3.7+ is required. Dependencies can be installed with `python3 -m pip install -r requirements.txt`.

## `merge.py`

This script can merge sensor metrics (easily obtained from its website) into GPX files. So that you can upload it to Strava, etc.

Usage: `./merge.py gpx_file json_file`, where:

* `gpx_file` is the GPX file exported from Xingzhe website, and
* `json_file` can be fetched from Xingzhe website at `https://www.imxingzhe.com/api/v4/segment_points/?workout_id=YOUR_WORKOUT_ID` (login required), in which `YOUR_WORKOUT_ID` is the number in the URL of current track.

This script will overwrite `gpx_file`, make sure you have backups before using.

## `to_influx.py`

This script can upload tracks in GPX files to InfluxDB. Then you can visualize it with Grafana and [TrackMap Plugin](https://grafana.com/grafana/plugins/pr0ps-trackmap-panel/).

To use, please install `influxdb` from PyPI first. Then fill in your configuration according to `influx.config.example.json`.
