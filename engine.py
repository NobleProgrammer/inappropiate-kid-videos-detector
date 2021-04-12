import numpy as np
import detection
import framework as fmw
import cv2
import math
import os
import audioDetection
import client


def main(video_name, option):  # please check the last line of code to change video name and option.
    cwd = os.path.abspath(os.getcwd())
    file = makeReportFile(video_name, cwd)  # return file report file :)
    file.write("Sensitivity/Tolerance set to: " + str(fmw.TOLERANCE) + "\n")

    if option == 1:
        print(f"## OPTION = {option}")
        file.write("Selected option: Detect Visual Ideologies Only.\n")
        model_names = ['xmas', 'star', 'pyramid', 'buddha', 'jack', 'mason', 'cross']
        makeOutFolders(cwd, model_names)
        detect(cwd, model_names, video_name, file)
    elif option == 2:
        print(f"## OPTION = {option}")
        file.write("Selected option: Detect Visual Violence Only.\n")
        model_names = ['knife', 'pistol', 'scissor', 'hammer']
        makeOutFolders(cwd, model_names)
        detect(cwd, model_names, video_name, file)
    elif option == 3:
        print(f"## OPTION = {option}")
        file.write("Selected option: Detect Auditory Violence Only.\n")
        detectAudio(cwd, video_name, file)
    elif option == 4:
        print(f"## OPTION = {option}")
        file.write("Selected option: Detect All.\n")
        model_names = ['xmas', 'knife', 'pistol', 'scissor', 'star', 'pyramid', 'buddha', 'hammer', 'jack', 'mason', 'cross']
        makeOutFolders(cwd, model_names)
        detect(cwd, model_names, video_name, file)
        # detectAudio(cwd, video_name, file)
    else:
        client.run()
    file.close()


def makeOutFolders(path, model_names):
    if "Output" not in os.listdir(path):
        os.mkdir("Output")

    for model in model_names:
        if "out_{}".format(model) not in os.listdir("{}\\Output".format(path)):
            os.mkdir("Output\\out_{}".format(model))


def makeReportFile(video_name, path):
    fname = video_name[:len(video_name) - 4]
    print(fname)
    f = None

    if "{}.txt".format(fname) in os.listdir(".\\Output"):
        print(f"video {fname} ALREADY ANALYZIED. \nplease delete report file if you want to reanalyise.")
    else:
        f = open(path + "\\Output\\" + fname + "_Report.txt", "w+")
    return f


def detect(path, model_names, video_name, file):
    cap = cv2.VideoCapture(path + "\\Input\\" + video_name)

    if not cap.isOpened():
        print("Error Opening video. System quit.")
        quit()
    width, height = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FRAME_SIZE = cap.get(cv2.CAP_PROP_FRAME_WIDTH) * cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    scene_counter = 0
    totalFrames = 0
    sceneDuration = 1 * cap.get(cv2.CAP_PROP_FPS)
    print("FPS: ", cap.get(cv2.CAP_PROP_FPS))

    while cap.isOpened():
        ret, frame = cap.read()  # this method return true/false for ret var. and the frame itself in frame var. if ret is true.
        if ret:
            size_matrix = np.zeros((int(height), int(width)))
            fmw.frames_list.append(0)
            for model_name in model_names:
                print("Processing: " + model_name + ", Current Frame: " + str(totalFrames + 1))
                boxes = detection.detectObject(frame, model_name, totalFrames)
                if len(boxes) > 0:
                    print(model_name + " Detected at second %.2f, at frame: %d" % (
                        ((totalFrames + 1) / cap.get(cv2.CAP_PROP_FPS)), (totalFrames + 1)))
                    file.write(model_name + " Detected at second %.2f, at frame: %d\n" % (
                        ((totalFrames + 1) / cap.get(cv2.CAP_PROP_FPS)), (totalFrames + 1)))
                    fmw.incAppearance(model_name)
                    fmw.frames_list[totalFrames] += 1
                    fmw.incSize(model_name, boxes, FRAME_SIZE, size_matrix)
                    size_matrix = np.zeros((int(height), int(width)))
                    fmw.addTotalObjs(model_name, len(boxes))
                    if fmw.getRecFlag(model_name):
                        fmw.incRecurrence(model_name)
                        fmw.scenes_list[scene_counter] += 1
                        print("Incremented Recurrence")
                        fmw.changeRecFlag(model_name)
            if (totalFrames + 1) % sceneDuration == 0:
                fmw.resetRecFlag()
                fmw.scenes_list.append(0)
                scene_counter += 1
                print("Recurrence list is reset.")
            totalFrames += 1
        else:
            break
    cap.release()

    writePrintReport(file, totalFrames, sceneDuration, model_names)


def detectAudio(path, video_name, file):
    audioDetection.analyizeAudio(video_name, file)


def writePrintReport(file, totalFrames, sceneDuration, model_names):
    print("\nTotal Frames: ", totalFrames)
    file.write("\nTotal Frames: " + str(totalFrames) + "\n")
    totalScenes = math.ceil(totalFrames / sceneDuration)
    print("====================" + "Video Analysis" + "====================\n")
    file.write("====================" + "Video Analysis" + "====================\n\n")
    for model_name in model_names:
        print("====================" + model_name + "====================")
        print("Total Number of detected objects = ", fmw.getTotalObjs(model_name))
        print("Total Appearance Duration = %.2f%s" % (fmw.calculateAD(model_name, totalFrames) * 100, "%"))
        print("Total Recurrence = %.2f%s" % (fmw.calculateRecurrence(model_name, totalScenes) * 100, "%"))
        print("Total Average Size = %.2f%s" % (fmw.calculateAvgSize(model_name) * 100, "%"))
        print("Alarm Percentage = %.2f%s" % (fmw.calculateAlarm(model_name, totalFrames, totalScenes) * 100, "%"))
        # File write
        file.write("====================" + model_name + "====================\n")
        file.write("Total Number of detected objects = " + str(fmw.getTotalObjs(model_name)))
        file.write("\nTotal Appearance Duration = %.2f%s\n" % (fmw.calculateAD(model_name, totalFrames) * 100, "%"))
        file.write("Total Recurrence = %.2f%s\n" % (fmw.calculateRecurrence(model_name, totalScenes) * 100, "%"))
        file.write("Total Average Size = %.2f%s\n" % (fmw.calculateAvgSize(model_name) * 100, "%"))
        local_ap = fmw.calculateAlarm(model_name, totalFrames, totalScenes) * 100
        file.write("Alarm Percentage = %.2f%s\n" % (local_ap, "%"))
        print("Alarm Degree = ", end="")  # default is n = "\n", and i dont want new line here.
        file.write("Alarm Degree = ")  # default is n = "\n", and i dont want new line here.
        print_alarm_degree(local_ap, file)

    print("\n====================" + "Classes Analysis" + "====================")
    print("Total Detected Classes = ", fmw.getTotalDetectedClasses())
    print("Global Appearance Duration = %.2f%s" % (fmw.getClassAD() * 100, "%"))
    print("Global Recurrence = %.2f%s" % (fmw.getClassRec(totalScenes) * 100, "%"))
    print("Global Average Size = %.2f%s" % (fmw.getClassSize(model_names) * 100, "%"))
    print("Global Alarm Percentage = %.2f%s" % (fmw.calculateAPAllClasses(model_names, totalScenes) * 100, "%"))
    file.write("\n====================" + "Classes Analysis" + "====================\n")
    file.write("Total Detected Classes = " + str(fmw.getTotalDetectedClasses()) + "\n")
    file.write("Global Appearance Duration = %.2f%s" % (fmw.getClassAD() * 100, "%"))
    file.write("\nGlobal Recurrence = %.2f%s" % (fmw.getClassRec(totalScenes) * 100, "%"))
    file.write("\nGlobal Average Size = %.2f%s" % (fmw.getClassSize(model_names) * 100, "%"))
    global_AP = fmw.calculateAPAllClasses(model_names, totalScenes) * 100
    file.write("\nGlobal Alarm Percentage = %.2f%s \n" % (global_AP, "%"))
    print("Alarm Degree = ", end="")  # default is n = "\n", and i dont want new line here.
    file.write("Alarm Degree = ")  # default is n = "\n", and i dont want new line here.
    print_alarm_degree(global_AP, file)


def print_alarm_degree(AP, file):
    if AP >= 80:
        print("{:.2f}% (Very High Alarm)".format(AP))
        file.write("{:.2f}% (Very High Alarm)\n".format(AP))
    elif AP >= 60:
        print("{:.2f}% (High Alarm)".format(AP))
        file.write("{:.2f}% (High Alarm)\n".format(AP))
    elif AP >= 40:
        print("{:.2f}% (Medium Alarm)".format(AP))
        file.write("{:.2f}% (Medium Alarm)\n".format(AP))
    elif AP >= 20:
        print("{:.2f}% (Low Alarm)".format(AP))
        file.write("{:.2f}% (Low Alarm)\n".format(AP))
    else:
        print("{:.2f}% (Very low Alarm)".format(AP))
        file.write("{:.2f}% (Very Low Alarm)\n".format(AP))


if __name__ == "__main__":
    main("The Best Of Bill Cipher_1Sec_Trim.mp4", 1)
