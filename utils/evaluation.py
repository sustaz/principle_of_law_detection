from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import pandas as pd

def compute_total_metrics(ground_truth_df, results_df):
    res_df = results_df.copy()
    gt_df = ground_truth_df.copy()

    gt_df['paragraph_number'] = gt_df['paragraph_number'].astype(str)
    res_df['paragraph_number'] = res_df['paragraph_number'].astype(str)

    # Mappare le etichette Y e N a JPOL e non-JPOL
    res_df['label'] = res_df['label'].map({'Y': 'JPOL', 'N': 'not_JPOL'})

    # Unire i due DataFrame sui campi paragraph_number e file_name
    merged_df = pd.merge(res_df, gt_df, on=['paragraph_number', 'file_name'], how='outer')

    # Creare le etichette binarie per il calcolo delle metriche
    merged_df['ground_truth_binary'] = merged_df['ground_truth'].apply(lambda x: 1 if x == 'JPOL' else 0)
    merged_df['predicted_binary'] = merged_df['label'].apply(lambda x: 1 if x == 'JPOL' else 0)

    # Calcolare precision, recall e f1-score
    precision = precision_score(merged_df['ground_truth_binary'], merged_df['predicted_binary'], zero_division=0)
    recall = recall_score(merged_df['ground_truth_binary'], merged_df['predicted_binary'], zero_division=0)
    f1 = f1_score(merged_df['ground_truth_binary'], merged_df['predicted_binary'], zero_division=0)

    return precision, recall, f1


def compute_metrics(ground_truth_df, results_df):

    res_df = results_df.copy()
    gt_df = ground_truth_df.copy()

    gt_df['paragraph_number'] = gt_df['paragraph_number'].astype(str)
    res_df['paragraph_number'] = res_df['paragraph_number'].astype(str)

    # Mappare le etichette Y e N a JPOL e non-JPOL
    res_df['label'] = res_df['label'].map({'Y': 'JPOL', 'N': 'not_JPOL'})

    # Unire i due DataFrame sui campi paragraph_number e file_name
    merged_df = pd.merge(res_df, gt_df, on=['paragraph_number', 'file_name'], how='outer')

    # Creare le etichette binarie per il calcolo delle metriche
    merged_df['ground_truth_binary'] = merged_df['ground_truth'].apply(lambda x: 1 if x == 'JPOL' else 0)
    merged_df['predicted_binary'] = merged_df['label'].apply(lambda x: 1 if x == 'JPOL' else 0)

    # Funzione per calcolare le metriche per ogni gruppo
    def calculate_metrics(group):
        precision = precision_score(group['ground_truth_binary'], group['predicted_binary'], zero_division=0)
        recall = recall_score(group['ground_truth_binary'], group['predicted_binary'], zero_division=0)
        f1 = f1_score(group['ground_truth_binary'], group['predicted_binary'], zero_division=0)
        return pd.Series({'precision': precision, 'recall': recall, 'f1': f1})

    # Calcolare le metriche per ogni valore di file_name
    metrics_by_filename = merged_df.groupby('file_name').apply(calculate_metrics).reset_index()

    return metrics_by_filename, merged_df