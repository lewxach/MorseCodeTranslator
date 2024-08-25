from pydub import AudioSegment
from pydub.generators import Sine

morseDict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', ' ': '/', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    '!': '-.-.--', '-': '-....-', '"': '.-..-.', '(': '-.--.', ')': '-.--.-',
    ':': '---...', ';': '-.-.-.', '/': '-..-.', '@': '.--.-.', "'": '.----.'
}

def morse2audio(morse_code, output_file):
    dot_duration = 100
    dash_duration = 3 * dot_duration
    frequency = 800
    silence_duration = dot_duration
    silence = AudioSegment.silent(duration=silence_duration)

    dot = Sine(frequency).to_audio_segment(duration=dot_duration)
    dash = Sine(frequency).to_audio_segment(duration=dash_duration)
    
    audio = AudioSegment.silent(duration=0)
        
    for symbol in morse_code:
        if symbol == '.':
            audio += dot + silence
        elif symbol == '-':
            audio += dash + silence
        elif symbol == ' ':
            audio += silence * 3
        elif symbol == '/':
            audio += silence * 7

    audio.export(output_file, format="wav")

def getMorseCode(text):
    text = text.upper()
    morse_code = ' '.join(morseDict.get(char, '') for char in text)
    return morse_code

def text2morse(text, output_file):
    morse_code = getMorseCode(text)
    morse2audio(morse_code, output_file)
    print(f"saved to {output_file}!!")

text = input("give the text to convert to morse code: ")
output_file = input("give the output file path (example, asdf.wav): ")
text2morse(text, output_file)