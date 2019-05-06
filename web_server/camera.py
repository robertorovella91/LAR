import cv2
import numpy as np

class VideoCamera(object):
    def __init__(self,n):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.n = n
        self.video = cv2.VideoCapture(self.n)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
	
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()

		#resize
        #w = 360
        #h = 720
        w = int(image.shape[1] * 80 / 100)
        h = int(image.shape[0] * 120 / 100)
        dim = (w, h)
      
        #image = image[0:image.shape[0], 100:image.shape[1]-100]
        
		# resize image
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        width  = image.shape[1]
        height = image.shape[0]
        distCoeff = np.zeros((4,1),np.float64)
        print(image.shape[0],image.shape[1])

	# TODO: add your coefficients here!
        k1 = 1.0e-3; # negative to remove barrel distortion
        k2 =0;
        p1 = 1.0e-5; #rotondita orizzontale
        p2 = 1.0e-5; #rotondità verticale

        distCoeff[0,0] = k1;
        distCoeff[1,0] = k2;
        distCoeff[2,0] = p1;
        distCoeff[3,0] = p2;

	# assume unit matrix for camera
        cam = np.eye(3,dtype=np.float32)

        cam[0,2] = width/2.0  # define center x
        cam[1,2] = height/2.0 # define center y
        cam[0,0] = 10.        # define focal length x
        cam[1,1] = 10.        # define focal length y

	# here the undistortion will be computed
        dst = cv2.undistort(image,cam,distCoeff)

	
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', dst)
        return jpeg.tobytes()
