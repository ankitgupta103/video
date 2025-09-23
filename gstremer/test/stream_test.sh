#!/bin/bash

# === CONFIGURATION ===
VIDEO_FILE="14392175_1920_1080_60fps.mp4"
RTMP_URL="rtmp://a.rtmp.youtube.com/live2/YOUR-STREAM-KEY"

# === USAGE HELP ===
usage() {
  echo "Usage: $0 [360p30 | 720p30 | 1080p60 | 4k30]"
  exit 1
}

# === CHECK ARGUMENT ===
if [ $# -eq 0 ]; then
  usage
fi

CASE=$1

# === TEST CASES ===
case $CASE in
  360p30)
    WIDTH=640
    HEIGHT=360
    FPS=30
    BITRATE=500               # kbps
    AUDIO_BR=64000            # bps
    KEYINT=60
    ;;
  720p30)
    WIDTH=1280
    HEIGHT=720
    FPS=30
    BITRATE=2000
    AUDIO_BR=96000
    KEYINT=60
    ;;
  1080p60)
    WIDTH=1920
    HEIGHT=1080
    FPS=60
    BITRATE=5000
    AUDIO_BR=128000
    KEYINT=120
    ;;
  4k30)
    WIDTH=3840
    HEIGHT=2160
    FPS=30
    BITRATE=15000
    AUDIO_BR=192000
    KEYINT=60
    ;;
  *)
    echo " Invalid option: $CASE"
    usage
    ;;
esac


# ====== PRINT TEST DETAILS ======
echo "========================================="
echo "Resolution: ${WIDTH}x${HEIGHT}"
echo "Frame Rate: ${FPS} FPS"
echo "Video Bitrate: ${VIDEO_BITRATE} kbps"
echo "Audio Bitrate: ${AUDIO_BITRATE} bps"
echo "Keyframe Interval: ${KEY_INT_MAX}"
echo "========================================="

# === RUN GSTREAMER PIPELINE ===
echo " Starting stream: $CASE ($WIDTH x $HEIGHT @ ${FPS}fps, ${BITRATE}kbps)"
# gst-launch-1.0 -v \
#   filesrc location="$VIDEO_FILE" ! decodebin ! \
#   videoconvert ! videoscale ! video/x-raw,width=$WIDTH,height=$HEIGHT,framerate=$FPS/1 ! \
#   x264enc tune=zerolatency bitrate=$BITRATE speed-preset=superfast key-int-max=$KEYINT ! \
#   h264parse ! flvmux streamable=true name=mux ! \
#   rtmpsink location="$RTMP_URL" \
#   audiotestsrc is-live=true wave=silence ! audioconvert ! voaacenc bitrate=$AUDIO_BR ! mux.
while true; do
  gst-launch-1.0 -v \
    filesrc location="$VIDEO_FILE" ! decodebin ! \
    videoconvert ! videoscale ! video/x-raw,width=$WIDTH,height=$HEIGHT,framerate=$FPS/1 ! \
    x264enc tune=zerolatency bitrate=$VIDEO_BITRATE speed-preset=superfast key-int-max=$KEY_INT_MAX ! \
    h264parse ! flvmux streamable=true name=mux ! \
    rtmpsink location="$RTMP_URL" \
    audiotestsrc is-live=true wave=silence ! audioconvert ! voaacenc bitrate=$AUDIO_BITRATE ! mux.
    
  echo "🔁 Video ended, restarting..."
done