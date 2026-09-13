# ollama library

import ollama

response = ollama.list()

# print(response)

# chat example

# res = ollama.chat(
#                 model="llama3.2",
#                 messages=[
#                     {
#                         "role":"user",
#                         "content":"why is the sky blue?"
#                     }
#                 ]
#             )

# print(res["message"]["content"])

# chat streaming example

# res = ollama.chat(
#                 model="llama3.2",
#                 messages=[
#                     {
#                         "role":"user",
#                         "content":"why is the sky blue?"
#                     }
#                 ],
#                 stream=True
#             )

# for chunk in res:
#     print(chunk["message"]["content"], end=" ", flush = True)



# res = ollama.generate(
#     model="llama3.2",
#     prompt="why is the sky blue?",
# )    

# show

# print(ollama.show("llama3.2"))


# create a new model with Modelfile

modelfile= """

FROM llama3.2
SYSTEM You are very smart assistant who knows everything about oceans. You are very succinct and informative.
PARAMETER temperature 0.1
"""

ollama.create(model="knowitall", modelfile=modelfile)

res = ollama.generate(model="knowitall", prompt="why is the ocean so salty?")
print(res["response"])

ollama.delete("knowitall")