import json
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
import tensorflow as tf
import joblib
import ast
from tqdm import tqdm
import matplotlib.pyplot as plt
import logging
from sklearn.preprocessing import OneHotEncoder
from collections import defaultdict

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('debug_log.txt')
    ]
)

# Define paths
model_path = 'my_lstm_model_final.h5'
mapping_path = 'demo_result/hdfs_log_templates.json'
feature_extractor_path = 'feature_extractor.joblib'
sequences_file = 'demo_result/hdfs_sequence1.csv'

def parse_sequence(seq_str):
    """Safely parse sequence strings."""
    try:
        seq_str = seq_str.replace("'", '"')  # Ensure valid JSON
        seq = json.loads(seq_str)
        return seq if isinstance(seq, list) else []
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(seq_str)
        except:
            logging.error(f"Failed to parse sequence: {seq_str}")
            return []

def verify_event_ids(event_sequences, eventid_to_idx):
    """Verify that all event IDs in sequences are present in the mapping."""
    unique_event_ids = set()
    for seq_str in event_sequences:
        seq = parse_sequence(seq_str)
        unique_event_ids.update(seq)
    
    missing_event_ids = [eid for eid in unique_event_ids if str(eid) not in eventid_to_idx]
    
    if missing_event_ids:
        logging.warning(f"Missing Event IDs in mapping: {missing_event_ids}")
    else:
        logging.info("All Event IDs are present in the mapping.")

def inspect_feature_extractor(feature_extractor, eventid_to_idx):
    """Detailed inspection of the feature extractor."""
    logging.info("\n=== Feature Extractor Inspection ===")
    
    # Check feature extractor type and attributes
    logging.info(f"Feature Extractor Type: {type(feature_extractor)}")
    logging.info(f"Feature Extractor Attributes: {dir(feature_extractor)}")
    
    if hasattr(feature_extractor, 'get_params'):
        logging.info(f"Parameters: {feature_extractor.get_params()}")
    
    if isinstance(feature_extractor, OneHotEncoder):
        logging.info("\nOneHotEncoder Categories:")
        for idx, category in enumerate(feature_extractor.categories_):
            logging.info(f"Feature {idx}: {category}")
    
    # Test transformation with different input shapes
    test_cases = [
        np.array([[1]]),          # Single value
        np.array([[1, 2]]),       # Two values
        np.array([[1], [2]]),     # Two sequences
    ]
    
    logging.info("\nTest Transformations:")
    for i, test_input in enumerate(test_cases):
        try:
            logging.info(f"\nTest case {i+1}:")
            logging.info(f"Input shape: {test_input.shape}")
            logging.info(f"Input content: {test_input}")
            result = feature_extractor.transform(test_input)
            logging.info(f"Output shape: {result.shape}")
            logging.info(f"Output content: {result}")
        except Exception as e:
            logging.error(f"Test case {i+1} failed: {str(e)}")
    
    # Test with actual sequence sample
    try:
        logging.info("\nTesting with actual sequence sample:")
        # Define a sample sequence (ensure it contains known Event IDs)
        sample_seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Example sequence
        logging.info(f"Original sequence: {sample_seq}")
        seq_indices = [eventid_to_idx.get(str(event_id), 0) for event_id in sample_seq]
        logging.info(f"Event indices: {seq_indices}")
        seq_array = np.array(seq_indices).reshape(1, -1)
        logging.info(f"Array shape before feature extraction: {seq_array.shape}")
        result = feature_extractor.transform(seq_array)
        logging.info(f"Output shape: {result.shape}")
        logging.info(f"Output content: {result}")
    except Exception as e:
        logging.error(f"Sample sequence test failed: {str(e)}")

def encode_sequences_debug(event_sequences, feature_extractor, eventid_to_idx, sequence_length):
    """Debug version of sequence encoding."""
    logging.info("\n=== Sequence Encoding Debug ===")
    
    # Process first 5 sequences in detail
    debug_sequences = event_sequences[:5]
    all_features = []
    
    for i, seq_str in enumerate(debug_sequences):
        logging.info(f"\nProcessing sequence {i+1}")
        
        # Parse sequence
        seq = parse_sequence(seq_str)
        logging.info(f"Original sequence: {seq}")
        
        # Convert to indices
        seq_indices = [eventid_to_idx.get(str(event_id), 0) for event_id in seq]
        logging.info(f"Event indices: {seq_indices}")
        
        # Pad or truncate the sequence
        if len(seq_indices) < sequence_length:
            seq_indices += [0] * (sequence_length - len(seq_indices))
        elif len(seq_indices) > sequence_length:
            seq_indices = seq_indices[:sequence_length]
        logging.info(f"Sequence indices after padding/truncating: {seq_indices}")
        
        # Create array and extract features
        seq_array = np.array(seq_indices).reshape(1, -1)
        logging.info(f"Array shape before feature extraction: {seq_array.shape}")
        
        try:
            # Extract features
            features = feature_extractor.transform(seq_array)
            logging.info(f"Features shape: {features.shape}")
            logging.info(f"Features content: {features}")
            all_features.append(features)
            
            if i > 0:
                is_identical = np.array_equal(features, all_features[0])
                logging.info(f"Features identical to first sequence: {is_identical}")
                if is_identical:
                    logging.warning("Features are identical despite different input sequences!")
        except Exception as e:
            logging.error(f"Feature extraction failed: {str(e)}")
    
    # Compare all debug sequences
    if all_features:
        features_array = np.vstack(all_features)
        unique_features = np.unique(features_array, axis=0)
        logging.info(f"\nUnique features in debug sample: {len(unique_features)} out of {len(debug_sequences)}")
    
    return all_features

def encode_sequences(event_sequences, feature_extractor, eventid_to_idx, sequence_length):
    """Main sequence encoding function."""
    encoded_sequences = []
    
    for seq_str in tqdm(event_sequences, desc="Encoding Sequences", unit="seq"):
        # Parse sequence
        seq = parse_sequence(seq_str)
        
        # Convert to indices
        seq_indices = [eventid_to_idx.get(str(event_id), 0) for event_id in seq]
        
        # Pad or truncate the sequence
        if len(seq_indices) < sequence_length:
            seq_indices += [0] * (sequence_length - len(seq_indices))
        elif len(seq_indices) > sequence_length:
            seq_indices = seq_indices[:sequence_length]
        
        logging.debug(f"Sequence indices: {seq_indices}")
        
        # Create array and extract features
        seq_array = np.array(seq_indices).reshape(1, -1)
        
        try:
            features = feature_extractor.transform(seq_array)
            
            if features.ndim == 2:
                features = features.reshape(1, -1)
            
            encoded_sequences.append(features)
        except Exception as e:
            logging.error(f"Feature extraction failed for sequence: {seq_str}")
            logging.error(f"Error: {str(e)}")
            # Optionally, append a zero vector or skip
            encoded_sequences.append(np.zeros((1, feature_extractor.transform(np.array([[0]*sequence_length])).shape[1])))
    
    # Stack all features into a single array
    result = np.vstack(encoded_sequences)
    logging.info(f"\nFinal encoded shape: {result.shape}")
    unique_features = np.unique(result, axis=0)
    logging.info(f"Number of unique feature vectors: {len(unique_features)} out of {len(event_sequences)}")
    
    return result

def main():
    # Print TensorFlow version
    logging.info(f"TensorFlow version: {tf.__version__}")
    
    # Clear Keras session
    K.clear_session()
    
    # Load EventId mapping
    try:
        with open(mapping_path, 'r') as f:
            eventid_to_idx = json.load(f)
        logging.info("Event ID mapping loaded successfully")
        logging.info(f"Number of unique event IDs: {len(eventid_to_idx)}")
    except Exception as e:
        logging.error(f"Error loading Event ID mapping: {e}")
        raise
    
    # Convert mapping keys to strings and ensure unique mapping
    eventid_to_idx = {str(event_id): int(idx) for event_id, idx in eventid_to_idx.items()}
    
    # Check for duplicate index assignments
    index_to_eventids = defaultdict(list)
    for event_id, idx in eventid_to_idx.items():
        index_to_eventids[idx].append(event_id)
    
    duplicate_indices = {idx: ids for idx, ids in index_to_eventids.items() if len(ids) > 1}
    if duplicate_indices:
        logging.error(f"Duplicate index assignments found: {duplicate_indices}")
        raise ValueError("Duplicate index assignments detected in EventId mapping.")
    else:
        logging.info("No duplicate index assignments in EventId mapping.")
    
    # Set parameters
    sequence_length = 10  # Adjust based on your data and training
    vocab_size = max(eventid_to_idx.values()) + 1
    logging.info(f"Vocabulary size: {vocab_size}")
    
    # Load feature extractor
    try:
        feature_extractor = joblib.load(feature_extractor_path)
        logging.info("Feature extractor loaded successfully")
    except Exception as e:
        logging.error(f"Error loading feature extractor: {e}")
        raise
    
    # Inspect feature extractor
    inspect_feature_extractor(feature_extractor, eventid_to_idx)
    
    # Load sequences
    try:
        sequences_df = pd.read_csv(sequences_file)
        event_sequences = sequences_df['EventSequence'].tolist()
        logging.info(f"Loaded {len(event_sequences)} sequences")
        
        # Log sample sequences
        logging.info("\nSample sequences:")
        for i, seq in enumerate(event_sequences[:3]):
            logging.info(f"Sequence {i+1}: {seq[:100]}...")  # First 100 chars for brevity
    except Exception as e:
        logging.error(f"Error loading sequences: {e}")
        raise
    
    # Verify all event IDs in sequences are present in the mapping
    verify_event_ids(event_sequences, eventid_to_idx)
    
    # Debug feature extractor with first 5 sequences
    logging.info("\nStarting detailed feature extraction debugging...")
    debug_features = encode_sequences_debug(event_sequences, feature_extractor, eventid_to_idx, sequence_length)
    
    # Process all sequences
    logging.info("\nProcessing all sequences...")
    sequences = encode_sequences(event_sequences, feature_extractor, eventid_to_idx, sequence_length)
    
    # Reshape for LSTM
    sequences = sequences.reshape((sequences.shape[0], 1, sequences.shape[1]))
    logging.info(f"Final sequence shape: {sequences.shape}")
    
    # Load and verify model
    try:
        model = load_model(model_path)
        logging.info("Model loaded successfully")
        model.summary()
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        raise
    
    # Make predictions
    try:
        logging.info("Starting predictions...")
        scores = model.predict(sequences, batch_size=512, verbose=1)
        logging.info("Predictions completed")
        
        # Log prediction statistics
        logging.info("\nPrediction Statistics:")
        logging.info(f"Min: {scores.min()}")
        logging.info(f"Max: {scores.max()}")
        logging.info(f"Mean: {scores.mean()}")
        logging.info(f"Std: {scores.std()}")
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise
    
    # Plot distribution
    plt.figure(figsize=(10, 6))
    plt.hist(scores, bins=50, color='skyblue', edgecolor='black')
    plt.title('Distribution of Prediction Scores')
    plt.xlabel('Prediction Score')
    plt.ylabel('Number of Sequences')
    plt.savefig('prediction_scores_distribution.png')
    plt.close()
    logging.info("Prediction scores distribution plotted and saved as 'prediction_scores_distribution.png'")
    
    # Set threshold and detect anomalies
    # threshold = np.percentile(scores, 95)  # Original dynamic threshold
    threshold = 0.5  # Static threshold set to 0.5
    logging.info(f"\nThreshold set to static value: {threshold}")
    
    predictions = (scores < threshold).astype(int).flatten()
    anomalous_indices = np.where(predictions == 1)[0]
    logging.info(f"Number of anomalies detected: {len(anomalous_indices)}")
    
    # Analyze anomalies
    if len(anomalous_indices) > 0:
        logging.info("\nAnalyzing anomalous sequences:")
        for idx in anomalous_indices[:10]:  # Show first 10 anomalies
            seq = parse_sequence(event_sequences[idx])
            logging.info(f"Anomaly at index {idx}:")
            logging.info(f"Score: {scores[idx]}")
            logging.info(f"Sequence: {seq}")
    else:
        logging.info("No anomalies detected.")
    
    # Close TensorFlow session
    K.clear_session()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Program failed: {e}", exc_info=True)
