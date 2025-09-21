# YouTube Live Streaming with GStreamer

This document explains how to stream video from a camera and audio to **YouTube Live** using a **GStreamer pipeline** via **RTMP**.

---

## Complete GStreamer Command

```bash
gst-launch-1.0 -v \
  v4l2src device=/dev/video0 ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! \
  x264enc tune=zerolatency bitrate=1000 speed-preset=superfast key-int-max=60 ! h264parse ! \
  flvmux streamable=true name=mux ! rtmpsink location="rtmp://a.rtmp.youtube.com/live2/vsgj-g361-09ua-cf8a-5c3y" \
  audiotestsrc is-live=true wave=silence ! audioconvert ! voaacenc bitrate=128000 ! mux.
```

---

## Tools & Technologies

- **gst-launch-1.0**: GStreamer CLI tool for building and running multimedia pipelines
- **YouTube RTMP Server**: YouTube Live accepts streams via RTMP (Real-Time Messaging Protocol)
- **Stream Key**: Unique identifier provided by YouTube Live Studio for your broadcast

---

## Pipeline Components Breakdown

### 1. Video Source
```bash
v4l2src device=/dev/video0
```
- **v4l2src**: Captures video from camera using Video4Linux2 drivers
- **device=/dev/video0**: Specifies the first camera connected to the system

### 2. Video Format Configuration
```bash
video/x-raw,width=640,height=480,framerate=30/1
```
- Sets raw video frame properties:
  - **Resolution**: 640x480 pixels
  - **Framerate**: 30 frames per second

### 3. Video Format Conversion
```bash
videoconvert
```
- Converts between different video color formats (YUV, RGB, etc.)
- Ensures compatibility with the H.264 encoder

### 4. Video Encoding (H.264)
```bash
x264enc tune=zerolatency bitrate=1000 speed-preset=superfast key-int-max=60
```
- **x264enc**: Encodes raw video into H.264 format
- **tune=zerolatency**: Optimizes for low-latency live streaming
- **bitrate=1000**: Sets video bitrate to 1000 kbps
- **speed-preset=superfast**: Prioritizes encoding speed over compression efficiency
- **key-int-max=60**: Inserts keyframe every 60 frames (~2 seconds at 30fps)

### 5. H.264 Stream Parsing
```bash
h264parse
```
- Ensures proper packetization of H.264 encoded stream for muxing

### 6. Audio Source (Silent)
```bash
audiotestsrc is-live=true wave=silence
```
- Generates silent audio stream (YouTube requires audio track)
- **is-live=true**: Marks source as live for proper synchronization
- **wave=silence**: Creates silent audio instead of test tones

### 7. Audio Format Conversion
```bash
audioconvert
```
- Converts raw audio formats for encoder compatibility

### 8. Audio Encoding (AAC)
```bash
voaacenc bitrate=128000
```
- **voaacenc**: Encodes audio into AAC format
- **bitrate=128000**: Sets audio bitrate to 128 kbps
- AAC format is mandatory for YouTube RTMP ingestion

### 9. Stream Multiplexing
```bash
flvmux streamable=true name=mux
```
- **flvmux**: Combines H.264 video and AAC audio into single FLV stream
- **streamable=true**: Optimizes for live streaming
- **name=mux**: Named reference point for connecting audio and video branches

### 10. RTMP Streaming Output
```bash
rtmpsink location="rtmp://a.rtmp.youtube.com/live2/YOUR-STREAM-KEY"
```
- **rtmpsink**: Sends FLV stream to YouTube via RTMP protocol
- Replace `YOUR-STREAM-KEY` with actual key from YouTube Live Studio 
- YOUR-STREAM-KEY = vsgj-g361-09ua-cf8a-5c3y
---

<!-- ## Data Flow Diagram

```
[Camera] → [v4l2src] → [Raw Video 640x480@30fps] → [videoconvert] → [x264enc] → [h264parse] ↘
                                                                                                [flvmux] → [rtmpsink] → [YouTube Live]
[Silent Audio] → [audiotestsrc] → [audioconvert] → [voaacenc AAC 128kbps] ↗
``` -->

## Data Flow Diagram

### Complete Pipeline Architecture

```
┌─────────────────────────── VIDEO PIPELINE ───────────────────────────-┐
│                                                                       │
│  Physical Camera (/dev/video0)                                        │
│         │                                                             │
│         ▼                                                             │
│  ┌─────────────┐    Raw Video Frames                                  │
│  │   v4l2src   │ ◄─── Captures from V4L2 driver                       │
│  └─────────────┘                                                      │
│         │                                                             │
│         ▼                                                             │
│  ┌─────────────────────────────────┐                                  │ 
│  │     video/x-raw                 │ ◄───  Format Specification       │
│  │  • Width: 640px                 │                                  │
│  │  • Height: 480px                │                                  │
│  │  • Framerate: 30 fps            │                                  │
│  │  • Color: RGB/YUV               │                                  │
│  └─────────────────────────────────┘                                  │
│         │                                                             │
│         ▼                                                             │
│  ┌─────────────┐                                                      │
│  │videoconvert │ ◄───  Color Space Conversion                         │
│  └─────────────┘      (RGB ↔ YUV, Format Compatibility)               │
│         │                                                             │
│         ▼                                                             │
│  ┌─────────────────────────────────┐                                  │
│  │         x264enc                 │ ◄───  H.264 Video Encoding       │
│  │  • Codec: H.264                 │                                  │
│  │  • Bitrate: 1000 kbps           │                                  │
│  │  • Tune: zerolatency            │                                  │
│  │  • Preset: superfast            │                                  │
│  │  • Keyframes: every 60 frames   │                                  │
│  └─────────────────────────────────┘                                  │
│         │                                                             │
│         ▼                                                             │
│  ┌─────────────┐                                                      │
│  │ h264parse   │ ◄───  Stream Validation & Packetization              │
│  └─────────────┘                                                      │
│         │                                                             │
│         ▼                                                             │
│  Encoded H.264 Video Stream                                           │
│                                                                       │
└───────────────────────┬───────────────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────────────────────────┐
    │                       MULTIPLEXER                             │
    │              ┌─────────────────────────────┐                  │
    │              │         flvmux              │                  │
    │              │  • Container: FLV           │ ◄─── Muxing      │
    │              │  • Streamable: true         │                  │
    │              │  • Combines A/V streams     │                  │
    │              │  • Name: mux                │                  │
    │              └─────────────────────────────┘                  │
    │                            │                                  │
    │                            ▼                                  │
    │                   Complete FLV Stream                         │
    │                (H.264 Video + AAC Audio)                      │
    └────────────────────────────┬──────────────────────────────────┘
                                 │
                                 ▼
    ┌───────────────────────────────────────────────────────────────┐
    │                        RTMP SINK                              │
    │              ┌─────────────────────────────┐                  │
    │              │        rtmpsink             │                  │
    │              │  • Protocol: RTMP           │ ◄───    Upload   │
    │              │  • Server: a.rtmp.youtube   │                  │
    │              │  • Endpoint: /live2/        │                  │
    │              │  • Auth: YOUR-STREAM-KEY    │                  │
    │              └─────────────────────────────┘                  │
    │                            │                                  │
    │                            ▼                                  │
    │                   YouTube Live Stream                         │
    └───────────────────────────────────────────────────────────────┘
                                 ▲
                                 │
┌─────────────────────────── AUDIO PIPELINE ───────────────────────────┐
│                                                                      │
│  Silent Audio Generator                                              │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────────────────────────┐                                 │
│  │       audiotestsrc              │ ◄───  Audio Source              │
│  │  • Wave: silence                │                                 │
│  │  • Is-live: true                │                                 │
│  │  • Format: Raw PCM              │                                 │
│  └─────────────────────────────────┘                                 │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────┐                                                     │
│  │audioconvert │ ◄───  Audio Format Conversion                       │
│  └─────────────┘      (PCM normalization)                            │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────────────────────────┐                                 │
│  │        voaacenc                 │ ◄───  AAC Audio Encoding        │
│  │  • Codec: AAC                   │                                 │
│  │  • Bitrate: 128 kbps            │                                 │
│  │  • Profile: LC (Low Complexity) │                                 │
│  └─────────────────────────────────┘                                 │
│         │                                                            │
│         ▼                                                            │
│  Encoded AAC Audio Stream                                            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
                        
                        
```

### Pipeline Flow Summary

1. **Video Capture**: Physical camera → V4L2 driver → Raw frames
2. **Video Processing**: Format specification → Color conversion → H.264 encoding
3. **Audio Generation**: Silent test source → Format conversion → AAC encoding  
4. **Stream Muxing**: Combine video + audio → FLV container format
5. **Live Streaming**: RTMP protocol → YouTube Live servers → Live broadcast

### Data Rates & Formats

| Stage | Input | Processing | Output |
|-------|--------|------------|---------|
| **Video Capture** | Camera sensor data | V4L2 capture | Raw RGB/YUV @ 9.2 MB/s |
| **Video Encoding** | Raw frames | H.264 compression | Compressed stream @ 125 KB/s |
| **Audio Generation** | Test signal | Silent PCM | Raw audio @ 176 KB/s |
| **Audio Encoding** | Raw PCM | AAC compression | Compressed audio @ 16 KB/s |
| **Final Stream** | H.264 + AAC | FLV muxing | Complete stream @ 141 KB/s |

---
---

## Format Specifications

| Component | Input Format | Output Format |
|-----------|-------------|---------------|
| **Video Input** | Raw frames (video/x-raw, RGB/YUV, 640x480, 30fps) | - |
| **Video Output** | - | H.264 compressed, 1000kbps |
| **Audio Input** | Silent test signal (raw PCM) | - |
| **Audio Output** | - | AAC, 128kbps |
| **Final Stream** | - | FLV container (H.264 + AAC) via RTMP |

---
