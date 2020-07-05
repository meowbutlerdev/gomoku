# reinforcement-learning-omok
본 프로그램은 아래 책을 참고하여 제작되었습니다.  
<img src="http://image.yes24.com/goods/90323579/800x0" width="30%" height="30%">
<img src="http://image.yes24.com/goods/57617908/800x0" width="26.5%" height="26.5%">

# Tree
```
.
├── omok/
│   ├── agent/
│   │   ├── base.py          : 에이전트 기본 인터페이스
│   │   └── navie.py         : 무작위 수를 두는 봇
│   ├── encoders/
│   │   ├── base.py          : 변환기 기본
│   │   └── oneplane.py      : 자기 자신의 돌은 1, 상대의 돌은 -1, 빈 곳은 0으로 변환하는 변환기
│   ├── mcts/
│   │   └── mcts.py          : MCTS 알고리즘
│   ├── board.py             : 바둑판 구현 및 게임 현황
│   ├── types.py             : 각 선수 및 돌의 좌표
│   ├── utils.py             : 돌 착수 위치 및 바둑판 출력
│   └── zobrist.py           : 조브리스트 해싱
├── bot_v_bot.py             : 봇끼리 대국 진행
├── generate_mcts_games.py   : MCTS로 대국 데이터 생성
└── human_v_bot.py           : 사람과 봇 대국 진행
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

#### Open Source License는 [이곳](NOTICE.md)에서 확인해주시고, 문의사항은 [Issue](https://github.com/IllIIIllll/image-scrapper/issues) 페이지에 남겨주세요.
