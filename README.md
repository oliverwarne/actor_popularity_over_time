# Actor popularity over time  

Little tool to examine an actors popularity over time

## Installation

Use pip to install the requirements.txt. Then set an environment variable, OMDB_API_KEY, to a valid [The Movie Database API key](https://developers.themoviedb.org/3/getting-started/introduction). 
You'll also need to extract pi.json. This file contains the names and ids of all
actors in TMDb

```bash
pip install -r requirements.txt
export OMDB_API_KEY=xxxapikeyherexxx
tar -zxvf pi.json.tar.gz
```

## Usage
```bash
flask run
```
Then go to [localhost:5000](http://localhost:5000/)

## Screenshots
![Daniel Radcliffe graph](https://i.imgur.com/NjrBhgk.jpg)
![Meryl Streep graph](https://i.imgur.com/ke7OvSa.jpg)

## License
[MIT](https://choosealicense.com/licenses/mit/)
