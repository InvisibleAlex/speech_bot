import pyttsx3

engine = pyttsx3.init()

def text_to_file_eng(text):
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
    tmp_file_name = 'test_eng'
    engine.save_to_file(text, f'data/{tmp_file_name}.mp3')
    engine.runAndWait()
    return f'data/{tmp_file_name}.mp3'
