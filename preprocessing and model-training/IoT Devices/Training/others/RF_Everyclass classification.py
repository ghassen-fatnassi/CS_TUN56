import os
import glob
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn import metrics
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sn
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

# Set path and load data
path = r'C:/Users/Youssef/Desktop/test3'
all_files = glob.glob(path + "/*.csv")
data_frames = []
for filename in all_files:
    df = pd.read_csv(filename, encoding='cp1252', index_col=None, header=0)
    data_frames.append(df)
    print(f"Read Completed for {filename}")
df = pd.concat(data_frames, axis=0, ignore_index=True)

# Basic Data Cleaning
data_clean = df.dropna().reset_index(drop=True)
data_clean.drop_duplicates(inplace=True)
labelencoder = LabelEncoder()
data_clean['label'] = labelencoder.fit_transform(data_clean['label'])
data_np = data_clean.to_numpy(dtype="float32")
data_np = data_np[~np.isinf(data_np).any(axis=1)]

# Separate features and labels
X = data_np[:, :-1]
Y = data_np[:, -1]

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the dataset
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.25, random_state=33, shuffle=True
)

# Define a Random Forest model
rf_model = RandomForestClassifier(class_weight="balanced", random_state=33)

# Hyperparameter tuning with RandomizedSearchCV
param_dist = {
    "n_estimators": [100, 200, 500],
    "max_depth": [20, 30, 40, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["sqrt", "log2", None]
}
random_search = RandomizedSearchCV(
    rf_model, param_distributions=param_dist, n_iter=10, cv=3, scoring='accuracy', random_state=33, n_jobs=-1
)

# Fit the model
random_search.fit(X_train, Y_train)
best_rf_model = random_search.best_estimator_

# Evaluate model
Y_pred = best_rf_model.predict(X_test)
accuracy = metrics.accuracy_score(Y_test, Y_pred)
precision = metrics.precision_score(Y_test, Y_pred, average='weighted', zero_division=0)
recall = metrics.recall_score(Y_test, Y_pred, average='weighted')
f1 = metrics.f1_score(Y_test, Y_pred, average='weighted')

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")

# Confusion Matrix
conf_mat = confusion_matrix(Y_test, Y_pred)
labels = labelencoder.classes_
cm_df = pd.DataFrame(conf_mat, index=labels, columns=labels)
plt.figure(figsize=(12, 10))
sn.heatmap(cm_df, annot=True, cmap='Blues', fmt='g')
plt.ylabel('Actual Class')
plt.xlabel('Predicted Class')
plt.title('Random Forest Confusion Matrix')
plt.savefig('C:/Users/Youssef/Desktop/test3/results/figures/RF_classification_confusion_matrix.eps', format='eps', dpi=1200)
plt.show()

# Classification Report
report = classification_report(Y_test, Y_pred, target_names=labels)
print("Classification Report:\n", report)

# Save the report to a file
report_df = pd.DataFrame(classification_report(Y_test, Y_pred, target_names=labels, output_dict=True)).transpose()
report_df.to_csv(r'C:/Users/Youssef/Desktop/test3/results/csvs/RF_classification_report.csv')
