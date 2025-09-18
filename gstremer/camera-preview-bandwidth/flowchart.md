# Camera Preview and Bandwidth Monitoring Script

This Python script captures video from a V4L2-compatible camera, displays a local preview using GStreamer, and prints detailed frame information along with an estimated bandwidth usage. It leverages **GStreamer** for video processing and **GLib MainLoop** for event handling.

---

## Features

- Captures video from a camera device (`/dev/video0` by default)
- Configurable resolution, framerate, and video format
- Displays local preview in a window
- Logs frame details: timestamp, resolution, framerate, pixel format
- Calculates estimated bandwidth usage in kbps
- Handles GStreamer messages including errors and End-of-Stream
- Graceful shutdown on `Ctrl+C`

---

## How It Works

1. **Import Modules**: Uses `gi` for GStreamer bindings and `time` for bandwidth calculation.
2. **Initialize GStreamer**: `Gst.init(None)` must be called before using any GStreamer functionality.
3. **Configuration**: Set video device, frame width, height, and framerate.
4. **Build Pipeline**:  
   `v4l2src -> video/x-raw -> videoconvert -> autovideosink`  
   - `v4l2src`: captures video from camera  
   - `video/x-raw`: sets width, height, and framerate  
   - `videoconvert`: ensures format compatibility  
   - `autovideosink`: displays video locally
5. **Attach Pad Probe**: `print_frame_info` function inspects each frame, prints frame info, and calculates bandwidth.
6. **Setup Bus**: Listens for GStreamer messages (`ERROR`, `EOS`) and handles them.
7. **Start Pipeline**: Sets pipeline to `PLAYING` state.
8. **Run Main Loop**: Keeps pipeline alive until interrupted.
9. **Keyboard Interrupt**: On `Ctrl+C`, stops the pipeline gracefully and ends the program.

---

## Flowchart

```mermaid
graph TD
    A[Start Program] --> B[Import modules: gi, time]
    B --> C[Initialize GStreamer (Gst.init(None))]
    C --> D[Set Configuration: VIDEO_DEVICE, WIDTH, HEIGHT, FRAMERATE]
    D --> E[Build GStreamer Pipeline: v4l2src -> video/x-raw -> videoconvert -> autovideosink]
    E --> F[Attach Pad Probe: print_frame_info (Frame info + Bandwidth)]
    F --> G[Setup Bus to handle messages (ERROR / EOS)]
    G --> H[Start Pipeline (pipeline.set_state(PLAYING))]
    H --> I[Run GLib Main Loop (loop.run())]
    I --> J{Keyboard Interrupt? (Ctrl+C)}
    J -- Yes --> K[Stop Pipeline (pipeline.set_state(NULL))]
    J -- No --> I
    K --> L[End Program]
