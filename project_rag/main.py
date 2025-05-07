from flask import Flask, request, jsonify
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

app = Flask(__name__)

# Load và index tài liệu từ thư mục "data"
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    response = query_engine.query(query)
    return jsonify({"response": str(response)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
