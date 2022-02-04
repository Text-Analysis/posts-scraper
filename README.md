# Posts scraper

Python module for collecting information about user posts on Instagram. The collected information is placed in the
PostgreSQL database.

## Results examples

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
2. Apply migrations to this database (see: `migrations`)
3. Create an account in Instagram or use existing (We recommend use new because account may be blocked by Instagram.
   because of many requests to this platform)

## Dependencies

Python >= 3.7

## Setup

````
$ git clone https://github.com/Text-Analysis/posts-scraper.git
$ cd posts-scraper
$ pip install -r requirements.txt
````

## .env configuration fields

Create `.env` file in the root of project (see: `.env.example`).

````
DATABASE_URL=                    # PostgreSQL connection string
INSTAGRAM_LOGIN=                 # Instagram account login
INSTAGRAM_PASSWORD=              # Instagram account password
TZ=                              # Timezone (e.g. Europe/Samara)
````

## Usage

````
python main.py
````

## References

[1] https://github.com/instaloader/instaloader

[2] https://github.com/golang-migrate/migrate