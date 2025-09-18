# H.265 Camera Capture and TCP Streaming Script

This Python script captures video from a local camera, encodes it using **H.265**, and optionally streams the encoded frames over a **TCP connection**. It also prints frame information and calculates approximate **bandwidth** in real-time.

---

## Features

- Capture video from a camera device (e.g., `/dev/video0`).
- Encode video using H.265 (`x265enc`) with low latency.
- Access frames in Python via `appsink`.
- Optionally send frames to a TCP server.
- Calculate and display bandwidth every second.
- Handle GStreamer messages and errors gracefully.

---

## Requirements

- Python 3
- GStreamer 1.0
- PyGObject (`gi`)

Install dependencies on Ubuntu/Raspberry Pi:

```bash
sudo apt install python3-gi gstreamer1.0-tools gstreamer1.0-plugins-base \
                 gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
                 gstreamer1.0-plugins-ugly gstreamer1.0-libav
```


## GStreamer Dependencies

This script relies on **GStreamer** and several plugins to capture, encode, and process video. Each component has a specific role:

### Python & GObject Introspection
- **`gi` (PyGObject)**: Allows Python to interact with GStreamer using GObject Introspection.
- **`Gst`**: The core GStreamer library for building and running pipelines.
- **`GLib`**: Provides the main loop and utility functions required by GStreamer.

### GStreamer Plugins / Elements
| Element / Plugin | Purpose |
|-----------------|---------|
| **`v4l2src`** | Captures video from a Linux camera device (e.g., `/dev/video0`). |
| **`video/x-raw`** | Specifies the raw video format including width, height, and framerate. |
| **`videoconvert`** | Converts video to a compatible format for encoders or sinks. Handles color space conversion. |
| **`x265enc`** | Encodes video using H.265/HEVC. Supports low-latency and fast presets for real-time streaming. |
| **`h265parse`** | Parses the H.265 stream to ensure proper framing and compatibility with downstream elements. |
| **`appsink`** | Allows Python to pull frames from the GStreamer pipeline for processing or TCP streaming. |

### GStreamer Plugin Packages
| Package | Provides |
|---------|---------|
| **`gstreamer1.0-plugins-base`** | Base elements like `videoconvert`, parsers, and sinks. |
| **`gstreamer1.0-plugins-good`** | Well-supported plugins including `v4l2src` and basic codecs. |
| **`gstreamer1.0-plugins-bad`** | Experimental or less-tested elements, sometimes needed for advanced codecs. |
| **`gstreamer1.0-plugins-ugly`** | Plugins with licensing restrictions, such as certain encoders. |
| **`gstreamer1.0-libav`** | Provides libav-based codecs and additional encoders/decoders for video processing. |

> **Note:** All these elements must be installed on your system. Missing plugins may cause errors like “not-negotiated” or “no element found” when running the pipeline.

---

### Installing Dependencies on Ubuntu / Raspberry Pi

```bash
sudo apt install python3-gi gstreamer1.0-tools \
                 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
                 gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
                 gstreamer1.0-libav
