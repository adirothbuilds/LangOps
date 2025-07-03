#!/usr/bin/env python3
"""
Enhanced demo showing how to use JenkinsParser with JSON output for LLM analysis.
This extends the original analysis_jenkins_errors.py to include JSON-based prompts.
"""

import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
from langops import ParserRegistry, LLMRegistry

# Load environment variables from .env file
load_dotenv()

# Initialize colorama for colored terminal output
init(autoreset=True)

JENKINS_LOG_PATH = "demo/data/jenkins_logs.txt"
BUILD_ID = "12345"
TIMESTAMP = "2023-10-01T12:00:00Z"


def analyze_jenkins_errors_with_json(log_path: str, build_id: str, timestamp: str):
    """
    Analyze Jenkins errors using both the traditional approach and JSON-based prompts.
    """
    print(Fore.BLUE + Style.BRIGHT + "🔍 Parsing Jenkins log for errors using JenkinsParser..." + Style.RESET_ALL)
    
    # Use JenkinsParser instead of ErrorParser for more structured analysis
    jenkins_parser_cls = ParserRegistry.get_parser("JenkinsParser")
    jenkins_parser = jenkins_parser_cls()
    
    # Parse the log file and get structured data
    from langops.core.types import SeverityLevel
    log_content = jenkins_parser.handle_log_file(log_path)
    parsed_data = jenkins_parser.parse(log_content, min_severity=SeverityLevel.WARNING)
    
    print(Fore.GREEN + Style.BRIGHT + f"✅ Found {len(parsed_data.stages)} stage(s) with issues." + Style.RESET_ALL)
    
    # Display summary
    summary = jenkins_parser.get_stages_summary(parsed_data)
    for stage_name, severity_counts in summary.items():
        total_issues = sum(severity_counts.values())
        print(Fore.CYAN + f"   📋 {stage_name}: " + Fore.YELLOW + f"{total_issues} issues " + Fore.WHITE + f"{severity_counts}" + Style.RESET_ALL)

    if not any(stage.logs for stage in parsed_data.stages):
        print(Fore.YELLOW + "⚠️  No errors found." + Style.RESET_ALL)
        return

    print(Fore.MAGENTA + Style.BRIGHT + "\n🔄 Converting to JSON format for LLM analysis..." + Style.RESET_ALL)
    
    # Method 1: Get clean JSON using Pydantic serialization
    json_data = parsed_data.model_dump_json(indent=2)
    print(Fore.CYAN + "📄 JSON structure preview:" + Style.RESET_ALL)
    print(Fore.WHITE + Style.DIM + (json_data[:300] + "..." if len(json_data) > 300 else json_data) + Style.RESET_ALL)

    print(Fore.BLUE + Style.BRIGHT + "\n🤖 Querying LLM with structured JSON prompt..." + Style.RESET_ALL)
    
    # Create enhanced prompt with JSON data
    llm_prompt = f"""You are a Jenkins CI/CD expert. Analyze this build failure data and provide actionable insights.

**Build Information:**
- Build ID: {build_id}
- Timestamp: {timestamp}

**Structured Log Data:**
```json
{json_data}
```

**Analysis Requirements:**
1. **Root Cause Analysis**: Identify the primary failure reasons
2. **Stage-by-Stage Breakdown**: Analyze each failing stage  
3. **Fix Recommendations**: Provide specific, actionable solutions
4. **Prevention Strategy**: Suggest improvements to avoid future failures

**Response Format:**
Please structure your response with clear sections and prioritize critical issues first."""

    # Query LLM
    api_key = os.getenv("OPENAI_API_KEY")
    status_color = Fore.GREEN if api_key else Fore.RED
    status_text = "✅ Found" if api_key else "❌ Not found"
    print(f"{status_color}🔑 API Key status: {status_text}{Style.RESET_ALL}")
    
    if api_key:
        print(Fore.CYAN + "🔑 OPENAI_API_KEY is set" + Style.RESET_ALL)
    
    if not api_key:
        print(Fore.YELLOW + "⚠️  OPENAI_API_KEY not set. Skipping LLM analysis." + Style.RESET_ALL)
        print(Fore.CYAN + "💡 Here's the prompt that would be sent to the LLM:" + Style.RESET_ALL)
        print(Fore.YELLOW + "=" * 80 + Style.RESET_ALL)
        print(Fore.WHITE + llm_prompt + Style.RESET_ALL)
        print(Fore.YELLOW + "=" * 80 + Style.RESET_ALL)
        return

    try:
        llm_cls = LLMRegistry.get_llm("openai")
        llm = llm_cls(api_key=api_key)
        
        # Send structured prompt to LLM
        messages = [{"role": "user", "content": llm_prompt}]
        response = llm.complete(messages)

        print(Fore.GREEN + Style.BRIGHT + "\n🎯 LLM Analysis Results:" + Style.RESET_ALL)
        print(Fore.CYAN + "=" * 80 + Style.RESET_ALL)
        print(Fore.WHITE + response.text + Style.RESET_ALL)
        print(Fore.CYAN + "=" * 80 + Style.RESET_ALL)
        
        print(Fore.MAGENTA + Style.BRIGHT + "\n📊 Response Metadata:" + Style.RESET_ALL)
        for key, value in response.metadata.items():
            print(Fore.CYAN + f"   {key}: " + Fore.WHITE + f"{value}" + Style.RESET_ALL)
            
    except Exception as e:
        print(Fore.RED + f"❌ Error querying LLM: {e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "💡 Prompt would have been:" + Style.RESET_ALL)
        print(Fore.WHITE + Style.DIM + llm_prompt[:500] + "..." + Style.RESET_ALL)


def compare_parsing_approaches(log_path: str):
    """
    Compare traditional ErrorParser vs new JenkinsParser approaches.
    """
    print(Fore.MAGENTA + Style.BRIGHT + "\n🔬 Comparing Parsing Approaches:" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    
    # Traditional approach
    print(Fore.YELLOW + Style.BRIGHT + "1️⃣ Traditional ErrorParser:" + Style.RESET_ALL)
    error_parser = ParserRegistry.get_parser("ErrorParser")
    errors = error_parser.from_file(log_path)
    print(Fore.WHITE + "   Found " + Fore.CYAN + f"{len(errors)}" + Fore.WHITE + " raw error lines" + Style.RESET_ALL)
    if errors:
        print(Fore.WHITE + Style.DIM + f"   First error: {errors[0][:80]}..." + Style.RESET_ALL)
    
    # New structured approach  
    print(Fore.YELLOW + Style.BRIGHT + "\n2️⃣ New JenkinsParser (structured):" + Style.RESET_ALL)
    jenkins_parser_cls = ParserRegistry.get_parser("JenkinsParser")
    jenkins_parser = jenkins_parser_cls()
    from langops.core.types import SeverityLevel
    log_content = jenkins_parser.handle_log_file(log_path)
    parsed_data = jenkins_parser.parse(log_content, min_severity=SeverityLevel.WARNING)
    
    total_entries = sum(len(stage.logs) for stage in parsed_data.stages)
    print(Fore.WHITE + "   Found " + Fore.CYAN + f"{total_entries}" + Fore.WHITE + " structured log entries across " + Fore.CYAN + f"{len(parsed_data.stages)}" + Fore.WHITE + " stages" + Style.RESET_ALL)
    
    # Show JSON size comparison
    if errors:
        simple_json_size = len(str(errors))  # Rough estimate
        structured_json_size = len(parsed_data.model_dump_json())
        
        print(Fore.WHITE + "   Raw data size: " + Fore.YELLOW + f"~{simple_json_size}" + Fore.WHITE + " chars" + Style.RESET_ALL)
        print(Fore.WHITE + "   Structured JSON size: " + Fore.GREEN + f"{structured_json_size}" + Fore.WHITE + " chars" + Style.RESET_ALL)
        overhead_color = Fore.GREEN if structured_json_size - simple_json_size > 0 else Fore.RED
        print(Fore.WHITE + "   Structure overhead: " + overhead_color + f"+{structured_json_size - simple_json_size}" + Fore.WHITE + " chars" + Style.RESET_ALL)
        
    print(Fore.GREEN + Style.BRIGHT + "\n✅ Structured approach provides:" + Style.RESET_ALL)
    benefits = [
        "Stage-level organization",
        "Timestamp extraction",
        "Severity classification", 
        "Deduplication",
        "Better LLM context"
    ]
    for benefit in benefits:
        print(Fore.CYAN + "   • " + Fore.WHITE + benefit + Style.RESET_ALL)


if __name__ == "__main__":
    print(Fore.CYAN + r"""
     _        _______  _        _______  _______  _______  _______ 
    ( \      (  ___  )( (    /|(  ____ \(  ___  )(  ____ )(  ____ \
    | (      | (   ) ||  \  ( || (    \/| (   ) || (    )|| (    \/
    | |      | (___) ||   \ | || |      | |   | || (____)|| (_____ 
    | |      |  ___  || (\ \) || | ____ | |   | ||  _____)(_____  )
    | |      | (   ) || | \   || | \_  )| |   | || (            ) |
    | (____/\| )   ( || )  \  || (___) || (___) || )      /\____) |
    (_______/|/     \||/    )_)(_______)(_______)|/       \_______)                                   
    """ + Fore.YELLOW + Style.BRIGHT + "                      L A N G O P S\n")

    print(Fore.RESET + Style.BRIGHT + "🚀 Jenkins Parser with JSON LLM Integration Demo 🚀\n")
    
    # Check if log file exists
    if not os.path.exists(JENKINS_LOG_PATH):
        print(Fore.RED + f"❌ Log file not found: {JENKINS_LOG_PATH}" + Style.RESET_ALL)
        print(Fore.YELLOW + "💡 Please ensure the demo data file exists." + Style.RESET_ALL)
        exit(1)
    
    # Run enhanced analysis
    analyze_jenkins_errors_with_json(JENKINS_LOG_PATH, BUILD_ID, TIMESTAMP)
    
    # Compare approaches
    compare_parsing_approaches(JENKINS_LOG_PATH)
    
    print(Fore.GREEN + Style.BRIGHT + "\n🎉 Demo completed!" + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "\n💡 Key Benefits of JSON Approach:" + Style.RESET_ALL)
    
    benefits = [
        "Structured data for better LLM understanding",
        "Stage-aware analysis",
        "Consistent format across different log types",
        "Easy integration with other tools",
        "Preserves timestamp and severity information"
    ]
    
    for benefit in benefits:
        print(Fore.GREEN + "   • " + Fore.WHITE + benefit + Style.RESET_ALL)
