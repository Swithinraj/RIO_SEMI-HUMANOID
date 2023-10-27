# Part 01 using opencv access webcam and transmit the video in HTML
import cv2
import pyshine as ps #  pip3 install pyshine==0.0.9
import socket
HTML="""
<html>
<head>
<title>PyShine Live Streaming</title>
</head>

<body>
<center>
<center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
</body>
</html>
"""
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    StreamProps = ps.StreamProps
    StreamProps.set_Page(StreamProps,HTML)
    address = (s.getsockname()[0],9000) # Enter your IP address 
    StreamProps.set_Mode(StreamProps,'cv2')
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)       
    capture.set(cv2.CAP_PROP_FPS,30)
    StreamProps.set_Capture(StreamProps,capture)
    StreamProps.set_Quality(StreamProps,90)
    server = ps.Streamer(address,StreamProps)
    print('Server started at','http://'+address[0]+':'+str(address[1]))
    server.serve_forever()
    sleep(300)
    capture.release()
    server.socket.close()
        
if __name__=='__main__':
    main()