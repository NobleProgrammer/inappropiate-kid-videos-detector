from pyAudioAnalysis.audioSegmentation import mid_term_file_classification, labels_to_segments
from pyAudioAnalysis.audioTrainTest import load_model
import os
import moviepy.editor as mp
from pyAudioAnalysis.audioSegmentation import mid_term_file_classification, labels_to_segments
from pyAudioAnalysis.audioTrainTest import load_model
from pyAudioAnalysis import audioBasicIO as aIO
import os
import moviepy.editor as mp
from pydub import AudioSegment


def convertToAudio(video_name):
    cwd = os.path.abspath(os.path.abspath(os.getcwd()))
    cap = mp.VideoFileClip(r"" + cwd + "\\Input\\" + video_name)
    audio_name = video_name[:len(video_name) - 4] + ".wav"
    cap.audio.write_audiofile(r"" + cwd + "\\Input\\" + audio_name)
    fs, s = aIO.read_audio_file(cwd + "\\Input\\" + audio_name)

    print(f"Duarion = {len(s) / float(fs)}")
    if len(s) / float(fs) <= 1:  # make audio file at least avoce one second long.
        pad_ms = 1000  # milliseconds of silence needed
        silence = AudioSegment.silent(duration=pad_ms)
        audio = AudioSegment.from_wav(cwd + "\\Input\\" + audio_name)
        padded = audio + silence  # Adding silence after the audio
        padded.export(cwd + "\\Input\\" + audio_name, format='wav')

    return video_name.replace("mp4", "wav")


def detectAudio(audio, model_name, file):
    cwd = os.path.abspath(os.getcwd())
    model = ""
    if (model_name == "screams"):
        model = "svm_screams_nonscream"
    else:
        model = "svm_explosion_nonexplosion"

    # divding audio file into segment, and pass the trained model.
    labels, class_names, _, _ = mid_term_file_classification(cwd + "\\Input\\" + audio,
                                                             cwd + "\\models\\{}".format(model), "svm_rbf", True)
    print("\nFix-sized segments:")
    for il, l in enumerate(labels):
        print(f'fix-sized segment {il}: {class_names[int(l)]}')

    # load mt_step of the model
    _, _, _, _, _, mt_step, _, _, _ = load_model(cwd + "\\models\\{}".format(model))

    # print "merged" segments (use labels_to_segments())
    flag = False
    print("\nSegments:")
    segs, c = labels_to_segments(labels, mt_step)
    for iS, seg in enumerate(segs):
        print(f'segment {iS} {seg[0]} sec - {seg[1]} sec: {class_names[int(c[iS])]}')
        if (class_names[int(c[iS])] == model_name):
            flag = True
            print('from {} sec - {} sec. \n'.format(int(seg[0]), int(seg[1])))
            file.write('from {} sec - {} sec. \n'.format(int(seg[0]), int(seg[1])))
    return flag


def analyizeAudio(video_name, file):
    audio = convertToAudio(video_name)

    print("\n====================" + "Audio Analysis" + "====================\n")
    file.write("\n====================" + "Audio Analysis" + "====================\n")

    print("\n===============" + "Scream detection" + "===============\n")
    file.write("\n===============" + "Scream detection" + "===============\n")
    if (not detectAudio(audio, "screams", file)):
        print("No screams detected in this video.")
        file.write("No screams detected in this video.")

    print("\n===============" + "Explosion detection" + "===============\n")
    file.write("\n===============" + "Explosion detection" + "===============\n")
    if (not detectAudio(audio, "explosion", file)):
        print("No explosions detected in this video.")
        file.write("No explosions detected in this video.")
