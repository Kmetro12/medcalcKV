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
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager,Screen #manages Screens 
from kivy.lang import Builder #allows to load kv file no matter name 
from kivy.uix.popup import Popup #including popup window 
from kivy.core.window import Window #setting the window size in kivy 
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.dropdown import DropDown
from medCalcSettingsJson import settings_json #importing the json from medCalcSettings 
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import ObjectProperty  
from kivy.config import Config
import cProfile
from configparser import ConfigParser

#Window.size=(360,600) # setting the window size for testing 

class medCalcNight(FloatLayout):
    #kv = Builder.load_file("medcalckvfile.kv")#loads the layout file, NIGHT MODE
    test_screen = ObjectProperty(None)
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
            
    def ivpFx(self):
        try:
            ivpMg = float(self.ids.entrIvpMgs.text)
            ivpMls = float(self.ids.entrIvpMls.text)
            ivpAns = round(ivpMg/ivpMls,5)
            self.ids.entrIvpAnswer.text = str(ivpAns)
        except:
            ivpAns = "ERROR"
            self.ids.entrIvpAnswer.text = ivpAns
            
    def ivdFx(self):
        try:
            ivdMg = float(self.ids.entrIvdMgs.text)
            ivdDrop = float(self.ids.entrIvdDrop.text)
            ivdConc = float(self.ids.entrIvdConc.text)
            ivdAns = round(ivdMg*ivdDrop/ivdConc,5)
            self.ids.entrIvdAns.text = str(ivdAns)
        except: 
            ivdAns = "ERROR"
            self.ids.entrIvdAns.text = ivdAns
    def dopaFx(self):
        try:
            dopaMcg = float(self.ids.entrDopaMcg.text)
            dopaKg = float(self.ids.entrDopaKg.text)
            dopaDrop = 60
            dopaConc = float(self.ids.entrDopaConc.text)
            dopaAns =  round(dopaMcg*dopaKg*dopaDrop/dopaConc,5)
            
            self.ids.entrDopaAns.text = str(dopaAns)
        except:
            dopaAns = "ERROR"
            self.ids.entrDopaAns.text = dopaAns
            
    def infusionFx(self):
        try:
            infVol = float(self.ids.entrInfVol.text)
            infDrop = float(self.ids.entrInfDrop.text)
            infMin = float(self.ids.entrInfMin.text)
            infAns = round(infVol*infDrop/infMin,5)
            self.ids.entrInfAns.text = str(infAns)      
        except:
            infAns = "ERROR"
            self.ids.entrInfAns.text = infAns
            

    def convertFx(self):
        
        try: #try-catch loop to catch conversions 
            unit = float(self.ids.entrConvUnit.text)
            
            #error checking for weigfhts 
            if self.ids.firstSpinDrop.text =="ibs" or self.ids.secondSpinDrop.text =="kg" and self.ids.firstSpinDrop.text !="ibs" or self.ids.secondSpinDrop.text!="kg":
                answer = "ERROR"
                self.ids.entrConvAns.text = answer #error checking for weight to ensure not visited in a unit 
            if self.ids.firstSpinDrop.text !="ibs" or self.ids.secondSpinDrop.text !="kg" and self.ids.firstSpinDrop.text =="ibs" or self.ids.secondSpinDrop.text=="kg":
                answer = "ERROR"
                self.ids.entrConvAns.text = answer
            
            #weight conversions 
            if self.ids.firstSpinDrop.text == "ibs" and self.ids.secondSpinDrop.text == "kg": #ibs to Kg
                ibstoKg = round(unit/2.2046226218,5)
                self.ids.entrConvAns.text=str(ibstoKg)
            if self.ids.firstSpinDrop.text == "kg" and self.ids.secondSpinDrop.text == "ibs": #Kg to ibs 
                Kgtoibs = round(unit*2.2046226218,5)
                self.ids.entrConvAns.text=str(Kgtoibs)
            if self.ids.firstSpinDrop.text == "ibs" and self.ids.secondSpinDrop.text == "ibs": #ibs to ibs
                ibstoibs = round(unit,5)
                self.ids.entrConvAns.text=str(ibstoibs)
            if self.ids.firstSpinDrop.text == "kg" and self.ids.secondSpinDrop.text == "kg": #kg to Kg
                kgtokg = round(unit,5)
                self.ids.entrConvAns.text=str(kgtokg)
                
            #volume conversions MG  
            if self.ids.firstSpinDrop.text == "mg" and self.ids.secondSpinDrop.text == "mcg": #Mgs to Mcgs 
                mgsTomcgs = round(unit*1000,5)
                self.ids.entrConvAns.text = str(mgsTomcgs)
            if self.ids.firstSpinDrop.text == "mg" and self.ids.secondSpinDrop.text == "g": #Mgs to gs 
                mgsTogs = round(unit/1000,5)
                self.ids.entrConvAns.text = str(mgsTomcgs)
            if self.ids.firstSpinDrop.text == "mg" and self.ids.secondSpinDrop.text == "mg": #Mgs to Mgs 
                mgsTomgs = round(unit,5)
                self.ids.entrConvAns.text = str(mgsTomgs)
                
            #volume conversions MCG    
            if self.ids.firstSpinDrop.text == "mcg" and self.ids.secondSpinDrop.text == "mcg": #Mcgs to Mcgs 
                mcgsTomcgs = round(unit,5)
                self.ids.entrConvAns.text = str(mcgsTomcgs)
            if self.ids.firstSpinDrop.text == "mcg" and self.ids.secondSpinDrop.text == "mg": #Mcgs to mg 
                mcgsTomgs = round(unit*1000,5)
                self.ids.entrConvAns.text = str(mcgsTomgs)
            if self.ids.firstSpinDrop.text == "mcg" and self.ids.secondSpinDrop.text == "g": #Mcgs to g 
                mcgsTogs = round(unit/1000000,5)
                self.ids.entrConvAns.text = str(mcgsTogs)
            #volume conersions Gs 
            if self.ids.firstSpinDrop.text == "g" and self.ids.secondSpinDrop.text == "mcg": #g to Mcgs 
                gsTomcgs = round(unit*1000000,5)
                self.ids.entrConvAns.text = str(gsTomcgs)
            if self.ids.firstSpinDrop.text == "g" and self.ids.secondSpinDrop.text == "mg": #g to mg 
                gsTomgs = round(unit*1000,5)
                self.ids.entrConvAns.text = str(gsTomgs)
            if self.ids.firstSpinDrop.text == "g" and self.ids.secondSpinDrop.text == "g": #g to g 
                gsTogs = round(unit,5)
                self.ids.entrConvAns.text = str(gsTogs)
        except:
            answer = "ERROR"
            self.ids.entrConvAns.text = answer
    def parklandFx(self):
        try:
            burnml = 4.0 
            burnBSA = float(self.ids.parkTBSA.text)
            burnKg = float(self.ids.parkKg.text)
            burnDrop = float(self.ids.parkDropFact.text)
            
            first8 = (burnml*burnBSA*burnKg) #top portion of the division problem 
            gttsFirst = round(first8*burnDrop/480,5)
            self.ids.parkFirst8.text = str(gttsFirst)
            
            gttsSecond = round(first8*burnDrop/960,5)
            self.ids.parkNext16.text = str(gttsSecond)
            
            total = burnml*burnBSA*burnKg
            self.ids.parkTotal.text = str(total)
            
        except:
            answer = "ERROR"
            self.ids.parkFirst8.text = answer 
            self.ids.parkNext16.text = answer
            self.ids.parkTotal.text = answer 
    def o2TankFx(self):
        try: 
            PSI = float(self.ids.entrPSIo.text)
            LPM = float(self.ids.entrLpmo.text)
            
            dCylfact = 0.16 #D cylinder factor
            jumboDnECylfact = 0.28 #jumboD and E cylinder factor
            mCylfact = 1.56 #M cylinder factor
            hCylfact = 3.14 #H cylinder factor 
            saferes = 200 #safe residual pressure 
            
            
            if self.ids.oSpinnDrop.text == "Select Tank":
                answer = "ERROR"
                self.ids.entrAnso.text = answer 
            if self.ids.oSpinnDrop.text == "Jumbo D" or self.ids.oSpinnDrop.text == "E Cylinder": 
                oxygenLeftTime = round(((PSI-saferes)*jumboDnECylfact)/LPM,5)
                self.ids.entrAnso.text = str(oxygenLeftTime)
            if self.ids.oSpinnDrop.text == "D Cylinder": 
                oxygenTimeLeft = round(((PSI-saferes)*dCylfact)/LPM,5)
                self.ids.entrAnso.text=str(oxygenTimeLeft)
            if self.ids.oSpinnDrop.text == "M Cylinder": 
                o2Time = round(((PSI-saferes)*mCylfact)/LPM,5)
                self.ids.entrAnso.text=str(o2Time)
            if self.ids.oSpinnDrop.text == "H Cylinder": 
                o2Timeh = round(((PSI-saferes)*hCylfact)/LPM,5)
                self.ids.entrAnso.text=str(o2Timeh)
                
        except:  
            answer = "ERROR"
            self.ids.entrAnso.text = answer 
#-----------------Dropdown Functions --------------------------------------
    def convClickedFirst(self, value): #for the conversion window and the spinner dropdown 
        self.ids.firstSpinDrop.text = value
        
    def convClickedSecond(self,value2): #the second spinner widget on the dropdown 
        self.ids.secondSpinDrop.text = value2
    def oxygenClickedSecond(self, o2Val):
        self.ids.oSpinnDrop.text = o2Val
#-----------------END Dropdown Functions --------------------------------------      
#-----------------Clear Functions --------------------------------------
    def clearSupply(self):
        self.ids.entrMgs.text ='' #textinputs in the supply screen 
        self.ids.entrMls.text=''
        self.ids.entrAnswer.text=''
    def clearIvp(self):
        self.ids.entrIvpMgs.text=''
        self.ids.entrIvpMls.text=''
        self.ids.entrIvpAnswer.text=''
        
    def clearIvd(self):
        self.ids.entrIvdMgs.text=''
        self.ids.entrIvdDrop.text=''
        self.ids.entrIvdConc.text=''
        self.ids.entrIvdAns.text=''
        
    def clearDopa(self):
        self.ids.entrDopaMcg.text=''
        self.ids.entrDopaKg.text=''
        self.ids.entrDopaConc.text=''
        self.ids.entrDopaAns.text=''
        
    def clearInfusion(self):
        self.ids.entrInfVol.text=''
        self.ids.entrInfDrop.text=''
        self.ids.entrInfMin.text=''
        self.ids.entrInfAns.text=''
   
    def clearConversion(self):
        self.ids.entrConvUnit.text=''
        self.ids.entrConvAns.text=''
        
    def clearPark(self):
        self.ids.parkTBSA.text=''
        self.ids.parkKg.text=''
        self.ids.parkDropFact.text=''
        self.ids.parkFirst8.text=''
        self.ids.parkNext16.text=''
        self.ids.parkTotal.text=''
        
    def clearO2(self):
        self.ids.entrPSIo.text=''
        self.ids.entrLpmo.text=''
        self.ids.entrAnso.text='' 
        
    def clear_screen(self):
        self.clear_widgets()
#----------------------Start config change functions----------------------------------
    def switchModes(self):
        if self.ids.chkNight.active == True:
            print("test worked")
        if self.ids.chkDay.active == True:
            Window.clearcolor=(1,1,1,1)
            Builder.unload_file("medcalckvfile.kv")#loads the layout file, NIGHT MODE
            self.clear_widgets() 
            medCalc().stop()
            if __name__ == "__main__":
                medCalcDay().run() 
                
            print("Daymode Worked")
        
#----------------------Empty Classes to hold various screens-------------------------      
class HomeScreen(Screen, medCalcNight): #homescreen button, Screen,medCalcNight 
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
class parklandScreen(Screen, medCalcNight):
    pass
class o2Screen(Screen, medCalcNight):
    pass
class settingsScreen(Screen, medCalcNight):
    pass 
class WindowManager(ScreenManager):#represent transitions between the windows, manages screens of applications  
    pass
#----------------------END Empty Classes to hold various screens------------------------- 
kv = Builder.load_file("medcalckvfile.kv")#loads the layout file, NIGHT MODE
kvD = Builder.load_file("medcalckvfileDAY.kv") #loads day mode  

config = ConfigParser() 

'''
class medCalcDay(App):
    def build(self):
        return kvD
'''
class medCalc(App): #building the application, main class of the application   
    
    def build(self):
        self.use_kivy_settings = False #setting the default kivy settings to false
        #settings = self.config.get('medCalcSett', 'Night_Mode') #getting your custom settings file 
        return kv
       
    #building the settings config file
    def build_config(self, config):#setting the default values of the config file
        config.setdefaults('medCalcSett',{  
            'color': 'Night_Mode'})
       
    #how to display those settings in the settings panel
    def build_settings (self, settings):
        settings.add_json_panel('Settings', self.config,data=settings_json)
            
         
    #running the code in response to user changes 
    def on_config_change(self, config, section, key, value):
        if section == "medCalcSett":
            if value == "Night_Mode":
                pass   
        if section == "medCalcSett":
            if value == "Day_Mode":
                value = "Day_Mode"
                Window.clearcolor=(1,1,1,1) #setting window color to white
                
                def restart(self):
                    #self.root.clear_widgets()
                    self.stop() #stops the application 
                    config.setdefaults('medCalcSett',{'color': 'Night_Mode'}) #resetting the default values 
                    Builder.unload_file("medcalckvfile.kv") #unload the night kv file 
                    if __name__ == "__main__": #running the DAY MODE application 
                        medCalcDay().run() #runs the daymode application to start a new look 
                medCalc.stop(self) #stops the night mode app from running 
                restart(self) 
       
    def on_start(self):
        config = self.config 
    #ways to save the application settings and enable them on startup
        
class medCalcDay(App): #building the application, main class of the application   
   
    def build(self):
        self.use_kivy_settings = False #setting the default kivy settings to false
        #settings = self.config.get('medCalcSett', 'Night_Mode') #getting your custom settings file 
        return kvD

    #building the settings config file
    def build_config(self, config):
        config.setdefaults('medCalcSett',{ #setting the default values of the config file 
            'color': 'Day_Mode'})
    #how to display those settings in the settings pannel
    def build_settings (self, settings):
        settings.add_json_panel('SettingsDAY', self.config,data=settings_json)
            
    #running the code in response to user changes 
    def on_config_change(self, config, section, key, value):
        config.setdefaults('medCalcSett',{   #setting the default values of the config file 
                            'color': 'Day_Mode'}) #resetting the default values 
        if section == "medCalcSett":
            if value == "Night_Mode":
                Window.clearcolor=(0.157,0.157,0.157,1)# setting the background window color
                def restart(self):
                    #self.root.clear_widgets()
                    self.stop()
                    Builder.unload_file("medcalckvfileDAY.kv")
                    #Builder.load_file("medcalckvfileDAY.kv")

                    if __name__ == "__main__": #running the NIGHT MODE application 
                        medCalc().run() 
                #Builder.unload_file("medcalckvfile.kv")
                #medCalc.stop(self) 
                medCalcDay.stop(self) 
                #Config.write() 
                restart(self) 
         
        if section == "medCalcSett":
            if value == "Day_Mode":
                pass 

if __name__ == "__main__": #running the application 
    medCalc().run()
