カラー作成ツール(RGB)に、HTML/CSSやmatplotlibで指定できるカラーネーム(cname)をカレーパレットにまとめたミニアプリ(mac版)です。
This is a mini app (mac version) that combines a color creation tool (RGB) and color names (cnames) that can be specified with HTML/CSS and matplotlib into a curry palette.


ver1.0
・研修の教材として提供していただいたRGBスライダー・アプリをベースにしています。
・カラーパレットには、W3Cで定義された141色(grayとgreyの重複排除)を納めています。Hex code順なので、使い勝手はよくありません。今後改善予定です。
・HTML/CSSやmatplotlibのcolor指定など、コーディング時に利用する想定で、コピーボタンとコピー状況をstatusバーに表示できるようにしています。
(補足)今後の改良予定として、色の指定方法、バレットの改良・拡張拡充など予定しています。



Upload common parts of reusable GUI. It assumes Qt Designer v5.9.6 for Mac.

| 実行ファイル(app) | main code   | ui code       | 
| ----------------- | ----------- | ------------- | 
| colorPal.app      | colorPal.py | rgb_cnames.py | (注)pythonコードは、前提 Qt Desinger v5.8を前提にしています。
|                   |             |               | 
