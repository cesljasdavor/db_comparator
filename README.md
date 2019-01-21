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
5. Start by executing `dist/Database-Comparator` script
    ```bash
    dist/Database-Comparator
    ```
    or start by clicking the desktop icon generated in build step

## Build
To build application as a shell script and generate Desktop icon start `build_application.sh` script
```bash
 sudo ./build_application
```

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
