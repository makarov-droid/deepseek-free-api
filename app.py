import os
from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)

@app.route("/v1/chat/completions", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "messages" not in data:
        return jsonify({"error": "No messages provided"}), 400
    messages = data["messages"]
    model = data.get("model", "deepseek-v3")
    try:
        client = Client()
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False
        )
        content = response.choices[0].message.content
        return jsonify({
            "id": "chatcmpl-" + str(int(time.time())),
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "DeepSeek Free API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
