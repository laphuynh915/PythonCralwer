from starnews import pymysql

# def create_connection():
#     return pymysql.connect("localhost", "root", "vertrigo", "tincongnghe")

def check_exist_tag(db, tag):
    # db = create_connection()
    cursor = db.cursor()
    sql = "SELECT term_id FROM wp_terms \
           WHERE name LIKE '%s'" % (tag)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        print("van on tag 1")
        # Fetch all the rows in a list of lists.
        result = cursor.fetchone()
        if result is None:
            return 0
        else:
            return result[0]
    except:
        print("Error: unable to fetch data")
    # disconnect from server
    # db.close()
