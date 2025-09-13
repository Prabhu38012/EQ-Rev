from agent.agent import build_agent

def main():
    agent = build_agent()
    print("Quick Commerce Agent is ready! Type 'exit' to quit.")
    
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        try:
            # Use invoke instead of run with proper input format
            response = agent.invoke({"input": query})
            print("Agent:", response["output"])
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()