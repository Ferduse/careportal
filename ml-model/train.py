import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler #Scale numerical features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score, f1_score, roc_auc_score
from sklearn.svm import SVC

import matplotlib.pyplot as plt

from imblearn.over_sampling import SMOTE

import torch
import torch.nn as nn

# --- Load Dataset ---

# read data
df = pd.read_csv("diabetes_prediction_dataset.csv")
print()

# -- Data Cleaning/Preprocessing ---

print("--- Data Cleaning/Preprocessing ---")
print()

# Check for the first 5 patients 
print(df.head())

# See how many rows and columns
print(df.shape)

# Check if theres missing values
print(df.isnull().sum())

# Check for duplicates
print("Duplicates:", df.duplicated().sum())

# Remove duplicates
df = df.drop_duplicates()
print("Shape after removing duplicates:", df.shape)

# Convert gender and smoking history to true/false
df = pd.get_dummies(df, columns=['gender','smoking_history'])

# Check the data types
print(df.dtypes)

# Check how many patients has and doesn't have diabetes
print(df['diabetes'].value_counts())
print(df['diabetes'].value_counts(normalize=True) * 100) # percentage of patients with and without diabetes

# Display the dataset cols
pd.set_option('display.max_columns', None)
print(df.head())

# --- Feature Selection ---
print()
print("--- Feature Selection ---")

# Separate features and target
X = df.drop("diabetes", axis=1) # features likes patient information
y = df["diabetes"] # target (output)

print("Features shape:", X.shape)
print("Target shape:", y.shape)

# --- Train/Test Split --- 
print()
print("--- Train/Test Split ---")

# Split into training (80%) and testing (20%) datasets
X_train, X_test, y_train, y_test = train_test_split(
    X, # Patient information
    y, # diabetes
    test_size=0.2, # 20% for testing
    random_state=42 # Ensure that the data is split the same way every time the program runs.
)
print("Training Features:", X_train.shape)
print("Training Labels:", y_train.shape)
print()
print("Testing Features:", X_test.shape)
print("Testing Labels:", y_test.shape)

# --- Feature Scaling ---
scaler = StandardScaler()

# These cols need to be scaled down 
numerical_cols = [
    "age",
    "bmi",
    "HbA1c_level",
    "blood_glucose_level"
]

# Take the numerical cols from the training data, 
# scale them, and replace the original numerical columns 
# with the scaled ones.
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])

# Take numerical cols from test data, scale and replace
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

print("\n--- Scaled Training Data ---")
print(X_train[numerical_cols].head())

print("\n--- Scaled Testing Data ---")
print(X_test[numerical_cols].head())

# SMOTE - to balance the minority group
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# SMOTE Testing Verification 
print("\n--- Class Distribution Before SMOTE ---")
print(y_train.value_counts())

print("\n--- Class Distribution After SMOTE ---")
print(y_train_smote.value_counts())

# --- Logistic Regression Model ---
print("\n--- Logistic Regression Model ---")
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
lr_predictions = lr_model.predict(X_test)
print(lr_predictions)

# Evaluate Logistic Regression Model predictions
print("\n--- Evaluating Logistic Regression Model ---")

# Accuracy is used to check how often the model was correct overall.
lr_accuracy = accuracy_score(y_test, lr_predictions)
print(f"Accuracy: {lr_accuracy * 100:.2f}%\n")

# Confusion Matrix
lr_cm = confusion_matrix(y_test, lr_predictions)
print("Confusion Matrix:")
print(lr_cm)
print()

# Recall is used to check how many diabetic patients were correctly identified by the model 
lr_recall = recall_score(y_test, lr_predictions)
print(f"Recall: {lr_recall * 100:.2f}%")

# Specificity is used to check if the model correctly identified patients who DO NOT have diabetes
lr_tn, lr_fp, lr_fn, lr_tp = lr_cm.ravel()
lr_specificity = lr_tn / (lr_tn + lr_fp)
print(f"Specificity: {lr_specificity * 100:.2f}%")

# Precision measures how many patients predicted as diabetic actually had diabetes
lr_precision = precision_score(y_test, lr_predictions)

# F1 score balances precision and recall
lr_f1 = f1_score(y_test, lr_predictions)

print(f"Precision: {lr_precision * 100:.2f}%")
print(f"F1 Score: {lr_f1 * 100:.2f}%")

# ROC-AUC
# Get the probability of the positive class: diabetes
lr_probabilities = lr_model.predict_proba(X_test)[:, 1]

# Measure how well the model separates diabetic and non-diabetic patients
lr_roc_auc = roc_auc_score(y_test, lr_probabilities)
print(f"ROC-AUC: {lr_roc_auc:.4f}")

# --- Random Forest Model ---
print("\n--- Random Forest Model ---")
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
print(rf_predictions)

# Evaluate Random Forest Model predictions
print("\n--- Evaluating Random Forest Model ---")

# Accuracy
rf_accuracy = accuracy_score(y_test,rf_predictions)
print(f"Accuracy: {rf_accuracy * 100:.2f}%\n")

# Confusion Matirx
rf_cm = confusion_matrix(y_test, rf_predictions)
print("Random Forest Confusion Matrix:")
print(rf_cm)
print()

# Recall
rf_recall = recall_score(y_test, rf_predictions)
print(f"Recall: {rf_recall * 100:.2f}%")

# Specificity
rf_tn, rf_fp, rf_fn, rf_tp = rf_cm.ravel()
rf_specificity = rf_tn / (rf_tn + rf_fp)
print(f"Specificity: {rf_specificity * 100:.2f}%")

# Precision
rf_precision = precision_score(y_test, rf_predictions)
print(f"Precision: {rf_precision * 100:.2f}%")

# F1 Score
rf_f1 = f1_score(y_test, rf_predictions)
print(f"F1 Score: {rf_f1 * 100:.2f}%")

# ROC-AUC
rf_probabilities = rf_model.predict_proba(X_test)[:, 1]
rf_roc_auc = roc_auc_score(y_test, rf_probabilities)
print(f"ROC-AUC: {rf_roc_auc:.4f}")


# --- Pytorch Neural Network ---
print("\n--- PyTorch Neural Network ---\n")

# Convert Pandas DataFrame to a float32 NumPy array, then to a PyTorch tensor
X_train_tensor = torch.tensor(X_train.to_numpy(dtype="float32"))
X_test_tensor = torch.tensor(X_test.to_numpy(dtype="float32"))
y_train_tensor = torch.tensor(y_train.to_numpy(dtype="float32"))
y_test_tensor = torch.tensor(y_test.to_numpy(dtype="float32"))

print("Training Features Tensor:", X_train_tensor.shape)
print("Training Labels Tensor:", y_train_tensor.shape)
print("Testing Features Tensor:", X_test_tensor.shape)
print("Testing Labels Tensor:", y_test_tensor.shape)
print()

class DiabetesNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(15, 16)
        self.fc2 = nn.Linear(16, 8)
        self.output = nn.Linear(8, 1)
        
        # Activation function ReLU to learn more complex patterns 
    def forward(self,x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.output(x)
        return x
  
torch.manual_seed(42)
model = DiabetesNN()

# --- WEIGHTED VERSION ---
# Count the number of non-diabetic and diabetic patients to calculate the positive class weight
# negative_count = (y_train_tensor == 0).sum()
# positive_count = (y_train_tensor == 1).sum()

# Give more importance to diabetic patients since they are the minority class
# pos_weight = negative_count / positive_count
# print("Positive class weight:\n", pos_weight.item())
# loss_function = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

# --- STANDARD VERSION (Using this one) --- 
# Loss function for binary classification problem
# Measures how much error the neural network made 
loss_function = nn.BCEWithLogitsLoss()

# Optimizer changes the weights after the model makes a mistake
# change the weight and biases values only if the model makes a mistake
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training the model

# Reshape the labels to match the model's output shape
y_train_tensor = y_train_tensor.view(-1, 1) # -1 means pytorch automatically adds the rows, but 1 means we want 1 column
y_test_tensor = y_test_tensor.view(-1, 1)

# For the learning curve graph
# losses = []

# Repeats training process 100 times 
epochs = 100
for epoch in range(epochs):
    # 1. Make predictions
    # Sends all training patient info into the NN 
    predictions = model(X_train_tensor)
    
    # 3. Calculate loss
    loss = loss_function(predictions, y_train_tensor)

    # 4. Clear old gradients from previous epoch so we can calculate new ones
    optimizer.zero_grad()

    # 5. Backpropagation
    # Calculate how each weight and bias should change to reduce the loss
    loss.backward()

    # 6. Update weights and biases
    # Apply those calculated changes to improve the model
    optimizer.step()

    # Save the loss for the learning curve
    # losses.append(loss.item())
    
    # Print the training progress every 10 epochs
    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch + 1}/{epochs}], "f"Loss: {loss.item():.4f}")
  
"""
# Create the learning curve (loss)
plt.figure(figsize=(8, 5))
plt.plot(range(1, epochs + 1), losses, marker="o", markersize=2)
plt.title("PyTorch Neural Network Learning Curve")
plt.xlabel("Epoch")
plt.ylabel("Training Loss")
# Make the graph start at Epoch 1
plt.xlim(1, epochs)
plt.xticks([1, 20, 40, 60, 80, 100])
plt.grid(True)
plt.show()
""" 

# Evaluate the neural network on the test data
model.eval()

with torch.no_grad():
    # Raw test outputs 
    test_logits = model(X_test_tensor)
    
    # Convert raw tests into probabilities
    test_probabilities = torch.sigmoid(test_logits)
    
    # Convert probalilities into class predictions using 0.5 as the threshold
    test_predictions = (test_probabilities >= 0.5).int()

# Convert tensors to one-dimensional NumPy arrays for evaluation
nn_predictions = test_predictions.numpy().ravel()
nn_y_test = y_test_tensor.numpy().ravel()

# Keep the probabilities for ROC-AUC
nn_probabilities = test_probabilities.numpy().ravel()

# Accuracy
nn_accuracy = accuracy_score(nn_y_test, nn_predictions)
print(f"\nAccuracy: {nn_accuracy:.2%}\n")

# Confusion Matrix
nn_cm = confusion_matrix(nn_y_test, nn_predictions)
print("Confusion Matrix:")
print(nn_cm)

# Recall
nn_recall = recall_score(nn_y_test, nn_predictions)
print(f"\nRecall: {nn_recall * 100:.2f}%")

# Specificity
nn_tn, nn_fp, nn_fn, nn_tp = nn_cm.ravel()
nn_specificity = nn_tn / (nn_tn + nn_fp)
print(f"Specificity: {nn_specificity * 100:.2f}%")

# Precision
nn_precision = precision_score(nn_y_test, nn_predictions, zero_division=0)
print(f"Precision: {nn_precision * 100:.2f}%")

# F1 Score
nn_f1 = f1_score(nn_y_test, nn_predictions)
print(f"F1 Score: {nn_f1 * 100:.2f}%")

# ROC-AUC: Uses probabilities instead of final 0/1 predictions
nn_roc_auc = roc_auc_score(nn_y_test, nn_probabilities)
print(f"ROC-AUC: {nn_roc_auc:.4f}\n")

# --- SVM Models ---
print("\n --- SVM - Linear ---")
linear_svm = SVC(kernel="linear", random_state=42) # probability=True estimates class probabilities after training. This is for ROC-AUC.
linear_svm.fit(X_train_smote, y_train_smote)
linear_predictions = linear_svm.predict(X_test) # evaluate on original test set 

# Evaluation metrics 

#Accuracy
linear_accuracy = accuracy_score(y_test, linear_predictions)
print(f"Accuracy: {linear_accuracy * 100:.2f}%\n")

# Confusion Matrix
linear_confusion = confusion_matrix(y_test, linear_predictions)
print("Confusion Matrix:")
print(linear_confusion)

# Recall
linear_recall = recall_score(y_test, linear_predictions)
print(f"\nRecall: {linear_recall * 100:.2f}%")

# Specificity
linear_tn, linear_fp, linear_fn, linear_tp = linear_confusion.ravel()
linear_specificity = linear_tn / (linear_tn + linear_fp)
print(f"Specificity: {linear_specificity * 100:.2f}%")

# Percision
linear_precision = precision_score(y_test, linear_predictions)
print(f"Precision: {linear_precision * 100:.2f}%")

# F1 Score
linear_f1 = f1_score(y_test, linear_predictions)
print(f"F1 Score: {linear_f1 * 100:.2f}%\n")

# ROC-AUC
# linear_probabilities = linear_svm.predict_proba(X_test)[:, 1]
# linear_auc = roc_auc_score(y_test, linear_probabilities)
# print(f"ROC-AUC: {linear_auc:.4f}")

# --- SVM - RBF ---
# Radial Basis Function, creates a curved decision boundary which is great for complex patterns 
print("--- SVM - RBF ---") 
rbf_svm = SVC(kernel="rbf", random_state=42)
rbf_svm.fit(X_train_smote, y_train_smote)
rbf_predictions = rbf_svm.predict(X_test)

# Evaluation metrics 

#Accuracy
rbf_accuracy = accuracy_score(y_test, rbf_predictions)
print(f"Accuracy: {rbf_accuracy * 100:.2f}%\n")

# Confusion Matrix
rbf_confusion = confusion_matrix(y_test, rbf_predictions)
print("Confusion Matrix:")
print(rbf_confusion)

# Recall
rbf_recall = recall_score(y_test, rbf_predictions)
print(f"\nRecall: {rbf_recall * 100:.2f}%")

# Specificity
rbf_tn, rbf_fp, rbf_fn, rbf_tp = rbf_confusion.ravel()
rbf_specificity = rbf_tn / (rbf_tn + rbf_fp)
print(f"Specificity: {rbf_specificity * 100:.2f}%")

# Percision
rbf_precision = precision_score(y_test, rbf_predictions)
print(f"Precision: {rbf_precision * 100:.2f}%")

# F1 Score
rbf_f1 = f1_score(y_test, rbf_predictions)
print(f"F1 Score: {rbf_f1 * 100:.2f}%\n")

# --- SVM - Polynomial ---
# Polynomial creates a curved decision boundary which is great from complex patterns 
print("--- SVM - Polynomial ---") 
poly_svm = SVC(kernel="poly", degree=3, random_state=42)
poly_svm.fit(X_train_smote, y_train_smote)
poly_predictions = poly_svm.predict(X_test)

# Evaluation metrics

# Accuracy
poly_accuracy = accuracy_score(y_test, poly_predictions)
print(f"Accuracy: {poly_accuracy * 100:.2f}%\n")

# Confusion Matrix
poly_confusion = confusion_matrix(y_test, poly_predictions)
print(poly_confusion)

# Recall
poly_recall = recall_score(y_test, poly_predictions)
print(f"\nRecall: {poly_recall * 100:.2f}%")

# Specificity
poly_tn, poly_fp, poly_fn, poly_tp = poly_confusion.ravel()
poly_specificity = poly_tn / (poly_tn + poly_fp)
print(f"Specificity: {poly_specificity * 100:.2f}%")

# Precision
poly_precision = precision_score(y_test, poly_predictions)
print(f"Precision: {poly_precision * 100:.2f}%")

# F1 Score
poly_f1 = f1_score(y_test, poly_predictions)
print(f"F1 Score: {poly_f1 * 100:.2f}%")