# Branch
Prototype example developed for KS2E.

The application is developed by using Python3.6 on Ubuntu 16.04. It requires:
- MongoDB v3.0.15
- Openssl v1.0.2g
- Python Package: numpy package, pymongo package

Branch_A.py demonstrates the interaction on Cloud A, including:
- Alice upload encrypted searchable indexes with time measurement
- Handle the sharing request initiated by Alice with time measurement

Branch_B.py demonstrates the interaction on Cloud B, including:
- Handle the sharing request initiated by Alice with time measurement
- Handle the search request initiated by Bob with time measurement

Diana_test.py demonstrates the Diana realization by python & C code.

# Usage

An example code is:
- python3.6 Branch_B.py lucene b 0
- python3.6 Branch_A.py lucene bcds 0

For more detail:

python3.6 Branch_A.py | test_db_name | test_phase | test_group
- test_db_name: the database name in MongoDB
- test_phase: b (setup the database) | c (updating data) | d (start the share phase ) | s (start the search phase)
- test_group: the number of test group

python3.6 Branch_B.py | test_db_name | test_phase | test_group
- test_db_name: the database name in MongoDB
- test_phase: b (setup the database and wating requests)  
- test_group: the number of test group

*The python code in the 'Database_Gen' provides our sample process on the Enron/Lucene/Wikipediadump databases.

*Please contact us for technical issues at acmccs2022con66@outlook.com.
