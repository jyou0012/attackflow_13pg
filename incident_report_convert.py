from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Union
import docx2txt
import PyPDF2
import argparse

import pandas as pd

# Load the dataset
dataset_filepath = 'dataset.csv'

# Create an argument parser
parser = argparse.ArgumentParser(description='Process and match text content with a dataset.')

# Add an argument for the file path
parser.add_argument('file_path', type=str, help='The path to the text file to be processed and matched.')

# Parse the arguments
args = parser.parse_args()

# Get the file path from the parsed arguments
file_path = args.file_path

# Function to read the content of a file based on its extension
def read_file_content(filepath: str) -> str:
    if filepath.endswith('.txt'):
        with open(filepath, 'r') as file:
            return file.read()
    elif filepath.endswith('.docx'):
        return docx2txt.process(filepath)
    elif filepath.endswith('.pdf'):
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return ''.join([reader.getPage(i).extractText() for i in range(len(reader.pages))])
    else:
        raise ValueError("Unsupported file format. Supported formats are .txt, .docx, and .pdf")

# Read the content of the text file
text_content = read_file_content(file_path)
dataset = pd.read_csv(dataset_filepath)

def batch_tokenize_and_match(content: str, dataset: pd.DataFrame, threshold: float = 0.5, batch_size: int = 200) -> pd.DataFrame:
    """
    Tokenize the content and match it with the dataset based on cosine similarity in batches to avoid memory issues.

    Parameters:
    - content: The content to be matched.
    - dataset: The dataset DataFrame containing the reference data.
    - threshold: The cosine similarity threshold for considering a match.
    - batch_size: The number of sentences to process in each batch.

    Returns:
    - A DataFrame containing the matched results.
    """
    # Split the content into sentences
    sentences = content.split('.')
    
    # Create a DataFrame to store the final matched results
    final_results = pd.DataFrame(columns=['ID', 'Name', 'Sentence','Cosine Similarity'])
    
    # Process the sentences in batches to avoid memory issues
    for i in range(0, len(sentences), batch_size):
        batch_sentences = sentences[i: i + batch_size]
        
        # Create a TfidfVectorizer to tokenize the batch sentences and dataset
        vectorizer = TfidfVectorizer().fit_transform(batch_sentences + dataset['sentence'].tolist())
        vectors = vectorizer.toarray()

        # Compute cosine similarity between the batch sentences and dataset sentences
        cosine_sim = cosine_similarity(vectors[:len(batch_sentences)], vectors[len(batch_sentences):])
        
        # Find matches based on the cosine similarity threshold
        matches = np.where(cosine_sim >= threshold)
        
        # Prepare the matched results for the current batch
        batch_results = pd.DataFrame({            
            'ID': dataset['label_tec'].iloc[matches[1]].values,
            'Name': dataset['tec_name'].iloc[matches[1]].values,
            'Sentence': np.array(batch_sentences)[matches[0]],
            'Cosine Similarity': cosine_sim[matches]
        })
        
        # Append the batch results to the final results DataFrame
        final_results = pd.concat([final_results, batch_results], ignore_index=True)
    
    return final_results

# Test the optimized function with the txt content and dataset
#matched_results_txt_optimized = batch_tokenize_and_match(text_content, dataset)

# Display the matched results
#matched_results_txt_optimized

def efficient_tokenize_and_match(content: str, dataset: pd.DataFrame, threshold: float = 0.5, batch_size: int = 500) -> pd.DataFrame:
    """
    Efficiently tokenize the content and match it with the dataset based on cosine similarity in batches.

    Parameters:
    - content: The content to be matched.
    - dataset: The dataset DataFrame containing the reference data.
    - threshold: The cosine similarity threshold for considering a match.
    - batch_size: The number of sentences to process in each batch.

    Returns:
    - A DataFrame containing the matched results.
    """
    # Split the content into sentences
    sentences = content.split('.')
    
    # Create a DataFrame to store the final matched results
    final_results = pd.DataFrame(columns=['label_tec', 'tec_name','Sentence', 'Cosine Similarity'])
    
    # Process the sentences in batches to avoid memory issues
    for i in range(0, len(sentences), batch_size):
        batch_sentences = sentences[i: i + batch_size]
        
        # Create a TfidfVectorizer to tokenize the batch sentences and dataset
        vectorizer = TfidfVectorizer().fit(batch_sentences + dataset['sentence'].tolist())
        vectors = vectorizer.transform(batch_sentences + dataset['sentence'].tolist())

        # Compute cosine similarity between the batch sentences and dataset sentences
        cosine_sim = cosine_similarity(vectors[:len(batch_sentences)], vectors[len(batch_sentences):])
        
        # Find matches based on the cosine similarity threshold
        matches = np.where(cosine_sim >= threshold)
        
        # Prepare the matched results for the current batch
        batch_results = pd.DataFrame({            
            'ID': dataset['label_tec'].iloc[matches[1]].values,
            'Name': dataset['tec_name'].iloc[matches[1]].values,
            'Sentence': np.array(batch_sentences)[matches[0]],
            'Cosine Similarity': cosine_sim[matches]
        })
        
        # Append the batch results to the final results DataFrame
        final_results = pd.concat([final_results, batch_results], ignore_index=True)
    
    return final_results

# Test the efficient function with the txt content and dataset
matched_results_txt_efficient = efficient_tokenize_and_match(text_content, dataset)

# Display the matched results
matched_results_txt_efficient

# Testing with a lower threshold of 0.1
matched_results_txt_lower_threshold = efficient_tokenize_and_match(text_content, dataset, threshold=0.1)

# Display the matched results
matched_results_txt_lower_threshold

# Testing various thresholds from 0.15 to 0.4
thresholds = [0.2, 0.25, 0.3, 0.35, 0.4, 0.5]
matched_results_various_thresholds = {}

for threshold in thresholds:
    matches = efficient_tokenize_and_match(text_content, dataset, threshold=threshold)
    matched_results_various_thresholds[threshold] = len(matches)

# Display the number of matches for each threshold
matched_results_various_thresholds

# Get the matched results with a threshold of 0.25
final_matched_results = efficient_tokenize_and_match(text_content, dataset, threshold=0.25)

# Export the matched results to an .xlsx file
output_filepath = 'matched_results.xlsx'
final_matched_results.to_excel(output_filepath, index=False)

# Show the final matched results and provide the download link
final_matched_results, output_filepath



def get_best_match_per_sentence(content: str, dataset: pd.DataFrame, threshold: float = 0.252) -> pd.DataFrame:
    """
    Efficiently tokenize the content, match it with the dataset based on cosine similarity, and get the best match per sentence.

    Parameters:
    - content: The content to be matched.
    - dataset: The dataset DataFrame containing the reference data.
    - threshold: The cosine similarity threshold for considering a match.

    Returns:
    - A DataFrame containing the best matched results per sentence.
    """
    # Split the content into sentences
    sentences = content.split('.')
    
    # Create a DataFrame to store the final matched results
    final_results = pd.DataFrame(columns=['ID', 'Name','Sentence', 'Cosine Similarity'])
    
    # Create a TfidfVectorizer to tokenize the sentences and dataset
    vectorizer = TfidfVectorizer().fit(sentences + dataset['sentence'].tolist())
    vectors = vectorizer.transform(sentences + dataset['sentence'].tolist())

    # Compute cosine similarity between the sentences and dataset sentences
    cosine_sim = cosine_similarity(vectors[:len(sentences)], vectors[len(sentences):])
    
    for i in range(len(sentences)):
        # Get the index of the best match in the dataset
        best_match_index = np.argmax(cosine_sim[i])
        
        # Get the cosine similarity of the best match
        best_match_score = cosine_sim[i][best_match_index]
        
        if best_match_score >= threshold:
            # Prepare the best matched result for the current sentence
            best_match_result = pd.DataFrame({                
                'ID': [dataset['label_tec'].iloc[best_match_index]],
                'Name': [dataset['tec_name'].iloc[best_match_index]],
                'Sentence': [sentences[i]],
                'Cosine Similarity': [best_match_score]
            })
            
            # Append the best matched result to the final results DataFrame
            final_results = pd.concat([final_results, best_match_result], ignore_index=True)
    
    return final_results[['ID', 'Name', 'Sentence','Cosine Similarity']]  # Reordering the columns to match the sample result structure





def read_file_content(filepath: str) -> str:
    """
    Read the content of a file based on its extension.

    Parameters:
    - filepath: The path to the file.

    Returns:
    - The content of the file as a string.
    """
    if filepath.endswith('.txt'):
        with open(filepath, 'r') as file:
            return file.read()
    elif filepath.endswith('.docx'):
        return docx2txt.process(filepath)
    elif filepath.endswith('.pdf'):
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return ''.join([reader.getPage(i).extractText() for i in range(len(reader.pages))])
    else:
        raise ValueError("Unsupported file format. Supported formats are .txt, .docx, and .pdf")



# Example usage
if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process and match text content with a dataset.')
    
    # Add an argument for the file path
    parser.add_argument('file_path', type=str, help='The path to the text file to be processed and matched.')
    
    # Parse the arguments
    args = parser.parse_args()

    # Get the file path from the parsed arguments
    file_path = args.file_path

    # Read the content of the text file
    text_content = read_file_content(file_path)

    # Load the dataset (assuming the dataset file is in the same directory as the script)
    dataset_df = pd.read_csv('dataset.csv')

    # Tokenize and match the text content with the dataset
    matched_results = get_best_match_per_sentence(text_content, dataset_df, threshold=0.04)

    # Print the matched results
    print(matched_results)

    # Save the matched results to an .xlsx file
    matched_results.to_excel('matched_results.xlsx', index=False)