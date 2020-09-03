# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import enum
from collections import namedtuple

# 흑과 백 선수 구현 클래스
class Player(enum.IntEnum):
    black = 1
    white = 2

    # 한 선수가 돌을 두면 other 메소드를 호출하여 색을 변경
    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

# 좌표
class Point(namedtuple('Point', 'row col')):
    pass