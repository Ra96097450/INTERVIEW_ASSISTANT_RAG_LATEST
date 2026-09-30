# Databases

## Database Indexing
An index is a data structure that helps a database find rows without scanning the entire table.

For example, if a table contains one million users and an index exists on user_id, a query searching for a specific user_id can use the index to locate the relevant row efficiently.

## B-Tree Index
A B-tree index keeps keys in sorted order and organizes them into a tree structure.

A database can compare the search key at internal nodes and choose the appropriate child rather than checking every row.

B-tree indexes are useful for equality searches and range queries such as:

WHERE age >= 30 AND age < 40

## Primary Key
A primary key uniquely identifies each row. Databases commonly create or maintain an index associated with a primary key.

The index does not mean that every query searches every unique value individually. Instead, the database uses the index structure to navigate toward the requested key efficiently.

## Composite Index
A composite index contains multiple columns, such as:

CREATE INDEX idx_user_city_age ON users(city, age)

The order of columns matters. Queries that use the leading columns of the index can generally benefit more from it.

## Index Trade-off
Indexes improve read performance but consume storage and add work during INSERT, UPDATE, and DELETE operations because the index may also need to be updated.
