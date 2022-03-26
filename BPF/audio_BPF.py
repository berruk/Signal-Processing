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
    data = struct.unpack('{n}h'.format(n=length), data)
    data = np.array(data)
    sound.close()
    return data

#Helper function for BPF filter
def BPF_helper(data,fcL,fcH):
    output = np.zeros(len(data))
    J = np.zeros(8) 
    for i in range(len(data)):
        y, Jnew = BandPassFilter(data[i],J,fcL,fcH,sample_rate)
        J = Jnew
        output[i]= y
    return output    

#Apply BPF
def BPF(file_name, fcL, fcH):
    return BPF_helper(open_wav(file_name),fcL,fcH)

#Save wav file from array
def save_wav(file_name,audio):
    wav_file=wave.open(file_name,"w")

    wav_file.setparams((1, 2, sample_rate, len(audio), "NONE", "not compressed"))

    for sample in audio:
        wav_file.writeframes(struct.pack('{n}h'.format(n=1), int(sample)))

    wav_file.close()

    return

#save_wav("Africanew.wav",BPF_helper(open_wav("Africa.wav"),400,3000))   

