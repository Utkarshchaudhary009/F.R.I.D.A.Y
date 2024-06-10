
import re

def extract_platform_and_search(command):
    # Define a regex pattern to match both formats
    pattern = r"(?:search|find|look up) (.*?) (?:on|in) (.*)|(?:on|in) (.*?) (?:search|find|look up) (.*)"
    
    # Use re.search to find matches
    match = re.search(pattern, command, re.IGNORECASE)
    
    if match:
        # Extract search term and platform from the correct groups
        search_term = match.group(1) if match.group(1) else match.group(4)
        platform = match.group(2) if match.group(2) else match.group(3)
        return {"platform": platform, "search_term": search_term.replace("for","").replace(" ","%20")}
    else:
        # print(command)
        return {"platform": "Not Found", "search_term": "None"}

web_map = {
    "youtube": "https://www.youtube.com/results?search_query=",
    "google": "https://www.google.com/search?q=",
    "bing": "https://www.bing.com/search?q=",
    "yahoo": "https://search.yahoo.com/search?p=",
    "duckduckgo": "https://duckduckgo.com/?q=",
    "amazon": "https://www.amazon.com/s?k=",
    "ebay": "https://www.ebay.com/sch/i.html?_nkw=",
    "wikipedia": "https://en.wikipedia.org/wiki/",
    "twitter": "https://twitter.com/search?q=",
    "facebook": "https://www.facebook.com/search/top?q=",
    "reddit": "https://www.reddit.com/search/?q=",
    "linkedin": "https://www.linkedin.com/search/results/all/?keywords=",
    "instagram": "https://www.instagram.com/explore/tags/",
    "pinterest": "https://www.pinterest.com/search/pins/?q=",
    "tumblr": "https://www.tumblr.com/search/",
    "quora": "https://www.quora.com/search?q=",
    "yelp": "https://www.yelp.com/search?find_desc=",
    "tripadvisor": "https://www.tripadvisor.com/Search?q=",
    "imdb": "https://www.imdb.com/find?q=",
    "rottentomatoes": "https://www.rottentomatoes.com/search?search=",
    "soundcloud": "https://soundcloud.com/search?q=",
    "spotify": "https://open.spotify.com/search/",
    "apple_music": "https://music.apple.com/us/search?term=",
    "goodreads": "https://www.goodreads.com/search?q=",
    "medium": "https://medium.com/search?q=",
    "stack_overflow": "https://stackoverflow.com/search?q=",
    "github": "https://github.com/search?q=",
    "bitbucket": "https://bitbucket.org/repo/all?name=",
    "gitlab": "https://gitlab.com/search?search=",
    "npm": "https://www.npmjs.com/search?q=",
    "news": "https://news.google.com/search?q=",
    "bbc": "https://www.bbc.co.uk/search?q=",
    "cnn": "https://www.cnn.com/search?q=",
    "nytimes": "https://www.nytimes.com/search?query=",
    "guardian": "https://www.theguardian.com/uk/",
    "forbes": "https://www.forbes.com/search/?q=",
    "bloomberg": "https://www.bloomberg.com/search?query=",
    "weather": "https://weather.com/weather/today/l/"
}
from web import website
def search_web(command):
    response_dict = extract_platform_and_search(command)
    platform, query = response_dict.get("platform", ""), response_dict.get("search_term", "")
    # print(f"platform:{platform}, query={query}")
    
    if platform in web_map:
        search_query = f"{web_map[platform]}{query}"
        print(search_query)
        # Uncomment the line below to open the search query in a web browser
        website(search_query)  
    else:
        print(f"Platform {platform} is not supported")

# Test caseshttps://www.theguardian.com/uk/sport
NLPPattern = [
              "search for best hotels in Paris on tripadvisor",
              "search for action movies on imdb",
#               "search for movie reviews on rottentomatoes",
# #               "search for relaxing music on soundcloud",
#               "search for workout playlists on youtube",
]
if __name__=="__main__":
    for command in NLPPattern:
        result = search_web(command)
