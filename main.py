import speech_recognition as sr
import keyboard
import pyaudio
import wave
import time
import sys
import re

CHUNK = 2**10
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
record_time = 10
output_path = "./temp/output.wav"
hotkey = "right win"
is_pressing_hotkey = False

r = sr.Recognizer()


def press_callback(e):
    global is_pressing_hotkey
    if not is_pressing_hotkey:
        print("press")
    is_pressing_hotkey = True


def release_callback(e):
    global is_pressing_hotkey
    if is_pressing_hotkey:
        print("release")
    is_pressing_hotkey = False


def main():
    keyboard.on_press_key(hotkey, press_callback)
    keyboard.on_release_key(hotkey, release_callback)

    p = pyaudio.PyAudio()

    try:
        while True:
            if is_pressing_hotkey:
                audio = record(p)
                number = recognize(audio)

                if number is not None:
                    keyboard.write(number)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Keybord Interrupt")
        p.terminate()
        sys.exit()


def record(p):
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("Recording ...")
    frames = []
    for i in range(0, int(RATE / CHUNK * record_time)):
        data = stream.read(CHUNK)
        frames.append(data)

        if not is_pressing_hotkey:
            break

    print("Done.")

    stream.stop_stream()
    stream.close()

    wf = wave.open(output_path, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    with sr.AudioFile(output_path) as source:
        audio = r.record(source)

    return audio


def recognize(audio):
    global r

    text = None
    try:
        text = r.recognize_google(audio, language="ja-JP")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )

    if text is None:
        return None

    number = re.sub(r"[^0-9]", "", text)
    print("recognized number = ", number)
    return number


main()
