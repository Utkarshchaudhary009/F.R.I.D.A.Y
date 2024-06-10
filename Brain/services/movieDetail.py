import re
import requests
import os
from Brain.utilities.readEnv import readEnv

def extract_details(user_input):
    # Define regular expressions to match patterns related to movies/series, seasons, and episodes
    movie_pattern = re.compile(r'movie\s+(.*)', re.IGNORECASE)
    series_pattern = re.compile(r'series\s+(.*)', re.IGNORECASE)
    season_pattern = re.compile(r'season\s+(\d+)', re.IGNORECASE)
    episode_pattern = re.compile(r'episode\s+(\d+)', re.IGNORECASE)

    # Search for matches in the user input
    movie_match = re.search(movie_pattern, user_input)
    series_match = re.search(series_pattern, user_input)
    season_match = re.search(season_pattern, user_input)
    episode_match = re.search(episode_pattern, user_input)

    # Initialize variables to store extracted details
    details = {}

    # Extract movie or series title from user input
    if movie_match:
        details['title'] = movie_match.group(1).strip()
        details['type'] = 'movie'
    elif series_match:
        details['title'] = series_match.group(1).strip()
        details['type'] = 'series'
    else:
        # If neither movie nor series is specified, return None
        return {"response": None}

    # Extract season and episode numbers if available
    if season_match:
        details['season'] = int(season_match.group(1))
    if episode_match:
        details['episode'] = int(episode_match.group(1))

    # Return the extracted details
    return {"response": details}

def get_movie_details(details, api_key):
    # Construct the OMDB API URL based on the extracted details
    if details['type'] == 'movie':
        url = f"http://www.omdbapi.com/?t={details['title'].replace(' ','+')}&apikey={api_key}&plot=full"
    elif details['type'] == 'series':
        url = f"http://www.omdbapi.com/?t={details['title'].replace(' ','+')}&season={details.get('season', '')}&episode={details.get('episode', '')}&apikey={api_key}&plot=full"

    # Make the API request
    response = requests.get(url)

    # Process the response
    if response.status_code == 200:
        movie_data = response.json()
        if movie_data['Response'] == 'True':
            title = movie_data['Title']
            if 'Year' in movie_data:
                year = movie_data['Year']
                genre = movie_data['Genre']
                plot = movie_data['Plot']
                director = movie_data['Director']
                writer = movie_data['Writer']
                runtime = movie_data['Runtime']
                actors = movie_data['Actors']
                if 'Episode' in movie_data:
                    episode = movie_data['Episode']
                    season = movie_data['Season']
                    return {"response": f"{title} Season {season} Episode {episode} was Released in {year}, directed by {director}, written by {writer}. Genre: {genre}, Runtime: {runtime}, Actors: {actors}, Plot: {plot}"}
            else:
                season = movie_data['Season']
                episodes = movie_data['Episodes']
                episode_details = ''
                for ep in episodes:
                    episode_details += f"Episode {ep['Episode']} was Released on {ep['Released']} with title {ep['Title']}. "
                return {"response": f'{title} Season {season} has {len(episodes)} episodes. {episode_details}'}
            return {"response": f"{title} was Released in {year}, directed by {director}, written by {writer}. Genre: {genre}, Runtime: {runtime}, Actors: {actors}, Plot: {plot}"}
        else:
            return {"response": "Movie/series not found!"}
    else:
        return {"response": "Failed to fetch data. Check your connection or API key."}

def moviedetails(user_input):
    # Read API key from environment variable
    api_key = readEnv("OMBD")
    
    # Extract movie/series details from user input
    details = extract_details(user_input)

    # If details are extracted successfully, fetch movie details from OMDB API
    if details['response'] is not None:
        return get_movie_details(details['response'], api_key)
    else:
        # If no valid movie/series details are found, return an error message
        return {"response": "Please provide a valid query about a movie or series."}

if __name__=="__main__":
    # Example usage:
    user_input = "tell me about movie Inception"
    print(moviedetails(user_input))
    
    user_input = "watch series Game of Thrones season 1 episode 3"
    print(moviedetails(user_input))
