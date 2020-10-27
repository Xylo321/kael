import random


class ZuoBiao(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class QiZi(object):
    CHE = '车'
    MA = '马'
    XIANG = '象'
    SHI = '士'
    JIANG = '将'
    ZU = '兵'

    HONG_QI = '红棋'
    HEI_QI = '黑棋'

    FAN_CHE = '車'
    FAN_MA = '馬'
    FAN_XIANG = '相'
    FAN_SHI = '仕'
    FAN_JIANG = '帥'
    FAN_ZU = '卒'

    KONG = '＋'

    def __init__(self, value, hong_hei_type):
        self._value = value
        self._hong_hei_type = hong_hei_type

    def __str__(self):
        return self._value

    def get_value(self):
        return self._value

    def get_type(self):
        return self._hong_hei_type


class XiangQi(object):
    def __init__(self):
        self._qi_pan = [
            [QiZi(QiZi.CHE, QiZi.HONG_QI), QiZi(QiZi.MA, QiZi.HONG_QI), QiZi(QiZi.XIANG, QiZi.HONG_QI),
             QiZi(QiZi.SHI, QiZi.HONG_QI), QiZi(QiZi.JIANG, QiZi.HONG_QI), QiZi(QiZi.SHI, QiZi.HONG_QI),
             QiZi(QiZi.XIANG, QiZi.HONG_QI), QiZi(QiZi.MA, QiZi.HONG_QI), QiZi(QiZi.CHE, QiZi.HONG_QI)],
            ['＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋'],
            ['＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋'],
            [QiZi(QiZi.ZU, QiZi.HONG_QI), '＋', QiZi(QiZi.ZU, QiZi.HONG_QI), '＋', QiZi(QiZi.ZU, QiZi.HONG_QI), '＋',
             QiZi(QiZi.ZU, QiZi.HONG_QI), '＋', QiZi(QiZi.ZU, QiZi.HONG_QI)],
            ['＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋'],
            # 楚河汉界
            ['＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋'],
            [QiZi(QiZi.FAN_ZU, QiZi.HEI_QI), '＋', QiZi(QiZi.FAN_ZU, QiZi.HEI_QI), '＋', QiZi(QiZi.FAN_ZU, QiZi.HEI_QI), '＋',
             QiZi(QiZi.FAN_ZU, QiZi.HEI_QI), '＋', QiZi(QiZi.FAN_ZU, QiZi.HEI_QI)],
            ['＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋'],
            ['＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋', '＋'],
            [QiZi(QiZi.FAN_CHE, QiZi.HEI_QI), QiZi(QiZi.FAN_MA, QiZi.HEI_QI), QiZi(QiZi.FAN_XIANG, QiZi.HEI_QI),
             QiZi(QiZi.FAN_SHI, QiZi.HEI_QI), QiZi(QiZi.FAN_JIANG, QiZi.HEI_QI), QiZi(QiZi.FAN_SHI, QiZi.HEI_QI),
             QiZi(QiZi.FAN_XIANG, QiZi.HEI_QI), QiZi(QiZi.FAN_MA, QiZi.HEI_QI), QiZi(QiZi.FAN_CHE, QiZi.HEI_QI)],
        ]

        if random.randint(0, 1) == 0:
            self._is_hong_hei_play = QiZi.HONG_QI
        else:
            self._is_hong_hei_play = QiZi.HEI_QI

    def get_qi_pan_print_str(self):
        qi_pan_print_str = ''
        j = 0
        for line in self._qi_pan:
            j += 1
            if j > 5 and j < 7:
                # print('   楚   河    汉   界   ')
                qi_pan_print_str += '   楚   河    汉   界   \n'
            i = 0
            for qi_zi in line:
                i += 1
                if i == 9:
                    # print(qi_zi, end='\n')
                    qi_pan_print_str += str(qi_zi) + "\n"
                else:
                    # print(qi_zi, end='-')
                    qi_pan_print_str += str(qi_zi) + "-"

        return qi_pan_print_str

    def get_is_hong_hei_play(self):
        return self._is_hong_hei_play

    def play(self, src_zuobiao, dst_zuobiao):
        # 校验，棋盘坐标
        if src_zuobiao.x >=0 and src_zuobiao <= 9 and dst_zuobiao.x >= 0 and dst_zuobiao.y <= 9:
            raise Exception('棋子坐标不在棋盘中。')

        # 校验，原坐标与目标坐标不能相同
        if src_zuobiao.x == dst_zuobiao.x and src_zuobiao.y == dst_zuobiao.y:
            raise Exception('原坐标与目标坐标相同。')

        # 获取对应坐标的棋子
        src_qi_zi = self._qi_pan[src_zuobiao.x][src_zuobiao.y]
        dst_qi_zi = self._qi_pan[dst_zuobiao.x][dst_zuobiao.y]

        # 校验，是不是由当前玩家走
        if self.get_is_hong_hei_play() != src_qi_zi.get_type():
            raise Exception('开局%s优先，%s莫动。' % (self._is_hong_hei_play, src_qi_zi.get_type()))

        # 校验，原棋子与目标棋子的类型，如果相同，则不能走棋
        if src_qi_zi.get_type() == dst_qi_zi.get_type():
            raise Exception('不能吃自己的棋子')

        # 校验，车，如果，到目标有障碍物，则不能走棋
        self.check_che(self, src_qi_zi, dst_qi_zi, src_zuobiao, dst_zuobiao)

        # TODO

        # 校验成功后，最终走棋结果
        self._qi_pan[dst_zuobiao.x][dst_zuobiao.y] = self._qi_pan[src_zuobiao.x][src_zuobiao.y]

        # 将下一个走棋者设置为当前走棋者的敌方
        self._is_hong_hei_play = dst_qi_zi.get_type()

    def check_che(self, src_qi_zi, dst_qi_zi, src_zuobiao, dst_zuobiao):
        # 校验，车，如果，到目标有障碍物，则不能走棋
        if src_qi_zi.get_value() in [QiZi.HEI_QI, QiZi.HONG_QI]:
            # 横向校验:
            # 如果，原棋子与目标棋子的纵坐标相同，则代表是竖着走，竖着走，则校验[n][y]，n属于[原棋子.x~目标棋子.x]
            # 之间是不是有障碍物
            if src_zuobiao.y == dst_qi_zi.y:
                y = src_zuobiao.y
                if src_zuobiao.x < dst_zuobiao.x:
                    for x in range(src_zuobiao.x + 1, dst_zuobiao.x):
                        if self._qi_pan[x][y] != QiZi.KONG:
                            raise Exception('原车到目标之间不能有障碍物。')
                else:
                    for x in range(dst_zuobiao.x + 1, src_zuobiao.x):
                        if self._qi_pan[x][y] != QiZi.KONG:
                            raise Exception('原车到目标之间不能有障碍物。')
            # 纵向校验
            # 如果，原棋子与目标棋子横坐标相同，则代表是横着走，横着走，则校验[x][n]，n属于[原棋子.y~目标棋子.y]
            # 之间是不是有障碍物
            if src_zuobiao.x == dst_qi_zi.x:
                x = src_zuobiao.x
                if src_zuobiao.y < dst_zuobiao.y:
                    for y in range(src_zuobiao.y + 1, dst_zuobiao.y):
                        if self._qi_pan[x][y] != QiZi.KONG:
                            raise Exception('原车到目标之间不能有障碍物。')
                else:
                    for y in range(dst_zuobiao.y + 1, src_zuobiao.y):
                        if self._qi_pan[x][y] != QiZi.KONG:
                            raise Exception('原车到目标之间不能有障碍物。')


if __name__ == '__main__':
    xq = XiangQi()
    qi_pan_print_str = xq.get_qi_pan_print_str()
    print(qi_pan_print_str)
    print(xq.get_is_hong_hei_play(), '先走')