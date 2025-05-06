import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('traffic_accidents.csv')

# Preprocessing
df['date_time'] = pd.to_datetime(df['date_time'])
df['hour'] = df['date_time'].dt.hour
df['day_of_week'] = df['date_time'].dt.dayofweek

# Convert categorical data
categorical_cols = ['weather', 'road_condition', 'vehicle_type']
df = pd.get_dummies(df, columns=categorical_cols)

# Target variable
df['accident_severity'] = df['accident_severity'].map({'Low': 0, 'Medium': 1, 'High': 2})

# Features and Labels
features = df.drop(['date_time', 'location', 'accident_severity'], axis=1)
labels = df['accident_severity']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)

# Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("Classification Report:\n", classification_report(y_test, y_pred))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.show()