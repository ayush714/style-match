import flask
from flask import Flask, jsonify, request

from creators_channel_scan import CreatorsScanMain

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/getsimilarity", methods=["GET", "POST"])
def get_similarity():
    data = request.get_json()
    creators_channel_link = data["creators_channel_link"]
    editors_channel_link = data["editors_channel_link"]
    creat_obj = CreatorsScanMain(creators_channel_link)
    topics_list = creat_obj.run_creators_scan()

    editor_obj = CreatorsScanMain(editors_channel_link)
    editor_topics_list = editor_obj.run_creators_scan()

    score = editor_obj.get_similarity_score(topics_list, editor_topics_list)
    return jsonify(
        {
            "Creators List": f"{topics_list}",
            "Editors List": f"{editor_topics_list}",
            "Similarity Score": f"{score}",
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
