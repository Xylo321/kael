from reborn.utils import video
from unittest import TestCase, main
import json


class VideoTest(TestCase):
    src_file = "./test.mp4"

    # def test_get_video_info(self):
    #     tp = video.get_video_infor(self.src_file)
    #     print('-----------------')
    #     print(json.dumps(tp))
    #
    # def test_convert_flv(self):
    #     resu = video.convert_flv(self.src_file, self.src_file + ".flv")
    #     print('-----------------')
    #
    #     print(resu)

    def test_get_first_image(self):
        vi = video.get_video_num_image(self.src_file)
        print('-----------------')

        print(vi)


main()