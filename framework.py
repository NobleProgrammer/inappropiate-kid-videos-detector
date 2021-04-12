# باسم الله، نتوكّل عليه.
import numpy as np

# Classes code:
# CROSS, XMAS, JACK, STAR, BUDDAH, PYRAMID, MASON, KNIFE, SCISSOR, HAMMER, PISTOL
# 0 - 10, respectively
weights = (1, 0.6, 0.5, 1, 0.8, 1, 1, 0.3, 0.2, 0.4, 1)  # tuple, cuz immutable.
TOLERANCE = 1
# factors of each class(Recurrence, Apperance duration, and object size respectively)
cross_list = [0, 0, 0]
xmas_list = [0, 0, 0]
jack_list = [0, 0, 0]
star_list = [0, 0, 0]
buddah_list = [0, 0, 0]
pyramid_list = [0, 0, 0]
mason_list = [0, 0, 0]
knife_list = [0, 0, 0]
scissor_list = [0, 0, 0]
hammer_list = [0, 0, 0]
pistol_list = [0, 0, 0]
recFlag = [True, True, True, True, True, True, True, True, True, True, True]
totalAP = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
totalObjects = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
scenes_list = [0]
frames_list = []


def getClass(className):  # return class' list and its cod.
    if className == 'cross':
        return cross_list, 0
    elif className == 'xmas':
        return xmas_list, 1
    elif className == 'jack':
        return jack_list, 2
    elif className == 'star':
        return star_list, 3
    elif className == 'buddha':
        return buddah_list, 4
    elif className == 'pyramid':
        return pyramid_list, 5
    elif className == 'mason':
        return mason_list, 6
    elif className == 'knife':
        return knife_list, 7
    elif className == 'scissor':
        return scissor_list, 8
    elif className == 'hammer':
        return hammer_list, 9
    else:
        return pistol_list, 10


def getClassAD():
    sum = 0
    for e in frames_list:
        if e > 0:
            sum += 1
    return sum / len(frames_list)


def getClassRec(total_scenes):
    sum = 0
    for e in scenes_list:
        if e > 0:
            sum += 1
    # print("Sum: ", sum)
    # print("len(scenes_list): ", len(scenes_list))
    return sum / total_scenes


def getClassSize(model_names):
    size_sum = 0
    for model_name in model_names:
        class_list, _ = getClass(model_name)
        size_sum += calculateAvgSize(model_name)
    if getTotalDetectedClasses() == 0:
        return 0
    else:
        size_sum /= getTotalDetectedClasses()
        return size_sum


def getWeightFlag(className):
    _, index = getClass(className)
    return weights[index]


def resetRecFlag():
    for i in range(len(recFlag)):
        recFlag[i] = True
    # print("Rec Flag: ", recFlag)


def changeRecFlag(className):
    _, index = getClass(className)
    recFlag[index] = False


def getRecFlag(className):
    _, index = getClass(className)
    return recFlag[index]


def getTotalObjs(className):
    _, index = getClass(className)
    return totalObjects[index]


def addTotalObjs(className, number):
    _, index = getClass(className)
    totalObjects[index] += number


def incRecurrence(className):
    class_list, _ = getClass(className)
    class_list[0] += 1


def incAppearance(className):
    class_list, _ = getClass(className)
    class_list[1] += 1


def incSize(className, boxes, frameSize, size_matrix):
    for i in range(len(boxes)):
        for j in range(len(boxes[i])):
            if boxes[i][j] < 0:
                boxes[i][j] = 0
    for box in boxes:
        size_matrix[box[1]: box[1] + box[3], box[0]: box[0] + box[2]] = 1
    total_area = np.sum(size_matrix > 0)
    print("Total Area: ", total_area)
    class_list, _ = getClass(className)
    class_list[2] += total_area / frameSize


def calculateRecurrence(className, totalVideoScenes):
    class_list, _ = getClass(className)
    recurrence = class_list[0] / totalVideoScenes
    return recurrence


def calculateAD(className, totalVideoFrames):
    class_list, _ = getClass(className)
    ad = class_list[1] / totalVideoFrames
    return ad


def calculateAvgSize(className):
    class_list, index = getClass(className)
    if class_list[1] == 0:
        return 0
    else:
        return (class_list[2] / class_list[1])


def calculateAlarm(className, totalFrames, totalScenes):
    class_list, code = getClass(className)
    AP = ((((calculateRecurrence(className, totalScenes)) + (calculateAD(className, totalFrames)) + (
        calculateAvgSize(className))) / 3) * (weights[code]) * TOLERANCE)
    totalAP[code] = AP
    return AP


def calculateAPAllClasses(model_names, total_scenes):
    total_ad = getClassAD()
    total_scenes = getClassRec(total_scenes)
    size_sum = getClassSize(model_names)
    return ((total_ad + total_scenes + size_sum) / 3) * getWeightOfGlobalAP() * TOLERANCE


def getTotalDetectedClasses():
    count = 0
    for AP in totalAP:
        if AP != 0:
            count += 1
    return count


def getWeightOfGlobalAP():
    sum = 0
    n = 0
    if cross_list[0] > 0:
        sum += weights[0]
        n += 1
    if xmas_list[0] > 0:
        sum += weights[1]
        n += 1
    if jack_list[0] > 0:
        sum += weights[2]
        n += 1
    if star_list[0] > 0:
        sum += weights[3]
        n += 1
    if buddah_list[0] > 0:
        sum += weights[4]
        n += 1
    if pyramid_list[0] > 0:
        sum += weights[5]
        n += 1
    if mason_list[0] > 0:
        sum += weights[6]
        n += 1
    if knife_list[0] > 0:
        sum += weights[7]
        n += 1
    if scissor_list[0] > 0:
        sum += weights[8]
        n += 1
    if hammer_list[0] > 0:
        sum += weights[9]
        n += 1
    if pistol_list[0] > 0:
        sum += weights[10]
        n += 1
    if n == 0:
        return 0
    else:
        return sum / n


def setTolerance(x):
    global TOLERANCE
    TOLERANCE = x


def reset_data():
    global cross_list
    cross_list = [0, 0, 0]
    global xmas_list
    xmas_list = [0, 0, 0]
    global jack_list
    jack_list = [0, 0, 0]
    global star_list
    star_list = [0, 0, 0]
    global buddah_list
    buddah_list = [0, 0, 0]
    global pyramid_list
    pyramid_list = [0, 0, 0]
    global mason_list
    mason_list = [0, 0, 0]
    global knife_list
    knife_list = [0, 0, 0]
    global scissor_list
    scissor_list = [0, 0, 0]
    global hammer_list
    hammer_list = [0, 0, 0]
    global pistol_list
    pistol_list = [0, 0, 0]
    global  recFlag
    recFlag = [True, True, True, True, True, True, True, True, True, True, True]
    global totalAP
    totalAP = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    global totalObjects
    totalObjects = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    global scenes_list
    scenes_list = [0]
    global frames_list
    frames_list = []
