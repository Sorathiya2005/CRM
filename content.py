import csv
import random
from urllib import request
import json
import datetime
import tweepy as tw

def get_quotes(quotes_file = "quotes.csv"):
    try:    #load quotes from a csv file 
        with open(quotes_file) as csvfile:
            quote = [{'Author': line[1],
            'quote': line[0]} for line in csv.reader(csvfile, delimiter='|')]
    
    except Exception as e: #load this default quote 
        quote = [{'Author' : "Thomas A. Edison",
        'quote' : "I have not failed. I've just found 10,000 ways that won't work."}]

    return random.choice(quote)

 
def get_article():
    try: # retrieve random Wikipedia article
        data = json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        return {'title': data['title'],
                'extract': data['extract'],
                'url': data['content_urls']['desktop']['page']}

    except Exception as e:
        print(e)


def get_twitter_trends(woeid = 2282863):
    try:
        api_key = " " #Enter a Your Api Key
        api_secret_key = "" # Enter a Your api Secret Key
        auth = tw.AppAuthHandler(api_key,api_secret_key)
        return tw.API(auth).get_place_trends(woeid)[0]["trends"]

    except Exception as e:
        print(e)

def get_weather_forecast(coords={"lat":21.77445,"lon":72.1525}):
    try:
        api_key = "00477cec11a6d15cf63edc19d2fe9dd2"
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["lon"]}&appid={api_key}&units=metric'
        data = json.load(request.urlopen(url))

        forecast = {"City" : data["city"]["name"],
        "Country" : data["city"]["country"],
        "periods" : list()}

        for period in data['list'][0:9]: # populate list with next 9 forecast periods 
            forecast['periods'].append({'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                                        'temp': round(period['main']['temp']),
                                        'description': period['weather'][0]['description'].title(),
                                         })
        
        return forecast
    
    except Exception as e:
        print(e)    


if __name__ == "__main__":
    
    # get_regular_news()

    #Code for Getting random quotes
    print("\nThe randomly generated motivational quote is: \n")
    quote = get_quotes()
    print(f'Random Quote is "{quote["quote"]}" - {quote["Author"]}')

    quote = get_quotes(quotes_file = None)
    print(f'Default Quote is "{quote["quote"]}" - {quote["Author"]}')

    #Code forweather forecast
    print('\nTesting weather forecast retrieval...')

    forecast = get_weather_forecast() # get forecast for default location
    if forecast:
        print(f'\nWeather forecast for {forecast["City"]}, {forecast["Country"]} is...')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    austin = {'lat': 23.033863,'lon': 72.585022} # coordinates for Texas State Capitol
    forecast = get_weather_forecast(coords = austin) # get Austin, TX forecast
    if forecast:
        print(f'\nWeather forecast for {forecast["City"]}, {forecast["Country"]} is...')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    invalid = {'lat': 1234.5678 ,'lon': 1234.5678} # invalid coordinates
    forecast = get_weather_forecast(coords = invalid) # get forecast for invalid location
    if forecast is None:
        print('Weather forecast for invalid coordinates returned None \n')

    #code for getting the trends from twitter
    trends = get_twitter_trends()
    if trends:
        print("Top 10 Twitter Trends of India right now are:")
        for trend in trends[0:10]:
            print(f'- {trend["name"]}: {trend["url"]}' )

    trends = get_twitter_trends(woeid=	1098081)
    if trends:
        print("\nTop 10 Twitter Trends of Australia right now are:")
        for trend in trends[0:10]:
            print(f'- {trend["name"]}: {trend["url"]}' )


    trends = get_twitter_trends(woeid = -1) # invalid WOEID
    if trends is None:
        print('\nTwitter trends for invalid WOEID returned None')

    #test get_wikipedia_article()
    print('\nTesting random Wikipedia article retrieval...')

    article = get_article()
    if article:
        print(f'\n{article["title"]}\n<{article["url"]}>\n{article["extract"]}')