import numpy as np
from collections import Counter
import pickle
import json
from sklearn.linear_model import LogisticRegression
from scipy.sparse import csr_matrix


def convertToSparseMatrix(features_idx, features_dict):
    """
    Convert feature idx matrix into sparse matrix
    :param features_idx: [list] original feature idx matrix
    :param features_dict: [dict] train_ngram_dict (for determine the dimension)
    :return: [dict] sparse matrix tuple
    """
    location = []
    for idx, line in enumerate(features_idx):
        for token in line:
            location.append([idx, token])

    row = [i[0] for i in location]
    col = [i[1] for i in location]
    elements = [1] * len(location)
    dim = [len(features_idx), len(features_dict) + 1]
    sparse_matrix = csr_matrix((elements, (row, col)), shape=(len(features_idx), len(features_dict)))

    results = {
        'idx': location,
        'sparse_matrix': sparse_matrix,
        'elements': elements,
        'dim': dim
    }
    return results


def tokenExtraction(window_size_list, data, mode):
    """
    Given data, extract the corresponding feature
    :param window_size_list: [list] define the window size of the n-grams
    :param data: [list] input data needs to contain the 'text' field
    :param mode: define how to extract features from the tweet
    :return: [list] extracted n-gram features
    """
    ngram_all = []
    for line in data:
        if 'text' not in line:
            print(f"Skipping entry without 'text' field: {line}")
            continue
        
        curr_ngram = []
        line_text = line['text'].split(" ")

        # Ensure <TARGET> exists in the text for feature extraction
        try:
            target_index = [idx for idx, token in enumerate(line_text) if token == "<TARGET>"][0]
        except IndexError:
            print(f"[ERROR] '<TARGET>' not found in text: {line_text}")
            ngram_all.append('<UNK>')
            continue

        # Extract n-grams based on window size and mode
        for window_size in window_size_list:
            start_index = max(0, target_index - window_size)
            end_index = min(target_index + window_size, len(line_text))
            if mode == "TARGET_two_sides":
                extracted_token = " ".join(line_text[start_index:end_index])
                curr_ngram.append(extracted_token)
            elif mode == "TARGET_one_side":
                if line_text[0] != "<TARGET>":
                    extracted_token = " ".join(line_text[start_index:target_index+1])
                    curr_ngram.append(extracted_token)
                if line_text[-1] != "<TARGET>":
                    extracted_token = " ".join(line_text[target_index:end_index])
                    curr_ngram.append(extracted_token)
            elif mode == "all":
                for idx in range(len(line_text) - window_size + 1):
                    extracted_token = " ".join(line_text[idx:idx+window_size])
                    curr_ngram.append(extracted_token)

        ngram_all.append(curr_ngram if curr_ngram else '<UNK>')

    return ngram_all



def convertFeature2Idx(actual_features, train_feature_dict):
    """
    Convert actual features into idx
    :param actual_features: real features extracted from tweets
    :param train_feature_dict: train_ngram_dict
    :return:
    """
    features_idx = []
    for line in actual_features:
        curr_feature = [train_feature_dict.get(token, train_feature_dict['<UNK>']) for token in line]
        features_idx.append(curr_feature)
    return features_idx


def buildTrainDict(train_ngram_all, verbose=False, set_threshold=False, threshold=1):
    """
    Build up train n-gram dictionary
    :param train_ngram_all: all extracted n-gram features
    :param verbose:
    :param set_threshold: if we want to remove n-grams with low frequency
    :param threshold: define low frequency
    :return: [dict] train_ngram_dict
    """
    train_ngram_all_flatten = [j for i in train_ngram_all for j in i]
    train_ngram_counter = Counter(train_ngram_all_flatten)
    train_ngram_counter = sorted(train_ngram_counter.items(), key=lambda x: x[1], reverse=True)
    
    if verbose:
        print("[I] total n-gram", len(train_ngram_all_flatten), "unique n-gram", len(set(train_ngram_all_flatten)))
        print("[I] the most frequent tokens: ", train_ngram_counter[:20])

    if set_threshold:
        train_ngram_counter = [ngram for ngram in train_ngram_counter if ngram[1] >= threshold]

    train_ngram_dict = {ngram: idx for idx, (ngram, _) in enumerate(train_ngram_counter)}
    train_ngram_dict['<UNK>'] = len(train_ngram_dict)
    return train_ngram_counter, train_ngram_dict


def trainLRModel(train_all, train_label, window_size_list, ngram_extract_mode, flag, save_model=False):
    """
    Given cyber threat data with severe / non-severe label, train a LR classifier
    :param train_all: training data
    :param train_label: training label
    :param window_size_list: n-gram window size
    :param ngram_extract_mode:
    :param flag:
    :param save_model:
    :return:
    """
    train_ngram_all = tokenExtraction(window_size_list, train_all, mode=ngram_extract_mode)
    train_ngram_counter, train_ngram_dict = buildTrainDict(train_ngram_all, set_threshold=True, threshold=1)
    train_features_idx = convertFeature2Idx(train_ngram_all, train_ngram_dict)

    train_features_no_dup = [list(set(line)) for line in train_features_idx]
    train_idx_sparse = convertToSparseMatrix(train_features_no_dup, train_ngram_dict)

    lr = LogisticRegression(solver='lbfgs')
    lr.fit(train_idx_sparse['sparse_matrix'], train_label)

    print('[I] Logistic regression training completed.')
    print('[I] Training set dimension: ', train_idx_sparse['sparse_matrix'].shape)

    if save_model:
        with open(f'./trained_model/{flag}_lr_model.pkl', 'wb') as f:
            pickle.dump(lr, f)
        with open(f'./trained_model/{flag}_train_ngram_counter.json', 'w') as f:
            json.dump(train_ngram_counter, f)
        with open(f'./trained_model/{flag}_train_ngram_dict.json', 'w') as f:
            json.dump(train_ngram_dict, f)
        print("[I] All model files have been saved.")

    return lr, train_ngram_dict


def evalLRModel(window_size_list, val_all, train_ngram_dict, ngram_extract_mode, model):
    """
    Cyber threat existence classifier
    :param window_size_list: define feature extraction window size
    :param val_all: data to be tested
    :param ngram_extract_mode: how the features are extracted
    :return:
    """
    val_ngram_all = tokenExtraction(window_size_list, val_all, mode=ngram_extract_mode)
    val_features_idx = convertFeature2Idx(val_ngram_all, train_ngram_dict)
    val_features_no_dup = [list(set(line)) for line in val_features_idx]
    val_idx_sparse = convertToSparseMatrix(val_features_no_dup, train_ngram_dict)

    val_prob = model.predict_proba(val_idx_sparse['sparse_matrix'])
    return val_prob
