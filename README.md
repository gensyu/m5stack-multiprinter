# multiprinter
マルチバイト文字などをM5Stackで表示するためのモジュールです。

## 中身
tools/convert.py
> .bdfのフォントファイルと文字リストから表示用のバイナリ、設定ファイルを作成

multiPrinter.py  
> M5StackのLCDに日本語を表示するモジュール

## 使用法
```
import multiPrinter
myprinter = multiPrinter.Printer('./tools/mycharset.txt', './tools/fontset.bin')
myprinter.multiprint('ほげほげ',0,0)
```