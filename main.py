# python core code 
import ollama
import re
import json
import time

# time the response
start_time = time.time()

resp = ollama.chat(
    model="qwen2.5vl:7b",
    messages=[
        {
            "role": "user",
            "content": "From this invoice, I need the party name, party address, party GST number, invoice amount, taxable amount, and all item details including item names and quantities, properly listed in JSON format",
            "images": ["C:/Users/Hello/Desktop/images/bill2.png"]
        }
    ],
    stream=True
)

content = ""
for chunk in resp:
    if "message" in chunk and "content" in chunk["message"]:
        piece = chunk["message"]["content"]
        # print(piece, end="", flush=True)  # realtime print
        content += piece


# time the response
end_time = time.time() 
elapsed = end_time - start_time


# JSON extract after full response
match = re.search(r"```json\n(.*?)```", content, re.DOTALL)
if match:
    json_data = json.loads(match.group(1))
    print(json.dumps(json_data, indent=2))
else:
    print("JSON not found in response")

print(f"\nResponse Time: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")


# Note :
# ollama model download

# ollama run qwen2.5vl:7b
# ollama run qwen2.5vl:32b