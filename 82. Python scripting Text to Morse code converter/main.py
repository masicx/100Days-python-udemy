morse_letters = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...',
    'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': ' '
}

def text_to_morse(text):
    morse_code = ''
    for char in text.upper():
        if char in morse_letters:
            morse_code += morse_letters[char] + ' '
        else:
            morse_code += '? '  # Unknown character
    return morse_code.strip()

morse_code = text_to_morse(input("Enter text to convert to Morse code: "))
print(morse_code)
