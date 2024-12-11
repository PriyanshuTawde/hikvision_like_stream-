import cv2

# Set the RTSP stream URL
rtsp_url = "rtsp://172.16.12.33:8554/stream_1"

# Open the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

# Check if the connection was successful
if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
else:
    print("RTSP stream opened successfully.")

# Loop to continuously read frames from the stream
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Display the frame
    cv2.imshow("RTSP Stream", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the stream and close the display window
cap.release()
cv2.destroyAllWindows()
