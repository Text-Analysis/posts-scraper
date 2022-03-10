import psycopg2

from models import *


class Database:

    def __init__(self, database_url: str):
        self.conn = psycopg2.connect(database_url)
        self.cur = self.conn.cursor()

        print('a connection to the database has been established')

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

        print('socialnet information added to the database: %s', new_socialnet.name)
        return new_socialnet

    def update_socialnet(self, socialnet: SocialnetScrapingModel) -> SocialnetDatabaseModel:
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

        print('entity information added to the database: %s', new_entity.name)
        return new_entity

    def update_entity(self, entity: EntityScrapingModel) -> EntityDatabaseModel:
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
        socialnet = self.update_socialnet(account.socialnet)
        entity = self.update_entity(account.entity)

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

        print('account information added to the database: %s', new_account.url)
        return new_account

    def update_account(self, account: AccountScrapingModel) -> AccountDatabaseModel:
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
        account = self.update_account(post.account)

        self.cur.execute(
            'INSERT INTO post (url, owner_id, picture, text, time, likes, tags, links) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '
            'RETURNING id',
            (post.url, account.id, post.picture, post.text, post.time, post.likes, post.tags, post.links,))
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

        print('post information added to the database: %s', new_post.url)
        return new_post

    def update_post(self, post: PostScrapingModel) -> PostDatabaseModel:
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

    def get_user_posts(self, user_url: str) -> List[PostDatabaseModel]:
        self.cur.execute('SELECT id '
                         'FROM account '
                         'WHERE url = %s',
                         (user_url,))

        account_id = self.cur.fetchone()[0]
        if account_id is None:
            return []

        self.cur.execute('SELECT id, url, owner_id, picture, text, time, likes, tags, links '
                         'FROM post '
                         'WHERE owner_id = %s '
                         'ORDER BY time',
                         (account_id,))

        query_result = self.cur.fetchall()

        return self.__get_posts_from_query(query_result)

    def get_posts_by_urls(self, urls) -> List[PostDatabaseModel]:
        if not urls:
            return []

        self.cur.execute('SELECT id, url, owner_id, picture, text, time, likes, tags, links '
                         'FROM post '
                         'WHERE url IN %s '
                         'ORDER BY time',
                         (urls,))

        query_result = self.cur.fetchall()

        return self.__get_posts_from_query(query_result)

    @staticmethod
    def __get_posts_from_query(query_result: List) -> List[PostDatabaseModel]:
        if query_result is None:
            return []

        posts: List[PostDatabaseModel] = []

        for item in query_result:
            posts.append(PostDatabaseModel(
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

        return posts

    def add_comment(self, comment: CommentScrapingModel, post_id: int) -> CommentDatabaseModel:
        self.cur.execute(
            'INSERT INTO comment (url, post_id, text, owner_url, time, likes, tags, links) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '
            'RETURNING id',
            (comment.url, post_id, comment.text, comment.owner_url, comment.time, comment.likes,
             comment.tags, comment.links,))
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

        print('comment information added to the database: %s', new_comment.url)
        return new_comment

    def get_comment(self, comment_id: int) -> CommentDatabaseModel:
        self.cur.execute('SELECT id, url, post_id, text, owner_url, time, likes, tags, links '
                         'FROM comment '
                         'WHERE id = %s',
                         (comment_id,))

        query_result = self.cur.fetchone()
        if query_result is None:
            raise Exception('comment not found')

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

    def update_comment(self, comment: CommentScrapingModel, post_id: int) -> CommentDatabaseModel:
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

    def get_user_posts_comments(self, user_url: str) -> List[CommentDatabaseModel]:
        self.cur.execute('SELECT id '
                         'FROM account '
                         'WHERE url = %s',
                         (user_url,))

        account_id = self.cur.fetchone()[0]
        if account_id is None:
            return []

        self.cur.execute('SELECT id '
                         'FROM post '
                         'WHERE owner_id = %s '
                         'ORDER BY time',
                         (account_id,))

        query_result = self.cur.fetchall()
        if query_result is None:
            return []

        posts_ids = tuple(item[0] for item in query_result)

        return self.get_comments_by_posts_ids(posts_ids)

    def get_comments_by_posts_ids(self, posts_ids) -> List[CommentDatabaseModel]:
        if not posts_ids:
            return []

        self.cur.execute('SELECT id, url, post_id, text, owner_url, time, likes, tags, links '
                         'FROM comment '
                         'WHERE post_id IN %s '
                         'ORDER BY time',
                         (posts_ids,))

        query_result = self.cur.fetchall()

        return self.__get_comments_from_query(query_result)

    def get_comments_by_urls(self, urls) -> List[CommentDatabaseModel]:
        if not urls:
            return []

        self.cur.execute('SELECT id, url, post_id, text, owner_url, time, likes, tags, links '
                         'FROM comment '
                         'WHERE url IN %s '
                         'ORDER BY time',
                         (urls,))

        query_result = self.cur.fetchall()

        return self.__get_comments_from_query(query_result)

    @staticmethod
    def __get_comments_from_query(query_result: List) -> List[CommentDatabaseModel]:
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

    def add_posts_with_comments(self, scraped_posts: List[PostScrapingModel]):
        print('the process of adding information to the database has started')

        for scraped_post in scraped_posts:
            db_post = self.update_post(scraped_post)
            for comment in scraped_post.comments:
                self.update_comment(comment, db_post.id)

        print('the process of adding information to the database has ended')

    def close_connection(self):
        self.cur.close()
        self.conn.close()

        print('a connection to the database has been closed')

    @staticmethod
    def remove_links_from_comment(comment: CommentDatabaseModel) -> CommentDatabaseModel:
        for link in comment.links:
            comment.text = comment.text.replace(f'@{link}', '')
        return comment
