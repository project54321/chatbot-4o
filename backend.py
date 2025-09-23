from flask import Flask, request, render_template, jsonify
import os
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ["GITHUB_TOKEN"]
)

def chat_with_gpt4o(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-4o", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,  
        max_tokens=500 
    )
    return response.choices[0].message.content.strip()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gpt/", methods=["GET", "POST"])
def gpt():
    return render_template("gpt.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_input = data.get("message", "")
    response = chat_with_gpt4o(user_input)
    return jsonify({"response": response})

@app.route("/aboutme/")
def aboutme():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
