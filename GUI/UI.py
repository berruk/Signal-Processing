#
#   GRAPHICAL
#   USER
#   INTERFACE
#

# @author Berru Karakaş
#             150190733
#               13.6.21

#Sometimes "YANIT VERMİYOR" and it takes long but eventually works!!!
#Maybe depends on the computer

import sys
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, QMessageBox, QPushButton
from PyQt5.QtCore import QSize 
import winsound
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

from audio import BPF_helper,BSF_helper,save_wav,open_wav #custom methods


#Main class for display
class MainWindow(QMainWindow):

    #Class variables
    freq = 0
    bw = 0
    mode = False 
    file_path = ""
    fcL = 0
    fcH = 0
    samplerate = 0

    def __init__(self):
        QMainWindow.__init__(self)
        #self.output = []
        #Set Window
        self.setMinimumSize(QSize(600, 220))    
        self.setWindowTitle("BAND FILTER") 

        ####SET INPUT LINES####

        #Frequency
        self.lineLabel = QLabel(self)
        self.lineLabel.setText('Frequency:')

        self.line = QLineEdit(self)
        self.line.move(80, 60)
        self.line.resize(200, 32)
        self.lineLabel.move(80, 20)

        #Bandwidth
        self.line_2Label = QLabel(self)     
        self.line_2Label.setText('Bandwidth %:')

        self.line_2 = QLineEdit(self)   
        self.line_2.move(300, 60)
        self.line_2.resize(200, 32)
        self.line_2Label.move(300, 20)


        #Combo Box for filter mode
        combo = QComboBox(self)
        combo.addItem("BPF")
        combo.addItem("BSF")
        combo.move(90, 120)
        self.qlabel = QLabel(self)
        self.qlabel.setText('Filter Mode')
        self.qlabel.move(90,90)
        combo.activated[str].connect(self.onChanged)   

        #####PUSH BUTTONS#####

        #Push button for sending input values
        pybutton = QPushButton('Send', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,32)
        pybutton.move(240, 120)

        #Push button for browsing input file
        browse = QPushButton('Browse', self)
        browse.clicked.connect(self.findFile)
        browse.resize(100,32)
        browse.move(380, 160)

        #Push button for playing filtered file
        play = QPushButton('Play', self)
        play.clicked.connect(self.playFile)
        play.resize(100,32)
        play.move(240, 160)

        #Push button for saving filtered file
        play = QPushButton('Save', self)
        play.clicked.connect(self.saveFile)
        play.resize(100,32)
        play.move(90, 160)
 
    #Method for finding file
    def findFile(self):
        filter = "wav(*.wav)" #filter for wav files

        #Search only wav files
        path = QtWidgets.QFileDialog.getOpenFileName(None, "Select Audio File", "", "Wav files (*.wav)")
        
        #Get file path
        self.file_path = path[0]
        
    #Method for filtering and playing file       
    def playFile(self):

        #If path not chosen, raise an exception
        if self.file_path == "":
            print("Choose a file")

        data, self.samplerate = sf.read(self.file_path)  #read file   

        #Band Stop Filter mode
        if self.mode:
            QMessageBox.about(self, "Filtering...","Band Stop Filter for fcL:{} fcH:{} applying".format(self.fcL,self.fcH))
            player = BSF_helper(data, self.fcL, self.fcH)
            QMessageBox.about(self, "DONE!","Press Play to listen, Save to Save")

        #Band Pass Filter mode
        else:
            QMessageBox.about(self, "Filtering...","Band Pass Filter for fcL:{} fcH:{} applying".format(self.fcL,self.fcH))
            player = BPF_helper(data, self.fcL, self.fcH)
            QMessageBox.about(self, "DONE!","Press Play to listen, Save to Save")
        
        #winsound.PlaySound(self.file_path, winsound.SND_FILENAME)
        sd.play(player, self.samplerate) #play audio

        #status = sd.wait()  # Wait until file is done playing

    #Method for saving file
    def saveFile(self):

        #Create file name with B appended to end
        splitted = self.file_path.split('.') #split with dot
        path = splitted[0] + "B." + splitted[1] #add B
        #write(path,self.samplerate, self.output.astype(np.int16))
        save_wav(path,self.file_path,self.fcL,self.fcH) #save
        QMessageBox.about(self, "Succesful", "Saved!")

    
    #Click for inputs
    def clickMethod(self):

        freq = float(self.line.text())
        bw = float(self.line_2.text())

        #Frequency and bandwidth bound check
        if (freq < 200 or freq > 7000) and (bw < 5 or bw > 50):
            QMessageBox.about(self, "Try Again!", "Frequency must be between 200 and 7000, Bandwidth must be between 5 and 50.")
        elif freq < 200 or freq > 7000:
            QMessageBox.about(self, "Try Again!", "Frequency must be between 200 and 7000")
        elif bw < 5 or bw > 50:
            QMessageBox.about(self, "Try Again!", "Bandwidth must be between 5 and 50")
        else:
            #High low frequency calculations
            self.fcH = freq + (freq*bw/100)
            self.fcL = freq - (freq*bw/100)
            print('Freq:{} {} '.format(self.fcH,self.fcL))
            print('Bandwidth:{} '.format(bw))

    #Click for
    def onChanged(self,text):
        
        #Choosing filter type
        if text == "BPF":
            self.mode = False
        else:
            self.mode = True

        self.qlabel.adjustSize() 

if __name__ == "__main__":
    
    #Create app
    app = QtWidgets.QApplication(sys.argv)
    #Create window
    mainWin = MainWindow()
    #Show window
    mainWin.show()
    #Execute app
    sys.exit(app.exec_())



       