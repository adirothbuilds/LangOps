import os
from agentops import ParserRegistry, PromptRegistry, LLMRegistry

JENKINS_LOG_PATH = "demo/data/jenkins_logs.txt"
BUILD_ID = "12345"
TIMESTAMP = "2023-10-01T12:00:00Z"

def analyze_jenkins_errors(log_path: str, build_id: str, timestamp: str):
    print("Parsing Jenkins log for errors...")
    error_parser = ParserRegistry.get_parser("ErrorParser")
    errors = error_parser.from_file(log_path)
    print(f"Found {len(errors)} error(s).")

    if not errors:
        print("No errors found.")
        return

    print("\nGenerating prompt...")
    prompt_cls = PromptRegistry.get_prompt("JenkinsErrorPrompt")
    prompt = prompt_cls(build_id=build_id, timestamp=timestamp)
    prompt.add_user_prompt(errors)

    print("\nQuerying LLM...")
    api_key = os.getenv("OPENAI_API_KEY")
    llm_cls = LLMRegistry.get_llm("openai")
    llm = llm_cls(api_key=api_key)
    messages = prompt.render_prompts()
    response = llm.complete(messages)

    print("\n📣 LLM Response:\n" + response.text)
    print("\n📄 Metadata:\n", response.metadata)

if __name__ == "__main__":
    analyze_jenkins_errors(JENKINS_LOG_PATH, BUILD_ID, TIMESTAMP)
