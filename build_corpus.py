import pandas as pd
import re

def process_data():
    """
    Reads medical transcriptions and the FDA drug list (both brand names and
    active ingredients), extracts all unique words, and saves them to the vocabulary file.
    """
    print("Starting data processing...")
    all_unique_words = set()

    # --- 1. Process Medical Transcriptions ---
    try:
        print("Loading mtsamples.csv...")
        df_transcriptions = pd.read_csv('mtsamples.csv')
        df_transcriptions = df_transcriptions.dropna(subset=['transcription'])
        full_transcription_text = ' '.join(df_transcriptions['transcription'])
        
        transcription_words = re.findall(r'\b[a-zA-Z0-9-]+\b', full_transcription_text)
        unique_transcription_words = {word.lower() for word in transcription_words if len(word) > 2}
        all_unique_words.update(unique_transcription_words)
        print(f"Extracted {len(unique_transcription_words)} unique words from transcriptions.")

    except FileNotFoundError:
        print("Warning: 'mtsamples.csv' not found. Skipping.")
    except Exception as e:
        print(f"An error occurred with mtsamples.csv: {e}")

    # --- 2. Process FDA Drug Dataset ---
    try:
        print("\nLoading drugs.csv...")
        df_drugs = pd.read_csv('drugs.csv')
        
        # --- THIS IS THE UPGRADE ---
        # We process both brand_name and active_ingredients columns
        drug_terms = set()
        
        # Process brand names
        df_drugs_brands = df_drugs.dropna(subset=['brand_name'])
        for name in df_drugs_brands['brand_name']:
            words_in_name = re.findall(r'\b[a-zA-Z0-9-]+\b', str(name))
            for word in words_in_name:
                if len(word) > 2:
                    drug_terms.add(word.lower())

        # Process active ingredients
        df_drugs_ingredients = df_drugs.dropna(subset=['active_ingredients'])
        for ingredients in df_drugs_ingredients['active_ingredients']:
            words_in_ingredients = re.findall(r'\b[a-zA-Z0-9-]+\b', str(ingredients))
            for word in words_in_ingredients:
                 if len(word) > 2:
                    drug_terms.add(word.lower())

        all_unique_words.update(drug_terms)
        print(f"Extracted {len(drug_terms)} unique words from drug names and ingredients.")

    except FileNotFoundError:
        print("Warning: 'drugs.csv' not found. Skipping.")
    except Exception as e:
        print(f"An error occurred with drugs.csv: {e}")

    # --- 3. Save the Combined Vocabulary ---
    if all_unique_words:
        print(f"\nTotal unique words from all sources: {len(all_unique_words)}")
        with open('medical_vocabulary.txt', 'w') as f:
            for word in sorted(list(all_unique_words)):
                f.write(f"{word}\n")
        
        print("\nSUCCESS: 'medical_vocabulary.txt' has been updated with combined data.")
    else:
        print("\nNo data processed. 'medical_vocabulary.txt' was not updated.")

if __name__ == '__main__':
    process_data()