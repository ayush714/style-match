import json
import logging
import re

from rich import print as rprint
from semantic_text_similarity.models import WebBertSimilarity

from scripts.youtube_transcriber import YoutubeTranscriber


class SimilarityUtilities:
    def __init__(self) -> None:
        pass

    def transcribe_video(
        self,
        video_url,
        use_content_moderation,
        use_topic_detection,
    ):
        youtube_transcriber = YoutubeTranscriber(
            api_key="84b10466cfdf4f52ab4c349a161cedaa",
            video_url=video_url,
            content_safety=use_content_moderation,
            iab_categories=use_topic_detection,
        )

        if youtube_transcriber.downloaded_audio_path is None:
            youtube_transcriber.download_audio()
            logging.info(f"Audio downloaded to {youtube_transcriber.downloaded_audio_path}")
        else:
            logging.info("hello")

        if youtube_transcriber.upload_url is None:
            youtube_transcriber.upload_audio()
            logging.info(f"upload url: {youtube_transcriber.upload_url}")

        if youtube_transcriber.transcription_id is None:
            youtube_transcriber.submit()
            logging.info(
                f"A transcription job (id={youtube_transcriber.transcription_id}) has been submitted"
            )

        if youtube_transcriber.transcription is None:
            youtube_transcriber.poll()
            logging.info("Transcription succeeded")

        output_name = youtube_transcriber.downloaded_audio_path.split("/")[-1].rstrip(".mp4")
        output_name = output_name.replace(" ", "_")

        youtube_transcriber.save_transcript(output_name)

        return youtube_transcriber.transcription

    def show_output(self, transcript, use_topic_detection):

        print("Transcription Output")
        print(transcript)
        if use_topic_detection:
            print("Topic extraction by video segment")
            results = transcript["iab_categories_result"]["results"]
            return results

    def get_topics_from_transcript(self, video_url, use_content_moderation, use_topic_detection):
        transcript = self.transcribe_video(
            video_url,
            use_content_moderation,
            use_topic_detection,
        )
        results = self.show_output(transcript=transcript, use_topic_detection=use_topic_detection)
        return results

    def get_max_rel_topic(self, results):
        relevant_topics = []
        for result in results:
            labels = result["labels"]
            max_relevance = max(labels, key=lambda x: x["relevance"])
            label_key = max_relevance["label"]
            relevant_topics.append(label_key)
        return relevant_topics


class TextSimilarityMeasures:
    def __init__(self) -> None:
        pass

    def similarity_measure(self, text1, text2):
        try:
            web_model = WebBertSimilarity(device="cpu", batch_size=10)
            pred = web_model.predict(
                [
                    (
                        text1,
                        text2,
                    )
                ]
            )
            return pred
        except Exception as e:
            logging.error(e)

    def main_get_similarity(self, video_url, editor_tags_from_replayed):
        Utilities = SimilarityUtilities()
        results = Utilities.get_topics_from_transcript(
            video_url=video_url, use_content_moderation=False, use_topic_detection=True
        )
        relevant = Utilities.get_max_rel_topic(results)
        # remove > and  every character after this symbol
        for i in range(len(relevant)):
            relevant[i] = re.sub(">.*", "", relevant[i])
        joined_list = ",".join(relevant)
        # remove punctuation only not spaces
        joined_list = re.sub(r"[^\w\s]", " ", joined_list)
        text_similarity_measures = TextSimilarityMeasures()
        similarity_score = text_similarity_measures.similarity_measure(
            joined_list, editor_tags_from_replayed
        )
        return similarity_score

    def get_topics_from_video(self, video_url):
        Utilities = SimilarityUtilities()
        results = Utilities.get_topics_from_transcript(
            video_url=video_url, use_content_moderation=False, use_topic_detection=True
        )
        relevant = Utilities.get_max_rel_topic(results)
        for i in range(len(relevant)):
            relevant[i] = re.sub(">.*", "", relevant[i])
        return relevant


if __name__ == "__main__":
    pass
    # Utilities = SimilarityUtilities()
    # video_url = "https://www.youtube.com/watch?v=5h5zurZsIQY"
    # results = Utilities.get_topics_from_transcript(
    #     video_url=video_url, use_content_moderation=False, use_topic_detection=True
    # )
    # relevant = Utilities.get_max_rel_topic(results)
    # rprint(relevant)
    # # remove > and  every character after this symbol
    # for i in range(len(relevant)):
    #     relevant[i] = re.sub(">.*", "", relevant[i])
    # rprint(relevant)
    # joined_list = ",".join(relevant)
    # # remove punctuation only not spaces
    # joined_list = re.sub(r"[^\w\s]", " ", joined_list)
    # rprint(joined_list)
    # text_similarity_measures = TextSimilarityMeasures()
    # pred = text_similarity_measures.similarity_measure(
    #     joined_list, "Tech Graphics Commentary Meme Music"
    # )
    # print(pred)
    # TextSimilarityMeasuress = TextSimilarityMeasures()
    # similarity = TextSimilarityMeasuress.main_get_similarity(
    #     video_url=video_url, editor_tags_from_replayed="Tech Graphics Commentary Meme Music"
    # )
    # print(similarity)
