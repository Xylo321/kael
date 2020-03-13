# import cv2
import ffmpeg
import filetype
import logging
import traceback


def get_num_image(file_name, num=1):
    """获取视频的第n帧图片

    """
    vidcap = cv2.VideoCapture(file_name)
    success, image = vidcap.read()
    n = 1
    while n < num:
        success, image = vidcap.read()
        n += 1
    # imag = cv2.imwrite('fdfd2.jpg', image)
    # if imag == True:
    #     print('ok')


def get_video_type(src):
    """获取视频文件的类型。src为视频文件名，返回类型字符串。

    """
    result = filetype.guess(src)
    if result:
        return result.extension
    return None


def convert_flv(src, dst):
    """将源视屏转换程flv格式。src为源视屏文件磁盘路径，dst为转换后的输出路径
    转换成功返回True，失败返回False。

    """
    src_type = get_video_type(src)

    if src_type:
        try:
            input_stream = ffmpeg.input(src, format=src_type)
            output_stream = ffmpeg.output(input_stream, dst, format='flv')
            ffmpeg.run(output_stream)
            return True
        except:
            logging.error(traceback.format_exc())

    return False