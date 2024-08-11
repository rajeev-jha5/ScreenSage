import os
import requests
import telebot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token and API key from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
MOVIE_API_KEY = os.getenv('MOVIE_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)

def get_movie_recommendations(movie_name):
    base_url = "https://api.themoviedb.org/3"
    
    # Search for the movie by name
    search_url = f"{base_url}/search/movie?api_key={MOVIE_API_KEY}&query={movie_name}"
    search_response = requests.get(search_url).json()
    
    if search_response['results']:
        movie_id = search_response['results'][0]['id']
        
        # Get recommendations based on the movie ID
        recommendations_url = f"{base_url}/movie/{movie_id}/recommendations?api_key={MOVIE_API_KEY}"
        recommendations_response = requests.get(recommendations_url).json()
        
        if recommendations_response['results']:
            recommended_movies = [movie['title'] for movie in recommendations_response['results'][:5]]
            return recommended_movies
        else:
            return ["Arre yaar, is movie ka to koi muqabla hi nahi hai!"]
    else:
        return ["Wah, wah! Aisi movie hai jo duniya mein hi nahi mil rahi."]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = ("🎬 *Namaste! Welcome to ScreenSage - The Movie Recommendation Bot!* 🍿\n\n"
                    "Bas aapko kisi movie ka naam likhna hai, aur main us jaise kuch movies suggest karunga. "
                    "Aap movie enjoy karo, ya nahi, aapki marzi! 😏")
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def recommend_movies(message):
    movie_name = message.text.strip()
    bot.reply_to(message, f"Arre wah, *{movie_name}*? Chalo, dhoondhne ki koshish karta hoon... 🕵️‍♂️", parse_mode='Markdown')
    
    recommendations = get_movie_recommendations(movie_name)
    
    if recommendations[0].startswith("Wah") or recommendations[0].startswith("Arre"):
        response = recommendations[0]
    else:
        response = (f"Lo, yeh rahe kuch movies jo *{movie_name}* jaise lagte hain:\n\n" +
                    "\n".join(f"🎥 {movie}" for movie in recommendations) +
                    "\n\nDekh lo, agar man kare. Warna mat dekho, aapki marzi! 😜")
    
    bot.reply_to(message, response, parse_mode='Markdown')

bot.infinity_polling()