import cv2
import pickle
import numpy as np
from keras.models import load_model
import sqlite3
import pyttsx3
from threading import Thread
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import string
import speech_recognition as sr
import matplotlib.pyplot as plt
import os
import time


class LiveVoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
                        'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office',
                        'do you have money', 'do you want something to drink', 'do you want tea or coffee', 'do you watch TV',
                        'dont worry', 'flower is beautiful', 'good afternoon', 'good evening', 'good morning', 'good night',
                        'good question', 'had your lunch', 'happy journey', 'hello what is your name',
                        'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
                        'i am not feeling well', 'i am thinking', 'i am tired', 'i am vegetarian', 'i am very busy',
                        'i do not understand anything', 'i go to a gym', 'i love to shop', 'i love traveling', 'i teach at a school',
                        'it is very far', 'lets go for a dinner', 'my father is a government employee', 'my mother is a home maker',
                        'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call an ambulance',
                        'please call me later', 'please clean the room', 'please give me your pen', 'please use dustbin',
                        'please wait for sometime', 'please wait for some time', 'shall I help you']  # Your list of phrases

    def recognize_and_display(self):
        arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                print("I am Listening")
                audio = self.recognizer.listen(source)
                try:
                    a = self.recognizer.recognize_google(audio).lower()
                    print('You Said: ' + a)

                    for c in string.punctuation:
                        a = a.replace(c, "")

                    if a == 'goodbye' or a == 'good bye' or a == 'bye':
                        print("Time to say goodbye")
                        break

                    if a in self.isl_gif:
                        root = tk.Tk()
                        gif_path = 'asl_to_tsl/ISL_Gifs/{0}.gif'.format(a.lower())
                        im = Image.open(gif_path)
                        photo = ImageTk.PhotoImage(im)
                        lbl = tk.Label(root, image=photo)
                        lbl.pack()
                        lbl.image = photo
                        root.mainloop()
                    else:
                        for i in range(len(a)):
                            if a[i] in arr:
                                ImageAddress = 'asl_to_tsl/letters/' + a[i] + '.jpg'
                                ImageItself = Image.open(ImageAddress)
                                ImageNumpyFormat = np.asarray(ImageItself)
                                plt.imshow(ImageNumpyFormat)
                                plt.draw()
                                plt.pause(0.12)
                                plt.close()
                                time.sleep(1)
                    
                    time.sleep(1)
                except Exception as e:
                    print("An error occurred:", e)
                    continue
                finally:
                    plt.close()

    def live_voice_and_display(self):
        self.recognize_and_display()


class GestureRecognitionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Recognition App")
        self.root.geometry("600x400")  # Set window size

        # Adding image to the main page
        image_path = 'C:/Users/MANISH SONI/Downloads/Sign-maj/asl_to_tsl/signlang.png'
        image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=self.photo)
        label.pack(pady=10)

        # Create an instance of LiveVoiceAssistant
        self.live_voice_assistant = LiveVoiceAssistant()

        # Load the Keras model
        self.model = load_model('cnn_model_keras2.h5')

        # Frame to hold the buttons
        button_frame = tk.Frame(root)
        button_frame.pack()

        self.live_voice_button = tk.Button(button_frame, text="Live Voice",
                                            command=self.live_voice_assistant.live_voice_and_display)
        self.live_voice_button.grid(row=0, column=0, padx=10, pady=10)

        self.sign_to_text_button = tk.Button(button_frame, text="Sign to Text", command=self.toggle_camera)
        self.sign_to_text_button.grid(row=0, column=1, padx=10, pady=10)

        self.canvas = tk.Canvas(root, width=400, height=300)  # Reduce canvas size
        self.canvas.pack()

        self.cap = None  # Initialize camera object
        self.camera_active = False  # Variable to track camera state
        self.hist = self.get_hand_hist()
        self.x, self.y, self.w, self.h = 200, 50, 200, 200  # Adjust image display position and size
        self.image_x, self.image_y = self.get_image_size()

    def close_app(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            if self.cap is not None:
                self.cap.release()
            self.root.destroy()

    def get_hand_hist(self):
        with open("hist", "rb") as f:
            hist = pickle.load(f)
        return hist

    def get_image_size(self):
        img = cv2.imread('gestures/0/100.jpg', 0)
        return img.shape

    def toggle_camera(self):
        if not self.camera_active:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.read()[0]:
                self.cap = cv2.VideoCapture(0)
            self.camera_active = True
            self.sign_to_text_button.config(text="Stop Camera")
            self.recognize()
        else:
            if self.cap is not None:
                self.cap.release()
            self.camera_active = False
            self.sign_to_text_button.config(text="Sign to Text")
            self.canvas.delete("all")

    def recognize(self):
        def run_recognize():
            result = self.run_recognize()
            if result == 2:
                self.show_buttons()

        recognize_thread = Thread(target=run_recognize)
        recognize_thread.start()

    def run_recognize(self):
        result = self.text_mode(self.cap)
        return result

    def text_mode(self, cam):
        text = ""
        word = ""
        count_same_frame = 0
        while self.camera_active:
            ret, img = cam.read()
            if not ret:
                break
            img = cv2.resize(img, (400, 300))  # Adjust camera feed size
            img, contours, thresh = self.get_img_contour_thresh(img)
            old_text = text
            if len(contours) > 0:
                contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(contour) > 10000:
                    text = self.get_pred_from_contour(contour, thresh)
                    if old_text == text:
                        count_same_frame += 1
                    else:
                        count_same_frame = 0

                    if count_same_frame > 20:
                        if len(text) == 1:
                            Thread(target=self.say_text, args=(text,)).start()
                        word = word + text
                        if word.startswith('I/Me '):
                            word = word.replace('I/Me ', 'I ')
                        elif word.endswith('I/Me '):
                            word = word.replace('I/Me ', 'me ')
                        count_same_frame = 0

                elif cv2.contourArea(contour) < 1000:
                    if word != '':
                        Thread(target=self.say_text, args=(word,)).start()
                    text = ""
                    word = ""
            else:
                if word != '':
                    Thread(target=self.say_text, args=(word,)).start()
                text = ""
                word = ""
            blackboard = np.zeros((300, 400, 3), dtype=np.uint8)  # Adjust blackboard size
            cv2.putText(blackboard, "Text Mode", (100, 25), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (255, 0, 0))  # Adjust text position
            cv2.putText(blackboard, "Predicted text- " + text, (10, 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 0))  # Adjust text position
            cv2.putText(blackboard, word, (10, 120), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255))  # Adjust text position
            cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 2)
            res = np.hstack((img, blackboard))
            cv2.imshow("Recognizing gesture", res)
            cv2.imshow("thresh", thresh)
            keypress = cv2.waitKey(1)
            if keypress == ord('q') or keypress == ord('c'):
                break

        if keypress == ord('c'):
            return 2
        else:
            return 0

    def keras_predict(self, image):
        processed = self.keras_process_image(image)
        pred_probab = self.model.predict(processed)[0]
        pred_class = list(pred_probab).index(max(pred_probab))
        return max(pred_probab), pred_class

    def get_pred_text_from_db(self, pred_class):
        conn = sqlite3.connect("gesture_db.db")
        cmd = "SELECT g_name FROM gesture WHERE g_id=" + str(pred_class)
        cursor = conn.execute(cmd)
        for row in cursor:
            return row[0]

    def get_pred_from_contour(self, contour, thresh):
        x1, y1, w1, h1 = cv2.boundingRect(contour)
        save_img = thresh[y1:y1 + h1, x1:x1 + w1]
        text = ""
        if w1 > h1:
            save_img = cv2.copyMakeBorder(save_img, int((w1 - h1) / 2), int((w1 - h1) / 2), 0, 0, cv2.BORDER_CONSTANT,
                                          (0, 0, 0))
        elif h1 > w1:
            save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1 - w1) / 2), int((h1 - w1) / 2), cv2.BORDER_CONSTANT,
                                          (0, 0, 0))
        pred_probab, pred_class = self.keras_predict(save_img)
        if pred_probab * 100 > 70:
            text = self.get_pred_text_from_db(pred_class)
        return text

    def keras_process_image(self, img):
        img = cv2.resize(img, (self.image_x, self.image_y))
        img = np.array(img, dtype=np.float32)
        img = np.reshape(img, (1, self.image_x, self.image_y, 1))
        return img

    def say_text(self, text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        while engine._inLoop:
            pass
        engine.say(text)
        engine.runAndWait()

    def get_img_contour_thresh(self, img):
        img = cv2.flip(img, 1)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([imgHSV], [0, 1], self.hist, [0, 180, 0, 256], 1)
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        cv2.filter2D(dst, -1, disc, dst)
        blur = cv2.GaussianBlur(dst, (11, 11), 0)
        blur = cv2.medianBlur(blur, 15)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        thresh = cv2.merge((thresh, thresh, thresh))
        thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
        thresh = thresh[self.y:self.y + self.h, self.x:self.x + self.w]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
        return img, contours, thresh


if __name__ == "__main__":
    print("Welcome to the Hearing Impairment Assistant!")

    root = tk.Tk()
    app = GestureRecognitionApp(root)

    # Display the main Tkinter GUI
    root.mainloop()
