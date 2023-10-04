import openai
import config
openai.api_key = config.OPENAI_API_KEY



def poem(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt= prompt,
        temperature=0.7,
        max_tokens=3500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if 'choices' in response:
        answer= response['choices'][0]['text']
    return answer


