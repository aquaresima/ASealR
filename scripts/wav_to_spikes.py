import pandas as pd
import os
import wave
import numpy as np

import sys
lauscher_path = "/home/alequa/Documents/Research/phd_project/speech/lauscher"
sys.path.insert(0,lauscher_path)
from lauscher.audiowaves import FileMonoAudioWave
from lauscher.helpers import CommandLineArguments
from lauscher.transformations.wave2spike import Wave2Spike

def save_wav_mono(audio_file):
    '''
    Take Wave_read object as an input and save one of its
    channels into a separate .wav file.
    https://www.codegrepper.com/code-examples/python/convert+stereo+to+mono+python
    '''

    wav = wave.open(audio_file)
    mono_wav = audio_file.split('.')[2][1:] + '_mono.wav'
    mono_wav= os.path.join(project_folder,mono_wav)
    print(mono_wav)
    # Read data
    nch   = wav.getnchannels()
    print(nch)
    depth = wav.getsampwidth()
    wav.setpos(0)
    sdata = wav.readframes(wav.getnframes())

    # Extract channel data (24-bit data not supported)
    typ = { 1: np.uint8, 2: np.uint16, 4: np.uint32 }.get(depth)
    if not typ:
        raise ValueError("sample width {} not supported".format(depth))
    # print ("Extracting channel {} out of {} channels, {}-bit depth".format(channel+1, nch, depth*8))
    data = np.fromstring(sdata, dtype=typ)
    d = data[0::nch]
    # Save channel to a separate file
    outwav = wave.open(mono_wav, 'w')
    outwav.setparams(wav.getparams())
    outwav.setnchannels(1)
    outwav.writeframes(d.tostring())
    outwav.close()
    return mono_wav


project_folder = "/home/alequa/Documents/Research/phd_project/speech/ASealR/"

data = pd.read_csv(os.path.join(project_folder, "data/vocalizations","vocalizations_info.csv"))

audio_file = data.iloc[1].Filepath
out_file  = "my_first_spiketrain.npz "

mono_wav = save_wav_mono(audio_file)
file_ = os.path.join(project_folder,audio_file)
trafo = Wave2Spike(num_channels=70)
spikes = FileMonoAudioWave(mono_wav).transform(trafo)
spikes.export(out_file)


# for audio_file in data.Filepath:
#     print(audio_file)
#     out_file = audio_file.split('.')[2][1:] + '_spike_train70.npz'
#     out_file= os.path.join(project_folder,out_file)
#     print(out_file)
#     mono_wav = save_wav_mono(audio_file)
#     trafo = Wave2Spike(num_channels=70)
#     spikes = FileMonoAudioWave(mono_wav).transform(trafo)
#     spikes.export(out_file)

# for audio_file in data.Filepath:
#     print(audio_file)
#     out_file = audio_file.split('.')[2][1:] + '_spike_train350.npz'
#     out_file= os.path.join(project_folder,out_file)
#     print(out_file)
#     mono_wav = save_wav_mono(audio_file)
#     trafo = Wave2Spike(num_channels=350)
#     spikes = FileMonoAudioWave(mono_wav).transform(trafo)
#     spikes.export(out_file)