import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from creators_channel_scan import CreatorsScanMain

# Declaring our FastAPI instance
app = FastAPI()


class CreatorsAPI(BaseModel):
    creators_channel_link: str
    editors_channel_link: str


@app.get("/")
def index():
    return {"message": "Hello, World"}


@app.get("/{name}")
def get_name(name: str):
    return {"Welcome To Krish Youtube Channel": f"{name}"}


@app.post("/get-similarity")
def predict_banknote(data: CreatorsAPI):
    data = data.dict()
    creators_channel_link = data["creators_channel_link"]
    editors_channel_link = data["editors_channel_link"]
    creat_obj = CreatorsScanMain(creators_channel_link)
    topics_list = creat_obj.run_creators_scan()

    editor_obj = CreatorsScanMain(editors_channel_link)
    editor_topics_list = editor_obj.run_creators_scan()

    score = editor_obj.get_similarity_score(topics_list, editor_topics_list)
    return {
        "Creators List": f"{topics_list}",
        "Editors List": f"{editor_topics_list}",
        "Similarity Score": f"{score}",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
