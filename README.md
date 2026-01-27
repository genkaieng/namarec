# namarec

ニコニコ生放送自動録画ツール。

## Dependencies

録画には streamlink, FFmpeg、配信開始通知の受信に genkaieng/nicopush に依存するので、それぞれインストールしておく。

- [streamlink](https://streamlink.github.io/)
- [FFmpeg](https://www.ffmpeg.org/)
- [genkaieng/nicopush](https://github.com/genkaieng/nicopush)

## Usage

### .env ファイルを作成

```sh
cp .env.example .env
```

#### .envファイルを設定

```
# 録画するユーザーIDを,(カンマ繋ぎ)繋ぎで設定
NAMAREC_USER_ID_LIST=
```

### 実行

```sh
make run
```

### 個別に実行

#### 配信開始通知受信プロセス

```sh
make nicopush
```

#### 自動録画プロセス

```sh
make recorder
```
