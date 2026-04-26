from tinydb import TinyDB

db = TinyDB("busterdb.json")

searches_table = db.table("searches")
documents_table = db.table("documents")
users_table = db.table("users")
dictionary_table = db.table("dictionary")