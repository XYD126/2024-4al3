import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, confusion_matrix, ConfusionMatrixDisplay 

# Load actual and predicted data
actual_data_path = "data/merged_ERI.csv"
predicted_data_path = "data/predicted_ERI_2021.csv"

# Load data
actual_data = pd.read_csv(actual_data_path)
predicted_data = pd.read_csv(predicted_data_path)

# Filter actual 2021 data
target_columns = ['Erosion_Value1N', 'Erosion_Value2N', 'Erosion_Value3N', 'Erosion_Value4N']
actual_2021 = actual_data[actual_data['Year'] == 2021][target_columns].reset_index(drop=True)

# Ensure alignment
if len(actual_2021) != len(predicted_data):
    raise ValueError("Mismatch between actual and predicted data lengths.")

# Evaluate performance
results = {}
for col in target_columns:
    actual = actual_2021[col]
    predicted = predicted_data[col]
    
    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(actual, predicted)
    r2 = r2_score(actual, predicted)
    
    results[col] = {
        "MSE": mse,
        "RMSE": rmse,
        "MAE": mae,
        "R2 Score": r2
    }

# Display evaluation results
results_df = pd.DataFrame(results).T
print("Evaluation Results:")
print(results_df)

# Visualization of predictions vs. actual
plt.figure(figsize=(14, 10))
for i, col in enumerate(target_columns, 1):
    plt.subplot(2, 2, i)
    plt.plot(actual_2021[col], label='Actual', marker='o')
    plt.plot(predicted_data[col], label='Predicted', marker='o', mec = 'r', mfc = 'r')
    plt.title(f"Actual vs Predicted for {col}")
    plt.xlabel("Sample Index")
    plt.ylabel("Erosion Value")
    plt.legend()
    plt.tight_layout()
plt.savefig("results/actual_vs_predicted.png")
plt.show()

# Residual analysis
plt.figure(figsize=(14, 10))
for i, col in enumerate(target_columns, 1):
    residuals = actual_2021[col] - predicted_data[col]
    plt.subplot(2, 2, i)
    plt.scatter(range(len(residuals)), residuals, alpha=0.7)
    plt.axhline(0, color='red', linestyle='--')
    plt.title(f"Residuals for {col}")
    plt.xlabel("Sample Index")
    plt.ylabel("Residual (Actual - Predicted)")
    plt.tight_layout()
plt.savefig("results/residuals_analysis.png")
plt.show()

# Function to map continuous values to categories
def map_to_category(value):
    if value < 6:
        return "Very Low"
    elif 6 <= value <= 11:
        return "Low"
    elif 11 < value <= 22:
        return "Moderate"
    elif 22 < value <= 33:
        return "High"
    else:
        return "Very High"

# Map actual and predicted values to categories
for col in target_columns:
    actual_2021[f"{col}_Category"] = actual_2021[col].apply(map_to_category)
    predicted_data[f"{col}_Category"] = predicted_data[col].apply(map_to_category)

# Confusion matrices
for col in target_columns:
    y_true = actual_2021[f"{col}_Category"]
    y_pred = predicted_data[f"{col}_Category"]
    cm = confusion_matrix(y_true, y_pred, labels=["Very Low", "Low", "Moderate", "High", "Very High"])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Very Low", "Low", "Moderate", "High", "Very High"])
    disp.plot(cmap=plt.cm.Blues, values_format='d')
    plt.title(f"Confusion Matrix for {col}")
    plt.tight_layout()
    plt.savefig(f"results/confusion_matrix_{col}.png")
    plt.show()