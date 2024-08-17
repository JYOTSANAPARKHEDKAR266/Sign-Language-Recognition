import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import string

# Define the 'isl_gif' list with phrases
isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
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
           'please wait for sometime', 'please wait for some time', 'shall I help you',
           'shall we go together tommorow', 'sign language interpreter is very expensive', 'there is a strike tomorrow',
           'this is my father', 'this is my mother', 'what are you doing', 'what is the problem', 'what is todays date',
           'what is your age', 'what is your father do', 'what is your job', 'what is your mobile number',
           'what is your name', 'what is your salary', 'what is your son doing', 'what is your surname', 'what time is it',
           'what will happen', 'what will you do', 'what you do', 'when are you coming back', 'when are you going to office',
           'when are you going to your home town', 'when did you come', 'when will you come', 'where are you coming from',
           'where are you going', 'where do you live', 'where is the market', 'where is the toilet', 'where is your house',
           'where were you yesterday', 'which colour do you like', 'which is the best college in the world',
           'which is your favourite colour', 'which language do you speak', 'which mobile is this', 'which one is better',
           'which one do you want', 'which one is your favorite', 'which school does your child go to', 'who is there',
           'who is your favourite actor', 'who is your favourite cricketer', 'who is your favourite person',
           'why are you late', 'why are you laughing', 'why did you do this', 'why did you not complete your homework',
           'why do you like this', 'why do you need this', 'why do you want to go', 'why dont you ask me',
           'why dont you eat anything', 'why dont you sit down', 'why dont you tell me', 'why have you come',
           'will you come', 'will you drink tea with me', 'will you give me your pen', 'will you help me',
           'will you marry me', 'will you please be quiet', 'will you teach me', 'will you write down your address for me',
           'yes there is', 'you are very beautiful', 'you drive', 'you speak english', 'you speak slow', 'you teach',
           'your father is calling you', 'your father is in a meeting', 'your fees has to be paid', 'your mother is a teacher',
           'your mother is in office', 'i am going to office']

def func():
    r = sr.Recognizer()

    arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z']

    plt.ion()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print("I am Listening")
            audio = r.listen(source)
            try:
                a = r.recognize_google(audio).lower()
                print('You Said: ' + a)

                for c in string.punctuation:
                    a = a.replace(c, "")

                if a == 'goodbye' or a == 'good bye' or a == 'bye':
                    print("Time to say goodbye")
                    break

                if a in isl_gif:
                    gif_path = 'asl_to_tsl/ISL_Gifs/{0}.gif'.format(a.replace(" ", "_"))
                    im = Image.open(gif_path)
                    im.show()
                else:
                    for i in range(len(a)):
                        if a[i] in arr:
                            ImageAddress = 'asl_to_tsl/letters/' + a[i] + '.jpg'
                            ImageItself = Image.open(ImageAddress)
                            ImageItself.show()
            except Exception as e:
                print("An error occurred:", e)
                continue
            finally:
                plt.ioff()
                plt.close()

if __name__ == "__main__":
    print("Welcome to the Hearing Impairment Assistant!")
    func()
