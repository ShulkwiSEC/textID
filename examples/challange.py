import os
import random
import shutil
import nltk
from nltk.corpus import gutenberg

# Setup
nltk.download('gutenberg', quiet=True)
DATA_DIR = os.path.join('..', 'data')

if os.path.exists(DATA_DIR):
    shutil.rmtree(DATA_DIR)
os.makedirs(DATA_DIR)

all_fileids = gutenberg.fileids()
real_author_pool = list(set([f.split('-')[0] for f in all_fileids]))
# Selecting 10 random authors
selected_authors = random.sample(real_author_pool, 10)

# This will store text that is NOT saved to disk
secret_test_paragraphs = {name: [] for name in selected_authors}

print(f"--- Generating Data for {len(selected_authors)} Authors ---")

for author_name in selected_authors:
    author_path = os.path.join(DATA_DIR, author_name)
    os.makedirs(author_path)
    
    works = [f for f in all_fileids if f.startswith(author_name)]
    
    for i, fileid in enumerate(works[:8], 1):
        raw_text = gutenberg.raw(fileid)
        lines = raw_text.splitlines()[50:] # Skip headers
        
        # Split the text: 80% for files, 20% for the secret test
        split_point = int(len(lines) * 0.8)
        training_lines = lines[:split_point]
        test_lines = lines[split_point:]
        
        # Save the training part to the folder
        file_name = f"{i}.md"
        file_path = os.path.join(author_path, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(training_lines))
        
        # Store paragraphs from the test part for later
        test_content = "\n".join(test_lines)
        paras = [p.strip() for p in test_content.split('\n\n') if len(p.strip()) > 200]
        secret_test_paragraphs[author_name].extend(paras)
        
        print(f"Created: {file_path} (Training data only)")

# 3. Select the "Unique" Paragraph
# Pick an author that actually has test paragraphs available
target_author = random.choice([a for a in selected_authors if secret_test_paragraphs[a]])
test_paragraph = random.choice(secret_test_paragraphs[target_author])

print("\n" + "="*60)
print(f"TARGET AUTHOR TO GUESS: {target_author}")
print("Note: This paragraph DOES NOT exist in the saved .md files.")
print("="*60)
print("UNIQUE TEST PARAGRAPH:")
print("-" * 60)
print(test_paragraph)
print("-" * 60)