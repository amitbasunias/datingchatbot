from flask import Flask, render_template, request, redirect, url_for
import openai
import write
import config
openai.api_key = config.OPENAI_API_KEY


def page_not_found(e):
    return render_template('404.html'), 404


app = Flask(__name__, static_url_path='/static')
app.register_error_handler(404, page_not_found)

# Initialize conversation history
conversation_history = []


@app.route('/', methods=["GET", "POST"])
def poem():
    if request.method == "POST":
        age = request.form.get('age')
        mood = request.form.get('mood')
        gender = request.form.get('gender')
        start = request.form.get('start')
        about = request.form.get('about')
        prompt = f"write a {start} for dating conversation for {gender} with following details:\n age: {age}\n mood: {mood} and following profile details: {about}"

        # Reset conversation history


        # Send user prompt to chatbot
        output = write.poem(prompt)
    return render_template('index.html', **locals())


@app.route('/chat', methods=["GET", "POST"])
def chat():
    response = request.args.get('output', default=None)
    if request.method == "POST":
        user_input = request.form.get('user')
        output = chatbot(user_input)
        return render_template('chatbot.html', output=output)
    return render_template('chatbot.html', response=response)


def chatbot(user_input):
    # Add user input to conversation history
    global conversation_history
    conversation_history.append({"role": "user", "content": user_input})

    # Retrieve conversation history for chatbot input
    messages = [
                   {"role": "system", "content": "Continue chat with dating app profile"}
               ] + conversation_history

    # Send messages to OpenAI chatbot
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Get chatbot reply
    reply = response.choices[0].message.content

    # Add chatbot reply to conversation history
    conversation_history.append({"role": "assistant", "content": reply})

    # Return conversation history
    return conversation_history


def entry(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="".format(prompt),
        temperature=0.7,
        max_tokens=3500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if 'choices' in response:
        answer= response['choices'][0]['text']
    return answer

if __name__ == '__main__':
    app.run()
