# -*- coding: utf-8 -*-
import os
import psycopg2 as db

def insert(table, columns, values, returnID=True):
    if returnID:
        query = "INSERT INTO {} ({}) VALUES ({}) RETURNING id".format(table, columns, values)
    else:
        query = "INSERT INTO {} ({}) VALUES ({})".format(table, columns, values)
    return run(query)

def select(columns, table, where=None, asDict=False):
    if asDict:
        keywords = [column.strip() for column in columns.split(',')]
    else:
        keywords = None

    if where:
        query = "SELECT {} FROM {} WHERE {}".format(columns, table, where)
    else:
        query = "SELECT {} FROM {}".format(columns, table)
    return run(query, keywords)

def update(table, columns, where):
    query = "UPDATE {} SET {} WHERE {}".format(table, columns, where)
    run(query)

def delete(table, where):
    query = "DELETE FROM {} WHERE {}".format(table, where)
    run(query)

def run(query, keywords=None):
    connection = None
    cursor = None
    result = None

    print("\nAttempted Query:\n", query, "\n--------\n")
    try:
        connection = db.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute(query)
        if not any(keyword in query for keyword in ['drop', 'update', 'delete']):
            result = cursor.fetchall()
    except db.DatabaseError as dberror:
        if connection:
            connection.rollback()
        result = dberror
        print("Database Error:", result)
    except SyntaxError as syntax_error:
        result = syntax_error
        print("Syntax Error:", result)
    except Exception as error:
        result = error
        print("Error:", result)
    finally:
        if connection:
            connection.commit()
            connection.close()
        if cursor:
            cursor.close()

    if keywords and result:
        if len(keywords) == 1:
            return [dict(zip(keywords, row)) for row in result][0]
        return [dict(zip(keywords, row)) for row in result]
    return result
