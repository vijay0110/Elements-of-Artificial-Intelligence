import matplotlib.pyplot as plt
import json

import subprocess

# Command to run
for dm in ['euclidian','chebyshev']:
    for i in ['1','2','3']:
        for k in ['3','6','9']:
            command = 'python3 main.py --dataset_path dataset_'+i+'.json --k '+k+' --distance_metric '+dm
            print(dm,'dataset_'+i+'.json', 'k = '+k )
            print(subprocess.run(command, shell=True, check=True, capture_output=True, text=True).stdout)


def plot_training_data(X_train, y_train, title):
    """
    Plot the training data with different classes.

    Parameters:
        X_train: list of lists
            The training data features (2D).
        y_train: list
            The training data labels.
        title: str
            The title of the plot.
    """
    classes = set(y_train)
    for cls in classes:
        class_points = [X_train[i] for i in range(len(X_train)) if y_train[i] == cls]
        x_coords = [point[0] for point in class_points]
        y_coords = [point[1] for point in class_points]
        plt.scatter(x_coords, y_coords, label=f"Class {cls}")

    plt.title(title)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.show()


# List of dataset files
dataset_files = ['dataset_1.json', 'dataset_2.json', 'dataset_3.json']

# Loop through each dataset and plot
for dataset_file in dataset_files:
    with open(dataset_file, 'r') as f:
        data = json.load(f)
        X_train, y_train = data['X_train'], data['y_train']
        plot_training_data(X_train, y_train, title=f"Training Data for {dataset_file}")
