DROP TABLE IF EXISTS dwh.topicpop_topics CASCADE;
DROP TABLE IF EXISTS dwh.topicpop CASCADE;
DROP TABLE IF EXISTS dwh.topicpop_by_week CASCADE;

CREATE TABLE dwh.topicpop_topics (
    id SERIAL NOT NULL,
    topic TEXT NOT NULL,
  	PRIMARY KEY (id)
);

CREATE TABLE dwh.topicpop (
    comment_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
  	PRIMARY KEY (comment_id),
    FOREIGN KEY (topic_id) REFERENCES dwh.topicpop_topics (id)
    FOREIGN KEY (comment_id) REFERENCES raw.comments (id)
);

CREATE TABLE dwh.topicpop_by_week (
    topic_id INTEGER NOT NULL,
    week SMALLINT NOT NULL,
    occurrence_count INTEGER NOT NULL,
    PRIMARY KEY (topic_id, week),
    FOREIGN KEY (topic_id) REFERENCES dwh.topicpop_topics (id)
);