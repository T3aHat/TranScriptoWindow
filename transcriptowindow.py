
#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.
NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:
    pip install pyaudio
"""

# [START speech_transcribe_streaming_mic]
from __future__ import division
import re
import sys
from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import types
import pyaudio
from six.moves import queue
from tkinter import ttk, messagebox
import tkinter
import threading
import textwrap

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        global tflag
        while not self.closed and tflag:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def btn_clicked():

    # subf.destroy()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "snow")
    root.attributes("-fullscreen", True)
    t1 = threading.Thread(target=work1)
    t1.setDaemon(True)
    t1.start()


def on_closing():
    global tflag
    try:
        subf.wm_attributes("-topmost", False)
    except:
        pass
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        tflag = False
        root.quit()
        try:
            subf.destroy()
        except:
            pass
    else:
        try:
            subf.wm_attributes("-topmost", True)
        except:
            pass


def work1():
    global var, tflag
    var.set("ここに音声認識結果が表示されます")
    language_code = 'ja-JP'  # a BCP-47 language tag
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)
        # Now, put the transcription responses to use.
        for response in responses:
            if not response.results:
                continue
            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript
            if not result.is_final:
                txtlist = textwrap.wrap(transcript, int(ww/w))
                print(txtlist)
                setxt = ""
                if(len(txtlist) <= num_comment):
                    for i in range(len(txtlist)):
                        setxt += txtlist[i]
                    var.set(setxt)
                else:
                    for i in range(num_comment):
                        setxt += txtlist[len(txtlist)-num_comment+i]
                    var.set(setxt)

            else:
                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    on_closing()


if __name__ == '__main__':
    fontsize = 30
    fontcolour = "red"
    num_comment = 3
    alpha = 50
    tflag = True
    bold = "bold"
    root = tkinter.Tk()
    ww = root.winfo_screenwidth()
    wh = root.winfo_screenheight()

    #root.wm_attributes("-topmost", True)
    ttk.Style().configure("TP.TFrame", background="snow")
    root.title("TranScriptoWindow")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    f = ttk.Frame(master=root, style="TP.TFrame", width=ww, height=wh)
    f.pack()
    var = tkinter.StringVar()
    tmp = "日本語"
    var.set(tmp)
    label = ttk.Label(root, textvariable=var,
                      wraplength=ww, font=("メイリオ", fontsize, bold), foreground=fontcolour, background="snow")
    w = label.winfo_reqwidth()/len(tmp)
    h = label.winfo_reqheight()
    label.place(x=0, y=(wh-num_comment*h-alpha))  # -αは下のタスクバーの分

    subf = tkinter.Tk()
    subf.protocol("WM_DELETE_WINDOW", on_closing)
    subf.wm_attributes("-topmost", True)
    subf.geometry("300x300+"+str(int(ww/2-300/2))+"+"+str(int(wh/2-300/2)))
    subf.title("Settings")

    lnumcomment = ttk.Label(subf, text="Number of comments",
                            wraplength=ww)
    lnumcomment.pack()
    txt1 = tkinter.Entry(subf, width=20)
    txt1.insert(tkinter.END, num_comment)
    txt1.pack()

    lfontsize = ttk.Label(subf, text="Fontsize",
                          wraplength=ww)
    lfontsize.pack()
    txt2 = tkinter.Entry(subf, width=20)
    txt2.insert(tkinter.END, fontsize)
    txt2.pack()

    lfontcolour = ttk.Label(subf, text="Font colour",
                            wraplength=ww)
    lfontcolour.pack()
    txt3 = tkinter.Entry(subf, width=20)
    txt3.insert(tkinter.END, fontcolour)
    txt3.pack()

    lalpha = ttk.Label(subf, text="y-axis correction(If positive,display above)",
                       wraplength=ww)
    lalpha.pack()
    txt4 = tkinter.Entry(subf, width=20)
    txt4.insert(tkinter.END, alpha)
    txt4.pack()

    bl1 = tkinter.BooleanVar(subf)
    bl1.set(True)
    CheckBox1 = tkinter.Checkbutton(
        subf, text="Bold", variable=bl1)
    CheckBox1.pack()

    def apply():
        global label, w, h, num_comment, alpha
        label.place_forget()
        num_comment = int(txt1.get())
        fontsize = int(txt2.get())
        fontcolour = txt3.get()
        alpha = float(txt4.get())
        if(bl1.get()):
            bold = "bold"
        else:
            bold = "normal"
        if(fontcolour == "snow"):
            fontcolour = "white"
        label = ttk.Label(root, textvariable=var,
                          wraplength=ww, font=("メイリオ", fontsize, bold), foreground=fontcolour, background="snow")
        w = label.winfo_reqwidth()/(len(tmp))
        h = label.winfo_reqheight()
        label.place(x=0, y=(wh-num_comment*h-alpha))

    btn = ttk.Button(subf, text="Start", command=btn_clicked)
    btn.pack(side="right")
    applybtn = ttk.Button(subf, text="Apply", command=apply)
    applybtn.pack(side="right")

    root.mainloop()
