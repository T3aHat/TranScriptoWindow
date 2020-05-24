# TranscripToWindow  
[公式ガイド](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/speech/microphone/transcribe_streaming_mic.py)の例をベースにしています.  
  
# 機能紹介  
![sample.mp4](https://github.com/T3aHat/TranscripToWindow/blob/master/sample/sample.gif)  
リアルタイムに音声認識した結果を字幕としてウィンドウにオーバーレイします.  
起動したまま別のタブを操作でき,あらゆるコンテンツに字幕をつけたまま画面共有できるので,画面共有するオンライン会議に有効です.  
  
# 環境  
* Windows10  
tkinterの`-transparentcolor`がかなり環境依存なため,windows環境以外では動作しません.  
* Python 3.7  
* pyaudio 0.2.11  
* Google Cloud SDK  

# 使用方法  
`$python transcriptowindow.py`を実行し,`start`ボタンを押してPCに向かって話しかけるのみです.  
環境構築方法は別記事にします.  
  
# 問題点  
Frameを閉じてもマイクのstreamingが終わりません.  
これは`threading`による影響だと考えていますが,まだ未解決ですので,コンソールを閉じて強制終了してください...  