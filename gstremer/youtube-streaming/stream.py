#!/usr/bin/env python3
"""
- Captures video from a camera device
- Encodes video in H.264 (YouTube RTMP requirement)
- Streams directly to YouTube RTMP server
- Logs frame info and bandwidth in real-time
"""

# -------------------------------
# Import required libraries
# -------------------------------
import gi            # GObject introspection for GStreamer
import time          # For timestamps and bandwidth calculation

# Use GStreamer 1.0
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# -------------------------------
# Initialize GStreamer
# -------------------------------
Gst.init(None)

# -------------------------------
# Configuration
# -------------------------------
VIDEO_DEVICE = "/dev/video0"      # Camera device path
WIDTH = 1280                      # Video width
HEIGHT = 720                      # Video height
FRAMERATE = 30                    # Frames per second
BITRATE = 2500                    # kbps for streaming

# Replace this with your actual YouTube Stream Key
YOUTUBE_STREAM_KEY = "YOUR_STREAM_KEY"
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"

# -------------------------------
# Build GStreamer pipeline
# -------------------------------
# YouTube requires H.264 video + AAC audio in FLV container
# Audio is optional; here we stream video only
pipeline_str = (
    f"v4l2src device={VIDEO_DEVICE} ! "                        # Capture video from camera
    f"video/x-raw,width={WIDTH},height={HEIGHT},framerate={FRAMERATE}/1 ! "
    "videoconvert ! "                                          # Format conversion
    "queue ! "
    f"x264enc tune=zerolatency bitrate={BITRATE} speed-preset=ultrafast ! "  # H.264 encoding
    "queue ! "
    "flvmux streamable=true name=mux ! "                       # FLV container
    f"rtmpsink location={RTMP_URL} "                           # RTMP output to YouTube
)

pipeline = Gst.parse_launch(pipeline_str)

# -------------------------------
# Frame info & bandwidth tracking
# -------------------------------
last_time = time.time()
total_bytes = 0

# Attach a probe on the encoder src pad to measure frame size
def on_probe(pad, info):
    global last_time, total_bytes

    buffer = info.get_buffer()
    if not buffer:
        return Gst.PadProbeReturn.OK

    # Get encoded frame size
    encoded_size = buffer.get_size()
    total_bytes += encoded_size

    # Frame timestamp
    timestamp = buffer.pts / Gst.SECOND if buffer.pts != Gst.CLOCK_TIME_NONE else 0

    # Log frame info
    print(f"[Frame] Time: {timestamp:.3f}s | Encoded Bytes: {encoded_size}")

    # Bandwidth calculation every second
    current_time = time.time()
    elapsed = current_time - last_time
    if elapsed >= 1.0:
        bandwidth_kbps = (total_bytes * 8) / (elapsed * 1000)
        print(f"[Bandwidth] ~{bandwidth_kbps:.2f} kbps over last {elapsed:.2f}s")
        last_time = current_time
        total_bytes = 0

    return Gst.PadProbeReturn.OK

# Attach probe to x264 encoder output
x264enc = pipeline.get_by_name("x264enc0")
if x264enc:
    srcpad = x264enc.get_static_pad("src")
    srcpad.add_probe(Gst.PadProbeType.BUFFER, on_probe)

# -------------------------------
# Handle GStreamer messages
# -------------------------------
bus = pipeline.get_bus()
bus.add_signal_watch()

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        print("End of Stream")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"Error: {err}, {debug}")
        loop.quit()
    return True

bus.connect("message", bus_call, GLib.MainLoop())

# -------------------------------
# Start streaming
# -------------------------------
pipeline.set_state(Gst.State.PLAYING)
print("📡 Streaming to YouTube started. Press Ctrl+C to stop...")

# Run main loop
try:
    loop = GLib.MainLoop()
    loop.run()
except KeyboardInterrupt:
    print("Stopping...")
finally:
    pipeline.set_state(Gst.State.NULL)
