import cv2
import ffmpeg
import filetype
import logging
import traceback
import os
from PIL import Image
from io import BytesIO



def get_video_num_image(file_name, num=1):
    """获取视频的第n帧图片

    :param file_name: 视屏文件名
    :type file_name: str
    :param num: 获取第几帧的视屏图片
    :type num: int

    """
    try:
        vidcap = cv2.VideoCapture(file_name)
        success, img_cv2 = vidcap.read()
        n = 1
        while n < num:
            success, img_cv2 = vidcap.read()
            n += 1

        img = Image.fromarray(img_cv2)
        # img.save('/root/test.png')

        bts = BytesIO()
        img.save(bts, format='png')

        return BytesIO(bts.getvalue())
    except:
        logging.error(traceback.format_exc())
        return None
    finally:
        if vidcap: vidcap.release()
        if bts: bts.close()


def get_video_type(src):
    """获取视频文件的类型。src为视频文件名，返回类型字符串。

    """
    result = filetype.guess(src)
    if result:
        return result.extension
    return None


def get_video_infor(src_file) -> dict or None:
    """获取视频文件的信息；

    :param src_file: 视屏文件路径；
    :type src_file: str

    :return: 视屏文件的字典；
    :rtype: dict or None

    如果获取信息时出错，则返回None，反之返回该视屏的信息字典，详情请下面
    的数据结构；

    Examples:

        {
        "streams": [
            {
                "index": 0,
                "codec_name": "aac",
                "codec_long_name": "AAC (Advanced Audio Coding)",
                "profile": "LC",
                "codec_type": "audio",
                "codec_time_base": "1/88200",
                "codec_tag_string": "mp4a",
                "codec_tag": "0x6134706d",
                "sample_fmt": "fltp",
                "sample_rate": "88200",
                "channels": 2,
                "channel_layout": "stereo",
                "bits_per_sample": 0,
                "r_frame_rate": "0/0",
                "avg_frame_rate": "0/0",
                "time_base": "1/44100",
                "start_pts": 0,
                "start_time": "0.000000",
                "duration_ts": 847870,
                "duration": "19.226077",
                "bit_rate": "127757",
                "max_bit_rate": "134624",
                "nb_frames": "828",
                "disposition": {
                    "default": 1,
                    "dub": 0,
                    "original": 0,
                    "comment": 0,
                    "lyrics": 0,
                    "karaoke": 0,
                    "forced": 0,
                    "hearing_impaired": 0,
                    "visual_impaired": 0,
                    "clean_effects": 0,
                    "attached_pic": 0,
                    "timed_thumbnails": 0
                },
                "tags": {
                    "creation_time": "2019-09-27T18:09:52.000000Z",
                    "language": "und",
                    "handler_name": "GPAC ISO Audio Handler"
                }
            },
            {
                "index": 1,
                "codec_name": "h264",
                "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
                "profile": "Main",
                "codec_type": "video",
                "codec_time_base": "481/23100",
                "codec_tag_string": "avc1",
                "codec_tag": "0x31637661",
                "width": 1280,
                "height": 720,
                "coded_width": 1280,
                "coded_height": 720,
                "has_b_frames": 0,
                "sample_aspect_ratio": "1:1",
                "display_aspect_ratio": "16:9",
                "pix_fmt": "yuv420p",
                "level": 51,
                "chroma_location": "left",
                "refs": 1,
                "is_avc": "true",
                "nal_length_size": "4",
                "r_frame_rate": "25/1",
                "avg_frame_rate": "11550/481",
                "time_base": "1/30000",
                "start_pts": 0,
                "start_time": "0.000000",
                "duration_ts": 577200,
                "duration": "19.240000",
                "bit_rate": "3104881",
                "bits_per_raw_sample": "8",
                "nb_frames": "462",
                "disposition": {
                    "default": 1,
                    "dub": 0,
                    "original": 0,
                    "comment": 0,
                    "lyrics": 0,
                    "karaoke": 0,
                    "forced": 0,
                    "hearing_impaired": 0,
                    "visual_impaired": 0,
                    "clean_effects": 0,
                    "attached_pic": 0,
                    "timed_thumbnails": 0
                },
                "tags": {
                    "creation_time": "2019-09-27T18:09:52.000000Z",
                    "language": "und",
                    "handler_name": "GPAC ISO Video Handler"
                }
            }
        ],
        "format": {
            "filename": "./test.mp4",
            "nb_streams": 2,
            "nb_programs": 0,
            "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
            "format_long_name": "QuickTime / MOV",
            "start_time": "0.000000",
            "duration": "19.202856",
            "size": "7789837",
            "bit_rate": "3245282",
            "probe_score": 100,
            "tags": {
                "major_brand": "mp42",
                "minor_version": "0",
                "compatible_brands": "mp42isom",
                "creation_time": "2019-09-27T18:09:52.000000Z"
            }
        }
    }

    """
    try:
        return ffmpeg.probe(src_file)
    except:
        logging.error(traceback.format_exc())
    return None


def parse_width_height(vi):
    """解析出视屏的宽和高

    :param vi: 视屏信息字典
    :type vi: dict

    :return: 视屏的宽和高
    :rtype: tuple
    """
    width = height = 0
    streams = vi['streams']
    for stream in streams:
        try:
            width = stream['width']
            height = stream['height']
            break
        except:
            logging.error(traceback.format_exc())

    if width == 0 or height == 0:
        return None

    return width, height


def convert_mp4(src, dst):
    """将源视屏转换程mp4格式。src为源视屏文件磁盘路径，dst为转换后的输出路径
    转换成功返回True，失败返回False。

    之前转换为flv，导致flv.min.js报错，但是用迅雷影音是可以打开的，flv.js解码
    错误，客户端直接卡成翔。

    """
    src_type = get_video_type(src)

    if src_type:
        try:
            if os.path.exists(dst):
                os.remove(dst)

            input_stream = ffmpeg.input(src, format=src_type)
            output_stream = ffmpeg.output(input_stream, dst, format='mp4')

            ffmpeg.run(output_stream)
            return True
        except:
            logging.error(traceback.format_exc())

    return False