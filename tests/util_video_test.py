from reborn.utils import video

src_file = "test.mp4"
tp = video.get_video_type(src_file)
print(tp)

resu = video.convert_flv(src_file, src_file + ".flv")

print(resu)