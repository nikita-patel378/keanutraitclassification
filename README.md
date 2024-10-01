# Text Classification for Keanu Reeves' Character Traits Using spaCy

This repository contains code to classify Keanu Reeves' characters based on the plot summaries of his movies. The classification is performed using two approaches: one with **spaCy's LLM** model and another using standard text classification techniques without an LLM. The goal is to classify each movie character into one or more of six traits: **Badass**, **Adventurous**, **Unapologetic**, **Romantic**, **Free-Spirited**, and **Relentless**.

## Project Overview

This project demonstrates how to:
- Perform text classification using **spaCy**.
- Use both **spaCy LLM** and standard text classification techniques.
- Clean data by filtering out irrelevant movie plot summaries (e.g., documentaries or movies where Keanu Reeves' character is not explicitly mentioned).

### Traits Used for Classification:
- **Badass**
- **Adventurous**
- **Unapologetic**
- **Romantic**
- **Free-Spirited**
- **Relentless**

### Data Source
The plot summaries for Keanu Reeves' movies from TMDB API were used as the primary data source for text classification. Data cleaning was performed to remove irrelevant summaries and documentaries.

