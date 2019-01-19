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
5. Install `matplotlib`, `numpy` and `basemap` packages for python
    ```bash
    pip install matplotlib
    ```
    ```bash
    pip install numpy
    ```
    ```bash
    sudo apt-get install libgeos-dev
    pip install --user https://github.com/matplotlib/basemap/archive/master.zip
    ```
6. Start application by executing `main.py`

## Generating Dbcom files
To generate `dbcom` files containing geo-spatial coordinates you can start python script `points_generator.py`.
For script to run successfully you must provide file name and number of points program arguments
Example:
```bash
python points_generator.py resources/mini.dbcom 10
```

## Usage
1. Click on "Actions" menu and pick one of the CRUD operations
2. Enter necessary parameters
3. Click "Compare databases" button
4. View results

## Author
Davor Češljaš
