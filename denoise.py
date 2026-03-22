import noisereduce as nr
import soundfile as sf


def process_audio_array(data, sr, prop_decrease=0.8, **kwargs):
    return nr.reduce_noise(y=data, sr=sr, prop_decrease=prop_decrease, **kwargs)


def process_audio(input_path, output_path, prop_decrease=0.8, **kwargs):
    data, sr = sf.read(input_path)
    reduced_noise = process_audio_array(data, sr, prop_decrease, **kwargs)
    sf.write(output_path, reduced_noise, sr)
    return output_path
