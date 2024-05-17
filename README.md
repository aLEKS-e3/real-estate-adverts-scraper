# Real Estate Scraper

The Real Estate Scraper is a Python tool engineered to facilitate the gathering of data about real estate listings, including prices, locations, images, descriptions, and other related information. This scraper uses Selenium to automate the process of collecting data from the [realtylink.org](https://realtylink.org/en) website.

## Features

- **Price Extraction:** Collects the listing prices of properties.
- **Location Details:** Gathers location information for each property.
- **Image Downloading:** Fetches images associated with each listing.
- **Description Gathering:** Extracts detailed descriptions of properties.
- **Comprehensive Data Collection:** Retrieves all related information available for each listing.

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/aLEKS-e3/real-estate-adverts-scraper.git
```

2. Set up a virtual environment and install the required dependencies using pip:
```bash
python -m venv venv
source venv/bin/activate # For linux/macos
venv\Scripts\activate # For windows
pip install -r requirements.txt
```

3. Run the main script to gather data in the json file:
```bash
python main.py
```

**Note: You can customize the links, filenames, and the number of adverts to scrape as needed.**