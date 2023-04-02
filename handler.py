import string
import pg8000.native
import os


def hello(event, context):
    print(event)
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    input_word = event.get('word')
    result = {}
    for c in string.ascii_lowercase:
        result[c] = 0
    

    con = pg8000.native.Connection(
        db_user, 
        db_host,
        'stringdb',
        5432,
        db_password
    )


    for row in con.run("SELECT * from kstrings"):
        result[row[0]] += row[1]    


    con.run("START TRANSACTION")
    for c in input_word:
        result[c] += 1
        con.run("UPDATE kstrings SET count = count + 1 where letter = " + "'" + c + "'")
    con.run("COMMIT")

    

    return result
