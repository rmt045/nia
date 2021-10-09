# nia

## Overview
nia, or NASA Image Archiver, is an application written to assist in archiving images accessible via the NASA Images API. This project implements the REST API specified by the agency in [their documentation](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf).

## Table of Contents
- [Prerequisites](#Prerequisites)
- [Installation](#Installation)
- [Configuration](#Configuration)
- [Usage](#Usage)
- [Output](#Output)
- [Limitations](#Limitations)
- [Contributing](#Contributing)
- [ToDo](#ToDo)
- [License](#License)

## Prerequisites
- Bash
- Python 3.4+

## Installation
1. Ensure all prerequisites are met
2. Clone the repository using ```git clone https://github.com/rmt045/nia.git```
3. Make the ```nia``` Bash script executable via ```chmod +x nia```

## Configuration
nia uses a JSON configuration file to determine where to save images, where to store log files, where to store discovered search terms, etc. The format for this configuration file can be found in the included example ```nia_config.json``` file in this repository; simply replace the dummy values with directories and filepaths appropriate to your needs. Below is an explanation of what each configuration item does:

- ```base_url```: The URL used to access the NASA Images API and search for images that match the supplied query. For example, if the query is "q=moon", the search URL sent will be ```http://images-api.nasa.gov/search?media_type=image&q=moon```.
- ```page_json_dir```: The directory where search result from the above URL Will be stored. Using the same query example, this directory will store ```json_q=moon_(1-100)```.
- ```img_json_dir```: NASA's Images API returns links to a separate JSON file that contains direct links to the images found in the above JSON files. These files are stored as ```(nasa_id).json```.
- ```img_dir```: The base directory where all the images found in a search are stored. These files are stored as ```(nasa_id).(ext)```.
- ```log_dir```: The directory where log files are stored. Using the above query example, the log file will be stored as ```q=moon.log```.
- ```terms_filepath```: The full filepath where the discovered search terms are stored. Additional search terms are found as each JSON file in ```page_json_dir``` is scanned. Included in this file is a list of centers, keywords, locations, photographers, secondary creators, and albums which may be used in future queries.

## Usage
Run the script using ```python3 main.py (query) (configuration file)```. For example, if the query string is "q=moon" and the configuration file is "nia_config.json", use ```./nia q=moon nia_config.json```

## Output
While running, the application will output logging information to stdout, which can be redirected to a log file as desired. Note that this behavior will change in a future version (see [ToDo](#ToDo)). Once the application has finished processing the supplied query, those files will be stored in the ```pages_json_dir```, ```img_json_dir```, and ```img_dir``` as specified in [Configuration](#Configuration).

## Limitations
The NASA Images API will only allow a maximum of 100 pages of search results to be returned per request. At 100 images per request page, this means that a maximum of 10,000 images can be returned per search. Since some search terms include collections larger than this limit, additional searches must be used to return all images in said collection.

## Contributing
Any contributes are greatly appreciated. To contribute to the project, please do the following:

1. Fork the project
2. Create your feature branch using ```git checkout -b feature/yourfeature```
3. Commit your changes using ```git commit -m 'your notes here'```
4. Push your changes using ```git push origin feature/yourfeature```
5. Open a pull request

## ToDo
- Implement logging
- Implement SQL integration to store image metadata
	- Make ```page_json_dir``` and ```img_json_dir``` temporary storage while the DB will be the permanent storage
	- Have ```terms_filepath``` pull data from teh DB rather than the above directories
- Implement methods to sort images into subdirectories based on image metadata
- Implement a method to search albums
- Implement unit testing
- Code refactoring, optimization, etc

## License
This project uses the [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html).

