from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from groq import Groq

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Criar o cliente Groq
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Configurar o prompt do sistema
system_prompt = {
    "role": "system",
    "content": "Você sabe de tudo, deve responder as perguntas de forma objetiva, porém caso demande uma grande explicação não poupe palavras."
}

# Inicializar o histórico do chat
chat_history = [system_prompt]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    user_input = request.form['user_input']
    
    # Adicionar a entrada do usuário ao histórico do chat
    chat_history.append({"role": "user", "content": user_input})

    # Fazer a chamada para completar o chat
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=1000,
        temperature=1.2
    )

    # Obter a resposta do assistente
    response_content = response.choices[0].message.content

    # Adicionar a resposta ao histórico do chat
    chat_history.append({
        "role": "assistant",
        "content": response_content
    })

    return response_content

if __name__ == "__main__":
    app.run(debug=True)
