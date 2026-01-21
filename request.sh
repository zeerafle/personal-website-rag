curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"message": "Who is sam?", "conversation_id": "123"}' \
    http://127.0.0.1:8000/chat

# {
#   "message": "Sam is an AI engineering enthusiast who enjoys using machine learning and AI to build things. He has a strong foundation in both the theoretical and practical aspects of these subjects and is currently pursuing a master's degree in AI.\n\nIn his free time, Sam enjoys watching and analyzing movies, reading science books, and listening to music. He also holds a Tensorflow Developer Certificate and a Microsoft AI Engineer certificate.\n\nSource: About page on Sam's website.",
#   "conversation_id": "123"
# }
