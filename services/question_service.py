"""
QI1489 Android — Question Service
Wraps DatabaseManager for game logic.
"""
import random
import uuid


def get_questions(db, category, continent='Worldwide', count=10, lang='en'):
    rows = db.get_questions(category, continent=continent, count=count, lang=lang)
    return _format_questions(rows, lang)


def get_geography_questions(db, count=10, lang='en'):
    rows = db.get_geography_questions(count=count, lang=lang)
    return _format_questions(rows, lang)


def _format_questions(rows, lang):
    out = []
    for r in rows:
        q_text = r['question_fr'] if lang == 'fr' and r.get('question_fr') else r['question_en']
        options = [r['answer'], r['option1'], r['option2'], r['option3']]
        random.shuffle(options)
        out.append({
            'id':       r['id'],
            'question': q_text,
            'answer':   r['answer'],
            'options':  options,
            'hint':     r['hint_fr'] if lang == 'fr' and r.get('hint_fr') else r.get('hint_en', ''),
            'category': r['category'],
            'continent': r.get('continent', ''),
            'country':  r.get('country', ''),
            'difficulty': r.get('difficulty', 'medium'),
        })
    return out


def calculate_score(correct, total, time_played):
    if total == 0:
        return 0
    base_score = correct * 10
    avg_time_per_q = time_played / total if total > 0 else 15
    time_bonus = max(0, int((15 - avg_time_per_q) / 3)) * correct
    return base_score + time_bonus


def get_rank(total_score):
    if total_score >= 5000:
        return 'Grand Master'
    elif total_score >= 2000:
        return 'Expert'
    elif total_score >= 500:
        return 'Advanced'
    elif total_score >= 100:
        return 'Intermediate'
    return 'Beginner'
