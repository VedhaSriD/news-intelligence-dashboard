-- ============================================================
-- NewsIntel — Seed: Trusted News Sources
-- Run after schema.sql + indexes.sql
-- ============================================================

INSERT INTO sources (name, slug, domain, newsapi_id, category, language, country, credibility_score, bias_label)
VALUES
  ('BBC News',              'bbc-news',             'bbc.com',               'bbc-news',             'world',      'en','gb', 0.95, 'center'),
  ('Reuters',               'reuters',               'reuters.com',            'reuters',               'world',      'en','us', 0.96, 'center'),
  ('Associated Press',      'associated-press',      'apnews.com',             'associated-press',      'world',      'en','us', 0.95, 'center'),
  ('The Guardian',          'the-guardian-uk',       'theguardian.com',        'the-guardian-uk',       'world',      'en','gb', 0.88, 'left'),
  ('Al Jazeera',            'al-jazeera-english',    'aljazeera.com',          'al-jazeera-english',    'world',      'en','qa', 0.82, 'center'),
  ('NPR',                   'npr',                   'npr.org',                'npr',                   'world',      'en','us', 0.90, 'center'),
  ('TechCrunch',            'techcrunch',            'techcrunch.com',          'techcrunch',            'technology', 'en','us', 0.85, 'center'),
  ('Wired',                 'wired',                 'wired.com',               'wired',                 'technology', 'en','us', 0.87, 'center'),
  ('The Verge',             'the-verge',             'theverge.com',            'the-verge',             'technology', 'en','us', 0.84, 'center'),
  ('Ars Technica',          'ars-technica',          'arstechnica.com',         'ars-technica',          'technology', 'en','us', 0.88, 'center'),
  ('MIT Technology Review', 'mit-tech-review',       'technologyreview.com',    NULL,                    'ai',         'en','us', 0.92, 'center'),
  ('Bloomberg',             'bloomberg',             'bloomberg.com',           'bloomberg',             'business',   'en','us', 0.90, 'center'),
  ('Financial Times',       'financial-times',       'ft.com',                  'financial-times',       'business',   'en','gb', 0.91, 'center'),
  ('The Economist',         'the-economist',         'economist.com',           NULL,                    'business',   'en','gb', 0.91, 'center'),
  ('New Scientist',         'new-scientist',         'newscientist.com',         'new-scientist',         'health',     'en','gb', 0.89, 'center'),
  ('Medical News Today',    'medical-news-today',    'medicalnewstoday.com',     NULL,                    'health',     'en','us', 0.81, 'center'),
  ('Times Higher Education','times-higher-education','timeshighereducation.com', NULL,                    'education',  'en','gb', 0.87, 'center'),
  ('ESPN',                  'espn',                  'espn.com',                'espn',                  'sports',     'en','us', 0.85, 'center'),
  ('BBC Sport',             'bbc-sport',             'bbc.com/sport',           'bbc-sport',             'sports',     'en','gb', 0.90, 'center'),
  ('Crunchbase News',       'crunchbase-news',       'news.crunchbase.com',      NULL,                    'startups',   'en','us', 0.82, 'center')
ON CONFLICT (slug) DO NOTHING;