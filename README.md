# smart_cafteria


## Sql constrain
SQL constraints are used to specify rules for data in a table.
```sql
        --syntax
        CREATE TABLE table_name (
            column1 datatype constraint,
            column2 datatype constraint,
            column3 datatype constraint,
            ....
        );
         
```
##Examples of constrains

- NOT NULL - Ensures that a column cannot have a NULL value
- UNIQUE - Ensures that all values in a column are different
- PRIMARY KEY - A combination of a NOT NULL and UNIQUE. Uniquely identifies each row in a table
- FOREIGN KEY - Prevents actions that would destroy links between tables
- CHECK - Ensures that the values in a column satisfies a specific condition
- DEFAULT - Sets a default value for a column if no value is specified
- CREATE INDEX - Used to create and retrieve data from the database very quickly


unique ensure different values on a column
```sql
               
        --unique SQL Server / Oracle / MS Access:
        CREATE TABLE Persons (
            ID int NOT NULL UNIQUE,
            LastName varchar(255) NOT NULL,
            FirstName varchar(255),
            Age int
        );
        --unique MySQL:
        CREATE TABLE Persons (
            ID int NOT NULL,
            LastName varchar(255) NOT NULL,
            FirstName varchar(255),
            Age int,
            UNIQUE (ID)
        );
        --composit key:
        --unique MySQL / SQL Server / Oracle / MS Access:
        CREATE TABLE Persons (
            ID int NOT NULL,
            LastName varchar(255) NOT NULL,
            FirstName varchar(255),
            Age int,
            CONSTRAINT UC_Person UNIQUE (ID,LastName)
        );
        --on alter
        ALTER TABLE Persons
        ADD UNIQUE (ID);
        --composite on alter
        ALTER TABLE Persons
        ADD CONSTRAINT UC_Person UNIQUE (ID,LastName);  
        --MySQL:
        ALTER TABLE Persons
        DROP INDEX UC_Person;
        --SQL Server / Oracle / MS Access:
        ALTER TABLE Persons
        DROP CONSTRAINT UC_Person;
```

Primary key on multiple columns, also similar co composite
```sql
--oncreate

    CREATE TABLE Persons (
        ID int NOT NULL,
        LastName varchar(255) NOT NULL,
        FirstName varchar(255),
        Age int,
        CONSTRAINT PK_Person PRIMARY KEY (ID,LastName)
    );
--onalter

--Note: If you use ALTER TABLE to add a primary key, the primary key 
--column(s) must have been declared to not contain NULL values (when the table was first created).

    --MySQL / SQL Server / Oracle / MS Access:
    ALTER TABLE Persons
    ADD PRIMARY KEY (ID);
    
    --MySQL / SQL Server / Oracle / MS Access:
    ALTER TABLE Persons
    ADD CONSTRAINT PK_Person PRIMARY KEY (ID,LastName);
   
 --ondrop
    --MySQL:
    ALTER TABLE Persons
    DROP PRIMARY KEY;

    --SQL Server / Oracle / MS Access:
    ALTER TABLE Persons
    DROP CONSTRAINT PK_Person;

    

```
The FOREIGN KEY constraint is used to prevent actions that would destroy links between tables.

```sql
--MySQL:

CREATE TABLE Orders (
    OrderID int NOT NULL,
    OrderNumber int NOT NULL,
    PersonID int,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (PersonID) REFERENCES Persons(PersonID)
);

--SQL Server / Oracle / MS Access:

CREATE TABLE Orders (
    OrderID int NOT NULL PRIMARY KEY,
    OrderNumber int NOT NULL,
    PersonID int FOREIGN KEY REFERENCES Persons(PersonID)
);

CREATE TABLE Orders (
    OrderID int NOT NULL,
    OrderNumber int NOT NULL,
    PersonID int,
    PRIMARY KEY (OrderID),
    CONSTRAINT FK_PersonOrder FOREIGN KEY (PersonID)
    REFERENCES Persons(PersonID)
);

--MySQL / SQL Server / Oracle / MS Access:

ALTER TABLE Orders
ADD FOREIGN KEY (PersonID) REFERENCES Persons(PersonID);

--MySQL / SQL Server / Oracle / MS Access:

ALTER TABLE Orders
ADD CONSTRAINT FK_PersonOrder
FOREIGN KEY (PersonID) REFERENCES Persons(PersonID);

--MySQL:

ALTER TABLE Orders
DROP FOREIGN KEY FK_PersonOrder;

--SQL Server / Oracle / MS Access:

ALTER TABLE Orders
DROP CONSTRAINT FK_PersonOrder;
```

The CHECK constraint is used to limit the value range that can be placed in a column.
If you define a CHECK constraint on a column it will allow only certain values for this column.

```sql
--oncreate
--MySQL:

CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    CHECK (Age>=18)
);
--SQL Server / Oracle / MS Access:
CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int CHECK (Age>=18)
);

--To allow naming of a CHECK constraint, and for defining a CHECK 
--constraint on multiple columns, use the following SQL syntax:

CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    City varchar(255),
    CONSTRAINT CHK_Person CHECK (Age>=18 AND City='Sandnes')
);

--onalter
--MySQL / SQL Server / Oracle / MS Access:

    ALTER TABLE Persons
    ADD CHECK (Age>=18);

--MySQL / SQL Server / Oracle / MS Access:

    ALTER TABLE Persons
    ADD CONSTRAINT CHK_PersonAge CHECK (Age>=18 AND City='Sandnes');

--ondrop
--SQL Server / Oracle / MS Access:

    ALTER TABLE Persons
    DROP CONSTRAINT CHK_PersonAge;

--MySQL:

    ALTER TABLE Persons
    DROP CHECK CHK_PersonAge;
```

he DEFAULT constraint is used to set a default value for a column.

```sql
CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    City varchar(255) DEFAULT 'Sandnes'
);

--The DEFAULT constraint can also be used to insert system values, by using functions like GETDATE():

CREATE TABLE Orders (
    ID int NOT NULL,
    OrderNumber int NOT NULL,
    OrderDate date DEFAULT GETDATE()
);

--onalter
--MySQL:

    ALTER TABLE Persons
    ALTER City SET DEFAULT 'Sandnes';
    
--SQL Server:

    ALTER TABLE Persons
    ADD CONSTRAINT df_City
    DEFAULT 'Sandnes' FOR City;
 
--MS Access:

    ALTER TABLE Persons
    ALTER COLUMN City SET DEFAULT 'Sandnes';

--Oracle:

    ALTER TABLE Persons
    MODIFY City DEFAULT 'Sandnes';
    
--ondrop
--MySQL:

    ALTER TABLE Persons
    ALTER City DROP DEFAULT;
    
--SQL Server / Oracle / MS Access:

    ALTER TABLE Persons
    ALTER COLUMN City DROP DEFAULT;

--SQL Server:
    ALTER TABLE Persons
    ALTER COLUMN City DROP DEFAULT;
```

The CREATE INDEX statement is used to create indexes in tables.

Indexes are used to retrieve data from the database more quickly than otherwise. 
The users cannot see the indexes, they are just used to speed up searches/queries.

```sql

--CREATE Duplicate  INDEX Syntax

    CREATE INDEX index_name
    ON table_name (column1, column2, ...);
    
--CREATE UNIQUE INDEX Syntax
    CREATE UNIQUE INDEX index_name
    ON table_name (column1, column2, ...);
    
    CREATE INDEX idx_lastname
    ON Persons (LastName);
    
    
 --MS Access:

DROP INDEX index_name ON table_name;

--SQL Server:

DROP INDEX table_name.index_name;

--DB2/Oracle:

DROP INDEX index_name;

--MySQL:

ALTER TABLE table_name
DROP INDEX index_name;
```

Syntax for MySQL
The following SQL statement defines the "Personid" column to be an auto-increment primary key 
field in the "Persons" table:

```sql
    CREATE TABLE Persons (
        Personid int NOT NULL AUTO_INCREMENT,
        LastName varchar(255) NOT NULL,
        FirstName varchar(255),
        Age int,
        PRIMARY KEY (Personid)
    );
    
    --By default, the starting value for AUTO_INCREMENT is 1, and it will increment by 1 for each new record.

    --To let the AUTO_INCREMENT sequence start with another value, use the following SQL statement:
    ALTER TABLE Persons AUTO_INCREMENT=100;
    
    --The MS SQL Server uses the IDENTITY keyword to perform an auto-increment feature.
    --Tip: To specify that the "Personid" column should start at value 10 and increment by 5, 
    --change it to IDENTITY(10,5).
    
    CREATE TABLE Persons (
        Personid int IDENTITY(1,1) PRIMARY KEY,
        LastName varchar(255) NOT NULL,
        FirstName varchar(255),
        Age int
    );
    
    --Tip: To specify that the "Personid" column should start at value 10 and increment by 5, 
    --change the autoincrement to AUTOINCREMENT(10,5).
    
    --Syntax for Oracle
    CREATE SEQUENCE seq_person
    MINVALUE 1
    START WITH 1
    INCREMENT BY 1
    CACHE 10;
    
    
```
 ## SQL Dates
**MySQL comes with the following data types for storing a date or a date/time value in the database:**

- DATE - format YYYY-MM-DD
- DATETIME - format: YYYY-MM-DD HH:MI:SS
- TIMESTAMP - format: YYYY-MM-DD HH:MI:SS
- YEAR - format YYYY or YY
**SQL Server comes with the following data types for storing a date or a date/time value in the database:**

- DATE - format YYYY-MM-DD
- DATETIME - format: YYYY-MM-DD HH:MI:SS
- SMALLDATETIME - format: YYYY-MM-DD HH:MI:SS
- TIMESTAMP - format: a unique number
- Note: The date types are chosen for a column when you create a new table in your database!


## Sql Views
In SQL, a view is a virtual table based on the result-set of an SQL statement.

```sql
    --Syntax
    CREATE VIEW view_name AS
    SELECT column1, column2, ...
    FROM table_name
    WHERE condition;
    
    --example creations and view
    CREATE VIEW [Brazil Customers] AS
    SELECT CustomerName, ContactName
    FROM Customers
    WHERE Country = 'Brazil';
    
    SELECT * FROM [Brazil Customers];
    
    CREATE VIEW [Products Above Average Price] AS
    SELECT ProductName, Price
    FROM Products
    WHERE Price > (SELECT AVG(Price) FROM Products);
    
    SELECT * FROM [Products Above Average Price];
    
    --Updating view
    --A view can be updated with the CREATE OR REPLACE VIEW statement.
    
    --syntax
    CREATE OR REPLACE VIEW view_name AS
    SELECT column1, column2, ...
    FROM table_name
    WHERE condition;
    
    --example
    CREATE OR REPLACE VIEW [Brazil Customers] AS
    SELECT CustomerName, ContactName, City
    FROM Customers
    WHERE Country = 'Brazil';
    
    --drop
    --syntax
    DROP VIEW view_name;
    
    --example
    DROP VIEW [Brazil Customers];
    
```
