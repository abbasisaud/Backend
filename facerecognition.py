import face_recognition
import cv2
import threading
from threading import Thread
import time
import concurrent.futures
import functions
from os import listdir
import numpy as np
import pickle
from imutils.video import VideoStream 

import main

rtsp_url = "rtsp://192.168.1.123:8080/h264_ulaw.sdp"
video_stream = VideoStream(rtsp_url).start()

rtsp_url2 = "rtsp://192.168.1.147:8080/h264_ulaw.sdp"
video_stream2 = VideoStream(rtsp_url2).start()


visname=main.visiterlist
face_locations = []
face_encodings = []
face_names = []

data = pickle.loads(open("encodings.pickle","rb").read())
process_this_frame = True
video_capture = cv2.VideoCapture(0)
  
 
def facerac(url,cam):
    idx = 0
    gap=2 
    video_stream = VideoStream(url).start()
    while True:
        # Grab a single frame of video
        #print('Capturing image')
        frame = video_stream.read()
        # Resize and gray scale frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        image_gray = cv2.cvtColor(small_frame,cv2.COLOR_BGR2GRAY)        
        if(idx==0 or idx % gap == 0):
            face_locations = face_recognition.face_locations(image_gray) #get location by hog using grayscale image
            face_encodings = face_recognition.face_encodings(small_frame, face_locations) #get encodings by rgb images
            if(face_encodings):
                
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(data["encodings"],face_encoding,0.5)
                    name = "Unknown"
                    #check to see if we have found a match
                    if True in matches:
                        matchIdx = [i for(i,b) in enumerate(matches) if b]#only get the True index of matches
                        counts = {}
                        for i in matchIdx:
                            name = data["names"][i] #get the name at index i
                            counts[name] = counts.get(name,0) + 1#put it into a dictionary
                        #get the fist max index, there would be some wrong cases
                        name = max(counts,key =counts.get) # get the name with max idx
                        des=functions.DestinationName(name)
                        descam=functions.DestinationCam(des)
                        path=functions.getPath(e=descam)
                        if (functions.checkpath(path=path,cam=cam)):
                            functions.saveAlerts(name,1,cam)
                        if(functions.checkcount(name,cam,main.countdata)):
                            functions.saveAlerts(name,1,cam)
                        if cam=='exitcam' and visname.__contains__(name):
                            functions.updatetime(name)
                            
                    face_names = []
                    face_names.append(name) #get the face_names
        # Display the results with the condition of 1 face
                # for (top, right, bottom, left), name in zip(face_locations, face_names):
                #     top *= 4
                #     right *= 4
                #     bottom *= 4
                #     left *= 4
                #     # Draw a box around the face
                #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 1)
                #     # Draw a label with a name below the face
                #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 25), cv2.FILLED)
                #     font = cv2.FONT_HERSHEY_DUPLEX
                #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)    
                #     print(name+" is at "+cam)
                
                # if (detectCam(cam)):
                #     saveName(name,1)                        
                # print(idx)       
        # Display the resulting image
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (0, 0), fx=0.55, fy=0.55)
        cv2.imshow(cam, frame) 
        idx += 1
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'): #truely turn off the system
            break
    cv2.destroyWindow(winname=cam)


# cv2.destroyAllWindows()
# video_capture.release()



# if __name__ =="__main__":
#     # facerac(video_stream,'cam1')
#     # facerac(video_stream)
#     # facerac()
      # t1 = threading.Thread(target=encoding)
#     # t1.start()
#     # t1.join()
#     # t2 = threading.Thread(target=writeEncoding)
#     # t2.start()
#     # t2.join()  
#     detaccam('cam1')    
    # t3 = threading.Thread(target=facerac,args=(video_stream,'cam1',)) 
    # t3.start()           
    # t4 = threading.Thread(target=facerac,args=(video_stream,'cam2'))
    # t4.start()
    
    
   
def create_threads(array, thread_count):
    array_len = len(array)
    chunk_size = array_len // thread_count
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = []
        for i in range(thread_count):
            start = i * chunk_size
            end = start + chunk_size
            if i == thread_count - 1:
                end = array_len
            futures.append(executor.submit(process_chunk, array[start:end]))
        
        for f in concurrent.futures.as_completed(futures):
            f.result()

def process_chunk(chunk):
    # Do something with the chunk of the array
    url=(chunk[0][1])
    cameraname=(chunk[0][0]) 
    facerac(url,cameraname)
    # facerac(url,cameraname)
cameraurl = [['cam1',"rtsp://192.168.1.123:8080/h264_ulaw.sdp"]]
create_threads(cameraurl,1)

 
