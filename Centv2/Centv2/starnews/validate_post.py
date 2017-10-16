from starnews import pymysql

# def create_connection():
#     return pymysql.connect("localhost", "root", "vertrigo", "tincongnghe")

def check_exist_post(db, title):
    # db = create_connection()
    cursor = db.cursor()
    sql = "SELECT count(*) FROM wp_posts \
           WHERE post_title LIKE '%s'" % (title)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        print("van on 1")
        # Fetch all the rows in a list of lists.
        result = cursor.fetchone()
        if result[0] == 0:
            print("Khuc true")
            return True
        else:
            print("Khuc false")
            return False
    except:
        print("Error: unable to fetch data")
    # disconnect from server
    # db.close()
