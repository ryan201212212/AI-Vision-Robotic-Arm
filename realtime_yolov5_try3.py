import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# GStreamer 초기화
Gst.init(None)

# GStreamer 파이프라인 생성
pipeline_str = "udpsrc port=9999 caps=\"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)JPEG\" ! rtpjpegdepay ! jpegdec ! autovideosink sync=false"
pipeline = Gst.parse_launch(pipeline_str)

# 파이프라인 상태 전환
pipeline.set_state(Gst.State.PLAYING)

# 메인 루프 시작
main_loop = GLib.MainLoop()
try:
    main_loop.run()
except KeyboardInterrupt:
    pass

# 파이프라인 상태 정지
pipeline.set_state(Gst.State.NULL)
