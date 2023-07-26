import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda:0" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("diegomiranda/eleuther_70m_cypher_generator")
model = AutoModelForCausalLM.from_pretrained("diegomiranda/eleuther_70m_cypher_generator").to(
    device
)

prefix = "\nCreate a Cypher statement to answer the following question:"

def generate_cypher(prompt):
    print("PROMPT ---->>>>  " + prompt)
    inputs = tokenizer(
        f"{prefix}{prompt}<|endoftext|>", return_tensors="pt", add_special_tokens=False
    ).to(device)
    tokens = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.0,
        repetition_penalty=1.0,
        num_beams=4,
    )[0]
    tokens = tokens[inputs["input_ids"].shape[1] :]

    result_test = tokenizer.decode(tokens, skip_special_tokens=True)

    return result_test
