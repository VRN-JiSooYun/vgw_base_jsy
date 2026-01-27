#!/bin/sh

# 데이터베이스가 준비될 때까지 기다림 (선택 사항이지만 권장)
# 호스트와 포트는 환경변수 등으로 설정
# python manage.py migrate 실행 전 database 가 ready 될때까지 기다리는 로직
# while ! nc -z $DB_HOST $DB_PORT; do
#  echo "Waiting for database..."
#  sleep 1
# done

sleep 5

# 마이그레이션 실행
python manage.py migrate

python manage.py createsuperuser --noinput || true  # 이미 슈퍼유저가 존재하면 오류 무시

python manage.py runserver 0.0.0.0:8000

# # Django 서버 실행
# exec "$@"