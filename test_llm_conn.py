from langchain_ollama import OllamaLLM

# Create an instance of the local LLM
llm = OllamaLLM(model="gemma3n:latest")  # or "mistral:7b-instruct", etc.

# Invoke the model with a prompt
response = llm.invoke("Write a 100 letter poem ")

# Print the model's response
print(response)



import subprocess

def check_ollama_gpu_usage():
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma3n:latest", "--verbose"],
            input="Hi",
            capture_output=True,
            text=True,
            encoding="utf-8",  
            timeout=90
        )
        output = result.stdout + result.stderr

        if "using CUDA" in output:
            return "✅ Ollama is using GPU (CUDA)"
        elif "using Metal" in output:
            return "✅ Ollama is using GPU (Apple Metal)"
        elif "using CPU" in output:
            return "🧠 Ollama is using CPU"
        else:
            print(output)
            return "⚠️ Could not determine backend from output."
    except subprocess.TimeoutExpired:
        return "⚠️ Ollama took too long to respond. Check model size or system load."
    except Exception as e:
        return f"❌ Error: {str(e)}"

print(check_ollama_gpu_usage())
