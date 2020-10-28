from unittest import TestCase
from kael.game.xiangqi import XiangQi, QiZi, ZuoBiao

class CheTest(TestCase):
    def test_qizi_not_in_qipan(self):
        xq = XiangQi()
        print(xq.get_qi_pan_print_str())

        if xq.get_is_hong_hei_play() == QiZi.HEI_QI:
            xq.play(ZuoBiao(9, 0), ZuoBiao(6, 0))
            print(xq.get_qi_pan_print_str())
        elif xq.get_is_hong_hei_play() == QiZi.HONG_QI:
            xq.play(ZuoBiao(0, 0), ZuoBiao(3, 0))
            print(xq.get_qi_pan_print_str())

    def test_qizi_zhengque(self):
        xq = XiangQi()
        print(xq.get_qi_pan_print_str())
        if xq.get_is_hong_hei_play() == QiZi.HEI_QI:
            xq.play(ZuoBiao(9, 0), ZuoBiao(8, 0))
            print(xq.get_qi_pan_print_str())
        elif xq.get_is_hong_hei_play() == QiZi.HONG_QI:
            xq.play(ZuoBiao(0, 0), ZuoBiao(1, 0))
            print(xq.get_qi_pan_print_str())
