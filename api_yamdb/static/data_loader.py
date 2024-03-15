import sqlite3

import pandas as pd

TABLE_DATA = {
    'data/genre.csv': 'reviews_genre',
    'data/category.csv': 'reviews_category',
    'data/comments.csv': 'reviews_comment',
    'data/genre_title.csv': 'reviews_title_genre',
    'data/review.csv': 'reviews_review',
    'data/titles.csv': 'reviews_title',
    'data/users.csv': 'yamdb_user_yamdbuser',
}

with sqlite3.connect('../db.sqlite3') as conn:
    for csv_path, table_name in TABLE_DATA.items():
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()
        df = df.fillna('')
        cursor = conn.execute(f'SELECT * FROM {table_name}')
        if missing_cols := (
            set(descr[0] for descr in cursor.description) - set(df.columns)
        ):
            for col_name in missing_cols:
                df.insert(len(df.columns), col_name, "")
        try:
            df.to_sql(table_name, conn, if_exists='append', index=False)
        except sqlite3.IntegrityError:
            continue
