from pytubefix import YouTube
from pytubefix import Search
from pytubefix.exceptions import RegexMatchError
import srt

def get_captions(url, lang_code='de'):
    """Fetches captions from a YouTube video.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str: The captions of the video, or an empty string if no captions are found.

    Raises:
        RegexMatchError: If the provided URL is not a valid YouTube video URL.

    Example:
        >>> get_captions('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        'This is a test video.'
    """

    yt = YouTube(url)
    captions = yt.captions.get_by_language_code(lang_code)
    assert captions is not None, "No captions found"
    return captions

# def search_youtube(query):
#     """Searches YouTube for videos matching a given query.

#     Args:
#         query (str): The search query.

#     Returns:
#         list: A list of YouTube video URLs matching the query.

#     Example:
#         >>> search_youtube('python tutorial')
#         ['https://www.youtube.com/watch?v=rfscVS0vtbw', 'https://www.youtube.com/watch?v=Z1RJmh1K9Ls', ...]
#     """

#     search = Search(query)
#     return [result.watch_url for result in search.results]


url = "http://www.youtube.com/watch?v=QdUOwKVlQlE"
#url = "https://www.youtube.com/watch?v=Md0LHGVgFIY"
url="https://www.youtube.com/watch?v=XOnBxRgMRBE"

yt = YouTube(url)
print(yt.captions)

try:
    captions = get_captions(url, lang_code='de')
    subtitle_generator = srt.parse(captions.generate_srt_captions())

except:
    captions = get_captions(url, lang_code='a.de')
    subtitle_generator = srt.parse(captions.generate_srt_captions())

subtitles = list(subtitle_generator)
for subt in subtitles:
    print(subt.content)