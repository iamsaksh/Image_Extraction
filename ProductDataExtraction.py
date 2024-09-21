from openai import OpenAI
import json
import os
import base64
import PyPDF2
import time
import urllib.request
import urllib.error

from urllib.parse import urlparse

client = OpenAI()

def load_json_schema(schema_file: str) -> dict:
    with open(schema_file, 'r') as file:
        return json.load(file)

image_path = 'C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python312\\Test\\Sample.jpg'
image_OP_path = "C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python312\\Test\\Output\\"
invoice_schema = load_json_schema('C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python312\\product_schema.json')
def sleep(timeout, retry=10):
    time.sleep(600)
with open(image_path, 'rb') as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
response = client.chat.completions.create(
    model='gpt-4o',
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "provide JSON file that represents this document. Use this JSON Schema: " +
                    json.dumps(invoice_schema)},          
		{
		    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                }
            ],
        }
    ],
    max_tokens=1000,
)
# time.sleep(120)
print(response.choices[0].message.content)
json_data = json.loads(response.choices[0].message.content)
filename_without_extension = os.path.splitext(os.path.basename(image_path))[0]
json_filename = f"{filename_without_extension}.json"
json_filename =image_OP_path+json_filename
with open(json_filename, 'w', encoding='utf8') as file:
    json.dump(json_data, file, indent=4, ensure_ascii=False)

#with open(json_filename, 'w') as file:
    #json.dump(json_data, file, indent=4)

print(f"JSON data saved to {json_filename}")