SQLALCHEMY_DATABASE_URI = "sqlite:///data/db.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = 'data/files'
ZIPS_FOLDER = 'data/zips'
MAX_CONTENT_LENGTH = 512 * 1024 * 1024
NOT_ALLOWED_CHARACTERS = ["/", "\\"]
EXPIRATION_TIME = {"days": 0, "hours": 0, "minutes": 2}
EXPIRATION_IDS = {"0": {"days": 0, "hours": 12, "minutes": 0},
                  "1": {"days": 1, "hours": 0, "minutes": 0},
                  "2": {"days": 7, "hours": 0, "minutes": 0}}
CLEANUP_EVERY = {"hours": 0, "minutes": 5, "seconds": 0}
