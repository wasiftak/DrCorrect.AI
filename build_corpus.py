import pandas as pd
import re

def process_data():
    """
    Reads the raw mtsamples.csv, extracts and cleans all unique words
    from the transcriptions, and saves them to a new file.
    """
    print("Starting data processing...")
    try:
        # Read the large CSV file
        df = pd.read_csv('mtsamples.csv')
        print("mtsamples.csv loaded successfully.")

        # Drop rows with missing transcriptions to avoid errors
        df = df.dropna(subset=['transcription'])

        # Combine all transcriptions into a single large text block
        full_text = ' '.join(df['transcription'])
        print(f"Combined {len(df)} transcriptions into one text block.")

        # Use regex to find all words. This will find words with letters,
        # numbers (like in medications), and hyphens.
        words = re.findall(r'\b[a-zA-Z0-9-]+\b', full_text)

        # Create a set of unique words (all lowercase) that are 3 characters or longer
        unique_words = {word.lower() for word in words if len(word) > 2}
        print(f"Extracted {len(unique_words)} unique words.")

        # Save the cleaned, unique words to a new file, one word per line
        with open('medical_vocabulary.txt', 'w') as f:
            for word in sorted(list(unique_words)): # Sort them for consistency
                f.write(f"{word}\n")
        
        print("\nSUCCESS: 'medical_vocabulary.txt' has been created.")

    except FileNotFoundError:
        print("\nERROR: 'mtsamples.csv' not found. Please download it and place it in the project folder.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    process_data()