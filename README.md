# Principle of Law Detection

A machine learning-based system for automatically detecting and extracting Judicial Principles of Law (JPOLs) from legal judgments using Large Language Models (LLMs).

## Overview

This project is part of the **Poline project** and focuses on identifying portions of legal text that contain judicial interpretations of rules, principles, or their consequences within the legal system. The system uses GPT-4 and advanced NLP techniques to analyze legal documents and classify text segments as containing judicial principles of law or not.

### What is a JPOL?

A **Judicial Principle of Law (JPOL)** is a portion of text from legal judgments that contains:
- Judicial interpretation of legal rules
- Establishment of legal principles
- Explanation of legal consequences
- Judicial reasoning that forms precedent

## Key Features

- **LLM-Powered Detection**: Utilizes GPT-4 and GPT-4-turbo for intelligent text analysis
- **Multiple Detection Strategies**:
  - Full-text analysis of entire judgments
  - Chunk-based processing for large documents
  - RAG-based approach with semantic similarity matching
- **Text Preprocessing**: Automatic extraction of argumentative sections from legal documents
- **Evaluation Framework**: Comprehensive metrics including precision, recall, F1-score, and accuracy
- **Multi-Format Support**: Handles XML, TXT, PDF, and DOCX formats
- **Semantic Search**: FAISS-based similarity search for finding relevant legal passages

## Performance

The system achieves strong performance on legal text classification:
- **F1-Score**: ~80%
- **Accuracy**: 89%
- **Test Dataset**: 11 judgments with 294 classified paragraphs

## Installation

### Prerequisites

- Python 3.7+
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sustaz/principle_of_law_detection.git
cd principle_of_law_detection
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Project Structure

```
principle_of_law_detection/
├── src/
│   ├── gpt_utils.py           # OpenAI API utilities and embedding functions
│   ├── text_preprocessing.py  # Text extraction and preprocessing
│   ├── utils.py                # Data manipulation and file I/O utilities
│   └── evaluation.py           # Metrics calculation and evaluation
├── gpt_notebook.ipynb          # Main notebook with experiments and workflows
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Usage

### Basic Workflow

1. **Load and Preprocess Legal Documents**:
```python
from src.gpt_utils import load_file, load_from_folder
from src.text_preprocessing import extract_text_between_markers

# Load a single file
text = load_file('path/to/judgment.txt')

# Or load multiple files from a folder
files = load_from_folder('path/to/judgments/')
```

2. **Detect Principles of Law**:
```python
from src.gpt_utils import ask_gpt_2

# Analyze text with GPT-4
result = ask_gpt_2(
    prompt=judgment_text,
    system_prompt="You are a legal expert analyzing judicial principles...",
    KEY=api_key,
    model="gpt-4-turbo-preview"
)
```

3. **Evaluate Results**:
```python
from src.evaluation import compute_metrics

# Compare predictions against ground truth
metrics, merged_df = compute_metrics(ground_truth_df, results_df)
print(f"Precision: {metrics['precision']}, Recall: {metrics['recall']}, F1: {metrics['f1']}")
```

### Working with Embeddings

```python
from src.gpt_utils import build_embedding, cosine_similarity, find_most_similar_k

# Generate embeddings for semantic search
embedding = build_embedding(text, model="text-embedding-3-large")

# Find similar text chunks
similar_texts = find_most_similar_k(k=5, df=embeddings_df, text=query_text)
```

## Technologies Used

### LLMs and NLP
- **OpenAI GPT-4 / GPT-4-turbo**: Primary language model for text analysis
- **OpenAI text-embedding-3-large**: Text embeddings for semantic search
- **Sentence Transformers**: Alternative embedding model (all-MiniLM-L6-v2)
- **tiktoken**: Token counting for API optimization

### Vector Search and Similarity
- **FAISS (CPU)**: Fast similarity search and clustering
- **scikit-learn**: TF-IDF vectorization and metrics

### Document Processing
- **python-docx**: Microsoft Word document handling
- **PyPDF2**: PDF processing
- **pandas**: Data manipulation and analysis

## Data Format

### Input
- **Judgment Files**: XML or TXT format containing court rulings
- **Annotation Files**: JSON format with ground truth labels
```json
{
  "task": "JPOL_detection",
  "documents": [
    {
      "document": "judgment_001.txt",
      "annotations": [
        {"text": "1 ...", "type": "JPOL"},
        {"text": "2 ...", "type": "not_JPOL"}
      ]
    }
  ]
}
```

### Output
- **Excel Files**: Predictions with paragraph numbers, labels, and file names
- **DOCX Files**: Detailed responses with reasoning
- **DataFrames**: Structured data with JPOL classifications

## Contributing

This is a research project. For questions or contributions, please contact the maintainers.

## License

Please refer to the repository license for usage terms.

## Contact

For more information about the Poline project or this implementation, please refer to the repository issues or contact the project maintainers.

## Acknowledgments

This project uses OpenAI's GPT models for legal text analysis. The evaluation dataset consists of European Court of Justice rulings and Italian legal cases.
