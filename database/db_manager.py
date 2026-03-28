"""
QI1489 Android — SQLite Database Manager
All CRUD operations for users, questions, scores, settings, disclaimer.
"""
import sqlite3
import os
import hashlib
import secrets
from datetime import datetime

from kivy.utils import platform


def get_db_path():
    if platform == 'android':
        path = os.environ.get('ANDROID_PRIVATE', '/data/data/org.smjxgame.qi1489')
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, 'qi1489.db')
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, 'qi1489.db')


def _hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    h = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    return f"{salt}${h}"


def _verify_password(password, stored):
    try:
        salt, h = stored.split('$', 1)
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest() == h
    except Exception:
        return False


class DatabaseManager:
    def __init__(self):
        self.db_path = get_db_path()

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    # ------------------------------------------------------------------ #
    #  INIT
    # ------------------------------------------------------------------ #
    def initialize(self):
        with self._conn() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT UNIQUE NOT NULL,
                email      TEXT UNIQUE NOT NULL,
                password   TEXT NOT NULL,
                is_admin   INTEGER DEFAULT 0,
                is_active  INTEGER DEFAULT 1,
                language   TEXT DEFAULT 'en',
                total_score INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS questions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                category    TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                question_en TEXT NOT NULL,
                question_fr TEXT NOT NULL,
                answer      TEXT NOT NULL,
                option1     TEXT NOT NULL,
                option2     TEXT NOT NULL,
                option3     TEXT NOT NULL,
                difficulty  TEXT DEFAULT 'medium',
                country     TEXT DEFAULT '',
                continent   TEXT DEFAULT '',
                hint_en     TEXT DEFAULT '',
                hint_fr     TEXT DEFAULT '',
                source      TEXT DEFAULT 'manual',
                is_active   INTEGER DEFAULT 1,
                times_shown INTEGER DEFAULT 0,
                times_correct INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now')),
                updated_at  TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS scores (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER REFERENCES users(id) ON DELETE SET NULL,
                guest_token     TEXT,
                guest_name      TEXT DEFAULT 'Guest',
                category        TEXT,
                continent       TEXT DEFAULT 'Worldwide',
                score           INTEGER DEFAULT 0,
                max_possible    INTEGER DEFAULT 0,
                questions_answered INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                time_played     INTEGER DEFAULT 0,
                created_at      TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS settings (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                description TEXT DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS disclaimer (
                id         INTEGER PRIMARY KEY CHECK (id = 1),
                text_en    TEXT DEFAULT '',
                text_fr    TEXT DEFAULT '',
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_questions_category
                ON questions(category, is_active);
            CREATE INDEX IF NOT EXISTS idx_questions_continent
                ON questions(continent, is_active);
            CREATE INDEX IF NOT EXISTS idx_scores_category
                ON scores(category, score DESC);
            """)

            # Seed defaults
            conn.execute("""
                INSERT OR IGNORE INTO settings(key, value, description) VALUES
                ('questions_per_game', '10', 'Questions per game session'),
                ('question_time',      '15', 'Seconds per question')
            """)
            conn.execute("""
                INSERT OR IGNORE INTO disclaimer(id, text_en, text_fr) VALUES
                (1,
                 'We hope that you enjoyed our game, donate to finance more +237676262622',
                 'Nous esperons que vous avez joue avec QI1489, soutenez le developpeur par un don au +237676262622')
            """)
            # Default admin account
            if not conn.execute("SELECT 1 FROM users WHERE username='admin'").fetchone():
                pw = _hash_password('admin@QI1489')
                conn.execute(
                    "INSERT INTO users(username,email,password,is_admin) VALUES(?,?,?,1)",
                    ('admin', 'admin@qi1489.com', pw)
                )
            conn.commit()

    # ------------------------------------------------------------------ #
    #  SETTINGS
    # ------------------------------------------------------------------ #
    def get_setting(self, key, default=None):
        with self._conn() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
            return row['value'] if row else default

    def set_setting(self, key, value, description=''):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO settings(key,value,description) VALUES(?,?,?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, str(value), description)
            )
            conn.commit()

    # ------------------------------------------------------------------ #
    #  DISCLAIMER
    # ------------------------------------------------------------------ #
    def get_disclaimer(self):
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM disclaimer WHERE id=1").fetchone()
            return dict(row) if row else {'text_en': '', 'text_fr': ''}

    def save_disclaimer(self, text_en, text_fr):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO disclaimer(id,text_en,text_fr,updated_at) VALUES(1,?,?,?) "
                "ON CONFLICT(id) DO UPDATE SET text_en=excluded.text_en, "
                "text_fr=excluded.text_fr, updated_at=excluded.updated_at",
                (text_en, text_fr, datetime.utcnow().isoformat())
            )
            conn.commit()

    # ------------------------------------------------------------------ #
    #  USERS
    # ------------------------------------------------------------------ #
    def create_user(self, username, email, password, is_admin=False):
        try:
            with self._conn() as conn:
                pw = _hash_password(password)
                conn.execute(
                    "INSERT INTO users(username,email,password,is_admin) VALUES(?,?,?,?)",
                    (username.strip(), email.strip().lower(), pw, 1 if is_admin else 0)
                )
                conn.commit()
                return True, 'Account created.'
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return False, 'Username already taken.'
            return False, 'Email already registered.'

    def authenticate_user(self, username_or_email, password):
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE (username=? OR email=?) AND is_active=1",
                (username_or_email, username_or_email.lower())
            ).fetchone()
            if row and _verify_password(password, row['password']):
                return dict(row)
        return None

    def get_user(self, user_id):
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
            return dict(row) if row else None

    def get_all_users(self, search=''):
        with self._conn() as conn:
            if search:
                rows = conn.execute(
                    "SELECT * FROM users WHERE username LIKE ? OR email LIKE ? ORDER BY created_at DESC",
                    (f'%{search}%', f'%{search}%')
                ).fetchall()
            else:
                rows = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
            return [dict(r) for r in rows]

    def toggle_user_active(self, user_id):
        with self._conn() as conn:
            conn.execute("UPDATE users SET is_active = 1 - is_active WHERE id=?", (user_id,))
            conn.commit()

    def toggle_user_admin(self, user_id):
        with self._conn() as conn:
            conn.execute("UPDATE users SET is_admin = 1 - is_admin WHERE id=?", (user_id,))
            conn.commit()

    def delete_user(self, user_id):
        with self._conn() as conn:
            conn.execute("UPDATE scores SET user_id=NULL WHERE user_id=?", (user_id,))
            conn.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()

    def update_user_stats(self, user_id, score_delta, games_delta=1):
        with self._conn() as conn:
            conn.execute(
                "UPDATE users SET total_score=total_score+?, games_played=games_played+? WHERE id=?",
                (score_delta, games_delta, user_id)
            )
            conn.commit()

    # ------------------------------------------------------------------ #
    #  QUESTIONS
    # ------------------------------------------------------------------ #
    def get_questions(self, category, continent='Worldwide', count=10, lang='en'):
        with self._conn() as conn:
            if continent and continent != 'Worldwide':
                rows = conn.execute(
                    "SELECT * FROM questions WHERE category=? AND continent=? AND is_active=1 "
                    "ORDER BY RANDOM() LIMIT ?",
                    (category, continent, count)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM questions WHERE category=? AND is_active=1 "
                    "ORDER BY RANDOM() LIMIT ?",
                    (category, count)
                ).fetchall()
            return [dict(r) for r in rows]

    def get_geography_questions(self, count=10, lang='en'):
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM questions WHERE category='geography' AND is_active=1 "
                "ORDER BY RANDOM() LIMIT ?",
                (count,)
            ).fetchall()
            return [dict(r) for r in rows]

    def get_all_questions(self, category='', continent='', search='', page=1, per_page=25):
        with self._conn() as conn:
            conditions = ["1=1"]
            params = []
            if category:
                conditions.append("category=?")
                params.append(category)
            if continent:
                conditions.append("continent=?")
                params.append(continent)
            if search:
                conditions.append("(question_en LIKE ? OR answer LIKE ?)")
                params.extend([f'%{search}%', f'%{search}%'])
            where = " AND ".join(conditions)
            total = conn.execute(f"SELECT COUNT(*) FROM questions WHERE {where}", params).fetchone()[0]
            offset = (page - 1) * per_page
            rows = conn.execute(
                f"SELECT * FROM questions WHERE {where} ORDER BY updated_at DESC LIMIT ? OFFSET ?",
                params + [per_page, offset]
            ).fetchall()
            return [dict(r) for r in rows], total

    def get_question(self, qid):
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM questions WHERE id=?", (qid,)).fetchone()
            return dict(row) if row else None

    def get_distinct_categories(self):
        with self._conn() as conn:
            rows = conn.execute("SELECT DISTINCT category FROM questions ORDER BY category").fetchall()
            return [r[0] for r in rows]

    def get_distinct_continents(self):
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT DISTINCT continent FROM questions WHERE continent != '' ORDER BY continent"
            ).fetchall()
            return [r[0] for r in rows]

    def create_question(self, data):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO questions(category,subcategory,question_en,question_fr,answer,"
                "option1,option2,option3,difficulty,country,continent,hint_en,hint_fr,source,is_active) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)",
                (data.get('category'), data.get('subcategory', ''),
                 data.get('question_en'), data.get('question_fr', data.get('question_en')),
                 data.get('answer'), data.get('option1'), data.get('option2'), data.get('option3'),
                 data.get('difficulty', 'medium'), data.get('country', ''),
                 data.get('continent', ''), data.get('hint_en', ''), data.get('hint_fr', ''),
                 data.get('source', 'admin'))
            )
            conn.commit()

    def update_question(self, qid, data):
        with self._conn() as conn:
            conn.execute(
                "UPDATE questions SET category=?,subcategory=?,question_en=?,question_fr=?,"
                "answer=?,option1=?,option2=?,option3=?,difficulty=?,country=?,continent=?,"
                "hint_en=?,hint_fr=?,updated_at=? WHERE id=?",
                (data.get('category'), data.get('subcategory', ''),
                 data.get('question_en'), data.get('question_fr', data.get('question_en')),
                 data.get('answer'), data.get('option1'), data.get('option2'), data.get('option3'),
                 data.get('difficulty', 'medium'), data.get('country', ''),
                 data.get('continent', ''), data.get('hint_en', ''), data.get('hint_fr', ''),
                 datetime.utcnow().isoformat(), qid)
            )
            conn.commit()

    def delete_question(self, qid):
        with self._conn() as conn:
            conn.execute("DELETE FROM questions WHERE id=?", (qid,))
            conn.commit()

    def toggle_question(self, qid):
        with self._conn() as conn:
            conn.execute("UPDATE questions SET is_active = 1 - is_active WHERE id=?", (qid,))
            conn.commit()

    def upsert_question(self, data):
        """Used by update_service. Match on (category, question_en)."""
        with self._conn() as conn:
            existing = conn.execute(
                "SELECT id FROM questions WHERE category=? AND question_en=?",
                (data['category'], data['question_en'])
            ).fetchone()
            if existing:
                conn.execute(
                    "UPDATE questions SET question_fr=?,answer=?,option1=?,option2=?,option3=?,"
                    "difficulty=?,country=?,continent=?,hint_en=?,hint_fr=?,updated_at=? WHERE id=?",
                    (data.get('question_fr', data['question_en']),
                     data['answer'], data['option1'], data['option2'], data['option3'],
                     data.get('difficulty', 'medium'), data.get('country', ''),
                     data.get('continent', ''), data.get('hint_en', ''), data.get('hint_fr', ''),
                     datetime.utcnow().isoformat(), existing['id'])
                )
                return 'updated'
            else:
                conn.execute(
                    "INSERT INTO questions(category,question_en,question_fr,answer,option1,option2,"
                    "option3,difficulty,country,continent,hint_en,hint_fr,source,is_active) "
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,1)",
                    (data['category'], data['question_en'],
                     data.get('question_fr', data['question_en']),
                     data['answer'], data['option1'], data['option2'], data['option3'],
                     data.get('difficulty', 'medium'), data.get('country', ''),
                     data.get('continent', ''), data.get('hint_en', ''), data.get('hint_fr', ''),
                     data.get('source', 'auto'))
                )
                return 'added'

    def increment_question_shown(self, qid):
        with self._conn() as conn:
            conn.execute("UPDATE questions SET times_shown=times_shown+1 WHERE id=?", (qid,))
            conn.commit()

    # ------------------------------------------------------------------ #
    #  SCORES
    # ------------------------------------------------------------------ #
    def save_score(self, user_id, guest_token, guest_name, category, continent,
                   score, max_possible, questions_answered, correct_answers, time_played):
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO scores(user_id,guest_token,guest_name,category,continent,score,"
                "max_possible,questions_answered,correct_answers,time_played) "
                "VALUES(?,?,?,?,?,?,?,?,?,?)",
                (user_id, guest_token, guest_name, category, continent, score,
                 max_possible, questions_answered, correct_answers, time_played)
            )
            conn.commit()
            return cur.lastrowid

    def get_score(self, score_id):
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM scores WHERE id=?", (score_id,)).fetchone()
            return dict(row) if row else None

    def get_leaderboard(self, category=None, limit=50):
        with self._conn() as conn:
            if category:
                rows = conn.execute(
                    "SELECT s.*, COALESCE(u.username, s.guest_name, 'Guest') as display_name "
                    "FROM scores s LEFT JOIN users u ON s.user_id=u.id "
                    "WHERE s.category=? ORDER BY s.score DESC LIMIT ?",
                    (category, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT s.*, COALESCE(u.username, s.guest_name, 'Guest') as display_name "
                    "FROM scores s LEFT JOIN users u ON s.user_id=u.id "
                    "ORDER BY s.score DESC LIMIT ?",
                    (limit,)
                ).fetchall()
            return [dict(r) for r in rows]

    def get_recent_scores(self, limit=10):
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT s.*, COALESCE(u.username, s.guest_name, 'Guest') as display_name "
                "FROM scores s LEFT JOIN users u ON s.user_id=u.id "
                "ORDER BY s.created_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [dict(r) for r in rows]

    # ------------------------------------------------------------------ #
    #  STATS
    # ------------------------------------------------------------------ #
    def get_stats(self):
        with self._conn() as conn:
            total_q   = conn.execute("SELECT COUNT(*) FROM questions WHERE is_active=1").fetchone()[0]
            total_u   = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            total_g   = conn.execute("SELECT COUNT(*) FROM scores").fetchone()[0]
            by_cat    = conn.execute(
                "SELECT category, COUNT(*) as cnt FROM questions WHERE is_active=1 GROUP BY category"
            ).fetchall()
            return {
                'total_questions': total_q,
                'total_users': total_u,
                'total_games': total_g,
                'by_category': {r['category']: r['cnt'] for r in by_cat}
            }
