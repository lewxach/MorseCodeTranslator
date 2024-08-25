from pydub import AudioSegment
import numpy as np
from scipy.signal import find_peaks

morseDict = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9', '/': ' ', '.-.-.-': '.', '--..--': ',', '..--..': '?',
    '-.-.--': '!', '-....-': '-', '.-..-.': '"', '-.--.': '(', '-.--.-': ')',
    '---...': ':', '-.-.-.': ';', '-..-.': '/', '.--.-.': '@', '.----.': "'"
}

def loadthabih(file_path):
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(1)
    return audio

def aud2wav(audio):
    samples = np.array(audio.get_array_of_samples())
    samples = samples / np.max(np.abs(samples))
    return samples

def detectTones(samples, threshold=0.5, min_duration=100):
    above_threshold = np.where(samples > threshold, 1, 0)
    tone_starts = np.diff(above_threshold) > 0
    tone_ends = np.diff(above_threshold) < 0
    
    tone_durations = []
    for start, end in zip(np.where(tone_starts)[0], np.where(tone_ends)[0]):
        duration = end - start
        if duration > min_duration:
            tone_durations.append(duration)
    
    return tone_durations


def tones2moressasdasdfwd(tone_durations, dot_duration=100):
    morse_code = ''
    for duration in tone_durations:
        if duration < 3 * dot_duration:
            morse_code += '.'
        else:
            morse_code += '-'
        morse_code += ' '

    return morse_code.strip()

def morse2text(morse_code):
    words = morse_code.split('   ')
    interpreted_text = []

    for word in words:
        characters = word.split(' ')
        interpreted_word = ''.join([morseDict.get(char, '') for char in characters])
        interpreted_text.append(interpreted_word)

    return ' '.join(interpreted_text)

def interpret(file_path):
    audio = loadthabih(file_path)
    waveform = aud2wav(audio)
    tone_durations = detectTones(waveform)
    morse_code = tones2moressasdasdfwd(tone_durations)
    return morse2text(morse_code)

file_path = input("give the morse code audio file's path: ")
text = interpret(file_path)
print("got text: ", text)