from google import genai

client = genai.Client(api_key="AIzaSyCNn4uJ0a4uTU0afDozVPoi6aajygxsqyM")

print(client.models.generate_content(model = "models/gemini-2.5-flash",contents="hello all").text)