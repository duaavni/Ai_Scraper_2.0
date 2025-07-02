from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define the prompt template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}.\n"
    "Please follow these instructions carefully:\n\n"
    "1. Extract only the information matching the description: {parse_description}.\n"
    "2. Do not include explanations or extra text.\n"
    "3. If nothing matches, return an empty string ('').\n"
    "4. Output should be raw extracted data only."
)

# Change model to gemma:2b (you must have it pulled via `ollama pull gemma:2b`)
model = OllamaLLM(model="gemma:2b")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            response = chain.invoke({
                "dom_content": chunk,
                "parse_description": parse_description
            })
            print(f"Parsed batch: {i} of {len(dom_chunks)}")
            parsed_results.append(response)
        except Exception as e:
            print(f"Error parsing chunk {i}: {e}")
            parsed_results.append("")

    return "\n".join(parsed_results).strip()
