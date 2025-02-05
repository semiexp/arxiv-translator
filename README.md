# arxiv-translator

OpenAI API を使い、arXiv 論文を日本語訳するローカル Web アプリです。

## 使い方

Node.js が入っている環境を前提とします。

1. このリポジトリを clone します

```
git clone https://github.com/semiexp/arxiv-translator.git
```

2. バックエンドを動かすために必要なライブラリをインストールします

```
cd arxiv-translator/backend
pip install -r requirements.txt
```

3. `backend/.secret/apikey.txt` に OpenAI の API key を保存します。
4. `frontend` 以下にて `npm run start` を実行します。

```
cd ../frontend
npm run start
```

5. フロントエンド、バックエンドそれぞれの URL が表示されるので、フロントエンド (Vite) 側の URL を開きます。
6. arXiv 論文の URL を URL 欄に入力し、"Translate" ボタンを押します。

## OpenAI 以外の API サーバーを使う場合

OpenAI API と互換性のある API サーバーに対応しています。

`frontend/package.json` の

```
    "server": "cd ../backend && PYTHONPATH=. python3 app/main.py",
```

の行を、次のように変更します。

```
    "server": "cd ../backend && PYTHONPATH=. python3 app/main.py --base-url <base_url> --model-name <model_name>",
```

`<base_url>` には API のエンドポイントの URL を、`<model_name>` にはモデル名を指定します。詳細は各 API サーバーのドキュメント等をご確認ください。
