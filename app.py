from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
from groq import Groq

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Necessário para usar 'flash' para mensagens

# Criar o cliente Groq
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Configurar o prompt do sistema
system_prompt = {
    "role": "system",
    "content": "Você é um cardiologista, eu lhe darei informações como minha pressão sistólica e a pressão diastólica. Lhe darei minha idade, peso e altura. A partir desses dados me dê um diagnóstico com base em diagnósticos de outros médicos ou dados."
}

# Inicializar o histórico do chat
chat_history = [system_prompt]

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Rota inicial redirecionando para o login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificação simples de usuário e senha
        if username == 'admin' and password == 'admin':
            return redirect(url_for('dashboard'))  # Redireciona para a página principal após o login
        else:
            flash('Usuário ou senha incorretos. Tente novamente.')  # Mensagem de erro

    return render_template('login.html')

# Rota para a página principal ou dashboard após o login
@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    # Obter os valores dos campos de input
    pressao_sistolica = request.form['pressao_sistolica']
    pressao_diastolica = request.form['pressao_diastolica']
    altura = request.form['altura']
    peso = request.form['peso']
    idade = request.form['idade']
    
    # Criar a mensagem do usuário com os dados fornecidos
    user_input = f"Pressão Sistólica: {pressao_sistolica}, Pressão Diastólica: {pressao_diastolica}, Altura: {altura}, Peso: {peso}, Idade: {idade}"
    
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

    # Retornar a resposta como JSON
    return jsonify({"response": response_content})

if __name__ == "__main__":
    app.run(debug=True)
