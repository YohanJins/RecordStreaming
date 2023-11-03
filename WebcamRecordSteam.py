import cv2
import os

cap = cv2.VideoCapture(0)
print('width :%d, height : %d' % (cap.get(3), cap.get(4)))

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = None
recording = False

def get_next_filename():
    """현재 디렉토리에 있는 파일 중 recorded_video[i].avi 형식을 가진 마지막 파일의 인덱스를 찾아서 다음 인덱스를 반환합니다."""
    index = 0
    while True:
        filename = f"recorded_video_{index}.avi"
        if not os.path.exists(filename):
            return filename
        index += 1

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    # 녹화 중이라면 "Now recording" 텍스트 추가
    if recording:
        cv2.putText(frame, "Now recording", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('webcam', frame)

    key = cv2.waitKey(1)

    # 'r'키를 누르면 녹화 시작
    if key == ord('r') and not recording:
        next_filename = get_next_filename()
        out = cv2.VideoWriter(next_filename, fourcc, 25.0, (int(cap.get(3)), int(cap.get(4))))
        recording = True
        print(f"Recording started... Saving to {next_filename}")

    # 's'키를 누르면 녹화 중지
    elif key == ord('s') and recording:
        recording = False
        out.release()
        print("Recording stopped.")

    # 'q'키를 누르면 웹캠 영상 중지, 만약 녹화 중이었다면 녹화도 중지
    elif key == ord('q'):
        if recording:
            recording = False
            out.release()
            print("Recording stopped.")
        break

    if recording:
        out.write(frame)

cap.release()
cv2.destroyAllWindows()