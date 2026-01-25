# namarec

ニコニコ生放送自動録画ツール。

## Dependencies

- [genkaieng/nldl](https://github.com/genkaieng/nldl)
- [genkaieng/nicopush](https://github.com/genkaieng/nicopush)

## Usage

### .env ファイルを作成

```sh
cp .env.example .env
```

.envファイルを設定

```
# 録画するユーザーIDを,(カンマ繋ぎ)繋ぎで設定
NAMAREC_USER_ID_LIST=
```

その他の設定項目については、[genkaieng/nldl](https://github.com/genkaieng/nldl)、[genkaieng/nicopush](https://github.com/genkaieng/nicopush)を参照

### 実行

```sh
python src/main.py
```
