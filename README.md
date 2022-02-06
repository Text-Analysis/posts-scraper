# Posts scraper

posts-scraper is a command-line application written in Python for collecting information about user posts on Instagram
for the selected time period. The collected information is stored in the PostgreSQL database.

## Examples of scraping results

`socialnet` table:

| id | name |
|----------------|---------|
| 1 | Instagram |

`entity` table:

| id | name | is_organization |
|----------------|---------|----------------|
| 1 | Pavel Kurmyza | f |
| 2 | Danil Abanin | f |

`account` table:

| id | url | entity_id | socialnet_id |
|---|---|---|---|
| 1 | https://www.instagram.com/tmrrwnxtsn/ | 1 | 1 |
| 2 | https://www.instagram.com/mouzzefire/ | 2 | 1 |

`post` table:

| id | url | owner_id | picture | text | time | likes |
|---|---|---|---|---|---|---|
| 1 | https://www.instagram.com/p/CZCD_27sxI3/ | 1 | https://instagram.fura3-1.fna.fbcdn.net/v/t51.2885-15/e35/272301986_1104448550356719_7483000766698731388_n.webp.jpg?_nc_ht=instagram.fura3-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=rU3YtAfaP4MAX_T5xCE&edm=ALQROFkBAAAA&ccb=7-4&ig_cache_key=Mjc1Njc4MzUwNDM1NDM4MjM5MQ%3D%3D.2-ccb7-4&oh=00_AT_SIE3Oq4WRQCFl63GcHK_EG1Yf0SBT4Yggrc4-1vqSkg&oe=62035CFF&_nc_sid=30a2ef | Hello, it's me | 2022-01-22 13:03:44+00 | 15 |

`comment` table:

| id | url | post_id | text | owner_url | time | likes |
|---|---|---|---|---|---|---|
| 1 | https://www.instagram.com/p/CZCD_27sxI3/c/17993429686418706/ | 1 | Nice!! | https://www.instagram.com/mouzzefire/ | 2022-01-22 13:40:44+00 | 2 |

## Preparing

1. Create PostgreSQL database or use existing.
2. Apply [migrations](https://github.com/golang-migrate/migrate) to this database (see `migrations` folder).
3. Create an account in Instagram or use existing (We recommend using new because account may be blocked by Instagram
   because of many requests to this platform).

## Dependencies

Python >= 3.7

## Setup

1. Clone project files from GitHub:

`git clone https://github.com/Text-Analysis/posts-scraper.git`

2. Move to the project directory:

`cd posts-scraper`

3. Create virtual environment:

`pip install virtualenv`

`python -m virtualenv venv`

4. Activate the virtual environment:

`./venv/Scripts/activate`

5. Install the project requirements:

`pip install -r requirements.txt`

## .env configuration fields

Create `.env` file in the root of project (see: `.env.example`).

```
DATABASE_URL=                    # PostgreSQL connection string
INSTAGRAM_LOGIN=                 # Instagram account login
INSTAGRAM_PASSWORD=              # Instagram account password
TZ=                              # Timezone (e.g. Europe/Samara)
```

## Usage

To scrape a user's posts information:

`python main.py <username> <start_time> <end_time>`

For example:

`python main.py tmrrwnxtsn 2021-12-30 2022-02-05`

*NOTE: To scrape a private user's posts you must be an approved follower.*

To see help message:

`python main.py --help`

Output:

```
usage: main.py [-h] username start_time end_time

Python module for collecting information about user posts on Instagram for the
selected time period. The collected information is saved in the PostgreSQL
database.

positional arguments:
  username    the account whose posts data will be saved into the PostgreSQL
              database
  start_time  the beginning of the publication time period (in the format:
              2022-01-01)
  end_time    the end of the publication time period (in the format:
              2022-01-01)

optional arguments:
  -h, --help  show this help message and exit
```

At the end of the work, deactivate the virtual environment:

`deactivate`
