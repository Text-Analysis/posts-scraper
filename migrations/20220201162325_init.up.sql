CREATE TABLE IF NOT EXISTS socialnet
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS entity
(
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(150) NOT NULL,
    is_organization BOOLEAN      NOT NULL
);

CREATE TABLE IF NOT EXISTS account
(
    id           SERIAL PRIMARY KEY,
    url          TEXT    NOT NULL UNIQUE,
    entity_id    INTEGER NOT NULL,
    socialnet_id INTEGER NOT NULL,
    CONSTRAINT fk_socialnet_account FOREIGN KEY (socialnet_id) REFERENCES socialnet (id),
    CONSTRAINT fk_entity_account FOREIGN KEY (entity_id) REFERENCES entity (id)
);

CREATE TABLE IF NOT EXISTS post
(
    id              SERIAL PRIMARY KEY,
    url             TEXT                     NOT NULL UNIQUE,
    owner_id        INTEGER                  NOT NULL,
    picture         TEXT,
    text            TEXT,
    created_at_time TIMESTAMP WITH TIME ZONE NOT NULL,
    likes           INTEGER                  NOT NULL,
    CONSTRAINT fk_account_post FOREIGN KEY (owner_id) REFERENCES account (id)
);

CREATE TABLE IF NOT EXISTS comment
(
    id              SERIAL PRIMARY KEY,
    url             TEXT                     NOT NULL UNIQUE,
    post_id         INTEGER                  NOT NULL,
    text            TEXT                     NOT NULL,
    owner_url       TEXT                     NOT NULL,
    created_at_time TIMESTAMP WITH TIME ZONE NOT NULL,
    likes           INTEGER                  NOT NULL,
    CONSTRAINT fk_post_comment FOREIGN KEY (post_id) REFERENCES post (id)
);