# Module Imports
import mariadb
import sys

import json

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="azblog",
        password="azblog",
        host="localhost",
        port=3306,
        database="azblog"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute(
    """SELECT ID, post_author, post_date_gmt, post_content, post_title, post_modified_gmt, guid
    FROM azblog.cd2b3uv_posts
    WHERE post_type = 'revision' AND post_content <> ''
    GROUP BY post_parent
    ORDER BY MAX(post_modified_gmt) DESC;
    """)

# Print Result-set
azblog_posts = []
for (ID, post_author, post_date_gmt, post_content, post_title, post_modified_gmt, guid) in cur:
    azblog_posts.append({
        "id": ID,
        "text": post_content,
        "source": "azblog",
        "source_id": "azblog",
        "url": guid,
        "created_at": post_date_gmt,
        "author": post_author,
        "title": post_title,
        "post_modified_gmt": post_modified_gmt,
    })

# Gen json data file
print(len(azblog_posts))
json_object = json.dumps(azblog_posts, indent=4, sort_keys=True, default=str)

with open("azblog_posts_old.json", "w") as outfile:
    outfile.write(json_object)