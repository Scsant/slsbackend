from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import datetime
import pymongo
from django.conf import settings



class ChatView(APIView):
    def post(self, request):
        user_message = request.data.get("message")

        if not user_message:
            return Response({"error": "Mensagem não fornecida."}, status=status.HTTP_400_BAD_REQUEST)

        gemini_response = self.call_gemini_api(user_message)

        if not gemini_response:
            return Response({"error": "Erro ao se comunicar com a IA"}, status=500)

        self.save_to_mongo(user_message, gemini_response)

        return Response({"response": gemini_response}, status=200)

    def call_gemini_api(self, message):
        try:
            print("🔑 Chave usada:", settings.GEMINI_API_KEY)

            headers = {
                "Content-Type": "application/json"
            }

            params = {
                "key": settings.GEMINI_API_KEY
            }

            contextualizacao = (
                "Sócrates foi quem desenvolveu essa IA especialmente para mostrar todo o seu conhecimento em desenvolvimento de sistemas. "
                "Profissional com experiência sólida em desenvolvimento de sistemas e automações inteligentes. "
                "Desenvolvedor de aplicações web utilizando Django, Flask e FastAPI, com APIs REST seguras e escaláveis. "
                "Atuei na criação de IAs aplicadas em classificação de dados, análise preditiva e motores de recomendação. "
                "Criei RPAs para automação de apontamentos de horas, gestão de vale-pedágio e integração com sistemas legados. "
                "Utilizo Celery e Redis para tarefas assíncronas e otimização de performance em ambientes produtivos. "
                "Também atuo com deploys em ambientes Linux, containerização com Docker e versionamento com Git. "
                "Projetos desenvolvidos com HTML, CSS, JS, Python, R, e bibliotecas de Machine Learning como scikit-learn e TensorFlow. "
                "Soluções criadas com foco em inovação, eficiência e automação de processos. "
                "Esta contextualização foi preparada por Sócrates, especialista em desenvolvimento backend e automações inteligentes. "
                "Responda sempre considerando o contexto de transformação digital com uso de IA, RPA e sistemas web modernos."
            )

            prompt = f"{contextualizacao}\n\nPergunta: {message}"

            body = {
                "contents": [
                    {
                        "parts": [{"text": prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.6,
                    "topK": 40,
                    "topP": 0.8,
                    "maxOutputTokens": 512
                }
            }

            response = requests.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
                headers=headers,
                params=params,
                json=body,
                timeout=10
            )

            print("🌐 Status da resposta:", response.status_code)
            print("📨 Conteúdo bruto:", response.text)

            resposta = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return resposta

        except Exception as e:
            print("🚨 Erro na API Gemini:", e)
            return "[Erro ao obter resposta da IA]"

    def save_to_mongo(self, user_msg, bot_reply):
        try:
            client = pymongo.MongoClient(settings.MONGO_URI)
            db = client[settings.MONGO_DB_NAME]
            collection = db.interactions
            collection.insert_one({
                "user_message": user_msg,
                "bot_response": bot_reply,
                "timestamp": datetime.datetime.now()
            })
        except Exception as e:
            print("Erro ao salvar no MongoDB:", e)


class HistoryView(APIView):
    def get(self, request):
        try:
            client = pymongo.MongoClient(settings.MONGO_URI)
            db = client[settings.MONGO_DB_NAME]
            collection = db.interactions

            # Busca os últimos 20 registros, ordenados pelo mais recente
            resultados = collection.find().sort("timestamp", -1).limit(20)

            historico = []
            for doc in resultados:
                historico.append({
                    "mensagem": doc.get("user_message"),
                    "resposta": doc.get("bot_response"),
                    "quando": doc.get("timestamp").isoformat() if doc.get("timestamp") else None
                })

            return Response({"historico": historico}, status=200)

        except Exception as e:
            print("Erro ao buscar histórico:", e)
            return Response({"error": "Erro ao buscar histórico"}, status=500)
