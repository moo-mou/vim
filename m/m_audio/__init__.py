from m_base import Base

from m_audio.data import AudioData
from m_audio.feature import AudioFeature
from m_audio.mixer import AudioMixer


class Audio(Base):
    data = AudioData()
    mixer = AudioMixer()
    feature = AudioFeature()
