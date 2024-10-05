CREATE SCHEMA dwh;

DROP TABLE IF EXISTS dwh.termpop_terms CASCADE;
DROP TABLE IF EXISTS dwh.termpop_agg CASCADE;

CREATE TABLE dwh.termpop_terms (
    id SERIAL,
    term TEXT,
  	PRIMARY KEY (id)
);

CREATE TABLE dwh.termpop_agg (
    term_id INTEGER NOT NULL,
    year SMALLINT NOT NULL,
    month SMALLINT NOT NULL,
    week SMALLINT NOT NULL,
    occurrence_count INTEGER NOT NULL,
    PRIMARY KEY (term_id, year, month, week),
    FOREIGN KEY (term_id) REFERENCES dwh.termpop_terms (id)
);


DELETE FROM dwh.termpop_agg;
INSERT INTO dwh.termpop_agg (term_id, year, month, week, occurrence_count)
SELECT 
    t.id AS term_id,
    EXTRACT(YEAR FROM c.time) AS year,
    EXTRACT(MONTH FROM c.time) AS month,
    EXTRACT(WEEK FROM c.time) AS week,
    COUNT(*) AS occurrence_count
FROM 
    dwh.termpop_terms t
JOIN 
    raw.comments c
ON 
    c.text ILIKE '%' || t.term || '%'
GROUP BY 
    t.id,
    EXTRACT(YEAR FROM c.time), 
    EXTRACT(MONTH FROM c.time), 
    EXTRACT(WEEK FROM c.time)
ORDER BY 
    t.id, year, month, week;
