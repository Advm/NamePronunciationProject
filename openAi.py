# export OPENAI_API_KEY='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'
import openai
import os
openai.api_key = "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"

# list engines
engines = openai.Engine.list()

# # print the first engine's id
# print(engines.data[0].id)

# # create a completion
# completion = openai.Completion.create(engine="ada", prompt="Hello world")

# # print the completion
# print(completion.choices[0].text)

completion = openai.Classification.create(
  search_model="ada", 
  model="curie",
  examples=[
    ["Croissant", "Romance"],
    ["Median", "Germanic"],
    ["鄙蝙蝠", "Japonic"]
  ],
  query="Notebook",
  labels=["Romance", "Germanic", "Japonic", "Sino-Tebetan"],
)

print(completion)c