import time
import cv2
import numpy as np
import pytesseract as tess
import matplotlib.pyplot as plt #debug
import os
import re
# Building:
from plate_verification import Car , Verificator

# Initialize
vehicle = Car("ABY8512")
verificator = Verificator()
# pytesseract location
tess.pytesseract.tesseract_cmd = r"E:\Programming_Files\OCR-Tesseract\tesseract.exe"
class ObjectDetection:
    def __init__(self):
        # load yolo weights and cfg
        self.MODEL = cv2.dnn.readNet(
            'models/yolov4.weights',
            'models/yolov4.cfg'
        )

        # initialize classes to used
        self.CLASSES = []
        with open("models/coco.names", "r") as f:
            self.CLASSES = [line.strip() for line in f.readlines()]

        # get layers of the yolo network | get index of output layers
        self.OUTPUT_LAYERS = [self.MODEL.getLayerNames()[i - 1] for i in self.MODEL.getUnconnectedOutLayers()]

        # Generate random color
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.CLASSES), 3), dtype="uint8")

    def detectObj(self, snap):
        height, width, channels = snap.shape 
        blob = cv2.dnn.blobFromImage(snap, 1/255, (352, 352), swapRB=True, crop=False) # create blob from image to transfer to your cnn

        self.MODEL.setInput(blob) # set blob as an input to your cv2.dnn.readNet
        outs = self.MODEL.forward(self.OUTPUT_LAYERS) # feed blob to the network and set it to variable | outs |

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:] # score of detected object
                class_id = np.argmax(scores) # set class_id of detected object
                confidence = scores[class_id] # confidence of detected object
                if confidence > 0.5: # if confidence is higher than 50%
                    # Object detected
                    center_x = int(detection[0]*width) # get center_x of detected object
                    center_y = int(detection[1]*height) #get center_y of detected object

                    w = int(detection[2]*width) 
                    h = int(detection[3]*height)

                    # Rectangle coordinates 
                    x = int(center_x - w/2) 
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h]) # append boxes coordinates (where the object is)
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

                    #Snap is still not cropped
                    # cv2.imshow("snapshot", snap)
                    # cv2.waitKey(2)

                    #DEBUG
                    # print("LIST:")
                    # print(boxes)
                    # print("=====")
                    # test = np.array(boxes[0])
                    # print(test)
                    # print(type(test))
                    #==================

                    # #DEBUG:
                    # ocr_boxes = np.array(boxes[0])
                    # recognize_plate(snap, ocr_boxes) # apply ocr and print text
                    # #===========


                    try:
                        ''' Try Recognize Plate'''
                        ocr_boxes = np.array(boxes[0])
                        # recognize_plate(snap, ocr_boxes) # apply ocr and print text
                        verificator.verify_car(recognize_plate(snap, ocr_boxes)) # apply ocr and verify
                    except:
                        print("No Plate Detected...")
                        ''' Except when no plate is available '''
                        continue


        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4) # NMS(non-maximum suppression) is for avoiding overlapping boxes
        font = cv2.FONT_HERSHEY_PLAIN # set font

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.CLASSES[class_ids[i]]) # get class name and set as label
                percentage = "{:.2f}%".format(confidences[0] * 100) # convert confidence to %
                # color = self.COLORS[i]
                color = [int(c) for c in self.COLORS[class_ids[i]]] # set color
                cv2.rectangle(snap, (x, y), (x + w, y + h), color, 2) # draw a rectangle
                cv2.putText(snap, label, (x, y - 5), font, 2, color, 2) # draw label text
                cv2.putText(snap, percentage, (x, y - 25), font, 2, color, 2) # draw percentage text

        try: 
            # Return labels
            ObjectDetection.lbl = label
        except:
            ObjectDetection.lbl = "No label"

        return snap # Return snap object


def recognize_plate(img, coords):
    ''' img should be  numpy.ndarray
        [438.   0. 482.  58.]
        <class 'numpy.ndarray'>
    '''

    #TODO: xmax and ymax are corrrect but xmin and ymin is far from the detection box
    # separate coordinates from box
    # xmin, ymin, xmax, ymax = coords
    

    #DEBUG:
    xmin, ymin, xmax, ymax = coords

    # xmin = xmin + 85
    # ymin = ymin + 12
    # xmax = xmax
    # ymax = ymax + 100
    # print (xmin , ymin , xmax , ymax)
    #======================

    # get the subimage that makes up the bounded region and take an additional 5 pixels on each side
    box = img[int(ymin)-5:int(ymax)+5, int(xmin)-5:int(xmax)+5] # box will be the subimage that is already cropped to the detected object

    
    #DEBUG:
    # cv2.imshow("Crop Debug", box)
    # cv2.waitKey(0)
    # #============================================================================================================

    # grayscale region within bounding box
    gray = cv2.cvtColor(box, cv2.COLOR_RGB2GRAY) # originally box
    # resize image to three times as large as original for better readability
    gray = cv2.resize(gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
    # perform gaussian blur to smoothen image
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    #cv2.imshow("Gray", gray)
    #cv2.waitKey(0)
    # threshold the image using Otsus method to preprocess for tesseract
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    #cv2.imshow("Otsu Threshold", thresh)
    #cv2.waitKey(0)
    # create rectangular kernel for dilation
    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    # apply dilation to make regions more clear
    dilation = cv2.dilate(thresh, rect_kern, iterations = 1)
    #cv2.imshow("Dilation", dilation)
    #cv2.waitKey(0)
    # find contours of regions of interest within license plate
    try:
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    except:
        ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # sort contours left-to-right
    sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
    # create copy of gray image
    im2 = gray.copy()
    # create blank string to hold license plate number
    plate_num = ""
    # loop through contours and find individual letters and numbers in license plate
    for cnt in sorted_contours:
        x,y,w,h = cv2.boundingRect(cnt)
        height, width = im2.shape

        # Countour Condition if not met skip the countour box

        # if height of box is not tall enough relative to total height then skip
        if height / float(h) > 6: 
            # print("Skip 1")
            continue

        ratio = h / float(w)
        # if height to width ratio is less than 1.5 skip
        if ratio < 1.5: 
            # print("Skip 2")
            continue

        # if width is not wide enough relative to total width then skip
        if width / float(w) > 15: 
            # print("Skip 3")
            continue

        area = h * w
        # if area is less than 100 pixels skip
        if area < 100: 
            # print("Skip 4")
            continue

        # draw the rectangle
        rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0),2)
        # grab character region of image
        roi = thresh[y-5:y+h+5, x-5:x+w+5]
        # perfrom bitwise not to flip image to black text on white background
        roi = cv2.bitwise_not(roi)
        # perform another blur on character region
        roi = cv2.medianBlur(roi, 5)

        try:
            text = tess.image_to_string(roi, config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
            # clean tesseract text by removing any unwanted blank spaces
            clean_text = re.sub('[\W_]+', '', text)
            plate_num += clean_text
        except: 
            print("Tried OCR , Failed ")
            text = None

        # #DEBUG:
        # print("Reading Plate Number...")
        # text = tess.image_to_string(roi, config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
        # # clean tesseract text by removing any unwanted blank spaces
        # clean_text = re.sub('[\W_]+', '', text)
        # plate_num += clean_text
        # print("Read Complete")
        #========================

    if plate_num != None:
        print("License Plate #: ", plate_num)
    #DEBUG:
    path = 'F:\Programming\Python\~PROJECTS\College~\secureV\SecureV-App\git_ignore\image_debug'
    cv2.imwrite(os.path.join(path, 'ocr.jpg') , im2)
    # cv2.imshow("Character's Segmented", im2)
    # cv2.waitKey(0)
    #=================================
    return plate_num
class VideoStreaming(object):
    def __init__(self):
        super(VideoStreaming, self).__init__()
        self.VIDEO = cv2.VideoCapture(0) # video input
        self.MODEL = ObjectDetection() # MODEL is the ObjectDetection Class
        self._preview = True
        self._detect = False

    # Getter setter functions
    @property
    def preview(self):
        return self._preview

    @preview.setter
    def preview(self, value):
        self._preview = bool(value)

    @property
    def detect(self):
        return self._detect

    @detect.setter
    def detect(self, value):
        self._detect = bool(value)

    def show(self):
        while(self.VIDEO.isOpened()):
            ret, snap = self.VIDEO.read() # capture video frame by frame
            
            if ret == True: # if camera enabled 

                if self._preview:
                    if self.detect: # if self.detect is true
                        snap = self.MODEL.detectObj(snap) # apply snap from video feed to model | snap = frame  
                        try:
                            VideoStreaming.lblret = self.MODEL.lbl
                            #DEBUG:
                            # print(self.MODEL.lbl) # PRINT CLASS NAME
                            #========
                        except:
                            pass

                else: # if camera disabled
                    snap = np.zeros((
                        int(self.VIDEO.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                        int(self.VIDEO.get(cv2.CAP_PROP_FRAME_WIDTH))
                    ), np.uint8)
                    label = 'camera disabled'
                    H, W = snap.shape
                    font = cv2.FONT_HERSHEY_PLAIN
                    color = (255,255,255)
                    cv2.putText(snap, label, (W//2 - 100, H//2), font, 2, color, 2)
                
                frame = cv2.imencode('.jpg', snap)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.01)

            else:
                break
        print('off')
