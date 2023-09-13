from pydub import AudioSegment


# 这里filepath填的是.mp3文件的名字（也可加上路径）
def trans_mp3_to_wav(filepath):
    song = AudioSegment.from_mp3(filepath)
    song.export("请佩戴口罩.wav", format="wav")


trans_mp3_to_wav('请佩戴口罩.mp3')
