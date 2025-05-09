
from TikTokApi import TikTokApi
import asyncio
import os
import pandas as pd
#import openpyxl

ms_token = os.environ.get("ms_code", None)


async def fetch(url):
    async with TikTokApi() as api:
        url = url
        print("Fetching video info for URL:", url)
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video_list = []
        video = api.video(url=url)
        video_info = await video.info()
        video_list.append(video_info)

        return video_list

def flatten_item(key, item, parent_key='', sep='-'):
    """Recursive helper function to flatten one item."""
    new_key = f"{parent_key}{sep}{key}" if parent_key else key
    if isinstance(item, dict):
        return flatten_dict(item, new_key, sep=sep)
    elif isinstance(item, list):
        return flatten_list(key, item, parent_key, sep=sep)
    else:
        return {new_key: item}

def flatten_dict(d, parent_key='', sep='-'):
    """Flatten a nested dictionary."""
    items = {}
    for k, v in d.items():
        items.update(flatten_item(k, v, parent_key, sep))
    return items

def flatten_list(key, lst, parent_key='', sep='-'):
    """Flatten a list of dictionaries (or other lists)."""
    items = {}
    for i, v in enumerate(lst):
        items.update(flatten_item(f"{key}_{i}", v, parent_key, sep))
    return items

def export(excel_name, flattened_dict):
    df = pd.DataFrame(flattened_dict)
    df.to_excel(excel_name, index=False)

# Read the Excel file
df = pd.read_excel('/Users/shanelim/scraping/url/url_only_nadhif/nadhif_urlOnly_15dec.xlsx')

# Create a list of URLs
url_list = df['urlNadhif'].tolist()

# Initialize a list to store all video metadata
all_video_metadata = []
error_urls = []

# Iterate through the URL list and fetch metadata for each URL
for url in url_list:
    try:
        video_metadata = asyncio.get_event_loop().run_until_complete(fetch(url))
        all_video_metadata.extend(video_metadata)
    except Exception as e:
        print(f"Ignoring error for URL: {url}")
        print(f"Error message: {str(e)}")
        error_urls.append(url)


# Print the URLs that generated errors
print("URLs with errors:")
for error_url in error_urls:
    print(error_url)


# Flatten the metadata and export to Excel
flattened_dict = [flatten_dict(d) for d in all_video_metadata]

print("downloading flattened_dict")
df = pd.DataFrame(flattened_dict)
df.to_excel('25Nov_test_multipleurl.xlsx')



