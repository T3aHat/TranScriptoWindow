# TranScriptoWindow  
[公式ガイドの例](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/speech/microphone/transcribe_streaming_mic.py)をベースにしています.  
  
# 機能及び変数紹介  
動画は[コチラ](https://twitter.com/T3ahat/status/1264638352743002112)  
![sample.gif](https://github.com/T3aHat/TranscripToWindow/blob/master/sample/sample.gif)  
リアルタイムに音声認識した結果を字幕としてウィンドウにオーバーレイします.  
起動したまま別のタブを操作でき,あらゆるコンテンツに字幕をつけたまま画面共有できるので,画面共有するオンライン会議に有効です.  
![settings.gif](https://github.com/T3aHat/TranscripToWindow/blob/master/sample/settings.png)  
* `Number of comments`  
表示される認識結果の行数.num_commentに相当.    
* `Fontsize`  
フォントサイズ.fontsizeに相当.  
* `Font colour`  
フォントカラー.fontcolourに相当.  
* `y-axis correction`  
y軸補正.下にタスクバーを表示している場合,一番下のコメントがタスクバーに重なってしまうのを避けるため.
正の整数ならコメントが全体的に下に移動する.  
* `bold`  
チェックで太字になる.  

# 環境  
* Windows10  
tkinterの`-transparentcolor`がかなり環境依存なため,windows環境以外では動作しません.  
* Python 3.7  
* pyaudio 0.2.11  
* Google Cloud SDK  

# 使用方法  
`$python transcriptowindow.py`を実行し,`start`ボタンを押してPCに向かって話しかけるのみです.  
環境構築方法は[コチラ](https://qiita.com/teahat/items/86b68e03056e914c80f8)

# 関連記事  
書いてみました.  
[リアルタイムに音声認識して字幕をオーバーレイしてみた【Python】](https://qiita.com/teahat/items/86b68e03056e914c80f8)
