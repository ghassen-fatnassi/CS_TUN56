import json
import pandas as pd
import logging
import ast
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('mapping_generation.log')
    ]
)

def parse_sequence(seq_str):
    """Safely parse sequence strings into lists of integers."""
    try:
        # Replace single quotes with double quotes for valid JSON
        seq_str = seq_str.replace("'", '"')
        seq = json.loads(seq_str)
        if isinstance(seq, list):
            return seq
        else:
            logging.error(f"Parsed sequence is not a list: {seq_str}")
            return []
    except json.JSONDecodeError:
        try:
            # Attempt to parse using ast.literal_eval
            return ast.literal_eval(seq_str)
        except Exception as e:
            logging.error(f"Failed to parse sequence: {seq_str}. Error: {e}")
            return []

def generate_eventid_mapping(sequences_file, output_mapping_path):
    """Generate EventId to index mapping from sequences."""
    try:
        sequences_df = pd.read_csv(sequences_file)
        event_sequences = sequences_df['EventSequence'].tolist()
        logging.info(f"Loaded {len(event_sequences)} sequences from {sequences_file}")
    except Exception as e:
        logging.error(f"Error loading sequences: {e}")
        raise

    unique_event_ids = set()

    for seq_str in event_sequences:
        seq = parse_sequence(seq_str)
        unique_event_ids.update(seq)

    logging.info(f"Extracted {len(unique_event_ids)} unique Event IDs")

    # Assign a unique index to each Event ID, starting from 1
    # Reserve 0 for OOV (Out-Of-Vocabulary)
    sorted_event_ids = sorted(unique_event_ids)
    eventid_to_idx = {str(event_id): idx for idx, event_id in enumerate(sorted_event_ids, start=1)}
    eventid_to_idx['OOV'] = 0  # Reserve 0 for unknown events

    # Check for duplicate index assignments
    index_to_eventids = defaultdict(list)
    for event_id, idx in eventid_to_idx.items():
        index_to_eventids[idx].append(event_id)

    duplicate_indices = {idx: ids for idx, ids in index_to_eventids.items() if len(ids) > 1 and idx != 0}
    if duplicate_indices:
        logging.error(f"Duplicate index assignments found: {duplicate_indices}")
        raise ValueError("Duplicate index assignments detected in EventId mapping.")
    else:
        logging.info("No duplicate index assignments in EventId mapping.")

    # Save the mapping to JSON
    try:
        with open(output_mapping_path, 'w') as f:
            json.dump(eventid_to_idx, f, indent=4)
        logging.info(f"EventId to index mapping saved to {output_mapping_path}")
    except Exception as e:
        logging.error(f"Error saving mapping: {e}")
        raise

if __name__ == "__main__":
    sequences_file = 'demo_result/hdfs_sequence1.csv'  # Path to your sequences file
    output_mapping_path = 'demo_result/hdfs_log_templates.json'  # Path to save the new mapping
    generate_eventid_mapping(sequences_file, output_mapping_path)
