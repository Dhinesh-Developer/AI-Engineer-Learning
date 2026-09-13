from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
            {"role":"system","content":"You are an Eastern poet."},
            {"role":"user","content":"""Write me a short poem about the moon. 
            write the poem in the style of india.
            Make sure to add the title for the poem."""}
    ]
)

print(response.choices[0].message.content)



