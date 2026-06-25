from history import History

db = History()

db.save(

    "show current user",

    "whoami",

    "ujwal",

    "Current user is ujwal."

)

rows = db.get_all()

for row in rows:

    print(row)