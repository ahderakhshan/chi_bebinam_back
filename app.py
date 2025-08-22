import os

from flask import Flask, jsonify, request
import random
import google.generativeai as genai
from flask_cors import CORS
from dotenv import load_dotenv

env_file = load_dotenv(dotenv_path=".env")
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
app = Flask(__name__)
CORS(app)


@app.route('/recommend_movie', methods=["POST"])
def movie_recommender():
    rand = int(random.uniform(1,100))
    print(rand)
    base_prompt = f"""As a movie recommendation system, your task is to suggest a suitable movie based on the user's answers to the questions. To do this, consider a pool of 100 movies and recommend the information of the movie with index {rand} that you select.
     These are questions and answer provide the movie title, genre, a short reason why it matches their profile, movie IMDB score, movie year of production, movie director and a summery of movie.\nyour answer must be in this form: Movie title: Movie title you recommend*Genre:Movie Genre you recommend*Description: a short description why you recommend this movie*Movie IMDB score: movie imdb score*Movie year of Production: movie year of production*Movie Director:movie director*Movie Summery:a summery of movie\nno other explanations at all. just this information for movie with index {rand} in your consideration items."""
    data = request.get_json()
    print(data)
    question_answers = data["prompt"]["question_answers"]
    print(question_answers)
    for question_answer in question_answers:
        question = question_answer["question"]
        answer = question_answer["answer"]
        base_prompt += f"\nQuestion: {question}, Answer: {answer}"
    response = model.generate_content(base_prompt)
    response_text = response.text
    response_value = response_text.split("*")
    result = {}
    for key_value in response_value:
        key, value = key_value.split(":")[0], key_value.split(":")[1]
        key = key.lower().strip()
        key = key.replace(" ", "_")
        result[key] = value
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False)