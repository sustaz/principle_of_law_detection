from docx import Document
import re
import json


def write_text_to_docx(text, file_path):
    """
    Write the given text to a .docx file.

    :param text: The text to write to the file.
    :param file_path: The path to the .docx file.
    """
    # Create a new Document
    doc = Document()

    # Add text to the document
    doc.add_paragraph(text)

    # Save the document to the specified file path
    doc.save(file_path)

import pandas as pd

def text_to_dataframe(text):
    # Split the text into paragraphs
    paragraphs = text.split("\n\n")

    data = []

    for para in paragraphs:
        if para.strip():  # Ignore any empty paragraphs
            # Split the paragraph into its number and content
            para_num, content = para.split(": ", 1)
            para_num = para_num.replace("Paragraph ", "").strip()

            # Determine the label and text
            if "\n- Reasoning:" in content:
                label, text = content.split("\n- Reasoning: ")
                label = label.strip()
                text = text.strip()
            else:
                label = content.strip()
                text = ""

            data.append([para_num, label, text])

    # Create the DataFrame
    df = pd.DataFrame(data, columns=["paragraph", "label", "text"])
    return df


def extract_paragraph_data(text):
    # Define the regex pattern to match each paragraph number and label
    #pattern = re.compile(r'Paragraph number: (\d+): (\w)')
    pattern = re.compile(r'Paragraph(?: number)?: (\d+): (\w)')

    # Find all matches in the text
    matches = pattern.findall(text)

    # Convert matches to a dataframe
    df = pd.DataFrame(matches, columns=['paragraph_number', 'label'])

    return df


def extract_paragraph_status(text):
  # Trova tutte le corrispondenze del tipo "Numero: N o Y"
  matches = re.findall(r'Paragraph (\d+): ([YN])', text)
  # Converte le corrispondenze in una lista di tuple
  results = [(int(num), status) for num, status in matches]
  return results


def concatenate_dataframes(data_tuples):
    # Initialize an empty list to store the dataframes
    dfs = []

    # Iterate over each tuple in the list
    for df, file_name in data_tuples:
        # Add a new column 'file_name' to the dataframe
        df['file_name'] = file_name
        # Append the dataframe to the list
        dfs.append(df)

    # Concatenate all dataframes in the list
    result_df = pd.concat(dfs, ignore_index=True)

    return result_df


def create_combined_dataframe(json_str, existing_df):
    # Load the JSON data
    data = json.loads(json_str)

    # Prepare a list to hold new rows
    new_rows = []

    # Iterate over the documents and annotations in the JSON data
    for document in data['documents']:
        file_name = document['document']
        for annotation in document['annotations']:
            text = annotation['text']
            label = annotation['type']
            number_paragraph = int(text.split()[0])  # Extract the paragraph number from the text

            # Append the new row to the list
            new_rows.append({
                'number_paragraph': number_paragraph,
                'label': label,
                'file_name': file_name
            })

    # Create a new DataFrame from the new rows
    new_df = pd.DataFrame(new_rows)

    # Combine the new DataFrame with the existing DataFrame
    combined_df = pd.concat([existing_df, new_df]).reset_index(drop=True)

    return combined_df

def merge_json_data(json_root, json_path):
    merged = {}

    for entry in json_path:
        entry = os.path.join(json_root, entry)
        entry = json.load(open(entry))
        task = entry['task']
        #annotator = entry['annotator']

        if task not in merged:
            merged[task] = {'task': task, 'documents': {}}

        for document in entry['documents']:
            doc_name = document['document']

            if doc_name not in merged[task]['documents']:
                merged[task]['documents'][doc_name] = {'document': doc_name, 'annotations': []}

            merged[task]['documents'][doc_name]['annotations'].extend(document['annotations'])

    # Convert back to the required format
    result = []
    for task in merged.values():
        documents = list(task['documents'].values())
        result.append({'task': task['task'], 'documents': documents})

    return result


def extract_paragraphs(text):
    # Regular expression to find pairs of number and answer (Y or N)
    pattern = r'(\d+): (Y|N)'
    matches = re.findall(pattern, text)

    # Convert matches to list of tuples
    #pairs = [(int(num), answer) for num, answer in matches]

    return pd.DataFrame(matches, columns=['paragraph_number', 'label'])