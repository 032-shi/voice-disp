# coding: UTF-8
import speech_recognition as sr

r = sr.Recognizer()

with sr.AudioFile("sample.wav") as source: #ここに音声ファイルを指定する（wav形式のファイルを使用すること）
  audio = r.record(source)

text = r.recognize_google(audio, language='ja-JP')

print(text)