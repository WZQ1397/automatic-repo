import sqlite3,os

db_filename = 'zach2.db'
schema_filename = 'zach_schema.sql'

db_is_new = not os.path.exists(db_filename)

project_name = "zachx"
with sqlite3.connect(db_filename) as conn:
    if db_is_new:
        print('Creating schema')

        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)

        print('Inserting initial data')
#TODO 脚本插入
        conn.executescript("""
        insert into project (name, description, deadline)
        values ('zach1', '51xyc',
                '2017-11-01');

        insert into task (details, status, deadline, project)
        values ('sqlite3', 'active', '2017-07-31',
                'wzq1397');
        """)

        query = """
    	select id, priority, details, status, deadline from task
    	where project = ?
    	"""
        conn.execute(query, (project_name,))

        conn.commit()

    else:
        print('Database exists, assume schema does, too.')

with sqlite3.connect(db_filename) as conn:
    cursor = conn.cursor()

    cursor.execute("""
    select id, priority, details, status, deadline from task
    where project like 'zach%'
    """)

    #conn.rollback()

    for row in cursor.fetchall():		#cursor.fetchmany(5)
        task_id, priority, details, status, deadline = row
        print('{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
            task_id, priority, details, status, deadline))

    data = [
        ('write about select', 'done', '2010-10-03',
         'pymotw'),
        ('write about random', 'waiting', '2010-10-10',
         'pymotw'),
        ('write about sqlite3', 'active', '2010-10-17',
         'pymotw'),
    ]

#TODO 批量执行
    conn.executemany("""
    insert into task (details, status, deadline, project)
    values (?, ?, ?, ?)
    """, data)

#TODO 迭代输出
    for text in conn.iterdump():
        print(text)
