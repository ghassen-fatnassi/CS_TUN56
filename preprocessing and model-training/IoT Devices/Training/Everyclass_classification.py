import os
import glob
import time
import numpy as np
import pandas as pd
import seaborn as sn
import datetime as dt
import tensorflow as tf
import matplotlib.pyplot as plt

from os import path
from tensorflow import keras
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, CSVLogger, TensorBoard
from matplotlib.pyplot import *
from keras.models import Model
from sklearn.model_selection import train_test_split
from keras.layers import Input, Dense, Dropout, Flatten, Convolution1D, MaxPooling1D, Concatenate
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn import metrics
from keras.optimizers import Adam
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score, f1_score, multilabel_confusion_matrix, classification_report

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

os.environ['TF_USE_LEGACY_KERAS'] = 'True'


path = r'./dataset' #path to dataset

all_files = glob.glob(path + "/*.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, encoding='cp1252', index_col=None, header=0)
    li.append(df)
    print("Read Completed for ", filename)
df = pd.concat(li, axis=0, ignore_index=True)
df.describe()
df.head()
df.info()

print(df.columns)
print(df['label'].value_counts())
print(df.shape)


# Data cleaning and encoding
data_clean = df.dropna().reset_index()
data_clean.drop_duplicates(keep='first', inplace=True)
labelencoder = LabelEncoder()
data_clean['label'] = labelencoder.fit_transform(data_clean['label'])

# Convert data to numpy and prepare features and labels
data_np = data_clean.to_numpy(dtype="float32")
data_np = data_np[~np.isinf(data_np).any(axis=1)]
X = data_np[:, :-1]
enc = OneHotEncoder()
Y = enc.fit_transform(data_np[:, -1].reshape(-1, 1)).toarray()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.20, random_state=33, shuffle=True)


_features = X.shape[1]
n_classes = Y.shape[1]

X_train = X_train.reshape(X_train.shape[0], _features, 1).astype('float32')
X_test = X_test.reshape(X_test.shape[0], _features, 1).astype('float32')

# Define the CNN model
input_img = Input(shape=(_features, 1))

# Parallel convolutional branches
branch1 = Convolution1D(64, kernel_size=3, activation='relu', padding='same')(input_img)
branch2 = Convolution1D(64, kernel_size=5, activation='relu', padding='same')(input_img)
branch3 = Convolution1D(64, kernel_size=11, activation='relu', padding='same')(input_img)

# Concatenate branches
concatenated = Concatenate(axis=-1)([branch1, branch2, branch3])

# Additional convolutional and max pooling layers
conv_layer = Convolution1D(72, kernel_size=7, activation='relu', padding='same')(concatenated)
pooling_layer = MaxPooling1D(pool_size=2)(conv_layer)

# Flatten and fully connected layers
flatten = Flatten()(pooling_layer)
dense1 = Dense(256, activation='relu')(flatten)
dropout1 = Dropout(0.2)(dense1)
output_layer = Dense(n_classes, activation='softmax')(dropout1)

# Build model
model = Model(inputs=input_img, outputs=output_layer)

# Compile model
opt = Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

# Callbacks
early_stop_callback = EarlyStopping(monitor='val_loss', patience=6)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, min_lr=1e-7)
model_checkpoint = ModelCheckpoint('best_model.keras', monitor='val_accuracy', save_best_only=True, mode='max')
csv_logger = CSVLogger('./results/history/CNN_training_log.csv')
tensorboard = TensorBoard(log_dir='./logs')
# Train model
start_fit = time.time()
history = model.fit(
    X_train, Y_train,
    batch_size=128,
    epochs=6,
    verbose=True,
    validation_data=(X_test, Y_test),
    callbacks=[early_stop_callback, reduce_lr, model_checkpoint, csv_logger, tensorboard]
)
end_fit = time.time()
fit_time = end_fit - start_fit
print("fit time: {:.2f} seconds".format(fit_time))

# Save training history and fit time
np.save('./results/history/CNN_Everyclass_classification_history.npy', history.history)
np.save('./history/CNN_Everyclass_classification_Fitting_time.npy', np.array([[start_fit, end_fit, fit_time]]))


# Plot training accuracy and loss
history_dict = history.history
epochs = range(1, len(history_dict['loss']) + 1)
plt.plot(epochs, history_dict['accuracy'], label='Training accuracy')
plt.plot(epochs, history_dict['val_accuracy'], label='Validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('./results/figures/CNN_Everyclass_classification_accuracy.eps', format='eps', dpi=1200)
plt.show()

plt.plot(epochs, history_dict['loss'], label='Training Loss')
plt.plot(epochs, history_dict['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.savefig('./results/figures/CNN_Everyclass_classification_loss.eps', format='eps', dpi=1200)
plt.show()

# Evaluate model
start_time = time.time()
pred = model.predict(X_test)
end_time = time.time()
inference_time = end_time - start_time
np.save('./results/history/CNN_Everyclass_classification_Inference_time.npy', np.array([[start_time, end_time, inference_time]]))

# Performance metrics
pred = np.argmax(pred, axis=1)
y_test = np.argmax(Y_test, axis=1)

score = accuracy_score(y_test, pred)
rscore = recall_score(y_test, pred, average='weighted')
ascore = precision_score(y_test, pred, average='weighted', zero_division=0)
ascore_macro = precision_score(y_test, pred, average='macro', zero_division=0)
f1score = f1_score(y_test, pred, average='weighted')

print(f"Validation score: {score}")
print(f"Recall score: {rscore}")
print(f"Precision score: {ascore}")
print(f"Precision score macro: {ascore_macro}")
print(f"F1 Measure score: {f1score}")

# Confusion matrix and plot
confMat = confusion_matrix(y_test, pred)
labels = ['DDoS-ACK_Fragmentation',     
        'DDoS-UDP_Flood',       
        'DDoS-SlowLoris',               
        'DDoS-ICMP_Flood',        
        'DDoS-RSTFINFlood',    
        'DDoS-PSHACK_Flood',        
        'DDoS-HTTP_Flood',              
        'DDoS-UDP_Fragmentation',     
        'DDoS-TCP_Flood',  
        'DDoS-SYN_Flood',        
        'DDoS-SynonymousIP_Flood',    
        'DDoS-ICMP_Fragmentation',
        'DoS-UDP_Flood',    
        'DoS-TCP_Flood',    
        'DoS-SYN_Flood',    
        'DoS-HTTP_Flood',
        'MITM-ArpSpoofing',     
        'DNS_Spoofing',
        'DictionaryBruteForce',
        'Recon-HostDiscovery', 
        'Recon-OSScan',     
        'Recon-PortScan',               
        'Recon-PingSweep',         
        'VulnerabilityScan',
        'SqlInjection',        
        'BrowserHijacking',         
        'CommandInjection',       
        'XSS',         
        'Backdoor_Malware',          
        'Uploading_Attack',
        'Mirai-greeth_flood',     
        'Mirai-udpplain',     
        'Mirai-greip_flood',
        'BenignTraffic']

plt.figure(figsize=(25,10))
sn.heatmap(pd.DataFrame(confMat), annot=True, fmt='g', xticklabels=labels, yticklabels=labels, cmap='Blues')
plt.ylabel('Actual Class')
plt.xlabel('Predicted Class')
plt.savefig('./results/figures/CNN_Everyclass_classification_confusion_matrix.eps', format='eps', dpi=1200)
plt.show()

# Classification report
class_report = classification_report(y_test, pred, target_names=labels, output_dict=True)
class_report_df = pd.DataFrame(class_report).transpose()
class_report_df.to_csv(r'./results/csvs/CNN_everyclass_classification_report.csv')

# Print summary of classification report
print("\nClassification Report:\n", classification_report(y_test, pred, target_names=labels))

# Ensure the directory exists
output_dir = './results/models'
os.makedirs(output_dir, exist_ok=True)

# Save the model
model_save_path = os.path.join(output_dir, 'cnn_everyclass_model.keras')
model.save(model_save_path)
print(f"Model saved to {model_save_path}")





