# import run_with_ngrok from flask_ngrok to run the app using ngrok
#from flask_ngrok import run_with_ngrok

from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse

#from wabot import ask, append_interaction_to_chat_log
import requests

from baybot import ask_chef, ask_friend, ask_qna, image_generator, translate, append_interaction_to_chat_log

app = Flask(__name__) #app name
#run_with_ngrok(app)

# if for some reason your conversation with the chef gets weird, change the secret key 
app.config['SECRET_KEY'] = 'top-important!'

help_txt = """Hi, 
Please following instruction in the below:
'1:free-text..' to chat with Chef
'2:free-text..' to chat with friend
'3:free-text..' to chat with QNA
'i:free-text..' to get generate image from Dall-E
'quote:' to get quote of the day
't:id:free-text..' to translate

BayBot Powered by OpenAI
"""

@app.route("/")
def hello():
  return "Hello Friends! . Thank you! for open this botapp."

@app.route('/bot', methods=['POST'])
def bot():
  incoming_msg = request.values.get('Body', '').lower()
  chat_log = session.get('chat_log')
  resp = MessagingResponse()
  msg = resp.message()
  responded = False
  if incoming_msg.startswith("quote:") == True:
    # return a quote
    r = requests.get('https://api.quotable.io/random')
    if r.status_code == 200:
        data = r.json()
        quote = f'{data["content"]} ({data["author"]})'
    else:
        quote = 'I could not retrieve a quote at this time, sorry.'
    msg.body(translate(quote))
    responded = True

  if incoming_msg.startswith("t:") == True:
    inc_msg = incoming_msg.replace('t:', '')
    lang = inc_msg[:2]
    inc_msg = inc_msg.replace(lang+':', '')
    trans = translate(inc_msg,lang)
    msg.body(str(trans))
    responded = True

  if incoming_msg.startswith("i:") == True:
    # return a cat pic
    inc_msg = incoming_msg.replace('i:', '')
    image = image_generator(inc_msg)
    msg.media(str(image))
    responded = True

  if incoming_msg.startswith("1:") == True:
    start_sequence = "\nChef:"
    restart_sequence = "\nPerson:"
    session_prompt = " YOUR CHEF'S STORY HERE "

    inc_msg = str(incoming_msg.replace('1:', ''))
    answer = ask_chef(start_sequence,restart_sequence,inc_msg, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(start_sequence,restart_sequence,session_prompt,inc_msg, answer,chat_log)
    msg.body(answer)
    responded = True

  if incoming_msg.startswith("2:") == True:
    start_sequence = "\nFriend:"
    restart_sequence = "\n\nYou: "
    session_prompt = "You: What have you been up to?\nFriend: Watching old movies.\nYou: Did you watch anything interesting?\nFriend: "

    inc_msg = str(incoming_msg.replace('2:', ''))
    answer = ask_friend(start_sequence,restart_sequence,inc_msg, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(start_sequence,restart_sequence,session_prompt,inc_msg, answer,chat_log)
    msg.body(answer)
    responded = True

  if incoming_msg.startswith("3:") == True:
    start_sequence = "\nA:"
    restart_sequence = "\nQ: "
    session_prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ:",

    inc_msg = str(incoming_msg.replace('3:', ''))
    answer = ask_qna(start_sequence,restart_sequence,inc_msg, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(start_sequence,restart_sequence,session_prompt,inc_msg, answer,chat_log)
    msg.body(answer)
    responded = True
  
  if not responded:
    msg.body(help_txt)   
  return str(resp)

if __name__ == "__main__":
  app.run()