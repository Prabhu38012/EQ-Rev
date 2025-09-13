from agent.direct_handler import handle_query

def main():
    print("Quick Commerce Agent is ready! Type 'exit' to quit.")
    print("You can also access the web interface by running 'python app.py' and visiting http://localhost:7860")
    
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