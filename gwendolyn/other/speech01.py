# coding: utf-8
import speech_recognition as sr
sr.__version__
r = sr.Recognizer()
r.recognize_google()
harvard = sr.AudioFile('harvard.wav')
with harvard as source:
    audio = r.record(source)
type(audio)
r.recognizer_google(audio)
r.recognize_google(audio)
with harvard as source:
    audio = r.record(source, duration=4)
r.recognize_google(audio)
jackhammer = sr.AudioFile('jackhammer.wav')
with jackhammer as source:
    audio = r.record(source)
r.recognize_google(audio)
with jackhammer as source:
    r.adjust_for_ambient_noise(source)
with jackhammer as source:
    r.adjust_for_ambient_noise(source)
with jackhammer as source:
    r.adjust_for_ambient_noise(source)
with jackhammer as source:
    r.adjust_for_ambient_noise(source)
with jackhammer as source:
    r.adjust_for_ambient_noise(source)
with jackhammer as source:
    r.adjust_for_ambient_noise(source)
    audio = r.record(source)
r.recognize_google(audio)
with jackhammer as soure:
    r.adjust_for_ambient_noise(source, duration=0.5)
with jackhammer as soure:
    r.adjust_for_ambient_noise(source, duration=0.5)
with jackhammer as soure:
    r.adjust_for_ambient_noise(source, duration=0.5)
with jackhammer as soure:
    r.adjust_for_ambient_noise(source, duration=0.5)
get_ipython().run_line_magic('colors', '')
get_ipython().run_line_magic('pinfo', '%colors')
with jackhammer as soure:
    r.adjust_for_ambient_noise(source, duration=0.5)
with jackhammer as source:
    
    r.adjust_for_ambient_noise(source, duration=0.5)
with jackhammer as source:
    r.adjust_for_ambient_noise(source, duration=0.5)
    audio = r.record(source)
r.recognize_google(audio)
r.recognize_google(audio, show_all=True)
