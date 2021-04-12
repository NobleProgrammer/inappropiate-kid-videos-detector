import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

'''

This function is used for computing ROC and plot it with AUC (can do more than this too, but we used it for ROC only),
but it requires dataset for TP and TN. so you probably cannot use this function.


from pyAudioAnalysis import audioTrainTest as aT 
import sklearn.metrics 
import plotly.graph_objs as go 
def plotROC (): # if code has bugs, try to provide full path for every folder.
    cwd = os.path.abspath(os.getcwd())
    _, _, _, _, _, fpr_scream, tpr_scream = aT.evaluate_model_for_folders([cwd+"\\testing\\screams", cwd+"\\testing\\non_scream"],cwd+"\\models\\svm_screams_nonscream", "svm_rbf","screams")
    
    _, _, _, _, _, fpr_explosion, tpr_explosion = aT.evaluate_model_for_folders([cwd+ "\\testing\\explosion", cwd+"testing\\non_explosion"],cwd+"\\models\\svm_explosion_nonexplosion", "svm_rbf","explosion")
    
    _, _, _, _, _, fpr_violent, tpr_violent = aT.evaluate_model_for_folders([cwd+"\\testing\\violent", cwd+"\\testing\\nonviolent"],cwd+"\\models\\svm_violent_nonviolent", "svm_rbf","violent")

    figs = go.Figure()
    figs.add_trace(go.Scatter(x=fpr_scream, y=tpr_scream, showlegend=True, name = "Screams (AUC = {:.2f})".format(sklearn.metrics.auc(fpr_scream, tpr_scream))))
    figs.add_trace(go.Scatter(x=fpr_explosion, y=tpr_explosion, showlegend=True , name = "Explosions (AUC = {:.2f})".format(sklearn.metrics.auc(fpr_explosion, tpr_explosion))))
    figs.add_trace(go.Scatter(x=fpr_violent, y=tpr_violent, showlegend=True, name = "Violent (AUC = {:.2f})".format(sklearn.metrics.auc(fpr_violent, tpr_violent))))
    figs.update_xaxes(title_text="false positive rate")
    figs.update_yaxes(title_text="true positive rate")
    figs.update_layout(title = 'ROC Curve for screams, explotions, and Violent')
    figs.show()
'''

def plot_figure(cm, name):
    print(cm)
    df_cm = pd.DataFrame(cm, range(2), range(2))
    sn.set(font_scale=1.4)  # for label size
    df_cm.columns = ['Actual Yes', 'Actual No']
    df_cm.index = ['Pred Yes', 'Pred No']
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}, fmt='g')  # font size
    plt.title(name)
    plt.show()


def plot_bar(labels, legend_labels, data):
    x = np.arange(len(labels))  # the label locations
    gap = 0.5
    bw = (1 - gap) / 4
    fig, ax = plt.subplots()
    colors = ["magenta", 'green', "purple", "orange"]

    for i in range(len(data)):
        ax.bar(x + bw * i, data[i], width=bw, color=colors[i])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Percentages')
    ax.legend(legend_labels)
    plt.show()


def print_cal(cm):
    print("Accuracy: %.4f" % calculate_accuracy(cm))
    print("Precision: %.4f" % calculate_precision(cm))
    print("Recall: %.4f" % calculate_recall(cm))
    print("F-1 Score: %.4f" % calculate_f1(cm))


def calculate_f1(cm):
    precision = calculate_precision(cm)
    recall = calculate_recall(cm)
    return (2 * precision * recall) / (precision + recall)


def calculate_recall(cm):
    return (cm[0][0]) / (cm[0][0] + cm[1][0])


def calculate_accuracy(cm):
    sum = 0
    for m in cm:
        sum += m[0] + m[1]
    return (cm[0][0] + cm[1][1]) / sum


def calculate_precision(cm):
    return (cm[0][0]) / (cm[0][0] + cm[0][1])


if __name__ == "__main__":
    total_cm = []
    model_names = ["Cross", "Buddha", "Star", "Pyramid", "Xmas", "Jack", "Mason", "Knife", "Pistol", "Hammer",
                   "Scissor"]
    model_names = ["screams/non_screams","explosion/non_explosion"]#,"violent/non_violent"] for audio
    models_cm = [
        [[9, 4],
         [3, 11]],  # Cross
        [[26, 3],
         [2, 12]],  # Buddha
        [[22, 2],
         [2, 13]],  # Star
        [[33, 0],
         [9, 15]],  # Pyramid
        [[21, 1],
         [10, 14]],  # Xmas
        [[28, 2],
         [3, 13]],  # Jack
        [[12, 0],
         [8, 15]],  # Mason
        [[15, 1],
         [13, 14]],  # Knife
        [[20, 1],
         [3, 14]],  # Pistol
        [[25, 4],
         [5, 11]],  # Hammer
        [[25, 1],
         [5, 14]]  # Scissor
    ]
    models_cm = [ [[14,5],[44,101]], [[6,11],[9,138]]]#, [[25,11],[69,59]]] for audio.
    TP = 0
    TN = 0
    FP = 0
    FN = 0

    for i in range(len(models_cm)):
        TP += models_cm[i][0][0]
        TN += models_cm[i][1][1]
        FP += models_cm[i][0][1]
        FN += models_cm[i][1][0]

    total_cm = [[TP, FP], [FN, TN]]

    # Uncomment this to plot each class separated.
    for i in range(len(models_cm)):
        plot_figure(models_cm[i], model_names[i])
    plot_figure(total_cm, "All models")

    for i in range(len(models_cm)):
        print("===============" + model_names[i] + "===============")
        print_cal(models_cm[i])

    print("===============" + "All Classes" + "===============")
    print_cal(total_cm)

    data = [
        [],  # Accuracy
        [],  # Precision
        [],  # Recall
        []  # F1-Score
    ]
    for cm in models_cm:
        acc = calculate_accuracy(cm)
        precision = calculate_precision(cm)
        recall = calculate_recall(cm)
        f1 = calculate_f1(cm)
        data[0].append(int(acc*100))
        data[1].append(int(precision*100))
        data[2].append(int(recall*100))
        data[3].append(int(f1*100))
        print(f"{cm} acc, pre, rec, f1: \n {data}")
    #plot_bar(model_names, ["Accuracy", "Precision", "Recall", "F1-Score"], data)
