import asyncio
import json
import os
import logging
from nyc_data_pipeline.source_extract_async import NYCUrlFetcher, NYCPublicDataFetcher, NYCEndpointFetcher
from orchestration.pipeline_utils import UnifiedPipelineManager, Event

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")

async def fetch_and_save_categories(url, temp_directory):
    output_file = os.path.join(temp_directory, 'category_links.json')
    fetcher = NYCUrlFetcher()
    category_data = await fetcher.run(url)

    with open(output_file, 'w') as file:
        json.dump(category_data, file, indent=4)

    logging.info(f"Category data saved to '{output_file}'.")

async def fetch_dataset_links(json_file_path, temp_directory):
    with open(json_file_path, 'r') as file:
        category_urls = json.load(file)

    all_data_links = {}
    for category, url in category_urls.items():
        logging.info(f"Processing category: {category} with URL: {url}")
        fetcher = NYCPublicDataFetcher(url)
        data_links = await fetcher.run()
        all_data_links[category] = data_links
        logging.info(f"Data links fetched for category: {category}")

    output_file = os.path.join(temp_directory, 'data_links.json')
    save_data_links(all_data_links, output_file)

def save_data_links(data_links, output_file):
    with open(output_file, 'w') as file:
        json.dump(data_links, file, indent=4)
    logging.info(f"Data links saved to '{output_file}'.")

async def fetch_endpoints(json_file_path, temp_directory, landingzone_directory):
    with open(json_file_path, 'r') as file:
        categories_data = json.load(file)

    fetcher = NYCEndpointFetcher(landingzone_directory)  # Assuming this fetcher saves data to the landingzone
    endpoints_dict = {}

    for category, datasets in categories_data.items():
        category_endpoints = {}
        for dataset_name, url in datasets.items():
            logging.info(f"Fetching endpoint for dataset: {dataset_name}")
            endpoint = await fetcher.run({dataset_name: url})
            category_endpoints[dataset_name] = endpoint or "No endpoint found"
        endpoints_dict[category] = category_endpoints

    output_file = os.path.join(temp_directory, 'api_endpoints.json')
    with open(output_file, 'w') as file:
        json.dump(endpoints_dict, file, indent=4)
    logging.info(f"API endpoints saved to '{output_file}'.")

async def main():
    temp_directory = 'temp'
    landingzone_directory = 'landingzone'
    start_url = "https://opendata.cityofnewyork.us/data/"

    ensure_directory_exists(temp_directory)
    ensure_directory_exists(landingzone_directory)

    await fetch_and_save_categories(start_url, temp_directory)

    pipeline = UnifiedPipelineManager()

    # Enqueue the task of fetching dataset links
    category_links_file = os.path.join(temp_directory, 'category_links.json')
    pipeline.enqueue_event(Event(fetch_dataset_links(category_links_file, temp_directory)))
    
    # Process enqueued tasks
    while not pipeline.is_empty():
        event = pipeline.dequeue_event()
        await event.data  # Assuming data is an awaitable function

    # Fetch endpoints and save data to the landingzone directory
    data_links_file = os.path.join(temp_directory, 'data_links.json')
    await fetch_endpoints(data_links_file, temp_directory, landingzone_directory)

if __name__ == "__main__":
    asyncio.run(main())
