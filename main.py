# coding: UTF-8
import wave
import struct
from scipy import fromstring,int16
import numpy as np
import os
import math
import speech_recognition as sr

#filenameに読み込むファイル、timeにカットする間隔
def cut_wav(filename,time):
  # timeの単位は[sec]

  # ファイルを読み出し
  wavf = filename + '.wav'
  wr = wave.open(wavf, 'r')

  # waveファイルが持つ性質を取得
  ch = wr.getnchannels()
  width = wr.getsampwidth()
  fr = wr.getframerate()
  fn = wr.getnframes()
  total_time = 1.0 * fn / fr
  integer = math.floor(total_time*100) # 小数点以下切り捨て
  t = int(time*100)  # 秒数[sec]
  frames = int(ch * fr * t /100)
  num_cut = int(integer//t)
  # waveの実データを取得し、数値化
  data = wr.readframes(wr.getnframes())
  wr.close()
  X = np.frombuffer(data, dtype=int16)

  for i in range(num_cut):
    print(i)
    # 出力データを生成
    outf = 'output/' + str(i) + '.wav'
    start_cut = int(i*frames)
    end_cut = int(i*frames + frames)
    print(start_cut)
    print(end_cut)
    Y = X[start_cut:end_cut]
    outd = struct.pack("h" * len(Y), *Y)

    # 書き出し
    ww = wave.open(outf, 'w')
    ww.setnchannels(ch)
    ww.setsampwidth(width)
    ww.setframerate(fr)
    ww.writeframes(outd)
    ww.close()

  for ii in range(num_cut): #分割した音声ファイルを文字起こし処理部へ渡し、文字起こし処理を繰り返す
    wav_file = 'output/' + str(ii) + '.wav'
    voice_disp(wav_file)

def voice_disp(wav_file):
  r = sr.Recognizer()
  with sr.AudioFile(wav_file) as source: #ここに音声ファイルを指定する（wav形式のファイルを使用すること）
    audio = r.record(source)
  text = r.recognize_google(audio, language='ja-JP')
  print(text)
  return voice_disp

# 一応既に同じ名前のディレクトリがないか確認。
file = os.path.exists("output")
print(file)

if file == False:
  #保存先のディレクトリの作成
  os.mkdir("output")

print("input filename = ")
f_name = "sample" #対象ファイル名を指定
print("cut time = ")
cut_time = input() #分割する長さは、実行時に指定する 単位は[sec]
cut_wav(f_name,float(cut_time))