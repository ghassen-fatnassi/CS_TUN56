import sys
import os
import re
import json
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import numpy as np
import Spell

input_dir  = ''  # Directory containing the raw logs
output_dir = 'demo_result/'     # Directory where outputs will be saved
log_file   = "HDFS.log/HDFS.log"            # Name of your log file

log_structured_file = os.path.join(output_dir, log_file + "_structured.csv")
log_templates_file = os.path.join(output_dir, log_file + "_templates.csv")
log_sequence_file = os.path.join(output_dir, "hdfs_sequence.csv")

def mapping():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Read the structured templates
    log_temp = pd.read_csv(log_templates_file)
    # Sort templates by occurrences in descending order
    log_temp.sort_values(by=["Occurrences"], ascending=False, inplace=True)
    # Create a mapping from EventId to index
    log_temp_dict = {event: idx+1 for idx, event in enumerate(list(log_temp["EventId"]))}
    print("EventId to Index Mapping:")
    print(log_temp_dict)
    # Save the mapping to a JSON file for future use
    with open(os.path.join(output_dir, "hdfs_log_templates.json"), "w") as f:
        json.dump(log_temp_dict, f)

def parser(input_dir, output_dir, log_file, log_format, type='spell'):
    if type == 'spell':
        # Spell parser settings (if you choose to use Spell)
        tau = 0.5
        regex = [
            r"(/[-\w]+)+",         # Replace file path with *
            r"(?<=blk_)[-\d]+"     # Replace block_id with *
        ]
        parser = Spell.LogParser(
            indir=input_dir,
            outdir=output_dir,
            log_format=log_format,
            tau=tau,
            rex=regex,
            keep_para=False
        )
        parser.parse(log_file)
   

def hdfs_sampling(log_file):
    print("Loading structured log file:", log_file)
    df = pd.read_csv(
        log_file,
        engine='c',
        na_filter=False,
        memory_map=True,
        dtype={'Date': object, "Time": object}
    )

    # Load the EventId to index mapping
    with open(os.path.join(output_dir, "hdfs_log_templates.json"), "r") as f:
        event_num = json.load(f)
    # Map EventIds to numerical indices
    df["EventId"] = df["EventId"].apply(lambda x: event_num.get(x, -1))

    # Group EventIds by BlockId (sessions)
    data_dict = defaultdict(list)  # Preserves insertion order
    for idx, row in tqdm(df.iterrows(), total=df.shape[0]):
        blkId_list = re.findall(r'(blk_-?\d+)', row['Content'])
        blkId_set = set(blkId_list)
        for blk_Id in blkId_set:
            data_dict[blk_Id].append(row["EventId"])

    # Convert the dictionary to a DataFrame and save it
    data_df = pd.DataFrame(list(data_dict.items()), columns=['BlockId', 'EventSequence'])
    data_df.to_csv(log_sequence_file, index=None)
    print("Log sequences saved to:", log_sequence_file)

def df_to_file(df, file_name):
    with open(file_name, 'w') as f:
        for row in df:
            f.write(' '.join([str(ele) for ele in eval(row)]))
            f.write('\n')

if __name__ == "__main__":
    # Parse the HDFS log
    log_format = '<Date> <Time> <Pid> <Level> <Component>: <Content>'  # HDFS log format
    parser(input_dir, output_dir, log_file, log_format, 'spell')
    # Create the EventId to index mapping
    mapping()
    # Generate sequences from the structured logs
    hdfs_sampling(log_structured_file)