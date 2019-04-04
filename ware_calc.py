import wave,io
import numpy as np
from pydub import AudioSegment
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt

# ./static/wuwen
def calc_ware(path_prefix):
    fp = open(path_prefix + ".mp3", 'rb')
    data = fp.read()
    fp.close()

    aud = io.BytesIO(data)
    sound = AudioSegment.from_file(aud, format='mp3')
    raw_data = sound._data

    l = len(raw_data)
    f = wave.open(path_prefix + ".wav", 'wb')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(16000)
    f.setnframes(l)
    f.writeframes(raw_data)
    f.close()

    f = wave.open(path_prefix + ".wav", "rb")

    params = f.getparams()

    nchannels, sampwidth, framerate, nframes = params[:4]

    str_data = f.readframes(nframes)
    print(str_data)
    print(params)
    f.close()

    wave_data = np.fromstring(str_data, dtype=np.short)

    time = np.arange(0, nframes) / framerate / 2

    fft_size = 8000

    xs = wave_data[:fft_size]

    freqs = np.linspace(0, framerate / 2, fft_size / 2 + 1)

    yy = fft(xs)
    yf = abs(fft(xs))
    yf1 = abs(fft(xs)) / ((len(freqs) / 2))

    xf = np.arange(len(xs)) - fft_size / 2
    print(wave_data.max())

    plt.subplot(311)
    plt.plot(time, wave_data / 29697)
    plt.xlabel("time(s)")
    plt.title('Data wave')

    plt.subplot(313)
    plt.plot(xf, yf1, 'r')
    plt.title('FFT of wave', color='#7A378B')
    plt.savefig(path_prefix + ".png")
    plt.close()
    return path_prefix + ".png", yf1
    # plt.show()
    # print("")