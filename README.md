<p align="center">
    <img src="images/fauxsnow-logo.png">
</p>

---

This repo contains the source code and documentation powering [fauxsnow.org](https://fauxsnow.org/).

## Overview

**fauxsnow.org** is a ski resort weather forecasting app that focuses on snow-starved 
resorts in the US Southeast and Midwest. In addition to forecasting snow, this
app also forecasts snowmaking conditions.

The purppose of this app is to provide a useful service while generating awareness
about the impact of climate change on recreation opportunities.


## Key Features

- Save a list of favorite resorts
- Filter to see All, Open or Favorite resorts
- Cumulative Snowfall and Number of Snowmaking Days for last 3 days
- Current conditions
- Forecasted Snow, Snowmaking Conditions, and Icy Conditions for the next 5 days


## Getting Started


### Prerequisites

1. Git
1. Python: any version 3.9 or later.
1. pip



### Installation

```
# Clone this repository
$ git clone https://github.com/jeff-dillon/fauxsnow.org.git

# navigate into the repository
$ cd fauxsnow.org

# create a virtual environment
$ python3 -m venv venv

# activate the virtual environment
$ source venv/bin/activate

# install dependencies
$ python -m pip install requirements.txt
```


### Running Locally

```
# initialize the database 
$ flask --app fauxsnow init-db

# run the unit tests 
$ PYTHONPATH=. pytest

# start the application server
$ flask --app fauxsnow --debug run

# open the site in your browser: http://127.0.0.1:5000/
```



## License

MIT license found in the `LICENSE` file.



## Contributing

Contributions are welcome. 

1. Choose an open issue
1. Ask questions in the issue if needed
1. Fork the repo
1. Create your branch (git checkout -b feature/fooBar)
1. Commit your changes (git commit -m 'Add some fooBar')
1. Push to the branch (git push origin feature/fooBar)
1. Create a new Pull Request linked to the issue
