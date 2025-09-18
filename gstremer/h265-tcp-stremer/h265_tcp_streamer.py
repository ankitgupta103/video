#!/usr/bin/env python3

# -------------------------------
# Import required libraries
# -------------------------------
import gi            # GObject introspection for GStreamer
import socket        # For TCP socket communication
import struct        # To pack/unpack data to send over TCP
import time          # For timestamps and bandwidth calculation

# Specify GStreamer version
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib  # GStreamer core and main loop

# -------------------------------
# Initialize GStreamer
# -------------------------------
Gst.init(None)  # Must be called before using any GStreamer functions

# -------------------------------
# Configuration
# -------------------------------
VIDEO_DEVICE = "/dev/video0"  # Camera device path
WIDTH = 640                   # Video width in pixels
HEIGHT = 480                  # Video height in pixels
FRAMERATE = 30                # Frames per second

TCP_IP = "127.0.0.1"          # TCP server IP (local machine)
TCP_PORT = 5005               # TCP server port

# -------------------------------
# Setup TCP socket
# -------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket
try:
    sock.connect((TCP_IP, TCP_PORT))                     # Try connecting to TCP server
    print(f"Connected to TCP server at {TCP_IP}:{TCP_PORT}")
except ConnectionRefusedError:
    # If server not running, disable sending
    print(f"Cannot connect to {TCP_IP}:{TCP_PORT}. Run a TCP server to receive frames.")
    sock = None

# -------------------------------
# Build GStreamer pipeline
# -------------------------------
pipeline_str = (
    f"v4l2src device={VIDEO_DEVICE} ! "                  # Capture video from camera
    f"video/x-raw,width={WIDTH},height={HEIGHT},framerate={FRAMERATE}/1 ! "  # Set format
    "videoconvert ! "                                    # Convert video to compatible format
    "x265enc bitrate=1000 tune=zerolatency speed-preset=ultrafast ! "  # H.265 encoding
    "h265parse ! "                                       # Parse H.265 stream
    "appsink name=appsink emit-signals=true max-buffers=1 drop=true"    # Get frames in Python
)

pipeline = Gst.parse_launch(pipeline_str)  # Build pipeline from string
appsink = pipeline.get_by_name("appsink")  # Reference appsink element to access frames

# -------------------------------
# Frame info & bandwidth tracking
# -------------------------------
last_time = time.time()  # Track last bandwidth calculation
total_bytes = 0          # Accumulate encoded frame size for bandwidth

# -------------------------------
# Callback for each new frame
# -------------------------------
def on_new_sample(sink):
    global last_time, total_bytes

    # Pull the next frame/sample from appsink
    sample = sink.emit("pull-sample")
    if sample:
        buffer = sample.get_buffer()       # Get buffer containing encoded frame
        caps = sample.get_caps()           # Get format info
        structure = caps.get_structure(0)
        width = structure.get_int("width")[1]    # Frame width
        height = structure.get_int("height")[1]  # Frame height
        framerate = structure.get_fraction("framerate")  # Frame rate
        timestamp = buffer.pts / Gst.SECOND if buffer.pts != Gst.CLOCK_TIME_NONE else 0  # Timestamp in seconds

        # Encoded frame size in bytes
        encoded_size = buffer.get_size()
        total_bytes += encoded_size  # Accumulate for bandwidth calculation

        # Print frame info
        print(
            f"[Frame] Time: {timestamp:.3f}s | "
            f"Resolution: {width}x{height} | "
            f"Framerate: {framerate[0]}/{framerate[1]} | "
            f"Encoded Bytes: {encoded_size}"
        )

        # Send encoded frame over TCP if connected
        if sock:
            try:
                # First send 4-byte frame size, then frame data
                sock.sendall(struct.pack(">I", encoded_size) + buffer.extract_dup(0, encoded_size))
            except Exception as e:
                print(f"TCP send error: {e}")

        # Calculate bandwidth every second
        current_time = time.time()
        elapsed = current_time - last_time
        if elapsed >= 1.0:
            bandwidth_kbps = (total_bytes * 8) / (elapsed * 1000)  # Convert bytes/sec to kbps
            print(f"[Bandwidth] ~{bandwidth_kbps:.2f} kbps over last {elapsed:.2f}s")
            last_time = current_time
            total_bytes = 0

    return Gst.FlowReturn.OK  # Continue streaming

# Connect the callback to appsink
appsink.connect("new-sample", on_new_sample)

# -------------------------------
# Handle GStreamer messages/errors
# -------------------------------
bus = pipeline.get_bus()         # Pipeline bus for messages
bus.add_signal_watch()           # Watch for messages

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
# Start GStreamer pipeline
# -------------------------------
pipeline.set_state(Gst.State.PLAYING)
print("H.265 encoded local capture + TCP streaming started. Press Ctrl+C to stop...")

# Run main loop to keep streaming
try:
    loop = GLib.MainLoop()
    loop.run()
except KeyboardInterrupt:
    print("Stopping...")
finally:
    pipeline.set_state(Gst.State.NULL)  # Stop pipeline
    if sock:
        sock.close()                   # Close TCP socket