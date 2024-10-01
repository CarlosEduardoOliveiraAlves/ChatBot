from dotenv import load_dotenv
import os
from groq import Groq

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()  # Não é necessário especificar o arquivo se for .env

# Criar o cliente Groq
api_key = os.environ.get("GROQ_API_KEY")

print("API Key carregada:", api_key)  # Para verificar se a chave foi carregada

if not api_key:
    raise ValueError("A variável de ambiente GROQ_API_KEY não está definida.")

client = Groq(api_key=api_key)

# Configurar o prompt do sistema
system_prompt = {
    "role": "system",
    "content": "You are a helpful assistant. You reply with very short answers."
}

# Inicializar o histórico do chat
chat_history = [system_prompt]

while True:
    # Obter entrada do usuário
    user_input = input("You: ")

    # Adicionar a entrada do usuário ao histórico do chat
    chat_history.append({"role": "user", "content": user_input})

    # Fazer a chamada para completar o chat
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=100,
        temperature=1.2
    )

    # Adicionar a resposta ao histórico do chat
    chat_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })

    # Imprimir a resposta
    print("Assistant:", response.choices[0].message.content)
