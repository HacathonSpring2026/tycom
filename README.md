# TyCom
- IT初学者
- タイピングが遅く、Linux,Git,Dockerのコマンドを覚えていないが、瞬時に打てるようになりたい人向け

# 環境構築
1. .envファイルの準備
    - `cp .env.sample .env`を実行する
3. 初回ビルド,起動
    - Docker Desktopを立ち上げる
    - Dockerイメージのビルドを行う<br />
      `docker compose build`
    - Dockerコンテナをバックグラウンドで起動<br />
      `docker compose up -d`
    - `tycom-django`と`tycom-db`という２つのコンテナが起動できたかを確認<br />
    `docker compose ps`
3. 以下のURLにアクセスして開発サーバーを起動<br />
    `http://localhost:8000`

# その他 
1. アプリを作成
    - 以下のコマンドでアプリ作成<br />
    `docker compose exec django-web python manage.py startapp {アプリ名}`
2. マイグレーション
    - DBのマイグレーションファイルを作成<br />
    `docker compose exec django-web python manage.py makemigrations`
    - DBをマイグレーション<br />
    `docker compose exec django-web python manage.py migrate`
4. 管理ユーザー(admin)作成
  `docker compose exec django-web python manage.py createsuperuser`
5. コンテナ停止
    `docker compose down`
   ※ボリュームを削除してDBの内容を初期化する場合<br />
   `docker compose down -v` 
