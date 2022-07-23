import logging
from itertools import chain

import pandas as pd
import scrapetube

from similarity_measure import TextSimilarityMeasures


class CreatorsScanMain:
    def __init__(self, channel_link) -> None:
        """
        TODO:
        """
        self.channel_link = channel_link

    def run_creators_scan(self):
        """ """
        try:
            df = self.extract_ten_latest_video()
            topics_list = self.extract_topics_from_creators_channel(df)
            return topics_list
        except Exception as e:
            logging.error(e)
            return None

    def get_similarity_score(self, topics1, topics2):
        try:
            similarity_obj = TextSimilarityMeasures()
            topics_creators = ",".join(topics1)
            topics_editor = ",".join(topics2)
            score: int = similarity_obj.similarity_measure(topics_creators, topics_editor)
            return score
        except Exception as e:
            logging.error(e)

    def extract_ten_latest_video(self):
        """
        TODO:
        """
        try:
            # c = Channel(self.channel_link)
            # df = pd.DataFrame()
            # urls = []
            # for url in c.video_urls:
            #     urls.append(url)
            # df["url"] = urls
            # # keep only top 10 rows
            # df = df.head(1)
            # df.to_csv("creators_channel_scan.csv", index=False)
            # return df
            videos = scrapetube.get_channel(channel_url=self.channel_link)
            df = pd.DataFrame()
            urls = []
            for video in videos:
                id = video["videoId"]
                url = "https://www.youtube.com/watch?v=" + str(id)
                urls.append(id)
            df["url"] = urls
            df.to_csv("creators_channel_scan.csv", index=False)
            return df
        except Exception as e:
            logging.error(e)
            return None

    def extract_topics_from_creators_channel(self, df_containing_urls):
        """
        TODO:
        """
        try:
            urls = df_containing_urls["url"].tolist()
            topics_list = []
            for url in urls:
                get_topics = TextSimilarityMeasures()
                topics = get_topics.get_topics_from_video(url)
                topics_list.append(topics)
            flatten_list = list(set(chain.from_iterable(topics_list)))
            # only keep unique topics
            return flatten_list
        except Exception as e:
            logging.error(e)
            return None


if __name__ == "__main__":
    creators_obj = CreatorsScanMain("https://www.youtube.com/c/WIRED/videos")
    df = creators_obj.extract_ten_latest_video()
    df_containing_urls = pd.read_csv("creators_channel_scan.csv")
    topics_list = creators_obj.extract_topics_from_creators_channel(df_containing_urls)
    # print(topics_list)
    flatten_list = list(set(chain.from_iterable(topics_list)))
    print(flatten_list)
