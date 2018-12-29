# Database comparator
![Image here](database_comparator.png)

This is a tool for comparing speeds of CRUD operations on spatial database and relational
database.

## Installation
1. Download PostgreSQL database
2. Download POSTGis extension
3. Create database 'db_comparator'
    ```bash
    sudo -i -u postgres
    psql
    ```
    ```postgresql
    CREATE DATABASE db_comparator; 
    ```
4. Add POSTGis extension
    ```postgresql
    CREATE EXTENSION postgis;
    ```
5. Start `db_setup.py` script to execute migrations
6. Start application by executing `main.py`

## Usage
TODO

## Author
Davor Češljaš
