# 아리 구현동화 (Ari Storytelling)

>2021년 SSAFY 2학기 특화프로젝트
>
>```AWS 배포환경에서 개발 및 AI 기술 이용으로 필수 key값들을 제외해 업로드하여, repo를 clone 받는다해도 작동하지 않을 가능성이 높으니 가급적 아래 프로젝트 소개 영상을 참고해주시기 바랍니다.```
>
>- [유투브 소개영상](https://www.youtube.com/watch?v=udTZicdGTxs)

---

[TOC]

---

![Ari Storytelling](Docs/img/index.png)



## Intro

- 개발기간: 2021년 3월 8일 - 2021년 4얼 9일
- 프로젝트 배경
  - 아이들에게 동화책을 읽어주기 어려운 부모들의 문제 해결
  - 아이들의 독서 습관 독려
- 서비스 개요
  - **어린이를 위해 그림동화책을 읽어주는 기능**을 제공한다.
  - **Image Captioning**: 이미지 캡셔닝을 통해 그림통화책의 내용을 텍스트로 전달한다.
  - **Text-to-speech(TTS)**: 텍스트를 음성으로 재생할 수 있다.
  - **Voice Conversion**: 부모님 등 제3자의 목소리로 그림동화책을 들을 수 있다.
  - **증강현실(AR)**: 그림책에 추가된 AR 기능을 사용할 수 있다.
- 프로젝트명
  - **아리(ARI) 구연동화**
  - AI + AR 기술이 합성된 것을 상징적으로 표현
  - Ari를 지혜를 상징하는 부엉이 모습으로 캐릭터화



## :computer: Tech Stack

- Frontend
  - Django
  - HTML, CSS
  - Bootstrap
- Backend
  - Django
  - Android



## :gear: Install and Usage

> `git clone`을 한 후 `backend` 폴더에서 **반드시** 아래의 환경설정을 해주어야 한다.

### 1. Python 버전

**python==3.7**

- AI 패키지 연결을 위해서 python==3.7 환경에서 세팅이 되어야한다.

### 2. pip 설치

- 먼저 requirements.txt에 있는 python package를 설치한다.

```bash
$ pip install -r requirements.txt
```

### 3. Image Captioning을 위한 설정

**3.1 CUDA 드라이버 설치**

- cmd에서 아래의 명령어로 현재 컴퓨터 사양에 맞는 CUDA Version을 확인한다.

```
nvidia-smi
```

- 여기서는 CUDA Version: 10.2를 기준으로 한다.
- CUDA 드라이브 설치 페이지에 가서 버전에 맞는 드라이브를 설치한다.
- 드라이브 설치 후 버전에 맞는 cudatoolkit과 pytorch를 다시 설치해준다.
- 먼저 기존에 설치한 pytorch를 제거해준다.

```
conda remove pytorch
```

- 그리고 다시 설치해준다.

```
conda install pytorch=1.7.0 torchvision torchaudio cudatoolkit=10.1 -c pytorch
```

**3.2 pdy 파일 생성**

- `backend/Codes/speack_image/IC/vqa_origin/` 폴더 위치에서 아래의 명령어를 실행한다.

```bash
$ python setup.py build develop
```

- `backend/Codes/speack_image/IC/vqa_origin/maskrcnn_benchmark/` 폴더에 __C로 시작하는 .pyd 파일이 생성된 것을 확인한다.
- :ballot_box_with_check: 작업환경이 변경되면 반드시 pdy 파일을 다시 생성해주어야 한다!!!

**3.3 checkpoints 설정**

- 추가 설치 라이브러리 ffmpeg, g2pk

  ```
  conda install -c conda-forge x264 ffmpeg
  pip install -v python-mecab-ko
  pip install g2pk
  ```

  그 외에 추가 라이브러리 오류는 많은 시행착오 속에 기록해두지 못했습니다.

  에러가 발생하면 그대로 설치해주시면 감사하겠습니다.

- IC, TTS, VC, TTS_KOR 모델 경로 설정

- IC와 TTS모델 중 일부는 용량이 너무 크고 기본 skeleton 코드 가이드에서 설치 경로가 존재하기에 따로 다운로드 받아 이하 경로에 저장 부탁드립니다.

- IC 모델 경로 설정

  - image_captioning.py파일만 수정
  - [detectron pre-trained model](https://drive.google.com/file/d/1A6S00G5uRtDYWrtB32QP5KkpYrgHBR68/view?usp=sharing) 다운로드 후 exec/IC 에 저장
  - [vocab](https://drive.google.com/file/d/13hJT7MV2K3ugC4gPE9hTvVR3PyuJzC67/view?usp=sharing) 다운로드 후 exec/IC 에 저장
  - [captioning pre-trained model](https://drive.google.com/file/d/1AZx47VgVLv58JtSe_FnWPSKfx88G72iS/view?usp=sharing) 다운로드 후 exec/IC 에 저장
  - 57번째 줄: cfg 파일 불러오는 경로를 {자신의 경로}/exec/backend/Codes/speak_image/IC/model_data/detectron_model.yaml 로 수정
  - 64, 161, 168번째 줄:  경로를 {자신의 경로}/exec/IC/{해당 모델 파일} 로 수정

- TTS 모델 경로 설정

  - tacotron.py파일만 수정
  - [Tacotron pre-trained model](https://drive.google.com/file/d/1IUWQHB2cFQXekNuo-yCoKrY5wD8nNpnV/view?usp=sharing) 다운로드 후 exec/TTS 에 저장
  - [Waveglow pre-trained model](https://drive.google.com/file/d/1lVP5gQoB-fi6aydKuxjVE64qMexGX2yL/view?usp=sharing) 다운로드 후 exec/TTS 에 저장
  - 36번째 줄: cfg 파일 불러오는 경로를 {자신의 경로}/exec/backend/Codes/speak_image/TTS/config.yaml 로 수정
  - 47, 60번째 줄: 경로를 {자신의 경로}/exec/TTS/{해당 모델 파일} 로 수정

- VC 모델 경로 설정

  - voice_conversion.py만 수정
  - 38번째 줄: cfg 파일 불러오는 경로를 {자신의 경로}/exec/backend/Codes/speak_image/VC/config.yaml 로 수정
  - 51, 95번째 줄: 경로를 {자신의 경로}/exec/VC/{해당 모델 파일} 로 수정

- KOR_TTS 모델 경로 설정

  - hparams.py만 수정
  - 56, 57번째 줄: os.path.join안에 절대경로를 {자신의 경로}/exec/VC/로 수정
  - 58~60번째 줄: 로그와 평가된 파일을 저장하는 곳으로 inference에서 쓰이지 않음

- 파이썬에서 상대경로 설정부분에서 같은 이름의 파일로 인해 충돌이 생기는 문제가 발생했습니다. 그 이유와 시간의 문제로 인해 부득이하게 절대경로를 사용하여 학습 모델을 사용할 때 절대 경로를 수정해야합니다.

**3.4 DATABASES 설정**

- 아래코드 부분 주석해제

```django
# backend/ari/settings.py 108번째 줄

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'ari',
#         'USER': 'ari',
#         'PASSWORD': 'ssafy',
#         'HOST': 'j4a402.p.ssafy.io',
#         'PORT': '3306',
#         'OPTIONS': {
#             'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
#         }
#     }
# }

# 주석해제 필요
```



### 4. 서버실행

- 위의 모든 설정이 끝나고나면, `backend` 폴더에서 아래의 명령어로 서버를 실행한다.

```bash
$ python manage.py runserver
```

- 서버를 실행 후 **안드로이드에서 접속**해준다.



## :family_man_woman_boy:Team Member

### 이규용(Lee Gyuyong)

> [@github](https://github.com/gyuyong290)

- Team Leader
- Frontend

### 윤서완(Yoon Seowan)

- Android

### 이송영(Lee Songyoung)

- Backend
- UCC

### 이형창(Lee HyungChang)

- Backend
- DataBase

### 조성훈(Cho Sunghoon)

- AI
- Server



## 알려진 버그

> 2021년 4월 9일 현재까지 없음



***Copyright\* © 2021 SSAFY_SEOUL4_TEAM2_ARI**

