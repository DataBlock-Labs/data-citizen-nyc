# NYC-Ai-Hackathon-2023
Hackathon team for NYC Open AI hackathon


## NYCPublicDataFetcher Class

### Class Description:
Handles fetching and parsing public data from a given New York City data source URL.

### Methods:

#### `__init__(self, start_url)`
  - **Description:** Initializes the NYCPublicDataFetcher instance with a starting URL.
  - **Parameters:** 
    - `start_url` (str): The URL to start data fetching from.
  - **Returns:** None.

#### `async fetch_content(self, url)`
  - **Description:** Asynchronously fetches content from a given URL.
  - **Parameters:** 
    - `url` (str): The URL to fetch content from.
  - **Returns:** 
    - String containing the fetched content, or an empty string if an error occurs.

#### `extract_view_ids_and_links(self, content)`
  - **Description:** Extracts view IDs and links from the fetched content.
  - **Parameters:** 
    - `content` (str): The HTML content to parse.
  - **Returns:** 
    - Dictionary of view IDs and their corresponding links.

#### `async run(self)`
  - **Description:** The main asynchronous method to run the fetching process.
  - **Returns:** 
    - Dictionary containing extracted data or an empty dictionary if no content is fetched.

---

## NYCEndpointFetcher Class

### Class Description:
Responsible for fetching specific endpoint URLs from the provided data dictionary.

### Methods:

#### `__init__(self)`
  - **Description:** Initializes the NYCEndpointFetcher instance.
  - **Returns:** None.

#### `async fetch_content(self, url)`
  - **Description:** Asynchronously fetches content from a URL and extracts API resource links.
  - **Parameters:** 
    - `url` (str): The URL to fetch content from.
  - **Returns:** 
    - API resource link as a string, or an empty string if an error occurs.

#### `bash_resource_link(self, file_name)`
  - **Description:** Executes a bash command to extract resource links from a file.
  - **Parameters:** 
    - `file_name` (str): The name of the file to extract resource links from.
  - **Returns:** 
    - Extracted resource link as a string, or None if an error occurs.

#### `async run(self, data_dict)`
  - **Description:** The main asynchronous method to run the endpoint fetching process.
  - **Parameters:** 
    - `data_dict` (dict): Dictionary of data to process.
  - **Returns:** 
    - Dictionary containing endpoints for each key in the input dictionary.

---

## NYCUrlFetcher Class

### Class Description:
Fetches URLs and content from a specified webpage, handling user-agent randomization.

### Methods:

#### `__init__(self)`
  - **Description:** Initializes the NYCUrlFetcher instance with a list of user agents and file path.
  - **Returns:** None.

#### `async fetch_content(self, url)`
  - **Description:** Asynchronously fetches HTML content from a URL using a random user agent.
  - **Parameters:** 
    - `url` (str): The URL to fetch content from.
  - **Returns:** 
    - HTML content as a string, or None if an error occurs.

#### `extract_data(self, html_content)`
  - **Description:** Extracts data from the HTML content.
  - **Parameters:** 
    - `html_content` (str): The HTML content to parse.
  - **Returns:** 
    - Dictionary of category names and their URLs.

#### `async run(self, url)`
  - **Description:** The main asynchronous method to run the URL fetching process.
  - **Parameters:** 
    - `url` (str): The URL to start fetching from.
  - **Returns:** 
    - Dictionary of extracted data or an empty dictionary if no content is fetched.
