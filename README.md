# gomoku
Actor-Critic과 Policy Gradient를 이용한 인공지능 오목

# Tree
```
.
├── gomoku/
│   ├── agents/
│   │   ├── base.py                     : 에이전트 기본 인터페이스
│   │   ├── navie.py                    : 무작위 수를 두는 봇
│   │   ├── pg.py                       : Policy Gradient 봇
│   │   └── predict.py                  : 심층 신경망을 이용한 수 예측 봇
│   ├── data/
│   │   ├── generator.py                : 모델 훈련용 제너레이터
│   │   ├── index_processor.py          : http://renjuoffline.com/의 기보 중 필요한 데이터만 추출
│   │   ├── notation.py                 : 기보 데이터 파싱(문자로 된 기보를 숫자로 변환)
│   │   ├── processor.py                : index_processor.py에서 추출된 데이터를 numpy 배열로 변환 및 저장
│   │   └── sampling.py                 : 추출된 데이터 중 훈련 데이터 샘플링
│   ├── encoders/
│   │   ├── base.py                     : 변환기 기본
│   │   ├── oneplane.py                 : 자기 자신의 돌은 1, 상대의 돌은 -1, 빈 곳은 0으로 변환하는 변환기
│   │   └── simple.py                   : 13차 평면의 기본 변환기
│   ├── mcts/
│   │   └── mcts.py                     : MCTS 알고리즘
│   ├── networks/
│   │   ├── large.py                    : 오목 수 예측용 큰 합성곱 신경망 층
│   │   ├── medium.py                   : 오목 수 예측용 중간 합성곱 신경망 층
│   │   └── small.py                    : 오목 수 예측용 작은 합성곱 신경망 층
│   ├── rl/
│   │   ├── ac.py                       : Actor-Critic 봇
│   │   ├── experience.py               : 경험 데이터셋 클래스
│   │   └── q.py                        : Q-Learning 봇
│   ├── board.py                        : 바둑판 구현 및 게임 현황
│   ├── kerasutil.py                    : save HDF5 & load HDF5
│   ├── types.py                        : 각 선수 및 돌의 좌표
│   ├── utils.py                        : 돌 착수 위치 및 바둑판 출력
│   └── zobrist.py                      : 조브리스트 해싱
├── bot_v_bot.py                        : 봇끼리 대국 진행
├── bot_v_bot_agent_pg.py               : 봇끼리 대국 진행(Policy Gradient 모델)
├── eval_ac_bot.py                      : Actor-Critic 모델 성능 평가
├── eval_pg_bot.py                      : Policy Gradient 모델 성능 평가
├── generate_deep_learning_model.py     : 수 예측 모델 생성
├── generate_mcts_games.py              : mcts를 이용한 대국 데이터 생성
├── human_v_bot.py                      : 사람과 봇(random) 대국 진행
├── human_v_bot_mcts.py                 : 사람과 봇(mcts) 대국 진행
├── init_ac_agent.py                    : 정책/가치 출력 신경망
├── self_play_ac.py                     : Actor-Critic 봇 대국을 통한 경험데이터 생성
├── self_play_pg.py                     : Policy Gradient 봇 대국을 통한 경험데이터 생성
├── train_ac.py                         : Actor-Critic 봇으로 생성한 경험데이터로 모델 훈련
└── train_pg.py                         : Policy Gradient 봇으로 생성한 경험데이터로 모델 훈련
```

# Skills
- python3
- Numpy
- Keras
- HDF5
- TensorFlow

# How to use  
#### 사람의 대국 기보 데이터로 최초 모델 훈련
```python
python generate_deep_learning_model.py --board-size 15 --encoder simple --num-games None --epochs 5 --batch-size 512 --model-out <path>
```
#### 경험데이터 생성
- Actor-Critic 경험데이터  
  ```python
  python init_ac_agent.py --baord-size 15 <path>
  python self_play_ac.py --board-size 15 --learning-agent <path> --num-games 5000 --experience-out <path>
  ```
- Policy Gradient 경험데이터  
  ```python
  python self_play_pg.py --board-size 15 --learning-agent <path> --num-games 5000 --experience-out <path>
  ```
#### 경험데이터를 이용하여 모델 훈련
- Actor-Critic 모델 훈련
  ```python
  python train_ac.py --learning-agent <path> --agent-out <path> --lr 0.01 --bs 32 <experience paths>
  ```
- Policy Gradient 모델 훈련
  ```python
  python train_pg.py --learning-agent <path> <experience paths>
  ```
#### 모델 성능 평가
- Actor-Critic 모델 성능 평가
  ```python
  python self_play_ac.py --agent1 <path> --agent2 <path> --num-games 100
  ```
- Policy Gradient 모델 성능 평가
  ```python
  python self_play_pg.py --agent1 <path> --agent2 <path> --num-games 100
  ```

<br>

---
  
<br>

#### Open Source License는 [이곳](NOTICE.md)에서 확인해주시고, 문의사항은 [Issue](https://github.com/IllIIIllll/gomoku/issues) 페이지에 남겨주세요.
