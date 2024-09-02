# now we're going to try text classification without using spaCy llm
import spacy
import pandas as pd

df = pd.read_csv('keanumoviescleaned.csv')


# this function normalizes the score.
# 1 will be used to classify that this is a trait and 0 is not having that trait
def min_max_normalize(scores):
    min_score = min(scores.values())
    max_score = max(scores.values())
    if max_score - min_score == 0:
        return {label: 0 for label in scores}  # Avoid division by zero
    return {label: (score - min_score) / (max_score - min_score) for label, score in scores.items()}


# Load the trained model (use 'model-best' or 'model-last')
nlp = spacy.load("trained/model-last")

doc = nlp("Nelson is a man devoted to his advertising career in San Francisco. One day, while taking a driving test at "
          "the DMV, he meets Sara. She is very different from the other women in his life. Nelson causes her to miss "
          "out on taking the test and later that day she tracks him down. One thing leads to another and Nelson ends up"
          "living with her through a November that will change his life forever.")

# Normalize the scores
normalized_cats = min_max_normalize(doc.cats)

# Print normalized scores
print("Normalized Scores:", normalized_cats)

relevant_labels = {label: score for label, score in normalized_cats.items() if score == 1}

print("Relevant Labels:", relevant_labels)

# now let's use this process to classify the traits for the rest of the movies
# Initialize an empty list to store the results
results = []

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    plot_summary = row['Plot Summary']

    # Process the plot summary with the SpaCy pipeline
    doc = nlp(plot_summary)

    # Normalize the scores
    normalized_cats = min_max_normalize(doc.cats)

    # Extract relevant labels (traits)
    relevant_labels = [label for label, score in normalized_cats.items() if score == 1]

    # Append the results to the list
    results.append({
        'Title': row['Title'],
        'Genres': row['Genres'],
        'Plot Summary': plot_summary,
        'Character': row['Character'],
        'Tagline': row['Tagline'],
        'Image URL': row['Image URL'],
        'Traits': ', '.join(relevant_labels)  # Convert the list of traits to a comma-separated string
    })

# Convert the results list into a DataFrame
classified_df = pd.DataFrame(results)

classified_df.to_csv('keanutraitclassificationwithoutspacyllm.csv')
