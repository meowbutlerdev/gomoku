# mcts-omok
개발중입니다.

# Tree
```
.
├── gomoku/
│   ├── agent/
│   │   ├── base.py                     : 에이전트 기본 인터페이스
│   │   └── navie.py                    : 무작위 수를 두는 봇
│   ├── checkpoints/                    : 모델 체크포인트
│   ├── data/
│   │   ├── generator_test_sample.py    : 샘플 모델 훈련
│   │   ├── generator.py                : 모델 훈련용 제너레이터
│   │   ├── index_processor.py          : http://renjuoffline.com/의 기보 중 필요한 데이터만 추출
│   │   ├── processor.py                : index_processor.py에서 추출된 데이터를 numpy 배열로 변환 및 저장
│   │   └── sampling.py                 : 추출된 데이터 중 훈련 데이터 샘플링
│   ├── encoders/
│   │   ├── base.py                     : 변환기 기본
│   │   └── oneplane.py                 : 자기 자신의 돌은 1, 상대의 돌은 -1, 빈 곳은 0으로 변환하는 변환기
│   ├── mcts/
│   │   └── mcts.py                     : MCTS 알고리즘
│   ├── networks/
│   │   ├── large.py                    : 오목 수 예측용 큰 합성곱 신경망 층
│   │   ├── medium.py                   : 오목 수 예측용 중간 합성곱 신경망 층
│   │   └── small.py                    : 오목 수 예측용 작은 합성곱 신경망 층
│   ├── data/
│   │   └── notation.py                 : 문자로 된 기보를 숫자로 변환
│   ├── board.py                        : 바둑판 구현 및 게임 현황
│   ├── types.py                        : 각 선수 및 돌의 좌표
│   ├── utils.py                        : 돌 착수 위치 및 바둑판 출력
│   └── zobrist.py                      : 조브리스트 해싱
├── bot_v_bot.py                        : 봇끼리 대국 진행
├── generate_mcts_games.py              : MCTS로 대국 데이터 생성
└── human_v_bot.py                      : 사람과 봇 대국 진행
```

# Skills
- python3

# Release  
|Version|Date|Comments|
|---|---|---|
|-|-|개발중|

<br>

---
  
<br>

#### Open Source License는 [이곳](NOTICE.md)에서 확인해주시고, 문의사항은 [Issue](https://github.com/IllIIIllll/mcts-omok/issues) 페이지에 남겨주세요.
