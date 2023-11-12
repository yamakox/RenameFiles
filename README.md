# RenameFiles - ファイル名を一括変更するためのWindows用wxPythonアプリ

## 使い方

1. アプリをビルドしてインストーラを作成します。
2. インストーラを使ってアプリをインストールすると、スタートメニューとエクスプローラのコンテキストメニューの「送る」にアイコンが登録されます。

## Windowsアプリのビルド方法

ソースコードのあるディレクトリで以下のコマンドを実行します。

```powershell
py -m venv venv
venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
python setup.py bdist_msi
```

.\distディレクトリにインストーラのmsiファイルが生成されます。

## 使用している素材について

アイコンは https://www.iconfinder.com/ にて公開されているフリーアイコンを使用しています。

* https://www.iconfinder.com/icons/49255/rename_icon
