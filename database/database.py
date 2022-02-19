import logging

import psycopg2

from configs import DATABASE_URL
from scraping.models import *
from .models import *


class Database:
    def __init__(self, logger: logging.Logger):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cur = self.conn.cursor()
        self.logger = logger

        self.logger.info('a connection to the database has been established')

    def add_socialnet(self, socialnet: SocialnetScrapingModel) -> SocialnetDatabaseModel:
        self.cur.execute('INSERT INTO socialnet (name) '
                         'VALUES (%s) '
                         'RETURNING id',
                         (socialnet.name,))
        self.conn.commit()

        socialnet_id = self.cur.fetchone()[0]
        new_socialnet = SocialnetDatabaseModel(
            id=socialnet_id,
            name=socialnet.name
        )

        self.logger.info('socialnet information added to the database: %s', new_socialnet)
        return new_socialnet

    def get_socialnet(self, socialnet: SocialnetScrapingModel) -> SocialnetDatabaseModel:
        self.cur.execute('SELECT id, name '
                         'FROM socialnet '
                         'WHERE name = %s',
                         (socialnet.name,))
        query_result = self.cur.fetchone()
        if query_result is None:
            return self.add_socialnet(socialnet)
        return SocialnetDatabaseModel(
            id=query_result[0],
            name=query_result[1]
        )

    def add_entity(self, entity: EntityScrapingModel) -> EntityDatabaseModel:
        self.cur.execute('INSERT INTO entity (name, is_organization) '
                         'VALUES (%s, %s) '
                         'RETURNING id',
                         (entity.name, entity.is_organization,))
        self.conn.commit()

        entity_id = self.cur.fetchone()[0]
        new_entity = EntityDatabaseModel(
            id=entity_id,
            name=entity.name,
            is_organization=entity.is_organization
        )

        self.logger.info('entity information added to the database: %s', new_entity)
        return new_entity

    def get_entity(self, entity: EntityScrapingModel) -> EntityDatabaseModel:
        self.cur.execute('SELECT id, name, is_organization '
                         'FROM entity '
                         'WHERE name = %s',
                         (entity.name,))
        query_result = self.cur.fetchone()
        if query_result is None:
            return self.add_entity(entity)
        return EntityDatabaseModel(
            id=query_result[0],
            name=query_result[1],
            is_organization=query_result[2]
        )

    def add_account(self, account: AccountScrapingModel) -> AccountDatabaseModel:
        socialnet = self.get_socialnet(account.socialnet)
        entity = self.get_entity(account.entity)

        self.cur.execute('INSERT INTO account (url, entity_id, socialnet_id) '
                         'VALUES (%s, %s, %s) '
                         'RETURNING id',
                         (account.url, entity.id, socialnet.id,))
        self.conn.commit()

        account_id = self.cur.fetchone()[0]
        new_account = AccountDatabaseModel(
            id=account_id,
            url=account.url,
            entity_id=entity.id,
            socialnet_id=socialnet.id
        )

        self.logger.info('account information added to the database: %s', new_account)
        return new_account

    def get_account(self, account: AccountScrapingModel) -> AccountDatabaseModel:
        self.cur.execute('SELECT id, url, entity_id, socialnet_id '
                         'FROM account '
                         'WHERE url = %s',
                         (account.url,))
        query_result = self.cur.fetchone()
        if query_result is None:
            return self.add_account(account)
        return AccountDatabaseModel(
            id=query_result[0],
            url=query_result[1],
            entity_id=query_result[2],
            socialnet_id=query_result[3]
        )

    def add_post(self, post: PostScrapingModel) -> PostDatabaseModel:
        account = self.get_account(post.account)

        self.cur.execute(
            'INSERT INTO post (url, owner_id, picture, text, time, likes, tags, links) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '
            'RETURNING id',
            (post.url, account.id, post.picture, post.text, post.time, post.likes, post.tags, post.links))
        self.conn.commit()

        post_id = self.cur.fetchone()[0]
        new_post = PostDatabaseModel(
            id=post_id,
            url=post.url,
            owner_id=account.id,
            picture=post.picture,
            text=post.text,
            time=post.time,
            likes=post.likes,
            tags=post.tags,
            links=post.links
        )

        self.logger.info('post information added to the database: %s', new_post)
        return new_post

    def get_posts_by_urls(self, *urls) -> List[PostDatabaseModel]:
        if not urls:
            return []

        self.cur.execute('SELECT id, url, owner_id, picture, text, time, likes, tags, links '
                         'FROM post '
                         'WHERE url IN %s', (urls,))

        query_result = self.cur.fetchall()
        if query_result is None:
            return []

        array_result: List[PostDatabaseModel] = []

        for item in query_result:
            array_result.append(PostDatabaseModel(
                id=item[0],
                url=item[1],
                owner_id=item[2],
                picture=item[3],
                text=item[4],
                time=item[5],
                likes=item[6],
                tags=item[7],
                links=item[8]
            ))
        return array_result

    def get_post(self, post: PostScrapingModel) -> PostDatabaseModel:
        self.cur.execute('SELECT id, url, owner_id, picture, text, time, likes, tags, links '
                         'FROM post '
                         'WHERE url = %s',
                         (post.url,))
        query_result = self.cur.fetchone()
        if query_result is None:
            return self.add_post(post)
        return PostDatabaseModel(
            id=query_result[0],
            url=query_result[1],
            owner_id=query_result[2],
            picture=query_result[3],
            text=query_result[4],
            time=query_result[5],
            likes=query_result[6],
            tags=query_result[7],
            links=query_result[8]
        )

    def add_comment(self, comment: CommentScrapingModel, post_id: int) -> CommentDatabaseModel:
        self.cur.execute(
            'INSERT INTO comment (url, post_id, text, owner_url, time, likes, tags, links) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '
            'RETURNING id',
            (comment.url, post_id, comment.text, comment.owner_url, comment.time, comment.likes,
             comment.tags, comment.links))
        self.conn.commit()

        comment_id = self.cur.fetchone()[0]
        new_comment = CommentDatabaseModel(
            id=comment_id,
            url=comment.url,
            post_id=post_id,
            text=comment.text,
            owner_url=comment.owner_url,
            time=comment.time,
            likes=comment.likes,
            tags=comment.tags,
            links=comment.links
        )

        self.logger.info('comment information added to the database: %s', new_comment)
        return new_comment

    def get_comments_by_urls(self, *urls) -> List[CommentDatabaseModel]:
        if not urls:
            return []

        self.cur.execute('SELECT id, url, post_id, text, owner_url, time, likes, tags, links '
                         'FROM comment '
                         'WHERE url IN %s', (urls,))

        query_result = self.cur.fetchall()

        if query_result is None:
            return []

        array_result: List[CommentDatabaseModel] = []

        for item in query_result:
            array_result.append(CommentDatabaseModel(
                id=item[0],
                url=item[1],
                post_id=item[2],
                text=item[3],
                owner_url=item[4],
                time=item[5],
                likes=item[6],
                tags=item[7],
                links=item[8]
            ))
        return array_result

    def get_comment(self, comment: CommentScrapingModel, post_id: int) -> CommentDatabaseModel:
        self.cur.execute('SELECT id, url, post_id, text, owner_url, time, likes, tags, links '
                         'FROM comment '
                         'WHERE url = %s AND post_id = %s',
                         (comment.url, post_id,))
        query_result = self.cur.fetchone()
        if query_result is None:
            return self.add_comment(comment, post_id)
        return CommentDatabaseModel(
            id=query_result[0],
            url=query_result[1],
            post_id=query_result[2],
            text=query_result[3],
            owner_url=query_result[4],
            time=query_result[5],
            likes=query_result[6],
            tags=query_result[7],
            links=query_result[8]
        )

    def add_posts_with_comments(self, scraped_posts: List[PostScrapingModel]):
        self.logger.info('the process of adding information to the database has started')

        for scraped_post in scraped_posts:
            db_post = self.get_post(scraped_post)
            for comment in scraped_post.comments:
                self.get_comment(comment, db_post.id)

        self.logger.info('the process of adding information to the database has ended')

    def close_connection(self):
        self.cur.close()
        self.conn.close()

        self.logger.info('a connection to the database has been closed')
