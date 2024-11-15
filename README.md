# !!

This project is still in production. (end with November 14th)
The work in this repository is under a restricted license until November 14th. (Sharing and modification for distribution are not permitted.)


# Introduction

The crime information displayed on this site is fictional and not related to any real persons, places, or addresses.


To login there are three accounts.
1. Username: Admin User / UserEmail: admin@example.com'

2. Username:  John Smith / UserEmail: john.smith@example.com

3. Username: Jane Doe/ UserEmail: jane.doe@example.com


# how to execute the code

 
 1. Enverionment setting

 1.1 pip install > requirements2.txt (for ubuntu requirements3.txt)

"requirments" is  for conda


1.2 create secrets.toml file

# Option:postsql
secrets.toml file content: 
[database]
DB_URL = "serverdb url"
# Option:sqllite
secrets2.toml file content:
[database]
DB_URL = "localdb url"

1.3 initial_db.py
execute initial_db to create db (line2, secrets.toml ->for postsql(server), secrets2.toml -> for sqllite(local))

2. Run


 python3 crime.py  (to excute) # postsql version

 python3 crime_local.py # sqlite version
 
 127.0.0.1:8111 (local)

