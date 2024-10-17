from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv
import os
from groq import Groq

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# Necessário para usar 'flash' para mensagens de erro
app.secret_key = 'chave_secreta'

# Criar o cliente Groq
api_key = os.environ.get("GROQ_API_KEY")

# Certifique-se de que a chave API foi carregada corretamente
if not api_key:
    raise ValueError("A chave da API do Groq não foi encontrada no arquivo .env")

client = Groq(api_key=api_key)

# Configurar o prompt do sistema
system_prompt = {
    "role": "system",
    "content": "Você é um cardiologista, eu lhe darei informações como minha pressão sistólica e a pressão diastólica. Lhe darei minha idade, peso e altura. A partir desses dados me dê um diagnóstico com base na OMS, não precisa ser uma resposta muito grande, no final avalie como Perigoso, Boa ou Ótima."
}

# Inicializar o histórico do chat
chat_history = [system_prompt]  # Certifique-se de que o system_prompt esteja no histórico
historico_diagnosticos = []  # Lista para armazenar os dados de diagnóstico

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

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        try:
            pressao_sistolica = request.form['pressao_sistolica']
            pressao_diastolica = request.form['pressao_diastolica']
            altura = request.form['altura']
            peso = request.form['peso']
            idade = request.form['idade']
            
            # Criar a mensagem do usuário com os dados fornecidos
            user_input = f"Pressão Sistólica: {pressao_sistolica}, Pressão Diastólica: {pressao_diastolica}, Altura: {altura}, Peso: {peso}, Idade: {idade}"
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
            
            # Adicionar ao histórico
            chat_history.append({"role": "assistant", "content": response_content})
            
            # Salvar os dados no histórico de diagnósticos
            diagnostico = {
                'pressao_sistolica': pressao_sistolica,
                'pressao_diastolica': pressao_diastolica,
                'altura': altura,
                'peso': peso,
                'idade': idade,
                'diagnostico': response_content
            }
            historico_diagnosticos.append(diagnostico)
            
            # Retornar a resposta do chatbot
            return jsonify({"response": response_content})

        except Exception as e:
            return jsonify({"error": str(e)})  # Captura e retorna o erro em formato JSON
    
    return render_template('index.html')

@app.route('/historico')
def historico():
    return render_template('historico.html', historico=historico_diagnosticos)

if __name__ == "__main__":
    app.run(debug=True)
