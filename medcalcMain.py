'''
Created on Jun 29, 2021

@author: Silvermoon
'''
import kivy #importing kivy and various tools needed 
from kivy.app import App
from kivy.uix.label import Label 
from kivy.uix.popup import Popup #for popup window
from kivy.uix.floatlayout import FloatLayout #for popup window 
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager,Screen #manages Screens 
from kivy.lang import Builder #allows to load kv file no matter name 
from kivy.uix.popup import Popup #including popup window 
from kivy.core.window import Window #setting the window size in kivy 
from kivy.properties import StringProperty, BooleanProperty

Window.size=(360,600) # setting the window size for testing 

class medCalcNight(FloatLayout):
    def __init__(self,**kwargs):#creating the constructor 
        super(medCalcNight, self).__init__(**kwargs)
        Window.clearcolor=(0.157,0.157,0.157,1)# setting the background window color 
        
#-------------Math Functions--------------------------------------------------
    def supplyFx(self, mg, ml): #function to calculate supply Mgs per 1mL
        try:
            mg = float(self.ids.entrMgs.text) #getting the text from the kv file and converting it to a float 
            ml = float(self.ids.entrMls.text)
            ans = round(mg/ml,5) #calculating the answer and rounding to 5 decimal places 
            self.ids.entrAnswer.text = str(ans) #placing the answer in the text input field 
        except:
            ans = "ERROR" #if exception is thrown then give error for answer 
            self.ids.entrAnswer.text = ans
                    
#-----------------Clear Functions --------------------------------------
    def clearSupply(self):
        self.ids.entrMgs.text ='' #textinputs in the supply screen 
        self.ids.entrMls.text=''
        self.ids.entrAnswer.text=''
         
class HomeScreen(Screen): #homescreen button 
    pass
class supplyScreen(Screen, medCalcNight): #supply screen button 
    pass
class ivpScreen(Screen, medCalcNight):
    pass
class ivdripScreen(Screen, medCalcNight):
    pass
class dopamineScreen(Screen, medCalcNight):
    pass
class infusionScreen(Screen, medCalcNight):
    pass
class conversionScreen(Screen, medCalcNight):
    pass
class extraScreen(Screen, medCalcNight):
    pass
class settingsScreen(Screen, medCalcNight):
    pass 
class WindowManager(ScreenManager):#represent transitions between the windows, manages screens of applications  
    pass

kv = Builder.load_file("medcalckvfile.kv")#loads the layout file  
    

class medCalc(App): #building the application, main class of the application   
    def build(self):
        return kv 
if __name__ == "__main__": #running the application 
    medCalc().run()
