# Assignment-4

## Part-1
please refer to the Part -1 folder

## Part-2
# Analysis of KNN Model Performance

This document provides an analysis of the K-Nearest Neighbors (KNN) model's performance across different datasets, values of \( k \), and distance metrics. The findings are based on the provided results and dataset plots.
### Euclidean Distance
| Dataset Name | K=3 | K=6 | K=9 |
|--------------|------|------|------|
| dataset_1    | 100  | 100  | 100  |
| dataset_2    | 72   | 72   | 74   |
| dataset_3    | 54   | 44   | 42   |

### Chebyshev Distance
| Dataset Name | K=3 | K=6 | K=9 |
|--------------|------|------|------|
| dataset_1    | 100  | 100  | 100  |
| dataset_2    | 68   | 72   | 74   |
| dataset_3    | 52   | 44   | 50   |

---

## Insights and Observations

### 1. How and why does the accuracy change across datasets?
- **Dataset 1**:
  - 
  ![ds_1](https://github.iu.edu/cs-b551-fall2024/visunku-atmalji-a4/assets/27296/ac59b4eb-20e0-415f-adcd-8777fd5779d1)
  - The classes are well-separated, as shown in the plot. This results in 100% accuracy across all values of \( k \) and distance metrics.
  - The choice of distance metric has minimal impact because of the clear class boundaries.

- **Dataset 2**:
  - 
  ![ds_2](https://github.iu.edu/cs-b551-fall2024/visunku-atmalji-a4/assets/27296/0a9b8a78-0ba0-4aeb-9ceb-7ccf64a41c0e)
  - Moderate overlap between classes leads to reduced accuracy compared to `dataset_1`.
  - Accuracy is slightly influenced by the choice of \( k \) and distance metric.

- **Dataset 3**:
  - 
  ![ds_3](https://github.iu.edu/cs-b551-fall2024/visunku-atmalji-a4/assets/27296/46233e91-3d2c-47a0-95e2-13241aab81d6)
  - High overlap and uneven class distribution significantly reduce accuracy.
  - Performance varies across \( k \) values and distance metrics, highlighting the challenge of classifying highly overlapping data.

---

### 2. How and why does model accuracy change across different values of \( k \)?
- **Small \( k \) (e.g., \( k = 3 \))**:
  - Highly sensitive to local patterns and noise.
  - Performs well for simple datasets with clear class boundaries (e.g., `dataset_1`).

- **Moderate \( k \) (e.g., \( k = 6 \))**:
  - Balances sensitivity to local patterns and robustness to noise.
  - Often provides the best trade-off for moderately complex datasets (e.g., `dataset_2`).

- **Larger \( k \) (e.g., \( k = 9 \))**:
  - More robust to noise by considering larger neighborhoods.
  - Can lead to misclassification in overlapping datasets (e.g., `dataset_3`), where distant points influence the decision.

---

### 3. How does the choice of distance metric impact the performance of the model?
- **Euclidean Distance**:
  - Measures the straight-line distance.
  - Performs well for compact, evenly distributed classes (e.g., `dataset_1` and `dataset_2`).
  - Struggles with highly overlapping datasets (e.g., `dataset_3`).

- **Chebyshev Distance**:
  - Measures the maximum absolute difference along any dimension.
  - Performs similarly to Euclidean for `dataset_1`.
  - Slightly better for datasets with uneven distributions or dominant features (e.g., `dataset_3`).

---

## Conclusion
1. **Dataset Complexity**:
   - Accuracy decreases as the complexity of the dataset increases (more overlap or uneven distributions).

2. **Value of \( k \)**:
   - Small \( k \) values work well for simple datasets but are sensitive to noise.
   - Larger \( k \) values are robust to noise but can fail with overlapping data.

3. **Distance Metric**:
   - Euclidean is effective for compact, evenly distributed data.
   - Chebyshev can be advantageous for datasets with dominant features or uneven distributions.


---

## Notes
1. The KNN implementation resolves ties by selecting the first label with the maximum count, ensuring consistent behavior in classification.
2. In cases where multiple data points are equidistant, the algorithm considers the first \( k \) nearest neighbors based on their order in the dataset.
