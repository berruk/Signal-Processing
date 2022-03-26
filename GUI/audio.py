#
#   AUDIO LIBRARY
#   Methods:
#    open_wav: opens wav files
#    save_wav: saves wav files      
#    BPF: applies band pass filter
#    BSF: applies band stop filter
#


# @author Berru Karakaş
#             150190733
#               13.6.21

import wave, struct
import numpy as np
from filter import BandPassFilter #custom lib

sample_rate = 44100

#Open a wav file and unpack to a numpy array
def open_wav(file_name):
    sound = wave.open(file_name, 'r')  # reads file
    length = sound.getnframes()   # get frames
    data = sound.readframes(length)
    data = struct.unpack('{n}h'.format(n=length), data) #unpack to array
    data = np.array(data) #transforms to np array
    sound.close()
    return data

#Helper function for BPF filter
def BPF_helper(data,fcL,fcH):

    output = np.zeros(len(data)) #initialize with zeros 
    J = np.zeros(8) #initialize with zeros

    #Pass through filter for each frame
    for i in range(len(data)):
        y, Jnew = BandPassFilter(data[i],J,fcL,fcH,sample_rate)
        J = Jnew
        output[i]= y

    return output    

#Helper function for BSF filter
def BSF_helper(data,fcL,fcH):
    output = np.zeros(len(data))
    J = np.zeros(8) 
    for i in range(len(data)):
        y, Jnew = BandPassFilter(data[i],J,fcL,fcH,sample_rate)
        J = Jnew
        output[i]= data[i] - y
    return output  

#Apply BPF
def BPF(file_name, fcL, fcH):
    return BPF_helper(open_wav(file_name),fcL,fcH)

#Apply BSP
def BSF(file_name, fcL, fcH):
    return BSF_helper(open_wav(file_name),fcL,fcH)

#Save wav file from array
def save(file_name,audio):

    #Open wav file
    wav_file=wave.open(file_name,"w")

    #Set parameters
    wav_file.setparams((1, 2, sample_rate, len(audio), "NONE", "not compressed"))

    #Pack samples
    for sample in audio:
        wav_file.writeframes(struct.pack('{n}h'.format(n=1), int(sample)))

    #Close file
    wav_file.close()

def save_wav(file_name,input_file,fcL,fcH):    
    save(file_name,BPF_helper(open_wav(input_file),fcL,fcH))   

    return

