# fauxsnow.org

This repo contains the source code and documentation powering [fauxsnow.org](https://fauxsnow.org/).

## Getting Started

### Prerequisites

1. Git
1. Python: any version 3.9 or later.
1. pip

### Installation

1. `cd fauxsnow.org` to go into the project root
1. create a virtual enviornment for loading dependencies
1. `pip install requirements.txt` to install the dependecies

### Running Locally

1. initialize the database: `flask --app fauxsnow init-db`
1. run the unit tests `pytest`
1. start the application server: `flask --app fauxsnow --debug run"`
1. open `http://127.0.0.1:5000/main` to open the site in your browser
## Contributing

Contact the repo owner directly to ask about contributing to the project.

## License

MIT license found in the `LICENSE` file.