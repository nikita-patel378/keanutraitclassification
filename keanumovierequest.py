import requests
import pandas as pd
import config

# Base URL for TMDB API
BASE_URL = 'https://api.themoviedb.org/3'

# API endpoint for searching people
SEARCH_PERSON_ENDPOINT = f'{BASE_URL}/search/person'
MOVIE_CREDITS_ENDPOINT = f'{BASE_URL}/person'
MOVIE_DETAILS_ENDPOINT = f'{BASE_URL}/movie'

# Headers for the request
HEADERS = {
    'Authorization': f'Bearer {config.READ_ACCESS_TOKEN}',
    'Content-Type': 'application/json;charset=utf-8'
}


def get_person_id(name):
    """Fetch the person ID for a given name."""
    params = {
        'api_key': config.API_KEY,
        'query': name
    }
    response = requests.get(SEARCH_PERSON_ENDPOINT, headers=HEADERS, params=params)
    data = response.json()
    if data['results']:
        return data['results'][0]['id']
    return None


def get_movie_credits(person_id):
    """Fetch movie credits for a person by their ID."""
    url = f'{MOVIE_CREDITS_ENDPOINT}/{person_id}/movie_credits'
    params = {
        'api_key': config.API_KEY
    }
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()


def get_movie_details(movie_id):
    """Fetch movie details for a given movie ID."""
    url = f'{MOVIE_DETAILS_ENDPOINT}/{movie_id}'
    params = {
        'api_key': config.API_KEY,
        'language': 'en-US',
        'append_to_response': 'images'
    }
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()


def main():
    # Get Keanu Reeves' person ID
    person_id = get_person_id('Keanu Reeves')
    if not person_id:
        print("Keanu Reeves not found.")
        return
    # Get movie credits for Keanu Reeves
    movie_credits = get_movie_credits(person_id)
    if 'cast' not in movie_credits:
        print("No movie credits found.")
        return

    # Extract movie information
    movie_list = []
    for movie in movie_credits['cast']:
        movie_id = movie['id']
        movie_details = get_movie_details(movie_id)
        if 'title' in movie_details and 'overview' in movie_details and 'genres' in movie_details:
            title = movie_details['title']
            genres = [genre['name'] for genre in movie_details['genres']]
            plot_summary = movie_details['overview']
            poster_path = movie_details.get('poster_path')
            image_url = f"https://image.tmdb.org/t/p/original{poster_path}" if poster_path else None
            character = movie['character']
            tagline = movie_details.get('tagline', '')
            movie_list.append({
                'Title': title,
                'Genres': genres,
                'Plot Summary': plot_summary,
                'Character': character,
                'Tagline': tagline,
                'Image URL': image_url
            })
    # Create DataFrame
    df = pd.DataFrame(movie_list)
    df.to_csv('keanumovies.csv')
    print(df)


if __name__ == '__main__':
    main()
