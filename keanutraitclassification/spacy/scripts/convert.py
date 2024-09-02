from pathlib import Path
import typer
import pandas as pd
from spacy.tokens import DocBin
import spacy

# Define the list of traits as categories
CATEGORIES = ["BADASS", "UNAPOLOGETIC", "ROMANTIC", "RELENTLESS", "ADVENTUROUS", "FREE-SPIRITED"]


def read_csv(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        # Split the traits string into a list of traits
        labels = {category: 0 for category in CATEGORIES}
        trait_list = row['Traits'].split(',')  # Assuming 'Traits' is the column with comma-separated traits
        for trait in trait_list:
            trait = trait.strip().upper()  # Clean and standardize the trait string
            if trait in labels:
                labels[trait] = 1
        yield {
            "text": row['Plot Summary'],  # Assuming 'Plot Summary' is the correct column name
            "labels": labels
        }


def convert_record(nlp, record, categories):
    """Convert a record from the CSV into a spaCy Doc object."""
    doc = nlp.make_doc(record["text"])
    # Initialize all categories with a value of 0
    doc.cats = {category: 0 for category in categories}
    # Set true labels to 1
    for label, value in record["labels"].items():
        doc.cats[label] = value
    return doc


def main(
        lang: str = "en",
        data_dir: Path = Path(__file__).parent.parent / "data",
        corpus_dir: Path = Path(__file__).parent.parent / "corpus"
):
    """Convert the CSV files to spaCy's binary format."""
    nlp = spacy.blank(lang)

    # Process each CSV file (train and test)
    for csv_file in ["traindata.csv", "testdata.csv"]:
        records = read_csv(data_dir / csv_file)
        docs = [convert_record(nlp, record, CATEGORIES) for record in records]
        out_file = corpus_dir / csv_file.replace(".csv", ".spacy")
        db = DocBin(docs=docs)
        db.to_disk(out_file)


if __name__ == "__main__":
    typer.run(main)
