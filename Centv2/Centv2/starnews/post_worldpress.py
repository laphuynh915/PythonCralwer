from starnews import pymysql
from starnews import validate_post
from starnews import validate_tag
import time
from slugify import slugify

def create_connection():
    db = pymysql.connect("localhost", "wpuser", "01228820234", "wordpress", charset='utf8')
    # db.set_charset('utf8')
    dbc = db.cursor()
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    return db

def insert_metapost(id_post, url):

    db = create_connection()
    cursor = db.cursor()
    sql_insert_post = "INSERT INTO wp_postmeta(post_id, meta_key, meta_value) VALUE ( '%d', '%s', '%s')" % \
    (id_post, 'fifu_image_url', url)
    try:
        cursor.execute(sql_insert_post)
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        raise
    db.close()

def insert_term(tag_name):

    db = create_connection()
    cursor = db.cursor()
    sql_insert_post = "INSERT INTO wp_terms(name, slug, term_group) VALUE ( '%s', '%s', '%d')" % \
    (tag_name, slugify(tag_name) , 0)
    try:
        cursor.execute(sql_insert_post)
        id_last_post = cursor.lastrowid
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        raise
    db.close()
    return id_last_post

def insert_term_taxonomy(term_id, typ):

    db = create_connection()
    cursor = db.cursor()
    sql_insert_post = "INSERT INTO wp_term_taxonomy(term_id, taxonomy, description, parent, count) VALUE ( '%d', '%s', '%s','%d', '%d')" % \
    (term_id, typ ,"", 0, 1)
    try:
        cursor.execute(sql_insert_post)
        id_last_post = cursor.lastrowid
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        raise
    db.close()
    return id_last_post

def insert_term_relationships(post_id, term_taxonomy_id):

    db = create_connection()
    cursor = db.cursor()
    sql_insert_post = "INSERT INTO wp_term_relationships(object_id, term_taxonomy_id, term_order) VALUE ( '%d', '%d', '%d')" % \
    (post_id, term_taxonomy_id ,0)
    try:
        cursor.execute(sql_insert_post)
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        raise
    db.close()


def insert_post(article_title, article_excerpt, article_content, article_name, source_url, pubtime, thumb_url,categories, tags):

    #article_content = '<img class="aligncenter" src="' + source_url + '" />'

    print("Post name la: %s" %article_name )

    db = create_connection()
    post_check = validate_post.check_exist_post(db, article_title )
    if(post_check):
        cursor = db.cursor()

        sql_insert_post = "INSERT INTO wp_posts(post_author, post_date, post_date_gmt, post_content, \
           post_title, post_excerpt, post_name,  to_ping, pinged, post_modified, post_modified_gmt, post_content_filtered, post_parent, post_type) \
           VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%d', '%s')" % \
              (1, pubtime, pubtime, article_content, article_title, '', article_name,'','',pubtime, pubtime, '', 0, 'post')

#------------------------- Day la phan tag-----------------------------------
        try:
            cursor.execute(sql_insert_post)
            id_last_post = cursor.lastrowid
            print("ID last post: %d", id_last_post)
            db.commit()
            insert_metapost(id_last_post, thumb_url)
            try:
                if tags:
                    for tag in tags:
                        tag_check = validate_tag.check_exist_tag(db, tag)
                        if tag_check == 0:
                            id_tag = insert_term(tag)
                            id_taxonomy = insert_term_taxonomy(id_tag, "post_tag")
                            insert_term_relationships(id_last_post, id_taxonomy)
                        else:
                            print("********Co trung tag**************")
                            sql = "SELECT term_taxonomy_id FROM wp_term_taxonomy \
                                    WHERE term_id LIKE '%d'" % tag_check
                            try:
                                cursor.execute(sql)
                                result = cursor.fetchone()
                                if result is None:
                                    print("Deo tim thay")
                                else:
                                    insert_term_relationships(id_last_post, result[0])
                            except:
                                print("Loi O Buoc kiem tra trung lap tag")
                else:
                    print("Deo lam gi ca tap 2")
            except:
                print("Phan nay deo nap dc tag")
#------------------------Day la phan category----------------------------------------------------------
            try:
                if categories:
                    for category in categories:
                        category_check = validate_tag.check_exist_tag(db, category)
                        if category_check == 0:
                            id_category = insert_term(category)
                            id_taxonomy = insert_term_taxonomy(id_category, "category")
                            insert_term_relationships(id_last_post, id_taxonomy)
                        else:
                            print("********Co trung category**************")
                            sql = "SELECT term_taxonomy_id FROM starnews_term_taxonomy \
                                    WHERE term_id LIKE '%d'" % category_check
                        try:
                            cursor.execute(sql)
                            result = cursor.fetchone()
                            if result is None:
                                print("Deo tim thay")
                            else:
                                insert_term_relationships(id_last_post, result[0])
                        except:
                            print("Loi O Buoc kiem tra trung lap category")
                else:
                        print("category deo lam gi dc")
            except:
                print("Phan nay deo category dc")

        except:
            # Rollback in case there is any error
            db.rollback()
            raise
    else:
        print("***************** Ton tai post trung*********************")
    db.close()
