import pandas as pd
from sklearn.model_selection import train_test_split

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
    random_state=42 
)
print("Training Features:", X_train.shape)
print("Training Labels:", y_train.shape)
print()
print("Testing Features:", X_test.shape)
print("Testing Labels:", y_test.shape)