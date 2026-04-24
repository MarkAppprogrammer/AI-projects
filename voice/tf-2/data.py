import os
import tensorflow as tf

#loading and spliting
DATASET_PATH = "/Users/mark/ai-projects/voice/speech_commands_v0.02"

def load_list(filename):
    with open(os.path.join(DATASET_PATH, filename), "r") as f:
        return set(line.strip() for line in f)

val_set = load_list("validation_list.txt")
test_set = load_list("testing_list.txt")

def get_label(file_path):
    return os.path.basename(os.path.dirname(file_path))

all_wavs = []

for root, _, files in os.walk(DATASET_PATH):
    for f in files:
        if f.endswith(".wav"):
            rel_path = os.path.relpath(os.path.join(root, f), DATASET_PATH)
            # Skip special folders like `_background_noise_` which are not labels.
            # These otherwise produce label_id == -1 via the lookup table default.
            first_dir = rel_path.split(os.sep, 1)[0]
            if first_dir.startswith("_"):
                continue
            all_wavs.append(rel_path)

train_files = []
val_files = []
test_files = []

for f in all_wavs:
    if f in val_set:
        val_files.append(f)
    elif f in test_set:
        test_files.append(f)
    else:
        train_files.append(f)

#mel spec tf
SAMPLE_RATE = 16000
FRAME_LENGTH = 480   # 30ms window
FRAME_STEP = 160     # 10ms frame shift
NUM_MEL_BINS = 40

def wav_to_mel_spectrogram(waveform):
    # 1. STFT
    stft = tf.signal.stft(
        waveform,
        frame_length=FRAME_LENGTH,
        frame_step=FRAME_STEP,
        fft_length=512
    )

    spectrogram = tf.abs(stft)

    num_spectrogram_bins = stft.shape[-1]

    mel_matrix = tf.signal.linear_to_mel_weight_matrix(
        num_mel_bins=NUM_MEL_BINS,
        num_spectrogram_bins=num_spectrogram_bins,
        sample_rate=SAMPLE_RATE,
        lower_edge_hertz=20.0,
        upper_edge_hertz=8000.0
    )

    mel_spectrogram = tf.matmul(spectrogram, mel_matrix)

    log_mel_spectrogram = tf.math.log(mel_spectrogram + 1e-6)

    return log_mel_spectrogram

max_shift = int(0.1 * 16000)

def time_shift(wav):
    shift = tf.random.uniform([], -max_shift, max_shift, dtype=tf.int32)

    return tf.roll(wav, shift=shift, axis=0)

noise_file_list = ["/Users/mark/ai-projects/voice/speech_commands_v0.02/_background_noise_/doing_the_dishes.wav", "/Users/mark/ai-projects/voice/speech_commands_v0.02/_background_noise_/dude_miaowing.wav", "/Users/mark/ai-projects/voice/speech_commands_v0.02/_background_noise_/exercise_bike.wav", "/Users/mark/ai-projects/voice/speech_commands_v0.02/_background_noise_/pink_noise.wav", "/Users/mark/ai-projects/voice/speech_commands_v0.02/_background_noise_/running_tap.wav", "/Users/mark/ai-projects/voice/speech_commands_v0.02/_background_noise_/white_noise.wav"]

noise_files = tf.constant(noise_file_list)

def add_noise(wav):
    prob = tf.random.uniform([])

    def apply_noise():
        noise_path = tf.random.shuffle(noise_files)[0]
        noise_audio = tf.io.read_file(noise_path)
        noise_audio, _ = tf.audio.decode_wav(noise_audio)

        noise_audio = tf.squeeze(noise_audio, axis=-1)
        wav_len = tf.shape(wav)[0]
        noise_len = tf.shape(noise_audio)[0]

        # Ensure noise matches wav length (pad/tile then slice).
        # Some background noise files can be shorter than a training clip.
        repeats = tf.maximum(1, tf.cast(tf.math.ceil(tf.cast(wav_len, tf.float32) / tf.cast(noise_len, tf.float32)), tf.int32))
        noise_audio = tf.tile(noise_audio, [repeats])
        noise_audio = noise_audio[:wav_len]

        return wav + 0.1 * noise_audio

    return tf.cond(prob < 0.8, apply_noise, lambda: wav)

#preprocessing
def decode_audio(filename):
    full_path = tf.strings.join([DATASET_PATH, filename], separator="/")
    audio_binary = tf.io.read_file(full_path)
    audio, _ = tf.audio.decode_wav(audio_binary)
    return tf.squeeze(audio, axis=-1)

labels = sorted(
    d
    for d in os.listdir(DATASET_PATH)
    if os.path.isdir(os.path.join(DATASET_PATH, d)) and not d.startswith("_")
)
label_to_index = tf.lookup.StaticHashTable(
    tf.lookup.KeyValueTensorInitializer(
        keys=tf.constant(labels),
        values=tf.constant(list(range(len(labels))))
    ),
    default_value=-1
)

def get_label_id(filename):
    parts = tf.strings.split(filename, "/")
    label = parts[-2]
    return label_to_index.lookup(label)

def preprocess(file):
    audio = decode_audio(file)

    audio = time_shift(audio)
    audio = add_noise(audio)

    audio = audio[:16000]
    audio = tf.pad(audio, [[0, 16000 - tf.shape(audio)[0]]])

    mel = wav_to_mel_spectrogram(audio)

    label = get_label_id(file)
    return mel, label

def tf_preprocess(f):
    mel, label = tf.py_function(preprocess, [f], [tf.float32, tf.int32])

    mel.set_shape([98, NUM_MEL_BINS])
    label.set_shape([])

    mel = tf.transpose(mel, [1, 0])

    # NHWC (freq, time, channels) for CPU compatibility
    mel = tf.expand_dims(mel, axis=-1)

    return mel, label

def make_dataset(files, batch_size=32, shuffle=True):
    ds = tf.data.Dataset.from_tensor_slices(files)

    if shuffle:
        ds = ds.shuffle(buffer_size=len(files))

    ds = ds.map(tf_preprocess, num_parallel_calls=tf.data.AUTOTUNE)

    ds = ds.batch(batch_size)  # no padding needed

    ds = ds.prefetch(tf.data.AUTOTUNE)

    return ds

# def make_dataset(files, batch_size=32, shuffle=True):
#     ds = tf.data.Dataset.from_tensor_slices(files)

#     if shuffle:
#         ds = ds.shuffle(buffer_size=len(files))

#     ds = ds.map(
#         lambda f: tf.py_function(preprocess, [f], [tf.float32, tf.int32]),
#         num_parallel_calls=tf.data.AUTOTUNE
#     )

#     # ds = ds.padded_batch(batch_size, padded_shapes=([None], []))
#     ds = ds.padded_batch(batch_size, padded_shapes=([None, None], []))

#     ds = ds.prefetch(tf.data.AUTOTUNE)

#     return ds


train_ds = make_dataset(train_files, batch_size=100, shuffle=True)
val_ds   = make_dataset(val_files, batch_size=100, shuffle=False)
test_ds  = make_dataset(test_files, batch_size=100, shuffle=False)