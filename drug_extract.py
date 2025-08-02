from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json

MODEL_NAME = "ibm-granite/granite-13b-chat-v1"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def extract_drugs(text):
    prompt = f"""
You are a medical assistant AI. Extract drug names and dosages from the following prescription text.
Respond in JSON list format like this: [{"drug": "paracetamol", "context": "Take Paracetamol 500mg after meals"}]

Prescription: {text}
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    outputs = model.generate(
        **inputs,
        max_length=512,
        temperature=0.7,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    try:
        start = response.index('[')
        end = response.rindex(']') + 1
        json_response = response[start:end]
        return json.loads(json_response)
    except Exception as e:
        return []
