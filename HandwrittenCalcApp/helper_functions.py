# helper_functions.py

import tensorflow as tf

# define unzip_data
import zipfile

def unzip_data(filename):
    zip_ref = zipfile.ZipFile(filename, "r")
    zip_ref.extractall()
    zip_ref.close()


# define walk_through_dir
import os

def walk_through_dir(dir_path):
    for dirpath, dirnames, filenames in os.walk(dir_path):
        print(f"{dirpath} 폴더에는 {len(dirnames)}개의 폴더와 {len(filenames)}개의 파일이 존재합니다.")    


# define create_tensorboard_callback
import datetime

def create_tensorboard_callback(dir_name, experiment_name):
    log_dir = dir_name + "/" + experiment_name + "/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir = log_dir
    )
    print(f"TensorBoard 로그 파일을 저장한 디렉토리 : {log_dir}")
    return tensorboard_callback


# define plot_loss_curves
import matplotlib.pyplot as plt

def plot_loss_curves(history):
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]

    accuracy = history.history["accuracy"]
    val_accuracy = history.history["val_accuracy"]

    epochs = range(len(history.history["loss"]))

    plt.plot(epochs, loss, label="training_loss")
    plt.plot(epochs, val_loss, label="val_loss")
    plt.title("Loss")
    plt.xlabel("Epochs")
    plt.legend()

    plt.figure()
    plt.plot(epochs, accuracy, label="training_accuracy")
    plt.plot(epochs, val_accuracy, label="val_accuracy")
    plt.title("Accuracy")
    plt.xlabel("Epochs")
    plt.legend()

# define compare_history
def compare_historys(original_history, new_history, initial_epochs = 5):
    acc = original_history.history["accuracy"]
    loss = original_history.history["loss"]

    print(len(acc))

    val_acc = original_history.history["val_accuracy"]
    val_loss = original_history.history["val_loss"]

    total_acc = acc + new_history.history["accuracy"]
    total_loss = loss + new_history.history["loss"]

    total_val_acc = val_acc + new_history.history["val_accuracy"]
    total_val_loss = val_loss + new_history.history["val_loss"]

    print(len(total_acc))
    print(total_acc)

    plt.figure(figsize = (8, 8))
    plt.subplot(2, 1, 1)
    plt.plot(total_acc, label = "Training Accuracy")
    plt.plot(total_val_acc, label = "Validation Accuracy")
    plt.plot(
        [initial_epochs, initial_epochs],
        plt.ylim(),
        label = "Start Fine Tuning"
    )
    plt.legend(loc = "lower right")
    plt.title("Training and Validation Accuracy")

    plt.subplot(2, 1, 2)
    plt.plot(total_loss, label = "Training Loss")
    plt.plot(total_val_loss, label = "Validation Loss")
    plt.plot(
        [initial_epochs, initial_epochs],
        plt.ylim(),
        label = "Start Fine Tuning"
    )
    plt.legend(loc = "upper right")
    plt.title("Training and Validation Loss")
    plt.xlabel("epoch")
    plt.show()