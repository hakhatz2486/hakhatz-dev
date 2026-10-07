---
title: "CapsLockをF13にして独自のキーバインドを使う【Windows/AutoHotkey】"
description: "一等地のCapsLockをF13に再開発しよう！AutoHotkeyでカーソル移動や日付挿入を割り当てた設定をまとめました。"
published: "2026-09-26"
---

# CapsLockをF13にして独自のキーバインドを使う【Windows/AutoHotkey】

## 目次

## 1. なぜCapsLockをF13にするのか

### 1.1 なぜCapsLock？

キーボードの一等地で唯一不要なキーだからです。「`CapsLock`を使用するときは`CapsLock`を解除するとき」と揶揄されるほど、その誤爆の多さと不要さに不満を持たれています。

> CapsLockキーは、度々その位置や存在意義に疑問が持たれている。
> [CapsLockキー - Wikipedia](https://ja.wikipedia.org/wiki/CapsLock%E3%82%AD%E3%83%BC#%E7%8F%BE%E4%BB%A3%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8B%E5%AD%98%E5%9C%A8%E6%84%8F%E7%BE%A9)

`CapsLock`を無効化するのも良いですが、この一等地のキーを使わないのももったいないものです。
そのため、既存の`Ctrl`や`Shift`,`Alt`に対する新たな修飾キーとして再割当てをします。

### 1.2 なぜF13？

`F13`-`F24`キーは一般に現代の入力方式では使われないファンクションキーです。
そのため、他のソフトと干渉することが少なく、言わば好き勝手に設定できるフロンティアのようなものです。
そのうち`F13`キーを選ぶ理由は特に無く、分かりやすさのためです。
将来的に`F13`が他のソフトと衝突すれば、`F14`,`F15`,...のように変えやすい利点もあります。

`Ctrl`や`Esc`に割り当てる派閥もありますが、どちらも今の位置のままで大して困りませんし、`Esc`が欲しくなれば`F13`との組み合わせに割り当てれば済みます。
何より`F13`のほうが自由度とワクワク感があります。

## 2. CapsLockをF13に置き換える

複数の方法があります。ここで紹介する方法は、どちらも最終的にレジストリを書き換える方法です。

### 2.1 Change Keyを使う場合

[「Change Key」非常駐型でフリーのキー配置変更ソフト - 窓の杜](https://forest.watch.impress.co.jp/library/software/changekey/)

LHA/LZH形式で圧縮されているので[7-Zip](https://7-zip.opensource.jp/)等を使用して展開してください。

1. 解凍後はChange Key(ChgKey.exe)を**管理者として実行**します。
2. まず変更するCapsLockを選択し、割当先は右上の「Scan code」から**必ず四桁で**`F13`の3スキャンコード`0064`を入力/貼り付けします。
3. メニューバーの「登録」から「現在の内容で登録をします」で反映します。
4. Windowsを再起動します。

### 2.2 PowerShellを使う場合

Change Keyも内部では同じレジストリの値を書き換えているため、ソフトを入れたくない場合はPowerShellから直接設定できます。

スタートボタンを右クリックして「ターミナル(管理者)」を開き、次のコマンドを実行します。

```powershell
$map = [byte[]](0,0,0,0, 0,0,0,0, 2,0,0,0, 0x64,0,0x3a,0, 0,0,0,0)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layout" -Name "Scancode Map" -PropertyType Binary -Value $map -Force
```

設定はWindowsを再起動すると反映されます。

`Scancode Map`の値は、次のように区切って読みます。

- `0,0,0,0, 0,0,0,0`: ヘッダー。常に0
- `2,0,0,0`: 以降に続くエントリーの数。置き換え1件と終端1件で2
- `0x64,0,0x3a,0`: 置き換え。前半の`0x64,0`が変換後のキー(F13)、後半の`0x3a,0`が変換前のキー(CapsLock)
- `0,0,0,0`: 終端

元に戻すときは、同じく管理者のターミナルで次のコマンドを実行してから再起動します。

```powershell
Remove-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layout" -Name "Scancode Map"
```

## 3. AutoHotkeyでキーバインドを設定する

GitHubで配布中の[hakhatz2486/f13-keybindings](https://github.com/hakhatz2486/f13-keybindings)を元に解説します。

### 3.1 カーソル移動

ホームポジションから動かずに矢印を触れます。
`IJKL`: 上下左右

### 3.2 日付と時刻の挿入

### 3.3 音量調整

### 3.4 その他(ブラウザ操作、CapsLock/NumLockの切り替えなど)

潰した`CapsLock`を使いたい場合のために、`F13+C`で`CapsLock`、テンキーレスキーボードでも`NumLock`を使うため、`F13+N`で`NumLock`。

## 4. スクリプトの実行

### 起動の効率化



## 5. 使ってみて分かったこと

### 5.1 ゲームでは基本使えない

### スタートアップフォルダは遅い

## 6. まとめ
