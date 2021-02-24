#Import relevant libraries, functions and dictionaries
import numpy as np
import cv2 as cv
import argparse
import subprocess
from subprocess import Popen
#import feh
from picamera import PiCamera
from time import sleep
from picamera.array import PiRGBArray
import os
from PIL import Image
import cv2.aruco as aruco

#Initialize camera module and set directory to be home/pi/Desktop
camera = PiCamera()
raw = PiRGBArray(camera)
os.chdir('/home/pi/Desktop')

#Global array posList to store position of pixel chosen by user
posList = []

#ImageCapture prompts the user for a file name and then saves a 2592 by 1944 image with an autoset white balance and a 4 second sleep
#to give the camera time to adjust before capturing the image

def ImageCapture():
    ImageName = input("Input a image file name: ")
    camera.resolution = (2592, 1944)
    camera.framerate = 15
    
    #Start image preview and 4 second sleep for camera adjustment to settings
    camera.start_preview()
    sleep(4)
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    
    #Capture raw image in bgr coloring and end preview
    camera.capture(raw, format="bgr")
    img = raw.array
    camera.stop_preview()
    
    #Create an rgb copy of the image for proper coloring and displaying to the user using cv.cvtColor and cv.COLOR_BGR2RGB functions
    #img = cv.imread('/home/pi/Desktop/ImageName.jpg')#,1)
    rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    #Display the rgb image
    #cv.imshow(ImageName, img)
    cv.imshow(ImageName, rgb)

    print(ImageName)
    #cv2.imwrite(ImageName, img)

    #Write the original bgr image to the desktop with the designated name and png filetype
    #These lines of code seem to always pass an error saying the file could not be saved but every time the file is succesfully saved
    #so it appears to not be an issue, it just likes to print out "Couldn't save each time for some reason
    try:
        cv.imwrite(ImageName+".png", img)
        #cv.imwrite("EX1.png", rgb)
        Print("Saved")
    except:
        print("Couldn't save "+ImageName)
        pass

    #These two lines wait for a key press and then destroy all open windows to clean off the desktop after execution
    cv.waitKey(0)
    cv.destroyAllWindows()


#This function accepts an image passed to the function so it can then prompt the user for a new filename and save the image as
#a png of half the size of the original (width, heigth) to the desktop
def resizeImage(img):
    
    #Prompt user for filename and read image passed to function
    ImageName = input("Input a image file name: ")
    img = cv.imread(img)
    
    #Set a scale of 50% to be used to resize the width and heigth by half using integer and image.shape
    scale = 50
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    size = (width, height)
    
    #Perform the resizing with new dimensions
    res = cv.resize(img, size)
    
    #A few lines of junk code kept for reference below
    #res = cv.resize(img,None,fx=2, fy=2, interpolation = cv.INTER_CUBIC)
    #resizedImg = cv.resize
    #cv.imwrite('/home/pi/Desktop/ResizedIMG.png',res)
    
    #Write the resized image with user designated filename to the desktop as a png with bgr coloring
    cv.imwrite('/home/pi/Desktop/'+ImageName+'.png',res)
    
    #cv.imshow(ImageName,res)
    
    #Create a rgb copy of the resized image for correct coloring during display to user using cv.cvtColor and cv.COLOR_BGR2RGB
    rgb = cv.cvtColor(res, cv.COLOR_BGR2RGB)
    #cv.imshow('ImageName',res)
    
    #Show the rgb image using cv.imshow
    cv.imshow("rgb resized image", rgb)
    #cv.imwrite("EX2.png", rgb)
    
    #Wait for key press and then destroy all open windows to cleanup after the code has run
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    #Return the resized (by 50% width and heigth) png image with bgr coloring as the functions output
    return res



#Some more junk code kept for reference and thought process during the creation of these functions
#def PixelColor(img):
#    img = cv.imread(img)
#    cv.imshow("Image", img)
#    (x,y) = cv.setMouseCallback("Image", img.on_mouse)
#    pix = img.load()
#    colors = img.getpixel(pixel)
#    print (pix[x,y])


#def mousePosition(event,x,y,flags,param):
#
#    if event == cv.EVENT_MOUSEMOVE:
#        print (x,y)
#        param = (x,y)


#def on_click(event, x, y, p1, p2):
#    if event == cv.EVENT_LBUTTONDOWN:
#        cv.circle(img, (x, y), 3, (255, 0, 0), -1)
#


#PixelColor reads a hard coded image from the working directory (home/pi/Desktop) converts it to rgb coloring, shows the user
#the rgb image and allows them to select a pixel on the photo. It then reprints the image with the selected pixels color values
#displayed on the image in both bgr and hsv values. The pixel coordinates are also printed to the terminal for reference.
def PixelColor():
    
    #The program currently loads and reads an image called "yell.png" from the pi desktop. This image is a picture of the colors.ppt
    #powerpoint provided with assignment 2: Intro to OpenCV on canvas for use with the yellow mask
    img = cv.imread('yell.png')
    
    #Standard bgr to rgb color conversion. The pi stores all these photos as bgr png images but I always convert to rgb for displaying
    #them due to color skewing that happens when displaying the default bgr images. Uses cv.cvtColor and cv.COLOR_BGR2RGB.
    rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    #cv.imshow is used to display the rgb image here with window titled "Image". Commented out line below would display in bgr.
    #cv.imshow("Image", img)
    cv.imshow("Image", rgb)

    #The cv.setMouseCallback function performs the task of calling the function "onMouse" when a pixel is selected by the
    #user (clicked). "Image" is the designated window for use with the function.
    cv.setMouseCallback('Image', onMouse)

    #Waits for key press and then kills all windows from the desktop. posNp is used as a numpy array from the global array posList
    #which stores and prints the selected pixels coordinates to the terminal for referencing.
    cv.waitKey(0)
    cv.destroyAllWindows()
    posNp = np.array(posList)     # convert to numpy array for other uses
    print(posNp)


#This function "onMouse" is critical for th PixelColor function to operate properly. The cv.setMouseCallback function from earlier
#calls this function which takes the pixel coordinates of the users click and upon detecion of the left button down press
#(cv.EVENT_LBUTTONDOWN) stores the x,y coordinates to the global posList and to bgr as an array of the img read (hard coded)
#this function hard codes the image being used to be "yell.png" from the desktop which is a picture of the "colors.ppt"
#presentation mentioned previously that was provided on canvas for the yellow mask portion of this assignment. Simply change the
#img = cv.imread("yell.png") line to include a different file if desired.
def onMouse(event, x, y, flags, param):
    #The following websited were referenced when building this function
    #https://stackoverflow.com/questions/28327020/opencv-detect-mouse-position-clicking-over-a-picture/49338267
    #https://python.hotexamples.com/examples/cv2/-/setMouseCallback/python-setmousecallback-function-examples.html
    
   global posList
   #Hard coded file of interest
   img = cv.imread('yell.png')
   
   #Waits for left button down press and then captures the pixel the user is at and saves it to global posList array and bgr
   #img array for use with color conversions and display
   if event == cv.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        bgr = img[y, x]
        
        #The following lines of code convert the pixel coordinated using numpy arrays to be in the hls and hsv image types
        #these each have different systems for storing the colors in each pixel
        hls = cv.cvtColor(np.asarray([[bgr]], dtype=img.dtype),
                               cv.COLOR_BGR2HLS)[0, 0]
        hsv = cv.cvtColor(np.asarray([[bgr]], dtype=img.dtype),
                               cv.COLOR_BGR2HSV)[0, 0]
        out = img.copy()
        
        #Creates a rgb copy of the image and displays the bgr and hsv color values for the selected pixel on the image
        rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        cv.putText(rgb, text='BGR={}, HSV={}'.format(bgr, hsv),
                        org=(0, 300), fontFace=cv.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5, color=(255, 255, 255))

        #Displays the rgb image with bgr and hsv color values for the pixel of choice then waits for a key press and destroys all
        #windows to clean off the window.
        cv.imshow('winname', rgb)
        #cv.imwrite("EX3.png", rgb)
        cv.waitKey(0)
        cv.destroyAllWindows()

#ConvGray is a simple function that is passed an image by the user during the function call. This image is then read and a
#bgr to gray color conversion os performed using the cv.cvtColor and cv.COLOR_BGR2GRAY functions
def ConvGray(img):
    img = cv.imread(img)
    
    #Color conversion to gray from bgr
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    #Displays the gray image to a new window then waits for a kep press and destroys all windows to clean up.
    cv.imshow('gray', gray)
    #cv.imwrite("EX4.png", gray)
    cv.waitKey(0)
    cv.destroyAllWindows()
    

#This function creates a mask of a resized image to filter out all colors except for yellow in the hsv color space
#then displays the resized image and the masked image side by side
def Yellow(yellowImg):
    #Very helpful link provided below for reference when building this function
    #https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
    
    #Image resizing performed using the resizeImage function from earlier
    reImg = resizeImage(yellowImg)
    
    #Creates an rgb and hsv copy of the resized image
    rgb = cv.cvtColor(reImg, cv.COLOR_BGR2RGB)
    hsv = cv.cvtColor(reImg, cv.COLOR_BGR2HSV)
    
    #Argument parsing lines here to find the image file path and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help = "path to the image")
    args = vars(ap.parse_args())
    
    
    #The next block of code was not used but is kept for reference and thought process records. The boundaries array can be
    #used to create lower and upper color value limits for multiple colors for mask application
    # load the image
    #image = cv.imread(args["image"])
    # define the list of boundaries
#    boundaries = [
#        ([17, 15, 100], [50, 56, 200]),
#        ([86, 31, 4], [220, 88, 50]),
#        ([25, 146, 190], [62, 174, 250]),
#        ([103, 86, 65], [145, 133, 128])
#    ]
#modified boundaries keep whats below
#    boundaries = [
#        ([17, 15, 100], [50, 56, 200]),
#        ([86, 31, 4], [220, 88, 50]),
#        ([26, 50, 20], [34, 255, 255]),
#        ([103, 86, 65], [145, 133, 128])
#    ]
#    # loop over the boundaries
#    for (lower, upper) in boundaries:
#        # create NumPy arrays from the boundaries
#        lower = np.array(lower, dtype = "uint8")
#        upper = np.array(upper, dtype = "uint8")
#        # find the colors within the specified boundaries and apply
#        # the mask
#my new modified ine for mask is first (on top)

    #Sets lower and upper boundaries for the color yellow in hsv color space using two numpy arrays for hue, saturation and
    #brightness as unsigned 8 bit integers.
    lower = np.array([60,150,30], dtype = "uint8")
    upper = np.array([105,255,255], dtype = "uint8")
    #mask = cv.inRange(hsv,(15, 100, 100), (45, 255, 255) )
    
    #Creates a mask using the hsv image and the lower and upper bounds for hsv color yellow and cv.inRange function
    mask = cv.inRange(hsv, lower, upper)
    #mask = cv.inRange(hsv, lower, upper)
    
    #Creates a mask of the rgb image using bitwise and to black out all pixels that are not in the bounds set for yellow in hsv
    output = cv.bitwise_and(rgb, rgb, mask = mask)  #reImg or hsv? Actually rgb works best with mask display with proper coloring
    
    # show the images side by side using numpy np.hstack function and the rgb image and mask output
    cv.imshow("images", np.hstack([rgb, output]))
    #cv.imwrite("EX5.png", np.hstack([rgb, output]))
    
    #Waits for a key press and then closes all windows to clean up the desktop
    cv.waitKey(0)
    cv.destroyAllWindows()
    

#The arucoDetect function accepts an image passed by the user and resizes it. It is then converted to grayscale and searched for
#aruco markers from the 6 by 6 library of 250 markers aruco.Dictionary_get(aruco.DICT_6X6_250). Paramters are created from the
#dictionary to help with aruco marker detection using corners, ids and rejected image points.
def arucoDetect(image):
    #img = cv.imread(image)
    
    #Resizes the passed image using the resizeImage function from earlier
    small = resizeImage(image)
    
    #Creates a grayscale copy of the bgr image
    gray = cv.cvtColor(small, cv.COLOR_BGR2GRAY)
    
    #Adds the 250 6 by 6 aruco markers from the proper dictionary with their detection parameters
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    
    #Serches the image for corners, aruco ids and rejected image points to aid in detecting aruco markers on grayscale image.
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    #Prints whether or not any markers were found to the terminal using the corners as reference (true or flase)
    if(not corners):marker = "No markers found"
    else:marker = "Found a marker"
    
    #Draws any detected markers corners and ids onto the grayscale image for easy identification and viewing
    markerImg = aruco.drawDetectedMarkers(gray, corners, ids)
    
    #Shows the new image with markers identified in a new window
    cv.imshow("image", markerImg)
    #cv.imwrite("EX6.png", markerImg)
    
    #I attempted and failed to print the status of finding markers on the new image itself. Code kept for reference and later use.
    #cv.putText(markerImg, marker, org = (0, 300), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color = (0, 0, 0))
    
    #Prints "Found a marker" or "No markers found" to the terminal depending on the situation.
    print(marker)
    print(corners)
    print(corners[0][0][0][0])
    print(corners[0][0][3][0])
    
    #Waits for a key press and destroys all open windows to clean off the desktop following code execution.
    cv.waitKey(0)
    cv.destroyAllWindows()
    

#This function is the beginning of a constant video capture of the cameras lense for quicker and nonstop aruco detection
#Some of this function is still pseudocode and some of it creates errors that are still being resolved, see below for details.
def arucoVideo():
    
    #Initiates video capturing from camera 1 (index 0) and prints if the camera was succesfully opened to the terminal.
    cap = cv.VideoCapture(0)
    print(cap.isOpened())
    
    #Sets the camera resolution to 1080p to hopefully allow for smoother code execution.
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    
    #Begins a infinite while loop to capture frames and convert to grayscale for aruco marker detection
    while(True):
        
        #This line of code should work and capture the frame from video capture, however it currently assigns ret and frame
        #to false and none respectively. A VIDIOC_STREAMON: Invalid argument is also printed to terminal.
        ret, frame = cap.read()
        
        #Prints for debugging
        print(ret)  
        print(frame)
        #frame = cv.VideoCapture(0)
        #print(frame)
        
        #This line is intended to convert the captured frame to grayscale but it results in a error: (-215:Assertion failed)
        #!_src.empty() in function cvtColor. I am still working to resolve this, the TAs and I are stumped currently and expect
        #this code to work based on examples online performing similar functions.
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        #Retrieves the 6 by 6 dictionary of 250 aruco markers and the associated detection parameters
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()
        
        #Checks the grayscale image for corners, marker ids and rejected points
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        
        #Prints the results of the detection attempt to the terminal for both cases
        if(not corners):marker = "No marker found"
        else:marker = "Found a marker!"
        #cv.putText(gray, marker, org = (0, 300), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color = (0, 0, 0))
        
        #Draws the detected markers onto a new image and displays the image in a new window
        grayM = aruco.drawDetectedMarkers(gray, corners, ids)
        cv.imshow('gray',grayM)
        
        #Prints the results to the terminal of if a marker was found or not
        print(marker)
        
        #Psuedocode for section 7 of the assignment, this code attempts to find the angle and distance of the detected aruco
        #marker using the pinhole camera method and simple trig. FOV = field of view, XRes = width of image in pixels
        #Calculate angle theta (camera to object angle): ((FOV = 54 deg)/2) *(((XRes=1920/2)-ArucoCenterX)/(XRes=1920/2))
        #Xres/2 = image center, Xres/2 - ArucoCenterX = distance from image center to object center, 
        #Calculate object distance from camera: ((XRes=1920/2)-ArucoCenterX)/tan(theta)
        
        #Breaks loop upon key press
        if cv.waitKey(1):
            break
    
    #Attempts to release the video capture (turn off camera) and destroys all windows
    cap.release()
    cv.destroyAllWindows()


#Uncomment to run any given function below. Watch for if any input arguments are passed or hard coded images are used in the function.
    
#resizeImage('EX1.png')

#PixelColor()
    
#ConvGray('w.png')
    
ImageCapture()

#Yellow('yell.png')

arucoDetect('aruco100and27.png')
        
#arucoVideo()




