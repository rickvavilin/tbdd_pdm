# TBDD_PDM
Simple [PDM](https://en.wikipedia.org/wiki/Product_data_management) system for internal use
# Requirements
* Python 3 
* [Flask](http://flask.pocoo.org/)
* [SQLAlchemy](http://www.sqlalchemy.org/)
* Flask-SQLAlchemy
* MySQL, SQLite as database backend

# Installing
1. Install requirements
2. Clone repository
3. Execute `python3 ./setup.py --install`

# Configure
 Default config location is `/etc/tbdd_pdm/config.json`
 
**db_connection_string** - connection string for database

*examples*: 

MySQL: `mysql+pymysql://user:password@localhost/tbdd_pdm?charset=utf8` 

SQLite: `sqlite+pysqlite:///test.db`

**storage_path** - path to files storage