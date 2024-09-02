import pandas as pd
from spacy_llm.util import assemble
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path='dot.env')

# Set the OpenAI API key environment variable for spacy-llm
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

df = pd.read_csv('keanumoviescleaned.csv')

# Assemble the SpaCy pipeline from the config file
config_path = "spacy-llmtraits.cfg"
nlp = assemble(config_path)

doc = nlp("Nelson is a man devoted to his advertising career in San Francisco. One day, while taking a driving test "
          "at the DMV, he meets Sara. She is very different from the other women in his life. Nelson causes her to "
          "miss out on taking the test and later that day she tracks him down. One thing leads to another and Nelson "
          "ends up living with her through a November that will change his life forever.")

print(doc.cats)

print(doc.user_data['llm_io']['llm']['response'][0])

# Initialize a list to store results
results = []

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    plot_summary = row['Plot Summary']

    # Process the plot summary with the SpaCy pipeline
    doc = nlp(plot_summary)

    # Extract the classified traits
    traits = doc.user_data['llm_io']['llm']['response'][0]

    # Append the results to the list
    results.append({
        'Title': row['Title'],
        'Genres': row['Genres'],
        'Plot Summary': plot_summary,
        'Character': row['Character'],
        'Tagline': row['Tagline'],
        'Image URL': row['Image URL'],
        'Traits': traits
    })

# Convert the results list into a DataFrame
classified_df = pd.DataFrame(results)

classified_df.to_csv('keanutraitclassificationwithspacyllmrevised.csv')