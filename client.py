import os
import sys
import engine
import framework


def getOption():
    while (True):
        interface()
        option = input("Please Enter option's key to execute that option: ")
        if (option == str(1)):
            return 1
        elif (option == str(2)):
            return 2
        elif (option == str(3)):
            return 3
        elif (option == str(4)):
            return 4
        elif (option == str(5)):
            print("Thank you.. Have a good day!")
            quit()
        else:
            print("Incorrect input, please Enter 1, 2, 3 or 4.")


def getVideoName(cwd):
    while (True):
        video_name = input("Please Enter Video Name with its extension (for example: .mp4, .mkv): ")
        if video_name in os.listdir(cwd + "\\input"):
            return video_name
        else:
            print("Video does not exists, please check video name.")


def interface():
    print("[1] - Detect Visual Ideologies Only.")
    print("[2] - Detect Visual Violence Only.")
    print("[3] - Detect Auditory Violence Only.")
    print("[4] - Detect All.")
    print("[5] - Quit Program.")


def checkVideoName(cwd, video_name):  # used for cmd args only, lots of redundancy i know...
    if video_name in os.listdir(cwd + "\\input"):
        return True
    else:
        return False


def checkOptionKey(option):  # used for cmd args only, lots of redundancy i know...
    if (option == 1 or option == 2 or option == 3 or option == 4):
        return True
    else:
        return False


def checkToleranceValue(tolerance): # for args only,  lots of redundancy i know...
    if tolerance <= 0 or tolerance > 1:
        return False
    else:
        return True


def setTolerance():
    while True:
        tolerance = input("Please set tolerance/sensitivity value greater than 0 and less than or equal 1: ")
        tolerance = float(tolerance)
        # print(f"value = {tolerance}")
        if tolerance <= 0.0 or tolerance > 1.0:
            print("Please Enter a value greater than 0 and less than or equal 1")
        else:
            framework.setTolerance(tolerance)
            break


def run():
    cwd = os.path.abspath(os.getcwd())
    #cwd = "C:\\Users\\Yatagarasu\\Desktop\\kids_detection"
    #os.chdir(cwd)

    video_name = ""
    option = -1
    tolerance = -1.0
    if len(sys.argv) == 4:
        video_name = sys.argv[1]
        option = int(sys.argv[2])
        tolerance = float(sys.argv[3])
    elif len(sys.argv) == 3:
        video_name = int(sys.argv[1])
        option = int(sys.argv[2])
        framework.setTolerance(1.0)
    elif len(sys.argv) == 2:
        video_name = int(sys.argv[1])
        option = 4
        framework.setTolerance(1.0)

    if checkVideoName(cwd, video_name) and checkOptionKey(option) and checkToleranceValue(tolerance):
        framework.setTolerance(tolerance)
        engine.main(video_name, option)
        quit()
    elif len(sys.argv) > 1:
        print("ERROR: One or more values passed has error, you will be directed to use the interface.")

    print("Welcome to the Detector of Inappropriate Video Content For Kids")
    while(True):
        framework.reset_data()
        video_name = getVideoName(cwd)
        option = getOption()
        setTolerance()
        engine.main(video_name,option)
        print("\nReport file is generated with detected images can be found in Output folder.")
        option = input("Enter c to Analysis Another video, or Enter any character to exit: ")
        if option != "c":
            break

    print("Thank for using our program. Have a good day!")


if __name__ == "__main__":
    run()
