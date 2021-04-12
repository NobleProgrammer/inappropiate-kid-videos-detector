# Inappropiate-Kid-Videos-Detector
 
**Project Objectives**: 
The objective of this project is to resolve the presence of inappropriate content in cartoons and in real-life videos. This is done by designing a program that serves as a filter by implementing image processing and artificial intelligence techniques and tools. The program will scan the video and determine violence (audio and imagery) or ideological symbols in video frames based on our trained dataset. The program then categorizes the video after analyzing it. Based on the categorization, the system will predict whether the video is alarming or not.

**Folder Structure**:
1.	Input: here ever video(s) that want to be detected should reside, and when running the program, you should pass the video name with its extension (for example: tom_and_jerry_episode01.mp4).
2.	Output: this is the location of the generated report, also all detected images with the bounding boxes will reside in this folder.
3.	Models: This folder contains all trained models (image and audio models). Note that every image detection model should have this suffix “yolov3_training_final.weights”, and the prefix should be the name of the model, for example “hammer_yolov3_training_final.weights”. It also contains “yolov3_testing.cfg”. For audio, every model come along with two additional files, they are: .arff and MEANS. This all should exists also, for example “svm_screams_nonscream” is the file of the trained model, “svm_screams_nonscream.arff” and “svm_screams_nonscreamMEANS” should come along with it. Note that the classifier should be a SVM, otherwise modifications on source code is needed.
4.	All .py files must reside in the root folder.
5.	Note that metrics.py is optional and is not needed for a program to run.

**Needed libraries and dependencies**:
1.	numpy.
2.	OpenCV.
3.	PyAudioAnalysis (https://github.com/tyiannak/pyAudioAnalysis).
4.	Moviepy (https://pypi.org/project/moviepy/).
5.	seaborn, pandas, matplotlib (all are optional, and they are used in metrics.py).

**How to run the program**:
The main gateway of the program is client.py, and you can either run it in a normal manner and the interface will ask you to enter video name, decide an option, and decide tolerance value. Or directly from command line you can send video name (with its extension), option, and tolerance as parameters. If only video name and option is provided, tolerance is set to 1 as default, if only video name is provided, option 4 (detect ideologies and violence) is set as default.

**Training model Analysis**: 
The following figure shows Accuracy, Precision, Recall, and F-1 Score for our visual models:
https://imgur.com/utUzkYU

The following figure shows Accuracy, Precision, Recall, and F-1 Score for our auditory models:
https://imgur.com/HiGoUub

The following figure shows the ROC curve and AUC for auditory models:
https://imgur.com/undefined
