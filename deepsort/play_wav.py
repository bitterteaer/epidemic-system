from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_wav("程序已经启动.wav")
play(song)
