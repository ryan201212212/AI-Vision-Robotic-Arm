import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import pyautogui
import sys
import time
import subprocess
from Xlib import display

# GStreamer 초기화
Gst.init(None)

# GStreamer 파이프라인 생성
pipeline_str = "udpsrc port=9999 caps=\"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)JPEG\" ! rtpjpegdepay ! jpegdec ! autovideosink sync=false"
pipeline = Gst.parse_launch(pipeline_str)

# 파이프라인 상태 전환
pipeline.set_state(Gst.State.PLAYING)

# 창 ID를 기반으로 창을 찾는다.
def get_window_by_id(id):
    window = display.Display().create_resource_object('window', id)
    return window

window_id = 0x2c00002  # Replace with your window ID
window = get_window_by_id(window_id)

if window is None:
    print('No window with this id exists')
    sys.exit(1)

# 캡처할 창의 위치와 크기 설정
window_x = 117
window_y = 107
window_width = 640
window_height = 480

# 스크린 캡처 함수
def capture_screenshot():
    try:
        time.sleep(1)

        # GStreamer가 표시하는 창의 스크린샷 캡처
        screenshot = pyautogui.screenshot(region=(window_x, window_y, window_width, window_height))
        time.sleep(1)
      
        # 스크린샷 저장
        screenshot.save("./real_time/screenshot.png")
        time.sleep(2)
        
        # YOLO 실행
        subprocess.run(["python", "detect_extraction_modify.py", "--weights", "./best.pt", "--source", "./real_time/screenshot.png"])

        # 프로그램 종료
        sys.exit()

    except pyautogui.FailSafeException:
        print("스크린 캡처 중단")
        return False

    return True

# 메인 루프 시작
main_loop = GLib.MainLoop()
try:
    while capture_screenshot():
        pass
except KeyboardInterrupt:
    pass

# 파이프라인 상태 정지
pipeline.set_state(Gst.State.NULL)

