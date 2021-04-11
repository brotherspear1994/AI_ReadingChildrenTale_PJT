# BE 환경설정

> ARI 프로젝트 백엔드를 사용하기 위해서는 **아래의 환경설정을 반드시 해주어야 한다.**

2021.04.01

---

[TOC] 

---



## 1. Python 버전

**python==3.7**

- AI 패키지 연결을 위해서 `python==3.7` 환경에서 세팅이 되어야한다.



## 2. pip 설치

- 먼저 requirements.txt에 있는 python package를 설치한다.
```bash
$ pip install -r requirements.txt
```
- 추가로 아래의 패키지를 설치한다.

<!-- ```bash
conda install pytorch=1.7.0 torchvision torchaudio cudatoolkit=10.1 -c pytorch
``` -->



## 3.Image Captioning을 위한 설정

### 3.1 CUDA 드라이버 설치

- cmd에서 아래의 명령어로 현재 컴퓨터 사양에 맞는 **CUDA Version**을 확인한다.
```bash
nvidia-smi
```
- 여기서는 **CUDA Version: 10.2**를 기준으로 한다.
- [CUDA 드라이브 설치 페이지](https://developer.nvidia.com/cuda-toolkit-archive)에 가서 버전에 맞는 드라이브를 설치한다.
- 드라이브 설치 후 버전에 맞는 **cudatoolkit**과 **pytorch**를 다시 설치해준다.
- 먼저 기존에 설치한 pytorch를 제거해준다.
```bash
$ conda remove pytorch
```
- 그리고 다시 설치해준다.
```bash
conda install pytorch=1.7.0 torchvision torchaudio cudatoolkit=10.1 -c pytorch
```

### 3.2 pdy 파일 생성

- `backend/Codes/speack_image/IC/vqa_origin/` 폴더 위치에서 아래의 명령어를 실행한다.
```bash
$ python setup.py build develop
```
- `backend/Codes/speack_image/IC/vqa_origin/maskrcnn_benchmark/` 폴더에 `__C`로 시작하는 `.pyd` 파일이 생성된 것을 확인한다.
- :ballot_box_with_check: **작업환경이 변경되면 반드시 pdy 파일을 다시 생성해주어야 한다!!!**



### 3.3 checkpoints 다운로드

- 구글 공유폴더에 들어있는 checkpoints 폴더를 다운받는다.
- 압축을 풀고 폴더 내의 파일&폴더를 `backend\Codes\speak_image\IC` 옮겨준다.






***Copyright* © 2021 SSAFY_SEOUL4_TEAM2_ARI**