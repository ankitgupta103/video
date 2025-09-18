#!/usr/bin/env python3
# Import necessary modules
import gi        # GObject Introspection, needed for GStreamer bindings
import time      # For measuring elapsed time and calculating bandwidth

# Specify GStreamer version
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib  # Import GStreamer and GLib for main loop

# -------------------------------
# Initialize GStreamer
# -------------------------------
# Must initialize before using any GStreamer functionality
Gst.init(None)

# -------------------------------
# Configuration: Set video capture parameters
# -------------------------------
VIDEO_DEVICE = "/dev/video0"  # Path to the camera device
WIDTH = 640                   # Width of the video frame
HEIGHT = 480                  # Height of the video frame
FRAMERATE = 30                # Frames per second

# -------------------------------
# Build GStreamer pipeline string
# -------------------------------
# v4l2src: capture video from a V4L2-compatible camera
# video/x-raw: set the format, width, height, and framerate
# videoconvert: ensures video format is compatible with sink
# autovideosink: display the video in a window
pipeline_str = (
    f"v4l2src device={VIDEO_DEVICE} name=source ! "
    f"video/x-raw,width={WIDTH},height={HEIGHT},framerate={FRAMERATE}/1 ! "
    "videoconvert ! "
    "autovideosink sync=false"
)

# Parse the pipeline string into a GStreamer pipeline object
pipeline = Gst.parse_launch(pipeline_str)

# -------------------------------
# Variables for frame info & bandwidth calculation
# -------------------------------
last_time = time.time()  # Last time we calculated bandwidth
frame_count = 0          # Count frames processed in the last interval
total_bytes = 0          # Total estimated bytes of frames processed

# -------------------------------
# Function to inspect each video frame
# -------------------------------
def print_frame_info(pad, info):
    """
    Called for each buffer/frame passing through the pipeline.
    Prints frame resolution, format, timestamp, and calculates bandwidth.
    """
    global last_time, frame_count, total_bytes

    buffer = info.get_buffer()           # Get the video buffer
    caps = pad.get_current_caps()        # Get the current capabilities (format info)

    if caps and buffer:
        structure = caps.get_structure(0)          # Access first structure of caps
        width = structure.get_int("width")[1]     # Frame width
        height = structure.get_int("height")[1]   # Frame height
        framerate = structure.get_fraction("framerate")  # Frame rate numerator/denominator
        format_str = structure.get_string("format")      # Pixel format
        timestamp = buffer.pts / Gst.SECOND if buffer.pts != Gst.CLOCK_TIME_NONE else 0

        # Estimate frame size in bytes (simplified: 3 bytes for RGB, 2 for YUV)
        bpp = 3 if format_str in ["RGB", "RGBx", "BGR"] else 2
        estimated_size = width * height * bpp

        # Update bandwidth stats
        frame_count += 1
        total_bytes += estimated_size
        current_time = time.time()
        elapsed = current_time - last_time

        # Print bandwidth every second
        if elapsed >= 1.0:
            bandwidth_kbps = (total_bytes * 8) / (elapsed * 1000)  # Convert bytes to kbps
            print(f"[Bandwidth] ~{bandwidth_kbps:.2f} kbps over last {elapsed:.2f}s")
            last_time = current_time
            total_bytes = 0
            frame_count = 0

        # Print detailed frame information
        print(
            f"[Frame] Time: {timestamp:.3f}s | "
            f"Resolution: {width}x{height} | "
            f"Framerate: {framerate[0]}/{framerate[1]} | "
            f"Format: {format_str} | "
            f"Estimated Bytes: {estimated_size}"
        )
    return Gst.PadProbeReturn.OK  # Continue passing buffer downstream

# Attach the above function to the source pad of the camera
src = pipeline.get_by_name("source")
src.get_static_pad("src").add_probe(Gst.PadProbeType.BUFFER, print_frame_info)

# -------------------------------
# Setup bus to listen for errors and end-of-stream messages
# -------------------------------
bus = pipeline.get_bus()
bus.add_signal_watch()  # Enable message signals

def bus_call(bus, message, loop):
    """
    Handles GStreamer messages such as errors or end-of-stream.
    """
    t = message.type
    if t == Gst.MessageType.EOS:
        print("End of Stream")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"Error: {err}, {debug}")
        loop.quit()
    return True

# Connect the bus callback to GLib MainLoop
bus.connect("message", bus_call, GLib.MainLoop())

# -------------------------------
# Start the pipeline
# -------------------------------
pipeline.set_state(Gst.State.PLAYING)
print("Local preview started with bandwidth calculation. Press Ctrl+C to stop...")

# -------------------------------
# Run GLib main loop to keep pipeline alive
# -------------------------------
try:
    loop = GLib.MainLoop()
    loop.run()  # This blocks until loop.quit() is called
except KeyboardInterrupt:
    print("Stopping...")  # Handle Ctrl+C
finally:
    pipeline.set_state(Gst.State.NULL)  # Properly stop pipeline