from agent.direct_handler import handle_query

def main():
    print("Quick Commerce Agent is ready! Type 'exit' to quit.")
    
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        try:
            response = handle_query(query)
            print("Agent:", response)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()