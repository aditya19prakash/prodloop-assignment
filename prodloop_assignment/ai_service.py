from google import genai
from django.conf import settings

client = genai.Client(api_key="AIzaSyCNn4uJ0a4uTU0afDozVPoi6aajygxsqyM")

GEMINI_MODELS = [
    "models/gemini-2.5-flash",         
    "models/gemini-2.0-flash",          
    "models/gemini-2.5-flash-lite",  
    "models/gemini-2.0-flash-lite",      
]

def summarize(data:dict):
    prompt = f"""
    This is task title {data.get("title")} , 
    Description {data.get("description")}
    Generate a brief, one-sentence summary of the task.
    Suggest 3 to 5 potential sub-tasks.
    Categorize the task into one of several predefined categories (e.g., "Bug Fix", "Feature", "DevOps", "Documentation").

    """
    for i in range(0,len(GEMINI_MODELS)):
        try:
            print(i)
            response = client.models.generate_content(model=GEMINI_MODELS[i],contents=prompt)
            return str(response.text)
        except Exception as e:
            print(f"Model {GEMINI_MODELS[i]} failed:", e)

    return None

        
