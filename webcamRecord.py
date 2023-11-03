import cv2
import os

# Initialize the webcam capture
cap = cv2.VideoCapture(0)
print('width :%d, height : %d' % (cap.get(3), cap.get(4)))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = None
recording = False

def get_next_filename():
    """Find the index of the last file in the current directory with the format 
    recorded_video[i].avi and return the next index."""
    index = 0
    while True:
        filename = f"recorded_video_{index}.avi"
        if not os.path.exists(filename):
            return filename
        index += 1

# Main loop for capturing webcam frames
while True:
    ret, frame = cap.read()
    
    # Break the loop if frame is not received
    if not ret:
        break

    # If recording, add "Now recording" text to the frame
    if recording:
        cv2.putText(frame, "Now recording", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('webcam', frame)

    # Capture keypresses
    key = cv2.waitKey(1)

    # If 'r' key is pressed, start recording
    if key == ord('r') and not recording:
        next_filename = get_next_filename()
        # Create a VideoWriter object to record video
        out = cv2.VideoWriter(next_filename, fourcc, 25.0, (int(cap.get(3)), int(cap.get(4))))
        recording = True
        print(f"Recording started... Saving to {next_filename}")

    # If 's' key is pressed, stop recording
    elif key == ord('s') and recording:
        recording = False
        # Release the VideoWriter object
        out.release()
        print("Recording stopped.")

    # If 'q' key is pressed, exit the program
    elif key == ord('q'):
        if recording:
            recording = False
            # Ensure the recording is properly stopped before exiting
            out.release()
            print("Recording stopped.")
        break

    # Write the frame to the video file if recording
    if recording:
        out.write(frame)

# Release the webcam capture and close all windows
cap.release()
cv2.destroyAllWindows()
