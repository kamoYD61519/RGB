import sys
from PyQt5 import QtCore as Qc, QtGui as Qg, QtWidgets as Qw  
from PyQt5.QtCore import Qt
#追加import
import pyperclip 
from matplotlib.colors import cnames

from rgb_cnames import *

class MyForm(Qw.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)      # 上位クラスの初期化ルーチンを呼び出す
        self.ui = Ui_MainWindow()     # importするapp.pyの中にあるUi_MainWindowsクラスのインスタンス化
        self.ui.setupUi(self)         # インスタンス・メソッドの実行

        # ----------  上記までが定型 ---------------------------
        # QSlider
        self.ui.rs.valueChanged.connect(self.colorChange)
        self.ui.gs.valueChanged.connect(self.colorChange)
        self.ui.bs.valueChanged.connect(self.colorChange)
        # ----------  上記までがr元RGBスライダーアプリの初期設定　----------------
        
        ## windowタイトルのセット
        self.setWindowTitle("Color RGB Slider & Palettes")

        #　カラーリストの取得とグループ分割
        grid_num = 28 # カラーパレットを7行x4列で表示するため
        self.colors = self.prepare_colors()
        self.groups = [self.colors[i:i + grid_num] for i in range(0, len(self.colors), grid_num)]
        
        # QComboBoxでグループを選択、カラーパレットの更新(update_grid)
        self.ui.combo_box.addItems([f"カラーグループ{i+1}" for i in range(len(self.groups))])  # 5グループ)
        self.ui.combo_box.currentIndexChanged.connect(self.update_grid)

        #
        self.ui.copyButton1.clicked.connect(self.copy_cname)
        self.ui.copyButton2.clicked.connect(self.copy_rgb)

        # 初期グリッド表示
        self.update_grid(0)

    # ---------- 関数 ---------------------------
    # color_labelの背景色に基づいて適切な文字色(white or black)を選択する
    def get_text_color1(self, r, b, g):
        # 明度を計算 (人間の目の感度を考慮)
        brightness = (r * 299 + g * 587 + b * 114) / 1000  
        return 'white' if brightness < 128 else 'black'
    
    def get_text_color2(self, hex_code):
        hex_code = hex_code.lstrip('#')
        r, g, b = int(hex_code[:2], 16), int(hex_code[2:4], 16), int(hex_code[4:], 16)
        # 明度を計算 (人間の目の感度を考慮)
        brightness = (r * 299 + g * 587 + b * 114) / 1000  
        return 'white' if brightness < 128 else 'black'
    
    def copy_rgb(self):
        rgb=self.ui.rgb.text()
        clipboard = Qg.QGuiApplication.clipboard()
        clipboard.setText(rgb)
        self.statusBar().showMessage(f"Copied '{rgb}' to clipboard", 2000)

    def copy_cname(self):
        c_name=self.ui.cnameLabel.text()
        if c_name == 'None' or c_name =='':
            self.statusBar().showMessage(f"Warning: cname does not exist.", 2000)
        else:
            clipboard = Qg.QGuiApplication.clipboard()
            clipboard.setText(c_name)
            self.statusBar().showMessage(f"Copied '{c_name}' to clipboard", 2000)

    # ----------  下記からが元のRGBスライダーアプリの関数　----------------
    # 追加1　ラベルrgb,hexLの文字カラーの動的変更
    # 追加2 status barへ情報表示
    # 追加3 cnameLabelのリセット
    def colorChange(self):
        r=self.ui.rs.value()
        self.ui.rn.setText(str(r))
        g=self.ui.gs.value()
        self.ui.gn.setText(str(g))
        b=self.ui.bs.value()
        self.ui.bn.setText(str(b))
        
        iro=f'#{r:02x}{g:02x}{b:02x}'
        irorgb=f'rgb({r},{g},{b})'
        text_iro = self.get_text_color1(r,g,b)
        self.ui.hexL.setStyleSheet(f"background-color:{iro};\n"
                                   "border-color: black;\n"
                                    "border-style:solid;\n" 
                                    "border-width:10px;\n" 
                                    f"color:{text_iro}"
                                    )
        self.ui.hexL.setText(iro)
        self.ui.rgb.setStyleSheet(f"background-color:{iro};\n"
                                    "border-radius:8px;\n"
                                    "border-color:#a1a1a1;\n"
                                    "border-style:solid;\n"
                                    "border-width:3px;\n"
                                    f"color:{text_iro}"
                                    )
        self.ui.rgb.setText(irorgb)
        self.ui.cnameLabel.setText('None')
        pyperclip.copy(iro)
        #
        
        # ** 追加 ** stausBarへの表示
        self.statusBar().showMessage(f"Copied '{iro}' to clipboard", 2000)
    # ----------  上記までが元のRGBスライダーアプリの関数　----------------

    # カラーパレット用データ準備: matplotlibのcnamesから色リストを取得してソート
    def prepare_colors(self):
        # matplotlib.colors.cnamesは辞書型のカラーリスト{'name':'#000000'}
        # cnames.item()は辞書型データのすべてのkey,valueの組み合わせをリストで返してくれるもの
        # cnamesから重複データを排除する
        color_list = {}
        for name, hex_code in cnames.items():
        # cnameがまだ登録されていない場合のみ追加
            if hex_code not in color_list.values():
                color_list[name] = hex_code
        # hex_code重複のうち、cyanとmagentaを追加する。他の重複はgrayとgreyの違い
        color_list['cyan']='#00FFFF'
        color_list['magenta']='#FF00FF' 
        # lambdaは、リストをソートする時のsorted関数の定型文
        # sorted(リスト, key=lambda x:  x[ソート対象にするするkeyにしたい要素index])
        color_items = sorted(color_list.items(), key=lambda x: x[1])  # HEXコードでソート
        return [(name, hex_code) for name, hex_code in color_items]
    
    
    def click_palette(self,name,hex_code):
        hex_code_ = hex_code.lstrip('#')
        r,g,b = int(hex_code_[:2], 16), int(hex_code_[2:4], 16), int(hex_code_[4:], 16)
        self.ui.rs.setProperty("value", r)
        self.ui.gs.setProperty("value", g)
        self.ui.bs.setProperty("value", b)
        self.ui.cnameLabel.setText(f"{name}")
        self.statusBar().showMessage(f"Selected {name} {hex_code} and Copied '{hex_code}' to clipboard", 3000)
        
    # グリッドを選択されたグループで更新
    def update_grid(self, group_index):
        # 現在のグリッド内のウィジェットを削除
        for i in reversed(range(self.ui.gridLayout.count())): # reversed(range())　rangeの逆順範囲を作る。逆順にwidjetしていくのがポイント
            widget = self.ui.gridLayout.itemAt(i).widget() # widgetはQLayoutItemに紐づけられている(親子関係)
            if widget is not None:
                widget.setParent(None) # 親をなくすことで子であるwidgetもクリアされる

        # 選択されたグループを取得
        group_colors = self.groups[group_index]

        # グリッドを再構築
        rows, cols = 7,4 # 7行4列
        for i in range(28):
            row = i // cols
            col = i % cols

            # ラベル作成
            color_label = Qw.QLabel()
            if i < len(group_colors):  # 色がある場合は表示
                name, hex_code = group_colors[i]
                color_label.setText(f"{name}\n{hex_code}")
                color_label.setAlignment(Qt.AlignLeft)

                # 背景色と文字色を設定
                tc=self.get_text_color2(hex_code)
                #tc="yellow"
                color_label.setStyleSheet("\n"
                f"color:{str(tc)};\n"
                f"font-size:12px;\n"
                f"background-color:{name};\n")
            else:
                # カラーリスト(group_colors)に表示するカラーがない場合は非表示
                color_label.setVisible(False)

            # サイズを調整
            color_label.setFixedSize(100, 36)
            # クリックイベントを設定
            color_label.mousePressEvent = lambda event, name=name,hex_code=hex_code: self.click_palette(name,hex_code)
            # グリッドに追加
            self.ui.gridLayout.addWidget(color_label, row, col)

    

# ----------  下記から定型 ---------------------------
if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)         #パラメータは正しくはコマンドライン引数を与える
    wmain = MyForm()                        #MyFormのインスタンスを作って
    wmain.show()                            #表示する
    sys.exit(app.exec())  