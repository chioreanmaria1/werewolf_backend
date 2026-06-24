from openai import OpenAI # sau biblioteca specifică pe care o folosești

# Configurează clientul cu URL-ul și API Key-ul tău
client = OpenAI(
    api_key="bc315679fc9b7675265b194d420449a0",
    base_url="https://chat-ai.academiccloud.de/v1"
)

# Listează modelele disponibile
models = client.models.list()

# Afișează fiecare model
for m in models.data:
    print(m.id)


# from openai import OpenAI
# import os

# # 1. Configurarea clientului cu endpoint-ul AcademicCloud și cheia ta API
# api_key = os.getenv("ACADEMIC_CLOUD_API_KEY", "PUNE_CHEIA_TA_API_AICI") 
# client = OpenAI(
#     api_key="de905758b4bf5da0bc26ec7555c2cd92",
#     base_url="https://chat-ai.academiccloud.de/v1"
# )

# # Setează exact numele modelului pe care vrei să-l testezi, 
# # conform listei returnate de client.models.list()
# NUME_MODEL = "qwen3-omni-30b-a3b-instruct" 

# def test_comportament_api(model_id):
#     print(f"Testăm comportamentul modelului: {model_id} prin API...\n")
    
#     # Prompt brut, neformatat
#     prompt_brut = "What is the capital of france?\n"
    
#     try:
#         # Folosim endpoint-ul de completions (dacă este expus de server)
#         # Acesta trimite textul exact cum este, fără șabloane de chat
#         response = client.completions.create(
#             model=model_id,
#             prompt=prompt_brut,
#             max_tokens=30,
#             temperature=0.3
#         )
        
#         text_generat = response.choices[0].text
        
#         print("=== REZULTAT ===")
#         print(prompt_brut + text_generat)
#         print("================")
        
#     except Exception as e:
#         print(f"Eroare la apelul Completions: {e}")
#         print("\nNotă: Dacă API-ul dă eroare (ex. endpoint lipsă), serverul permite probabil doar endpoint-ul de Chat (/v1/chat/completions).")
#         test_comportament_chat_api(model_id, prompt_brut)

# def test_comportament_chat_api(model_id, prompt_brut):
#     print(f"\nÎncercăm testarea folosind endpoint-ul de Chat...")
#     try:
#         # Trimitem textul într-un mesaj de utilizator. 
#         # Serverul va aplica automat șablonul de chat (dacă există).
#         response = client.chat.completions.create(
#             model=model_id,
#             messages=[{"role": "user", "content": prompt_brut}],
#             max_tokens=30,
#             temperature=0.3
#         )
        
#         text_generat = response.choices[0].message.content
        
#         print("=== REZULTAT (din Chat) ===")
#         print(text_generat)
#         print("================")
        
#     except Exception as e:
#          print(f"Eroare la apelul Chat: {e}")

# test_comportament_api(NUME_MODEL)