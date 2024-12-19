import json
import argparse


# Calculate the Euclidean distance between two points.
def euclidean_distance(point1, point2):
    sum = 0
    for i in range(len(point1)):
        # Sum the squared differences between each coordinate
        sum = sum + (point1[i] - point2[i]) ** 2
    return sum ** 0.5  # Return the square root of the sum

# Calculate the Chebyshev distance between two points.
def chebyshev_distance(point1, point2):
    max_v = 0
    for i in range(len(point1)):
        # Find the maximum absolute difference along any dimension
        max_v = max(max_v, abs(point1[i] - point2[i]))
    return max_v

# Train and predict using the K-Nearest Neighbors (KNN) algorithm.
def knn_train_prediction(X_train, y_train, X_test, k, distance_metric):
    predictions = []
    for test_point in X_test:
        # Compute distances from the test point to all training points
        if distance_metric == 'euclidian':
            distances = [euclidean_distance(test_point, train_point) for train_point in X_train]
        elif distance_metric == 'chebyshev':
            distances = [chebyshev_distance(test_point, train_point) for train_point in X_train]

        # Find the indices of the k-nearest neighbors
        k_indices = sorted(range(len(distances)), key=lambda i: distances[i])[:k]

        # Extract the labels of the k-nearest neighbors
        k_labels = [y_train[i] for i in k_indices]

        # Determine the most common label among the neighbors
        label_count = {}
        for label in k_labels:
            label_count[label] = label_count.get(label, 0) + 1
        most_common_label = max(label_count, key=label_count.get)

        # Append the predicted label to the predictions list
        predictions.append(most_common_label)
    return predictions


def accuracy_fn(y_test, y_pred):
    """
    Calculate the accuracy of predictions.

    Parameters:
        y_test: list
            The true labels of the test data.
        y_pred: list
            The predicted labels.

    Returns:
        float
            The accuracy of the predictions as a percentage.
    """
    num = 0
    for i in range(len(y_test)):
        # Count the number of correct predictions
        if y_test[i] == y_pred[i]:
            num += 1
    return (num / len(y_test)) * 100  # Calculate and return accuracy as a percentage


def K_Nearest_Neighbors(file: str, k: int, distance_metric: str):
    """ Implements K-Nearest Neighbors Algorithm

    Args:
        file (str): path to the dataset file
        k (int): number of nearest Neighbors considered in the analysis
        distance_metric (str): distance metric for K-NN algorithm

    Returns:
        float: accuracy on the test set
    """

    with open(file, 'r') as f:
        data = json.load(f)
        X_train, y_train, X_test, y_test = data['X_train'], data['y_train'], data['X_test'], data['y_test']
    # print(type(X_train))
    y_pred = knn_train_prediction(X_train, y_train, X_test, k, distance_metric)
    # print(len(X_train),len(y_train),len(X_test),len(y_test),len(y_pred))

    # Implement K_Nearest_Neghbors Algorithm here.

    # Calculate accuracy for test set.
    accuracy_test_set = accuracy_fn(y_test, y_pred) # between 0 and 100

    return accuracy_test_set

def main():
    parser = argparse.ArgumentParser(description='KNN Classification with Synthetic Data')
    parser.add_argument('--dataset_path', type=str, help="path to the json file containing data")
    parser.add_argument('--k', type=int, help="k for k-NN algorithm")
    parser.add_argument('--distance_metric', type=str, help="distance metric for K-NN")
    args = parser.parse_args()
    
    accuracy = K_Nearest_Neighbors(args.dataset_path, args.k, args.distance_metric)
    print(f"Test set accuracy for {args.dataset_path} - {accuracy}.")

if __name__ == '__main__':
    main()