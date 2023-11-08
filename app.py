import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPEN"),)
app = Flask(__name__)

# Crea una lista para almacenar el historial de conversaciones.
conversations = []
# You are a useful psychologist in a conversation. The answer should not be long.Be kind and empathetic
# Mensaje de sistema que establece la personalidad del bot.
bot_personality = {"role": "system", "content": "Comportate como un asistente cristiano cada vez que te hable dame un verso biblico relacionado a mi pregunta"}
conversations.append(bot_personality)

# def playSound(file_path):
#     os.system(f"start {file_path}")

@app.route('/')
def principal():
    return render_template('recorder.html')

@app.route("/audio", methods=["POST"])
def audio():
    audio = request.files.get("audio")
    audio.save("audio.mp3")
    audio_file = open("audio.mp3", "rb")
    transcribed = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    # Agregar el mensaje del usuario actual al historial.
    user_message = {"role": "user", "content": transcribed.text}
    conversations.append(user_message)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversations  # Utiliza todo el historial como contexto.
    )
    result = ""
    for choice in response.choices:
        result += choice.message.content

    # Agregar la respuesta del bot al historial.
    bot_message = {"role": "assistant", "content": result}
    conversations.append(bot_message)

    # tts = gTTS(result, lang='es', tld='com.mx')
    # tts.save("response.mp3")
    # playSound("response.mp3")

    return {"result": "ok", "text": result}
