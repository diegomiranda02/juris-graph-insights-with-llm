
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "diegomiranda/text-to-cypher"
prefix = "Create a Cypher statement to answer the following question:"
sufix = "<|endoftext|>"

def generate_cypher(prompt):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        use_fast=True,
        trust_remote_code=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map={"": "cpu"},
        trust_remote_code=True,
    )
    model.cpu().eval()

    inputs = tokenizer(prefix + prompt + sufix, return_tensors="pt", add_special_tokens=False).to("cpu")

    tokens = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        min_new_tokens=2,
        max_new_tokens=500,
        do_sample=False,
        num_beams=2,
        temperature=float(0.0),
        repetition_penalty=float(1.0),
        renormalize_logits=True
    )[0]

    tokens = tokens[inputs["input_ids"].shape[1]:]
    answer = tokenizer.decode(tokens, skip_special_tokens=True)

    return answer
