import json
import os
import speech_recognition as sr
import pyttsx3

# Função para carregar o FAQ de um arquivo JSON
def carregar_faq():
    if os.path.exists("faq.json"):
        with open("faq.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

# Função para salvar o FAQ no arquivo JSON
def salvar_faq(faq):
    with open("faq.json", "w", encoding="utf-8") as f:
        json.dump(faq, f, ensure_ascii=False, indent=4)

# Função para treinar o chatbot com novas perguntas e respostas
def treinar_bot(faq):
    print("Modo de treinamento iniciado. Digite 'sair' para sair.")
    while True:
        pergunta = input("Pergunta: ").strip()
        if pergunta.lower() == "sair":
            break
        resposta = input("Resposta: ").strip()
        if not pergunta or not resposta:
            print("Pergunta ou resposta inválida! Tente novamente.")
            continue
        faq[pergunta] = resposta
        print("Treinamento concluído!")
    salvar_faq(faq)

# Função para iniciar o reconhecimento de voz
def iniciar_reconhecimento_voz():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escutando...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Reconhecendo...")
        return r.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        print("Não consegui entender o que você disse.")
        return ""
    except sr.RequestError:
        print("Não consegui me conectar aos serviços de reconhecimento de fala.")
        return ""

# Função para sintetizar fala (Text-to-Speech)
def sintetizar_fala(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Velocidade da fala
    engine.setProperty('volume', 1)  # Volume da fala (0.0 a 1.0)
    engine.say(texto)
    engine.runAndWait()

# Função principal do chatbot
def chatbot(faq):
    print("Chatbot: Olá! Sou seu assistente virtual. Pergunte algo ou digite 'sair' para encerrar.")
    
    # Banco de dados de URLs (links para redirecionamento)
    redirecionamentos = {
        "portal do aluno": "https://alcantaraxz.github.io/teste/index.html",
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
    }

    while True:
        # Captura de áudio do usuário
        entrada_usuario = iniciar_reconhecimento_voz().strip().lower()

        if entrada_usuario in ["sair", "tchau", "adeus"]:
            sintetizar_fala("Até logo! Espero ter ajudado.")
            break
        
        # Checa se a pergunta é sobre algum site específico
        for site, url in redirecionamentos.items():
            if site in entrada_usuario:
                resposta = f"Aqui está o link para o {site.capitalize()}: {url}"
                sintetizar_fala(resposta)
                print(f"Chatbot: {resposta}")
                break
        else:
            # Caso o site não seja encontrado no banco de dados
            if entrada_usuario in faq:
                resposta = faq[entrada_usuario]
                sintetizar_fala(resposta)
                print(f"Chatbot: {resposta}")
            else:
                resposta = "Hmm, eu ainda não sei responder isso. Você pode me ensinar?"
                sintetizar_fala(resposta)
                print(f"Chatbot: {resposta}")
                treinar_bot(faq)

# Função principal para o programa
def principal():
    faq = carregar_faq()
    while True:
        print("\nEscolha uma opção:")
        print("1. Iniciar chat")
        print("2. Treinar chatbot")
        print("3. Sair")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            chatbot(faq)
        elif escolha == "2":
            treinar_bot(faq)
        elif escolha == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Executa a função principal
if __name__ == "__main__":
    principal()
