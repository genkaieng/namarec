# namarec  -生REC-

ニコ生録画ツールです。<br>
HLS配信をmp4ファイルに保存します。

:white_check_mark: 生放送録画<br>
:white_check_mark: タイムシフト録画

<sup><b>※ コメントやギフト演出は付きません。</b></sup>

## インストール

### Go:

```sh
go install github.com/genkaieng/namarec@latest
```

## Requirements

このツールは内部で[FFmpeg](https://www.ffmpeg.org/)を利用しているので、FFmpegをインストールしてパスを通しておく必要があります。<br>
各OSで利用できるパッケージマネージャを使うなりしてインストールしておいてください。

FFmpegが利用できることを確認

```sh
ffmpeg -version
```

## 実行

### 生放送録画

生放送ID(lv123456789)を指定して録画を開始出来ます。

```sh
namarec lv123456789
```

### タイムシフト録画

タイムシフトを録画するには、タイムシフトを見れるアカウントのセッションIDを渡す必要があります。

```sh
SESSION=<セッションID> namarec lv123456789
```

#### セッションIDを取得するには

1. ブラウザで[ニコニコ生放送ページ](https://live.nicovideo.jp)を開いてログインする。
2. ブラウザの開発者ツールを開く(F12キー)
3. Cookies一覧から`https://live.nicovideo.jp`のCookieの中からキー名`user_session`の値を取り出す<br>
**※セッションIDは**`user_session_{ユーザーID}_{ランダムな文字列}`**の形になってます。**
