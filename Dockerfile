# vgw_sample 폴더 한단계 위로 Dockerfile 이동시켜서 사용할 것 
# 여기서는 build context 제한 때문에 외부 폴더를 가져올 수 없음
# 
# VORA v2는 vgw_vora 폴더에서 빌드된 상태
# VORA v1은 vgw_vora_master 폴더에서 빌드된 상태

FROM ubuntu:24.04

LABEL org.opencontainers.image.source https://github.com/voronoi-dev-team/vgw_vora
LABEL org.opencontainers.image.description "Docker Image for Development Deploy Voronoi VORA"

RUN apt update && apt upgrade -y && apt install wget software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa && apt install -y \
  python3.9 \
  python3.9-venv \
  python3.9-dev \
  python3-pip

# R 설치
RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
RUN add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/" 
RUN apt install --no-install-recommends r-base-core=4.4.1-3.2404.0 r-base=4.4.1-3.2404.0 r-recommended=4.4.1-3.2404.0 -y

# pycairo 설치
RUN apt install -y build-essential libcairo2-dev

# 작업 디렉토리 설정
WORKDIR /app

# 가상 환경 생성
RUN python3.9 -m venv /app/venv

# 가상 환경의 python과 pip을 기본으로 설정
ENV PATH="/app/venv/bin:$PATH"

# pip 업그레이드
RUN pip install --upgrade pip

# (필요 시) requirements.txt 복사 및 패키지 설치
COPY ./vgw_sample/requirements.txt .
RUN pip install -r requirements.txt

# 프로젝트 파일 복사
COPY ./vgw_sample .
COPY ./vgw_vora ./VORA
COPY ./vgw_vora_master ./VDE

# ENTRYPOINT 스크립트 실행 권한 부여
RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]