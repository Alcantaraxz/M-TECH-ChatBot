import json
import os
import webbrowser  # Importa a biblioteca para abrir sites
import speech_recognition as sr  # Para reconhecimento de voz
import pyttsx3  # Para resposta de voz
import re  # Para expressões regulares
import datetime  # Para manipulação de datas e horas
import requests  # Para fazer requisições HTTP

# Função para falar com o usuário
def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

# Função para ouvir comandos de voz
def ouvir_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        try:
            audio = recognizer.listen(source)
            comando = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            print("Não entendi o que você disse. Tente novamente.")
            return ""
        except sr.RequestError as e:
            print(f"Erro ao acessar o serviço de reconhecimento de voz: {e}")
            return ""

# Função para calcular impostos
def calcular_imposto(tipo_imposto, valor):
    try:
        if tipo_imposto.lower() == "ir":
            # Imposto de Renda (simulação)
            if valor <= 1903.98:
                imposto = 0
            elif valor <= 2826.65:
                imposto = valor * 0.075
            elif valor <= 3751.05:
                imposto = valor * 0.15
            elif valor <= 4664.68:
                imposto = valor * 0.225
            else:
                imposto = valor * 0.275
            return f"Imposto de Renda a ser pago: R${imposto:.2f}"

        elif tipo_imposto.lower() == "icms":
            # ICMS (simulação de alíquota de 18%)
            imposto = valor * 0.18
            return f"ICMS a ser pago: R${imposto:.2f}"

        elif tipo_imposto.lower() == "ipva":
            # IPVA (simulação de alíquota de 4% do valor do veículo)
            imposto = valor * 0.04
            return f"IPVA a ser pago: R${imposto:.2f}"

        else:
            return "Tipo de imposto desconhecido."

    except Exception as e:
        return f"Ocorreu um erro: {e}"

# Função que ensina sobre impostos (explicações)
def ensinar_impostos():
    explicacao = (
        "Aqui estão alguns exemplos de impostos que eu posso calcular:\n\n"
        "1. Imposto de Renda (IR): É um imposto sobre a renda das pessoas físicas e jurídicas. Ele varia de acordo com a faixa de renda.\n"
        "2. ICMS: É um imposto sobre circulação de mercadorias e serviços, com uma alíquota média de 18%.\n"
        "3. IPVA: É um imposto sobre a propriedade de veículos automotores, que varia conforme o estado.\n\n"
        "Eu posso calcular esses impostos para você. Apenas me diga o tipo de imposto e o valor."
    )
    return explicacao

# Função para carregar o FAQ (se já houver)
def carregar_faq():
    if os.path.exists("faq.json"):
        with open("faq.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

# Função para salvar o FAQ
def salvar_faq(faq):
    with open("faq.json", "w", encoding="utf-8") as f:
        json.dump(faq, f, ensure_ascii=False, indent=4)

# Função para treinar o chatbot
def treinar_bot(faq):
    print("Modo de treinamento iniciado. Diga 'sair' para sair.")
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

# Função para interagir com o chatbot
def chatbot(faq):
    print("Chatbot: Olá! Sou seu assistente virtual. Pergunte algo ou diga 'sair' para encerrar.")
    while True:
        entrada_usuario = input("Você: ").strip()

        # Comando para sair do chatbot
        if entrada_usuario.lower() in ["sair", "tchau", "adeus"]:
            print("Chatbot: Até logo! Espero ter ajudado.")
            break

        # Comando para obter a data e hora atual
        elif "data e hora" in entrada_usuario.lower():
            resultado = obter_data_hora()
            print(f"Chatbot: {resultado}")
        
        # Comando para perguntar a hora atual
        elif "qual a hora de agora" in entrada_usuario.lower() or "quantas horas são" in entrada_usuario.lower():
            resultado = obter_hora_atual()
            print(f"Chatbot: {resultado}")

        # Comando para calcular a diferença entre duas datas
        elif "diferenca entre datas" in entrada_usuario.lower():
            print("Chatbot: Informe a primeira data (no formato dia/mês/ano):")
            data1 = input("Primeira data: ").strip()
            print("Chatbot: Informe a segunda data (no formato dia/mês/ano):")
            data2 = input("Segunda data: ").strip()
            resultado = calcular_diferenca_datas(data1, data2)
            print(f"Chatbot: {resultado}")

        # Comando para perguntar sobre impostos
        elif "imposto" in entrada_usuario.lower():
            print("Chatbot: Qual imposto você gostaria de calcular? (Exemplo: IR, ICMS, IPVA)")
            tipo_imposto = input("Digite o tipo de imposto (IR, ICMS, IPVA): ").strip().lower()
            
            if tipo_imposto not in ["ir", "icms", "ipva"]:
                print("Chatbot: Não conheço esse tipo de imposto. Tente novamente.")
                continue  # Volta para pedir o tipo de imposto novamente

            print(f"Chatbot: Você escolheu calcular o imposto {tipo_imposto}. Qual é o valor?")
            try:
                valor = float(input("Qual o valor? R$ "))
                resultado = calcular_imposto(tipo_imposto, valor)
                print(f"Chatbot: {resultado}")
            except ValueError:
                print("Chatbot: Por favor, insira um valor numérico válido.")

        # Comando para abrir o Instagram
        elif "instagram" in entrada_usuario.lower():
            print("Chatbot: Abrindo o Instagram...")
            webbrowser.open("https://www.instagram.com")  # Ou o link para o perfil específico
        elif "portal do aluno" in entrada_usuario.lower():
            print("Chatbot: Abrindo o Portal do Aluno...")
            webbrowser.open("https://alcantaraxz.github.io/teste/")
        elif "banco de arquivos" in entrada_usuario.lower():
            print("Chatbot: Abrindo o Banco de Arquivos...")
            webbrowser.open("http://192.168.1.80:8000/")
        elif "spotify" in entrada_usuario.lower():
            print("Chatbot: Abrindo o Spotify...")
            try:
                os.system("start spotify:")
            except Exception as e:
                print(f"Erro ao tentar abrir o Spotify: {e}")
                webbrowser.open("https://www.spotify.com")
        elif "github" in entrada_usuario.lower():
            print("Chatbot: Abrindo o seu GitHub...")
            webbrowser.open("https://github.com/alcantaraxz")
        else:
            print("Chatbot: Não entendi. Você pode tentar novamente?")

# Função para mostrar a data e hora atual
def obter_data_hora():
    agora = datetime.datetime.now()
    data_hora_atual = agora.strftime("%d/%m/%Y %H:%M:%S")  # Formato: dia/mês/ano hora:minuto:segundo
    return f"A data e hora atuais são: {data_hora_atual}"

# Função para mostrar a hora atual
def obter_hora_atual():
    agora = datetime.datetime.now()
    hora_atual = agora.strftime("%H:%M:%S")  # Formato: hora:minuto:segundo
    return f"A hora de agora é: {hora_atual}"

# Função para calcular a diferença entre duas datas
def calcular_diferenca_datas(data1_str, data2_str):
    try:
        # Convertendo as strings de data para objetos datetime
        data_format = "%d/%m/%Y"  # Formato: dia/mês/ano
        data1 = datetime.datetime.strptime(data1_str, data_format)
        data2 = datetime.datetime.strptime(data2_str, data_format)
        
        # Calculando a diferença entre as duas datas
        diferenca = abs((data2 - data1).days)
        return f"A diferença entre {data1_str} e {data2_str} é de {diferenca} dias."
    
    except ValueError:
        return "Erro: Formato de data inválido. Use o formato dia/mês/ano."

# Função para obter a taxa de câmbio em tempo real e converter moedas
def obter_taxa_cambio():
    url = "https://v6.exchangerate-api.com/v6/6d2c2564073245b497d151fe9a0aa416/latest/BRL"  # Substitua YOUR_API_KEY pela sua chave
    try:
        resposta = requests.get(url)
        dados = resposta.json()

        if dados["result"] == "success":
            return dados["conversion_rates"]
        else:
            print("Erro ao obter as taxas de câmbio.")
            return None
    except Exception as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None

# Função para converter moedas usando taxas de câmbio em tempo real
def converter_moeda(valor, moeda_origem, moeda_destino):
    taxas = obter_taxa_cambio()
    if taxas and moeda_origem in taxas and moeda_destino in taxas:
        taxa = taxas[moeda_destino] / taxas[moeda_origem]
        valor_convertido = valor * taxa
        return f"{valor} {moeda_origem} é igual a {valor_convertido:.2f} {moeda_destino}."
    else:
        return "Desculpe, não posso converter essas moedas no momento."

# Função principal
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

if __name__ == "__main__":
    principal()
