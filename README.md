# gifparse [Work in progress.]

Goal: Parse the GIF 89a file format, down to the minor details.

## Installation

`pip install gifparse`

## Usage

```python
# Download a GIF
import requests
gif_bytes = requests.get("http://imgs.xkcd.com/comics/frequency/heartbeat.gif").content

# Parse it
import gifparse
gif = gifparse.parse(gif_bytes)

print gif.__dict__
```

## Features

Currently, `gifparse` can parse a GIF 89a file into its constituent blocks and sublocks. It can determine the delay time for individual frames in a GIF, and compute the total delay time. Planning to add support for other details of the spec.
