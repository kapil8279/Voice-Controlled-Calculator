import pyttsx3 #used for setup voice engine and for speaking the system
from tkinter import * #used for GUI
import speech_recognition as sr #used for speech recognition using google api it conver all the audio data into text
import threading #used for multiprocessing and create threads
import time 

class Calculator():
    # this is the constructor
    def __init__(self):
        self.EntStr = ''
        self.resEntStr = ''
        self.is_listning = False
        self.allThreadStart = False
        # this variabli is for our main window 
        self.MainWindow = Tk()
        self.EntVar = StringVar()
        self.resultEntVar = StringVar()
        self.MyGUIComponent()
        # this is tha main loop of our software and also a main thread 
        self.MainWindow.mainloop()
    

    def StartThreading(self):
        if not self.allThreadStart:
            self.ListenEngineLabel['text'] = 'Wait . . .'
            self.VoiceEngineLabel['text'] = 'Wait . . .'
            self.ListenLabel['text'] = 'Wait . . .'
            # this is the second thread and used for setup the voice engine
            self.setupVoiceThread = threading.Thread(target=self.SetupVoiceEngine)
            self.setupVoiceThread.daemon = True
            self.setupVoiceThread.start()

            # this is third thread used for setup speech recognition engine
            self.setupsrenginethread = threading.Thread(target=self.SetupSREngine)
            self.setupsrenginethread.daemon = True
            self.setupsrenginethread.start()
            # this is fourth thread and used for listening our command
            if self.RecEngine:
                self.takecommandthread = threading.Thread(target = self.takeCommand)
                self.takecommandthread.daemon = True
                self.takecommandthread.start()
                
            self.allThreadStart = True
            
    # this function is used for stop all thead except main thead
    def StopThreading(self):
        if self.allThreadStart:
            self.is_listning = False
            
            self.allThreadStart = False
            self.takeCommand()
            self.ProcessCommand()
            #print("All Proccess stop")
        


    def SetupVoiceEngine(self):
        #this function is use for septup voice engine and set the propeties of the engine like voice and rate
        try:
            self.VoiceEngine = pyttsx3.Engine('sapi5')
            voice = self.VoiceEngine.getProperty("voices")
            if len(voice)>0:
                self.VoiceEngine.setProperty('voice',voice[0])
            else:
                self.VoiceEngineLabel['text'] = 'No Voice Installed'

            self.VoiceEngine.setProperty('rate',100)
            
            self.VoiceEngineLabel['text'] = "Voice Engine setup successfully"
        except Exception as e:
            print(e)
            self.VoiceEngineLabel['text'] = 'Unknown error occur'


    def Speak(self,voice):
        #this function is used for speaking whatever i want 
        self.VoiceEngine.say(voice)
        self.VoiceEngine.startLoop(False)
        self.VoiceEngine.iterate()
        self.VoiceEngine.endLoop()
        return
        

    # this fuction is used for setup speech recognition engine 
    def SetupSREngine(self):
        self.RecEngine = sr.Recognizer()
        self.is_listning = True
        self.ListenEngineLabel['text'] = 'Listening Engine setup'

    #this fuction take command from microphone
    def takeCommand(self):
        try:
            with sr.Microphone() as source:
                if not self.RecEngine:
                    self.ListenEngineLabel['text'] = "Speech recognition is not working"
                    return
                if self.is_listning:
                    self.ListenLabel['text'] = 'Listening . . . .'
                    self.audio = self.RecEngine.listen(source)
                    #amount of second for wait whe no one is speaking
                    #self.RecEngine.pause_threshold = 0.8
                    self.RecEngine.energy_threshold = 300
                    # after listening process the command
                    self.ProcessCommand()
                else:
                    self.ListenLabel['text'] = "Listening Stopped"
                    return
        except OSError as e:
            print(e)
            self.StopThreading()
            self.ListenLabel['text'] = "OS error Occur \nListening Stopped\nRestart the process"
            
        
    #this function process the command using google api
    def ProcessCommand(self):
        query = ''
        voice = ''
        if not self.is_listning:
            return
        if self.audio.get_raw_data != None:
            self.ListenLabel['text'] = 'Processing Please Wait'
            try:
                #this google api is convert the audio data into text
                query = self.RecEngine.recognize_google(self.audio,language='en-in')
                if 'x' in query or 'X' in query or 'multiply' in query:
                    query = query.replace('x','*')
                    query = query.replace('X','*')
                    query = query.replace('multiply','*')
                if 'plus' in query:
                    query = query.replace('plus','+')
                if 'minus' in query:
                    query = query.replace('minus','-')
                if 'by' in query:
                    query = query.replace('by','/')
                    query = query.replace('divide','')
                if 'divide' in query:
                    query = query.replace('by','')
                    query = query.replace('divide','/')
                if 'stop' in query:
                    self.StopThreading()
                    #self.is_listning = False
                    #self.takeCommand()
                    return
                    # result is calculate using eval() function
                self.resultEntVar.set(eval(query))
                self.EntVar.set(query)
                voice = str(query) + 'is' + str(eval(query))
                voice = self.ClearVoice(voice)
                #for speaking the output
                self.Speak(voice)
                
                
            except Exception as e:
                #print('Query is ' + query)
                #print(e)
                self.ListenLabel['text'] = "Can't Recognized.Please say again"
                time.sleep(3)
            if self.is_listning:
                #print('hi')
                self.takeCommand()
    # this function cleat the voice or remove unwanted words for processing
    def ClearVoice(self,voice):
        if '/' in voice:
            voice = voice.replace('/','by')
        if '*' in voice:
            voice = voice.replace('*','multiply by')
        if '.' in voice:
            voice = voice.replace('.','point')
        return voice
    # this functio insert the value in calculator window
    def putnum(self,x):
        if not self.is_listning:
            self.EntStr = self.EntVar.get()
            self.EntStr += str(x)
            self.EntVar.set(self.EntStr)
    # to calculate the answer and show on gui window
    def getAns(self):
        if not self.is_listning:
            ans = ''
            query = self.Ent.get()
            try:
                ans = round(float(eval(query)),2)
            except:
                ans = 'Bad Expression'
            self.resultEntVar.set(ans)
            self.EntStr = ''
            self.resEntStr = ''
    # to clear the input and output
    def Clear(self):
        self.EntStr = ''
        self.resEntStr = ''
        self.EntVar.set(self.EntStr)
        self.resultEntVar.set(self.resEntStr)
    # initialize all GUI components like Button Label Frames
    def MyGUIComponent(self):
        height = 2
        width = 10
        fontsize = 15
        self.TopFrame = Frame(self.MainWindow)
        self.TopHeading = Label(self.TopFrame,font=('normal', fontsize+10),text = 'Voice Control Calculator')
        self.Ent = Entry(self.TopFrame,width = 25,textvariable = self.EntVar)
        self.resultEnt = Entry(self.TopFrame,width = 15,textvariable = self.resultEntVar)
        self.MiddleFrame = Frame(self.MainWindow)
        self.BottomFrame = Frame(self.MainWindow)
        self.ListenLabel = Label(self.BottomFrame,font=('normal', fontsize),text = '')
        self.VoiceEngineLabel = Label(self.BottomFrame,font=('normal', fontsize),text = '')
        self.ListenEngineLabel = Label(self.BottomFrame,font=('normal', fontsize),text = '')

        #My all buttons here
        self.btn1 = Button(self.MiddleFrame,text = '1',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('1'))
        self.btn2 = Button(self.MiddleFrame,text = '2',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('2'))
        self.btn3 = Button(self.MiddleFrame,text = '3',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('3'))
        self.btn4 = Button(self.MiddleFrame,text = '4',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('4'))
        self.btn5 = Button(self.MiddleFrame,text = '5',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('5'))
        self.btn6 = Button(self.MiddleFrame,text = '6',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('6'))
        self.btn7 = Button(self.MiddleFrame,text = '7',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('7'))
        self.btn8 = Button(self.MiddleFrame,text = '8',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('8'))
        self.btn9 = Button(self.MiddleFrame,text = '9',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('9'))
        self.btn0 = Button(self.MiddleFrame,text = '0',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('0'))
        self.btneql = Button(self.MiddleFrame,text = '=',width = width,height = height,font=('normal', fontsize),command = self.getAns)
        self.btnplus = Button(self.MiddleFrame,text = '+',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('+'))
        self.btnminus = Button(self.MiddleFrame,text = '-',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('-'))
        self.btnmultiply = Button(self.MiddleFrame,text = '*',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('*'))
        self.btndivide = Button(self.MiddleFrame,text = '/',width = width,height = height,font=('normal', fontsize),command = lambda:self.putnum('/'))
        self.btnclear = Button(self.MiddleFrame,text = 'C',width = width,height = height,font=('normal', fontsize),command = self.Clear)
        self.btnStartVoice = Button(self.MiddleFrame,text = 'Start Voice\n Control',width = width,height = height,font=('normal', fontsize),command = self.StartThreading)
        self.btnStopVoice = Button(self.MiddleFrame,text = 'Stop Voice\n Control',width = width,height = height,font=('normal', fontsize),command = self.StopThreading)
        self.btnexit = Button(self.MiddleFrame,text = 'Exit',width = width,height = height,font=('normal', fontsize),command = self.MainWindow.destroy)
        self.PackGUIComponent()
    # to set all GUI components on main window
    def PackGUIComponent(self):
        self.TopFrame.pack()
        self.MiddleFrame.pack()
        self.BottomFrame.pack()
        self.TopHeading.grid(row = 0,columnspan = 2)
        self.Ent.grid(row = 1 ,column= 0)
        self.resultEnt.grid(row = 1,column = 1)
        self.btn9.grid(row = 1,column = 0)
        self.btn8.grid(row = 1,column = 1)
        self.btn7.grid(row = 1,column = 2)
        self.btn6.grid(row = 2,column = 0)
        self.btn5.grid(row = 2,column = 1)
        self.btn4.grid(row = 2,column = 2)
        self.btn3.grid(row = 3,column = 0)
        self.btn2.grid(row = 3,column = 1)
        self.btn1.grid(row = 3,column = 2)
        self.btn0.grid(row = 4,column = 1)
        self.btnplus.grid(row = 0,column = 0)
        self.btnminus.grid(row = 0,column = 1)
        self.btnmultiply.grid(row = 0,column = 2)
        self.btndivide.grid(row = 0,column = 4)
        self.btneql.grid(row = 4,column = 0)
        self.btnclear.grid(row = 4,column = 2)
        self.btnStartVoice.grid(row = 1,column = 4)
        self.btnStopVoice.grid(row = 2,column = 4)
        self.btnexit.grid(row = 3,column = 4)
        self.VoiceEngineLabel.grid(row = 0,column = 0)
        self.ListenEngineLabel.grid(row = 1,column = 0)
        self.ListenLabel.grid(row = 2,column = 0)
        
if __name__ == "__main__":
    Calculator()