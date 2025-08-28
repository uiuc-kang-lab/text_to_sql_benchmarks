extract_prompt = """/* Some extract examples are provided based on similar problems: */
/* Answer the following: Please give the name of the course in which most numbers of the students got an A. Also, list the full name of the students who got an A in this course. */
define:  most number of students got an A refers MAX(COUNT(student_id WHERE grade = 'A')); full name = f_name, l_name; got an A refers to grade = 'A';
SQL: SELECT T3.name, T2.f_name, T2.l_name FROM registration AS T1 INNER JOIN student AS T2 ON T1.student_id = T2.student_id INNER JOIN course AS T3 ON T1.course_id = T3.course_id WHERE T1.grade = 'A' GROUP BY T3.name ORDER BY COUNT(T1.student_id) DESC LIMIT 1
#reason: The question requires display in order: "name of the course", "full name"."A" is filtering condition.
#SELECT: course.name, student.f_name, student.l_name
#columns: course.name, student.f_name, student.l_name, registration.grade, registration.student_id
#values: A

/* Answer the following:How much more votes for episode 1 than for episode 5? */
define: more votes refers to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
SQL: SELECT SUM(CASE WHEN T1.episode = 1 THEN T2.votes ELSE 0 END) - SUM(CASE WHEN T1.episode = 5 THEN T2.votes ELSE 0 END) AS diff FROM Episode AS T1 INNER JOIN Vote AS T2 ON T2.episode_id = T1.episode_id;
#reason: The question requires display in order: "How much more vote". The definition of "more vote" is SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)). 1, 5 are filtering conditions.
#SELECT: SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
#columns: Episode.episode, Vote.votes
#values:1, 5

/* Answer the following: What is the average score of the movie "The Fall of Berlin" in 2019? */
define: Average score refers to Avg(rating_score);
SQL: SELECT SUM(T1.rating_score) / COUNT(T1.rating_id) FROM ratings AS T1 INNER JOIN movies AS T2 ON T1.movie_id = T2.movie_id WHERE T1.rating_timestamp_utc LIKE '2019%' AND T2.movie_title LIKE 'The Fall of Berlin'
#reason: The question requires display in order: "average score". Average score is Avg(rating_score), "The Fall of Berlin",2019 are filtering conditions.
#SELECT: Avg(rating_score)
#columns: ratings.rating_score, ratings.rating_id, ratings.rating_timestamp_utc, movies.movie_title
#values: The Fall of Berlin, 2019

/* Answer the following: How many distinct orders were there in 2003 when the quantity ordered was less than 30? */
define: "year(orderDate) = '2003'; quantityOrdered < 30;"
SQL: SELECT COUNT(DISTINCT T1.orderNumber) FROM orderdetails AS T1 INNER JOIN orders AS T2 ON T1.orderNumber = T2.orderNumber WHERE T1.quantityOrdered < 30 AND STRFTIME('%Y', T2.orderDate) = '2003'
#reason:  The question requires display in order: "How many distinct orders"." in 2003", "less than 30" are filtering conditions.
#SELECT: COUNT(DISTINCT orderdetails.orderNumber)
#columns: orderdetails.orderNumber, orderdetails.quantityOrdered, orders.orderDate
#values: 30, 2003

{fewshot}

/* Database schema */
{db_info}

#Now, you need to process the question content based on the above database information, and provide the SQL query result set (the SELECT part in SQL, requested columns by the question), candidate columns for the question, and extract all values from the query according to the database information. Please list the SQL query result set in the form of table.column according to the order of questions asked (context of SELECT), list relevant candidate columns in the format of table.field after "columns". List the values the question want to filter( WHERE conditional expressions) after "values". Use a comma "," to separate values and columns, and separate columns and values with a tab. The text format you will receive is ```question: {{question}}\ndefine:{{define or evidence}}\n#answer:```, and the output format you need to provide is #reason:{{why pick query, columns and values}} #SELECT:{{which to SELECT}} #columns:{{related columns}} #values:{{WHERE filter values}}:
Now, you need to process the following text:

/*question: {query} */
define: {hint}
#answer:
"""
#ext prompt 是不包括stand和sqllike的
extract_prompt1 = """/* Some extract examples are provided based on similar problems: */
/* Answer the following: Please give the name of the course in which most numbers of the students got an A. Also, list the full name of the students who got an A in this course. */
define:  most number of students got an A refers MAX(COUNT(student_id WHERE grade = 'A')); full name = f_name, l_name; got an A refers to grade = 'A';
SQL: SELECT T3.name, T2.f_name, T2.l_name FROM registration AS T1 INNER JOIN student AS T2 ON T1.student_id = T2.student_id INNER JOIN course AS T3 ON T1.course_id = T3.course_id WHERE T1.grade = 'A' GROUP BY T3.name ORDER BY COUNT(T1.student_id) DESC LIMIT 1
#reason: The question requires display in order: "name of the course", "full name"."A" is filtering condition.
#Standardization: Show the name of course and full name of students, the condition is the course which most students got an A.
#SELECT: course.name, student.f_name, student.l_name
#columns: course.name, student.f_name, student.l_name, registration.grade, registration.student_id
#values: A
#SQL-like: Show course.name, student.f_name, student.l_name, where registration.grade = 'A' , group by course.name, order by the number of T1.student_id

/* Answer the following:How much more votes for episode 1 than for episode 5? */
define: more votes refers to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
SQL: SELECT SUM(CASE WHEN T1.episode = 1 THEN T2.votes ELSE 0 END) - SUM(CASE WHEN T1.episode = 5 THEN T2.votes ELSE 0 END) AS diff FROM Episode AS T1 INNER JOIN Vote AS T2 ON T2.episode_id = T1.episode_id;
#reason: The question requires display in order: "How much more vote". The definition of "more vote" is SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)). 1, 5 are filtering conditions.
#Standardization: Show the number of votes by which the total votes for episode 1 exceed the total votes for episode 5.
#SELECT: SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
#columns: Episode.episode, Vote.votes
#values:1, 5
#SQL-like: Show SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))

/* Answer the following: What is the average score of the movie "The Fall of Berlin" in 2019? */
define: Average score refers to Avg(rating_score);
SQL: SELECT SUM(T1.rating_score) / COUNT(T1.rating_id) FROM ratings AS T1 INNER JOIN movies AS T2 ON T1.movie_id = T2.movie_id WHERE T1.rating_timestamp_utc LIKE '2019%' AND T2.movie_title LIKE 'The Fall of Berlin'
#reason: The question requires display in order: "average score". Average score is Avg(rating_score), "The Fall of Berlin",2019 are filtering conditions.
#Standardization: Show the average score of the movie "The Fall of Berlin" in 2019?
#SELECT: Avg(rating_score)
#columns: ratings.rating_score, ratings.rating_id, ratings.rating_timestamp_utc, movies.movie_title
#values: The Fall of Berlin, 2019
#SQL-like: Show Avg(rating_score), where ratings.rating_timestamp_utc = 2019 and movies.movie_title = 'The Fall of Berlin'

/* Answer the following: How many distinct orders were there in 2003 when the quantity ordered was less than 30? */
define: "year(orderDate) = '2003'; quantityOrdered < 30;"
SQL: SELECT COUNT(DISTINCT T1.orderNumber) FROM orderdetails AS T1 INNER JOIN orders AS T2 ON T1.orderNumber = T2.orderNumber WHERE T1.quantityOrdered < 30 AND STRFTIME('%Y', T2.orderDate) = '2003'
#reason:  The question requires display in order: "How many distinct orders"." in 2003", "less than 30" are filtering conditions.
#Standardization: Show the number of distinct orders, the condition is time in 2003 and quantity ordered was less than 30
#SELECT: COUNT(DISTINCT orderdetails.orderNumber)
#columns: orderdetails.orderNumber, orderdetails.quantityOrdered, orders.orderDate
#values: 30, 2003
#SQL-like: Show COUNT(DISTINCT orderdetails.orderNumber), where orders.orderDate = 2003 and orderdetails.quantityOrdered < 30

{fewshot}

/* Database schema */
{db_info}

#Now, you need to process the question content based on the above database information:
1. Standardize the question into a format that aligns more closely with SQL, in order to clearly reflect components: SELECT, WHERE, GROUP BY, ORDER BY, etc. 
2. provide the SQL query result set (the SELECT part in SQL, requested columns by the question), candidate columns for the question, and extract all values from the query according to the database information. Please list the SQL query result set in the form of table.column according to the order of questions asked (context of SELECT), list relevant candidate columns in the format of table.field after "columns". List the values the question want to filter( WHERE conditional expressions) after "values". Use a comma "," to separate values and columns, and separate columns and values with a tab. 
The text format you will receive is ```#question: {{question}}\ndefine:{{define or evidence}}\n#answer:```, and the output format you need to provide is #reason:{{why pick query, columns and values}} #Standardization:{{standardize question}} #SELECT:{{which to SELECT}} #columns:{{related columns}} #values:{{WHERE filter values}} #SQL-like:{{question that similar SQL}}
Now, you need to process the following text:

#question: {query}
define: {hint}
#answer:
"""
extract_prompt_wo_hint = """/* Some extract examples are provided based on similar problems: */
/* Answer the following: Please give the name of the course in which most numbers of the students got an A. Also, list the full name of the students who got an A in this course. */
define:  most number of students got an A refers MAX(COUNT(student_id WHERE grade = 'A')); full name = f_name, l_name; got an A refers to grade = 'A';
SQL: SELECT T3.name, T2.f_name, T2.l_name FROM registration AS T1 INNER JOIN student AS T2 ON T1.student_id = T2.student_id INNER JOIN course AS T3 ON T1.course_id = T3.course_id WHERE T1.grade = 'A' GROUP BY T3.name ORDER BY COUNT(T1.student_id) DESC LIMIT 1
#reason: The question requires display in order: "name of the course", "full name"."A" is filtering condition.
#Standardization: Show the name of course and full name of students, the condition is the course which most students got an A.
#SELECT: course.name, student.f_name, student.l_name
#columns: course.name, student.f_name, student.l_name, registration.grade, registration.student_id
#values: A
#SQL-like: Show course.name, student.f_name, student.l_name, where registration.grade = 'A' , group by course.name, order by the number of T1.student_id

/* Answer the following:How much more votes for episode 1 than for episode 5? */
define: more votes refers to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
SQL: SELECT SUM(CASE WHEN T1.episode = 1 THEN T2.votes ELSE 0 END) - SUM(CASE WHEN T1.episode = 5 THEN T2.votes ELSE 0 END) AS diff FROM Episode AS T1 INNER JOIN Vote AS T2 ON T2.episode_id = T1.episode_id;
#reason: The question requires display in order: "How much more vote". The definition of "more vote" is SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)). 1, 5 are filtering conditions.
#Standardization: Show the number of votes by which the total votes for episode 1 exceed the total votes for episode 5.
#SELECT: SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
#columns: Episode.episode, Vote.votes
#values:1, 5
#SQL-like: Show SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))

/* Answer the following: What is the average score of the movie "The Fall of Berlin" in 2019? */
define: Average score refers to Avg(rating_score);
SQL: SELECT SUM(T1.rating_score) / COUNT(T1.rating_id) FROM ratings AS T1 INNER JOIN movies AS T2 ON T1.movie_id = T2.movie_id WHERE T1.rating_timestamp_utc LIKE '2019%' AND T2.movie_title LIKE 'The Fall of Berlin'
#reason: The question requires display in order: "average score". Average score is Avg(rating_score), "The Fall of Berlin",2019 are filtering conditions.
#Standardization: Show the average score of the movie "The Fall of Berlin" in 2019?
#SELECT: Avg(rating_score)
#columns: ratings.rating_score, ratings.rating_id, ratings.rating_timestamp_utc, movies.movie_title
#values: The Fall of Berlin, 2019
#SQL-like: Show Avg(rating_score), where ratings.rating_timestamp_utc = 2019 and movies.movie_title = 'The Fall of Berlin'

/* Answer the following: How many distinct orders were there in 2003 when the quantity ordered was less than 30? */
define: "year(orderDate) = '2003'; quantityOrdered < 30;"
SQL: SELECT COUNT(DISTINCT T1.orderNumber) FROM orderdetails AS T1 INNER JOIN orders AS T2 ON T1.orderNumber = T2.orderNumber WHERE T1.quantityOrdered < 30 AND STRFTIME('%Y', T2.orderDate) = '2003'
#reason:  The question requires display in order: "How many distinct orders"." in 2003", "less than 30" are filtering conditions.
#Standardization: Show the number of distinct orders, the condition is time in 2003 and quantity ordered was less than 30
#SELECT: COUNT(DISTINCT orderdetails.orderNumber)
#columns: orderdetails.orderNumber, orderdetails.quantityOrdered, orders.orderDate
#values: 30, 2003
#SQL-like: Show COUNT(DISTINCT orderdetails.orderNumber), where orders.orderDate = 2003 and orderdetails.quantityOrdered < 30

{fewshot}

/* Database schema */
{db_info}

#Now, you need to process the question content based on the above database information:
1. Standardize the question into a format that aligns more closely with SQL, in order to clearly reflect components: SELECT, WHERE, GROUP BY, ORDER BY, etc. 
2. Provide the SQL query result set (the SELECT part in SQL, requested columns by the question). Please list the SQL query result set in the form of table.column according to the order of questions asked (context of SELECT)
3. Provide candidate columns for the question. list relevant candidate columns in the format of table.field after "#columns". Retain the top 10 to 15 most relevant columns
4. List the values the question want to filter( WHERE conditional expressions) after "#values". 
5. Use a comma "," to separate values and columns, and separate columns and values with a tab. 

6. The text format you will receive is ```#question: {{question}}\n#answer:```, and the output format you need to provide is #reason:{{why pick query, columns and values}} #Standardization:{{standardize question}} #SELECT:{{which to SELECT}} #columns:{{related columns}} #values:{{WHERE filter values}} #SQL-like:{{question that similar SQL}}
Now, you need to process the following text:

/* Answer the following: {query} */ 
#answer:
"""

extract_prompt_wo_hint_no_fix_fewshot="""/* Some extract examples are provided based on similar problems: */
{fewshot}

/* Database schema */
{db_info}

#Now, you need to process the question content based on the above database information:
1. Standardize the question into a format that aligns more closely with SQL, in order to clearly reflect components: SELECT, WHERE, GROUP BY, ORDER BY, etc. 
2. Provide the SQL query result set (the SELECT part in SQL, requested columns by the question). Please list the SQL query result set in the form of table.column according to the order of questions asked (context of SELECT)
3. Provide candidate columns for the question. list relevant candidate columns in the format of table.field after "#columns". Retain the top 10 to 15 most relevant columns
4. List the values the question want to filter( WHERE conditional expressions) after "#values". 
5. Use a comma "," to separate values and columns, and separate columns and values with a tab. 

6. The text format you will receive is ```#question: {{question}}\n#answer:```, and the output format you need to provide is #reason:{{why pick query, columns and values}} #Standardization:{{standardize question}} #SELECT:{{which to SELECT}} #columns:{{related columns}} #values:{{WHERE filter values}} #SQL-like:{{question that similar SQL}}
Now, you need to process the following text:

/* Answer the following: {query} */ 
#answer:
"""
extract_prompt_wo_hint_new_Sqllike = """/* Some extract examples are provided based on similar problems: */
/* Answer the following: Please give the name of the course in which most numbers of the students got an A. Also, list the full name of the students who got an A in this course. */
define:  most number of students got an A refers MAX(COUNT(student_id WHERE grade = 'A')); full name = f_name, l_name; got an A refers to grade = 'A';
SQL: SELECT T3.name, T2.f_name, T2.l_name FROM registration AS T1 INNER JOIN student AS T2 ON T1.student_id = T2.student_id INNER JOIN course AS T3 ON T1.course_id = T3.course_id WHERE T1.grade = 'A' GROUP BY T3.name ORDER BY COUNT(T1.student_id) DESC LIMIT 1
#reason: The question requires display in order: "name of the course", "full name"."A" is filtering condition.
#Standardization: Show the name of course and full name of students, the condition is the course which most students got an A.
#SELECT: course.name, student.f_name, student.l_name
#columns: course.name, student.f_name, student.l_name, registration.grade, registration.student_id
#values: A
#SQL-like: SELECT name of course and full name of students WHERE the course most students got an A , GROUP BY course's name, order by the number of students

/* Answer the following:How much more votes for episode 1 than for episode 5? */
define: more votes refers to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
SQL: SELECT SUM(CASE WHEN T1.episode = 1 THEN T2.votes ELSE 0 END) - SUM(CASE WHEN T1.episode = 5 THEN T2.votes ELSE 0 END) AS diff FROM Episode AS T1 INNER JOIN Vote AS T2 ON T2.episode_id = T1.episode_id;
#reason: The question requires display in order: "How much more vote". The definition of "more vote" is SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)). 1, 5 are filtering conditions.
#Standardization: Show the number of votes by which the total votes for episode 1 exceed the total votes for episode 5.
#SELECT: SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
#columns: Episode.episode, Vote.votes
#values:1, 5
#SQL-like: SELECT SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))

/* Answer the following: What is the average score of the movie "The Fall of Berlin" in 2019? */
define: Average score refers to Avg(rating_score);
SQL: SELECT SUM(T1.rating_score) / COUNT(T1.rating_id) FROM ratings AS T1 INNER JOIN movies AS T2 ON T1.movie_id = T2.movie_id WHERE T1.rating_timestamp_utc LIKE '2019%' AND T2.movie_title LIKE 'The Fall of Berlin'
#reason: The question requires display in order: "average score". Average score is Avg(rating_score), "The Fall of Berlin",2019 are filtering conditions.
#Standardization: Show the average score of the movie "The Fall of Berlin" in 2019?
#SELECT: Avg(rating_score)
#columns: ratings.rating_score, ratings.rating_id, ratings.rating_timestamp_utc, movies.movie_title
#values: The Fall of Berlin, 2019
#SQL-like: SELECT Avg(rating_score) WHERE time in 2019 AND movie_title = 'The Fall of Berlin'

/* Answer the following: How many distinct orders were there in 2003 when the quantity ordered was less than 30? */
define: "year(orderDate) = '2003'; quantityOrdered < 30;"
SQL: SELECT COUNT(DISTINCT T1.orderNumber) FROM orderdetails AS T1 INNER JOIN orders AS T2 ON T1.orderNumber = T2.orderNumber WHERE T1.quantityOrdered < 30 AND STRFTIME('%Y', T2.orderDate) = '2003'
#reason:  The question requires display in order: "How many distinct orders"." in 2003", "less than 30" are filtering conditions.
#Standardization: Show the number of distinct orders, the condition is time in 2003 and quantity ordered was less than 30
#SELECT: COUNT(DISTINCT orderdetails.orderNumber)
#columns: orderdetails.orderNumber, orderdetails.quantityOrdered, orders.orderDate
#values: 30, 2003
#SQL-like: SELECT the number of distinct orders WHERE year(orderDate) = '2003' AND quantityOrdered < 30

{fewshot}

/* Database schema */
{db_info}

#Now, you need to process the question content based on the above database information:
1. Standardize the question into a format that aligns more closely with SQL, in order to clearly reflect components: SELECT, WHERE, GROUP BY, ORDER BY, etc. 
2. Provide the SQL query result set (the SELECT part in SQL, requested columns by the question). Please list the SQL query result set in the form of table.column according to the order of questions asked (context of SELECT)
3. Provide candidate columns for the question. list relevant candidate columns in the format of table.field after "#columns". Retain the top 10 to 15 most relevant columns
4. List the values the question want to filter( WHERE conditional expressions) after "#values". 
5. Use a comma "," to separate values and columns, and separate columns and values with a tab. 

6. The text format you will receive is ```#question: {{question}}\n#answer:```, and the output format you need to provide is #reason:{{why pick query, columns and values}} #Standardization:{{standardize question}} #SELECT:{{which to SELECT}} #columns:{{related columns}} #values:{{WHERE filter values}} #SQL-like:{{question that similar SQL}}
Now, you need to process the following text:

/* Answer the following: {query} */ 
#answer:
"""

extract_prompt_wo_hint_no_Sqllike = """/* Some extract examples are provided based on similar problems: */
/* Answer the following: Please give the name of the course in which most numbers of the students got an A. Also, list the full name of the students who got an A in this course. most number of students got an A refers MAX(COUNT(student_id WHERE grade = 'A')); full name = f_name, l_name; got an A refers to grade = 'A'; */
SQL: SELECT T3.name, T2.f_name, T2.l_name FROM registration AS T1 INNER JOIN student AS T2 ON T1.student_id = T2.student_id INNER JOIN course AS T3 ON T1.course_id = T3.course_id WHERE T1.grade = 'A' GROUP BY T3.name ORDER BY COUNT(T1.student_id) DESC LIMIT 1
#reason: The question requires display in order: "name of the course", "full name"."A" is filtering condition.
#Standardization: Show the name of course and full name of students, the condition is the course which most students got an A.
#SELECT: course.name, student.f_name, student.l_name
#columns: course.name, student.f_name, student.l_name, registration.grade, registration.student_id
#values: A

/* Answer the following: How much more votes for episode 1 than for episode 5? more votes refers to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
SQL: SELECT SUM(CASE WHEN T1.episode = 1 THEN T2.votes ELSE 0 END) - SUM(CASE WHEN T1.episode = 5 THEN T2.votes ELSE 0 END) AS diff FROM Episode AS T1 INNER JOIN Vote AS T2 ON T2.episode_id = T1.episode_id;
#reason: The question requires display in order: "How much more vote". The definition of "more vote" is SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)). 1, 5 are filtering conditions.
#Standardization: Show SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
#SELECT: SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
#columns: Episode.episode, Vote.votes
#values:1, 5

/* Answer the following: What is the average score of the movie "The Fall of Berlin" in 2019?  Average score refers to Avg(rating_score); */
SQL: SELECT SUM(T1.rating_score) / COUNT(T1.rating_id) FROM ratings AS T1 INNER JOIN movies AS T2 ON T1.movie_id = T2.movie_id WHERE T1.rating_timestamp_utc LIKE '2019%' AND T2.movie_title LIKE 'The Fall of Berlin'
#reason: The question requires display in order: "average score". Average score is Avg(rating_score), "The Fall of Berlin",2019 are filtering conditions.
#Standardization: Show the Avg(rating_score) of the movie "The Fall of Berlin" in 2019?
#SELECT: Avg(rating_score)
#columns: ratings.rating_score, ratings.rating_id, ratings.rating_timestamp_utc, movies.movie_title
#values: The Fall of Berlin, 2019

/* Answer the following: How many distinct orders were there in 2003 when the quantity ordered was less than 30? "year(orderDate) = '2003'; quantityOrdered < 30;" */
SQL: SELECT COUNT(DISTINCT T1.orderNumber) FROM orderdetails AS T1 INNER JOIN orders AS T2 ON T1.orderNumber = T2.orderNumber WHERE T1.quantityOrdered < 30 AND STRFTIME('%Y', T2.orderDate) = '2003'
#reason:  The question requires display in order: "How many distinct orders"." in 2003", "less than 30" are filtering conditions.
#Standardization: Show the number of distinct orders, the condition is year(orderDate) = '2003'; quantityOrdered < 30;
#SELECT: COUNT(DISTINCT orderdetails.orderNumber)
#columns: orderdetails.orderNumber, orderdetails.quantityOrdered, orders.orderDate
#values: 30, 2003

{fewshot}

/* Database schema */
{db_info}

#Now, you need to process the question content based on the above database information:
1. Standardize the question into a format that aligns more closely with SQL, in order to clearly reflect components: SELECT, WHERE, GROUP BY, ORDER BY, etc. 
2. Provide the SQL query result set (the SELECT part in SQL, requested columns by the question). Please list the SQL query result set in the form of table.column according to the order of questions asked.
3. Provide candidate columns for the question. list relevant candidate columns in the format of table.field after "#columns". Retain the top 10 to 15 most relevant columns
4. List the values the question want to filter( WHERE conditional expressions) after "#values". 
5. Use a comma "," to separate values and columns, and separate columns and values with a tab. 
6. The text format you will receive is ```/* Answer the following: {{question}} */\n#answer:```, and the output format you need to provide is #reason:{{why pick query, columns and values}} #Standardization:{{standardize question}} #SELECT:{{which to SELECT}} #columns:{{related columns}} #values:{{WHERE filter values}}
Now, you need to process the following text:

/* Answer the following: {query} */ 
#answer:
"""

reparse_extract_prompt = """/* Some extract examples are provided based on similar problems: */
/* Answer the following: Please give the name of the course in which most numbers of the students got an A. Also, list the full name of the students who got an A in this course. most number of students got an A refers MAX(COUNT(student_id WHERE grade = 'A')); full name = f_name, l_name; got an A refers to grade = 'A'; */
#reason: The question requires display in order: "name of the course", "full name"."A" is filtering condition.
#SELECT: course.name, student.f_name, student.l_name
#columns: course.name, student.f_name, student.l_name, registration.grade, registration.student_id
#values: "A"

/* Answer the following:How much more votes for episode 1 than for episode 5? more votes refers to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)) */
#reason: The question requires display in order: "How much more vote". The definition of "more vote" is SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)). 1, 5 are filtering conditions.
#SELECT: SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
#columns: Episode.episode, Vote.votes
#values: "1", "5"

/* Answer the following: What is the average score of the movie "The Fall of Berlin" in 2019? Average score refers to Avg(rating_score); */
#reason: The question requires display in order: "average score". Average score is Avg(rating_score), "The Fall of Berlin",2019 are filtering conditions.
#SELECT: Avg(rating_score)
#columns: ratings.rating_score, ratings.rating_id, ratings.rating_timestamp_utc, movies.movie_title
#values: "The Fall of Berlin", "2019"

/* Answer the following: How many distinct orders were there in 2003 when the quantity ordered was less than 30? "year(orderDate) = '2003'; quantityOrdered < 30;" */
#reason:  The question requires display in order: "How many distinct orders"." in 2003", "less than 30" are filtering conditions.
#SELECT: COUNT(DISTINCT orderdetails.orderNumber)
#columns: orderdetails.orderNumber, orderdetails.quantityOrdered, orders.orderDate
#values: "30", "2003"

{fewshot}

/* Database schema */
{db_info}

/* Answer the following: {query} */
Please answer the question in the following format without any other content:
```
#reason: Analysis of which columns and values might be relevant to the question. Note that when dealing with questions about time, who, which, what, etc., you should keep column related to time, names, and locations in the #column.(format: The question query xxx, the related column include table.column, the values include values)
#columns: The top 10 columns relevant to the question( format: table.column_1, table.column_2 ...)
#values: Potential filter values that the question might query(format: "value1", "value2" ...)
```"""
new_extract_prompt = """/* Some extract examples are provided based on similar problems: */
/* Answer the following: Please give the name of the course in which most numbers of the students got an A. Also, list the full name of the students who got an A in this course. most number of students got an A refers MAX(COUNT(student_id WHERE grade = 'A')); full name = f_name, l_name; got an A refers to grade = 'A'; */
#reason: The question requires display in order: "name of the course", "full name"."A" is filtering condition.
#columns: course.name, student.f_name, student.l_name, registration.grade, registration.student_id
#values: "A"

/* Answer the following:How much more votes for episode 1 than for episode 5? more votes refers to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)) */
#reason: The question requires display in order: "How much more vote". The definition of "more vote" is SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)). 1, 5 are filtering conditions.
#columns: Episode.episode, Vote.votes
#values: "1", "5"

/* Answer the following: What is the average score of the movie "The Fall of Berlin" in 2019? Average score refers to Avg(rating_score); */
#reason: The question requires display in order: "average score". Average score is Avg(rating_score), "The Fall of Berlin",2019 are filtering conditions.
#columns: ratings.rating_score, ratings.rating_id, ratings.rating_timestamp_utc, movies.movie_title
#values: "The Fall of Berlin", "2019"

/* Answer the following: How many distinct orders were there in 2003 when the quantity ordered was less than 30? "year(orderDate) = '2003'; quantityOrdered < 30;" */
#reason:  The question requires display in order: "How many distinct orders"." in 2003", "less than 30" are filtering conditions.
#columns: orderdetails.orderNumber, orderdetails.quantityOrdered, orders.orderDate
#values: "30", "2003"

{fewshot}

/* Database schema */
{db_info}

Attention:
1. if the question have when\where\which, pay attention to pick table.column related to time, location and name in #columns
2. Please answer the question in the following format without any other content:
```
#reason: Analysis of which columns and values might be relevant to the question. Note that when dealing with questions about time, who, which, what, etc., you should keep column related to time, names, and locations in the #column.(format: The question query xxx, the related column include table.column, the values include values)
#columns: The top 10 columns relevant to the question( format: table.column_1, table.column_2 ...)
#values: Potential filter values that the question might query(format: "value1", "value2" ...)
```
/* Answer the following: {query} */
"""
new_extract_prompt_wofewshot = """{fewshot}
/* Database schema */
{db_info}

Attention:
1. if the question have when\where\which, pay attention to pick table.column related to time, location and name in #columns
2. Please answer the question in the following format without any other content:
```
#reason: Analysis of which columns and values might be relevant to the question. Note that when dealing with questions about time, who, which, what, etc., you should keep column related to time, names, and locations in the #column.(format: The question query xxx, the related column include table.column, the values include values)
#columns: The top 10 columns relevant to the question( format: table.column_1, table.column_2 ...)
#values: Potential filter values that the question might query(format: "value1", "value2" ...)
```
/* Answer the following: {query} */
"""
correct_prompt = """{fewshot}

/* Database schema is as follows: */
{db_info}

/* Fix the SQL and answer the question */
#question: {q}
define: {hint}
{key_col_des}
#Error SQL: {result_info}
{advice}
Now, please give the right SQL that differs from the Error SQL, without any other content:
#New SQL: """
correct_prompt_nodb = """{fewshot}

/* Fix the SQL and answer the question */
#question: {q}
define: {hint}
{key_col_des}
#Error SQL: {result_info}
{advice}
Now, please give the right SQL that differs from the Error SQL, without any other content:
#New SQL: """
correct_prompt_wo_hint = """You are an expert in SQL. Here are some examples of fix SQL
{fewshot}

/* Database schema is as follows: */
{db_info}
{key_col_des}

/* Now Plesease fix the following error SQL */
#question: {q}
#Error SQL: {result_info}
{advice}

Please answer according to the format below and do not output any other content.:
```
#reason: Analysis of How to fix the error
#SQL: right SQL
```"""
new_prompt0="""{fewshot}

/* Database schema */
{db_info}
/* Answer the following: {question}*/
define: {hint}
{key_col_des}

#Based on the database schema and the question, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. #candidate values represent the actual values that exist in the database; Give SQL relies on these values. #column represent the candidate columns of SQL.
3. #SELECT is query result set of SQL SELECT content, do not SELECT other content to SQL

Please rewrite the question in the format: "Show #SELECT (table.column), WHERE condition is xxx (refer to #column and #values), Group by/Order By (refer to columns). Here is an example: #rewrite question: Show top 5 cards.id, where condition is cards.spend>100, order by cards.spend. 
#SQL: SELECT id FROM cards WHERE spend > 100 ORDER BY spend

Answer the question in the following format:
#rewrite question: 
#SQL:"""
#new_prompt0是不包括sQllike和stand question的
new_prompt1="""{fewshot}

/* Database schema */
{db_info}

*******
#Based on the database schema and the question, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. #values display some values obtained from querying the database; Please ignore the unnecessary #values.
3. #SELECT is query result set of SQL SELECT content, please only respond with the required information in this question, without providing explanations or any other non-requested information.

Please rewrite the question to SQL-like question in the format: "Show #SELECT (table.column), WHERE condition are xxx (refer to #column and #values), Group by/Order By (refer to columns). Here are 3 example: 

#SQL-like: Show top 5 cards.id, where condition is cards.spend>100, order by cards.spend. 
#SQL: SELECT id FROM cards WHERE spend > 100 ORDER BY spend LIMIT 5

#SQL-like: Show Count(PaperAuthor.Name), Where condition is Paper.Year = 0
#SQL: SELECT COUNT(T2.Name) FROM Paper AS T1 INNER JOIN PaperAuthor AS T2 ON T1.Id = T2.PaperId WHERE T1.Year = 0

#SQL-like: Show Author.Name, Where condition is Author.Affiliation = 'University of Oxford', Order By Author.Name
#SQL: SELECT Name FROM Author WHERE Affiliation = 'University of Oxford' ORDER BY Name ASC

/* Answer the following: {question} */
{key_col_des}

Please answer the question in the following format:
```#SQL-like: {{SQL-like question}}
#SQL: {{SQL}}```

#SQL-like:"""
new_prompt2="""{fewshot}

/* Database schema */
{db_info}
{key_col_des}

/* Based on the database schema and the question, pay attention to the following */
1. For parts involving division that contain integer types, CAST them to REAL.
2. #values display the closest values obtained from querying the database, formatted as "Queried Value: similar Value in Database"; Please ignore the unnecessary values.
3. #SELECT is query result set of SQL SELECT content. please only give SQL with the required information in this question, without providing explanations or any other non-requested information.

Please rewrite the question to SQL-like question in the format: "Show #SELECT (table.column), WHERE condition are xxx (refer to #values), Group by/Order By (refer to columns). Here are 3 example: 

#SQL-like: Show top 5 cards.id, where condition is cards.spend>100, order by cards.spend. 
#SQL: SELECT id FROM cards WHERE spend > 100 ORDER BY spend LIMIT 5

#SQL-like: Show Count(PaperAuthor.Name), Where condition is Paper.Year = 0
#SQL: SELECT COUNT(T2.Name) FROM Paper AS T1 INNER JOIN PaperAuthor AS T2 ON T1.Id = T2.PaperId WHERE T1.Year = 0

#SQL-like: Show Author.Name, Where condition is Author.Affiliation = 'University of Oxford', Group By Author.Name Order By Author.spent
#SQL: SELECT Name FROM Author WHERE Affiliation = 'University of Oxford' Group By Name ORDER BY spent ASC

/* Answer the following: {question} */

Please answer the question in the following format:
```
#reason: How to Convert question into SQL
#SELECT: SELECT content(format: table.column)
#WHERE: where condition(format: table.column <op> value)
#columns: All fields ultimately used in SQL(format: table.column_1, table.column_2 ...)
#SQL-like: SQL-like statements ignoring Join conditions
#SQL: SQL
```"""

new_prompt3="""You are an SQL expert, and now I would like you to write SQL based on the question.
{fewshot}

/* Database schema */
{db_info}
{key_col_des}

/* Based on the database schema and the question, pay attention to the following */
1. For parts involving division that contain integer types, CAST them to REAL.
2. #values in db display part values from the database. Please ignore the unnecessary values.

Please rewrite the question to SQL-like query in the format: "Show #SELECT (table.column), WHERE condition are xxx (refer to #values), Group by/Order By (refer to columns). Here are 3 example: 

#SQL-like: Show top 5 cards.id, where condition is cards.spend>100, order by cards.spend. 
#SQL: SELECT id FROM cards WHERE spend > 100 ORDER BY spend LIMIT 5

#SQL-like: Show Count(PaperAuthor.Name), Where condition is Paper.Year = 0
#SQL: SELECT COUNT(T2.Name) FROM Paper AS T1 INNER JOIN PaperAuthor AS T2 ON T1.Id = T2.PaperId WHERE T1.Year = 0

#SQL-like: Show Author.Name, Where condition is Author.Affiliation = 'University of Oxford', Group By Author.Name Order By Author.spent
#SQL: SELECT Name FROM Author WHERE Affiliation = 'University of Oxford' Group By Name ORDER BY spent ASC

/* Answer the following: {question} */
Please answer the question in the following format without any other content:
```
#reason: Analyze how to generate SQL based on the question.(format: the question want to ..., so the SQL SELECT ... and ...)
#columns: All columns ultimately used in SQL(format: table.column_1, table.column_2)
#values: the filter in SQL (format: 'filter in question' refer to table.column: value. e.g. 'name is not tom' refer to name <> "tom", 2007 refer to strftime('%Y', Date) = '2007')
#SELECT: SELECT content (display in the order asked by the questions, do not display content not specified by the questions).
#SQL-like: SQL-like statements ignoring Join conditions
#SQL: SQL
```"""

new_prompt3_wocot="""You are an SQL expert, and now I would like you to write SQL based on the question.
{fewshot}

/* Database schema */
{db_info}
{key_col_des}

/* Based on the database schema and the question, pay attention to the following */
1. For parts involving division that contain integer types, CAST them to REAL.
2. #values in db display part values from the database. Please ignore the unnecessary values.

/* Answer the following: {question} */
Please answer the question in the following format without any other content:
```
#SQL: SQL
```"""
new_prompt_O="""{fewshot}

/* Database schema */
{db_info}
{key_col_des}

# Based on the database schema and the examples above, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. "#Values in Database" display part values from the database. Please ignore the unnecessary values.
3. Please refer to the examples above and answer in the following format without any other content:
```
#reason: Analyze how to generate SQL based on the question.(format: the question want to ..., so the SQL SELECT ... and ...)
#columns: All columns ultimately used in SQL(format: table.column_1, table.column_2)
#values: the filter in SQL (format: 'filter in question' refer to 'table.column <op> value'. e.g. 'name is not tom' refer to name <> 'tom', 'in 2007' refer to "strftime('%Y', Date) = '2007'")
#SELECT: SELECT content (format like: 'query in question' refer to table.column. The order of columns in the SELECT clause must be the same as the order in the question.)
#SQL-like: SQL-like statements ignoring Join conditions
#SQL: SQL
```

/* Answer the following: {question} */
{q_order}"""

new_prompt_O1="""{fewshot}

/* Database schema */
{db_info}
{key_col_des}

# Based on the database schema and the examples above, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. "#Values in Database" display part values from the database. Please ignore the unnecessary values.
3. Please refer to the examples above and answer in the following format without any other content:
```
#reason: Analyze how to generate SQL based on the question.(format: the question want to ..., so the SQL SELECT ... and ...)
#columns: All columns ultimately used in SQL(format: table.column_1, table.column_2)
#values: the filter in SQL (format: 'filter in question' refer to 'table.column <op> value'. e.g. 'name is not tom' refer to name <> 'tom', 'in 2007' refer to "strftime('%Y', Date) = '2007'")
#SELECT: SELECT content (format like: 'query in question' refer to table.column. The order of columns in the SELECT clause must be the same as the order in the question.)
#SQL-like: SQL-like statements ignoring Join conditions(format like: SELECT table1.a WHERE table1.b = x AND time(table2.c) = X)
#SQL: SQL
```

/* Answer the following: {question} */
{q_order}"""

new_prompt_O_wocot="""{fewshot}

/* Database schema */
{db_info}
{key_col_des}

# Based on the database schema and the examples above, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. "#Values in Database" display part values from the database. Please ignore the unnecessary values.
3. Please refer to the examples above and answer in the following format without any other content:
```
#SQL: SQL
```

/* Answer the following: {question} */
{q_order}"""
new_prompt_unstruct_cot="""{fewshot}

/* Database schema */
{db_info}
{key_col_des}

# Based on the database schema and the examples above, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. "#Values in Database" display part values from the database. Please ignore the unnecessary values.
3. Please refer to the examples above and answer in the following format without any other content:
```
{{Provide your thoughts step by step}}
#SQL: SQL
```

/* Answer the following: {question} */
{q_order}"""
new_prompt_wo_hint="""{fewshot}

/* Database schema */
{db_info}

#Based on the database schema and the question, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. #values represent the actual values that exist in the database; Give SQL relies on these values. #column represent the candidate columns of SQL.
3. #SELECT is query result set of SQL SELECT content, do not SELECT other content to SQL
4. When ORDER BY COUNT, it is preferable to use COUNT(table.column) to avoid using COUNT(*)

Please rewrite the question to SQL-like question in the format: "Show #SELECT (table.column), WHERE condition is xxx (refer to #column and #values), Group by/Order By (refer to columns). Here are 3 example: 

#SQL-like: Show top 5 cards.id, where condition is cards.spend>100, order by cards.spend. 
#SQL: SELECT id FROM cards WHERE spend > 100 ORDER BY spend LIMIT 5

#SQL-like: Show Count(PaperAuthor.Name), Where condition is Paper.Year = 0
#SQL: SELECT COUNT(T2.Name) FROM Paper AS T1 INNER JOIN PaperAuthor AS T2 ON T1.Id = T2.PaperId WHERE T1.Year = 0

#SQL-like: Show Author.Name, Where condition is Author.Affiliation = 'University of Oxford', Order By Author.Name
#SQL: SELECT Name FROM Author WHERE Affiliation = 'University of Oxford' ORDER BY Name ASC


/* Answer the following: {question} */
{key_col_des}

Please answer the question in the following format:
#SQL-like: {{SQL-like question}}
#SQL: {{SQL}}

#SQL-like:"""

new_prompt_wo_hint_new_sqllike="""{fewshot}

/* Database schema */
{db_info}

#Based on the database schema and the question, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. #candidate values represent the actual values that exist in the database; Give SQL relies on these values. #column represent the candidate columns of SQL.
3. #SELECT is query result set of SQL SELECT content, do not SELECT other content to SQL
4. When ORDER BY COUNT, it is preferable to use COUNT(table.column) to avoid using COUNT(*)

Please rewrite the question to SQL-like question in the format: "SELECT xxx, WHERE condition is xxx , Group by/Order By xxx, LIMIT xxx. Here are 3 example: 

#SQL-like: SELECT id of cards, WHERE users' spend > 100, order by spend, LIMIT 5
#SQL: SELECT id FROM cards WHERE spend > 100 ORDER BY spend LIMIT 5

#SQL-like: SELECT the number of PaperAuthor.Name, Where publish years = 0
#SQL: SELECT COUNT(T2.Name) FROM Paper AS T1 INNER JOIN PaperAuthor AS T2 ON T1.Id = T2.PaperId WHERE T1.Year = 0

#SQL-like: SELECT Author's name, WHERE Affiliation of them = 'University of Oxford', ORDER BY Author.Name
#SQL: SELECT Name FROM Author WHERE Affiliation = 'University of Oxford' ORDER BY Name ASC

/* Answer the following: {question} */
{key_col_des}

Please answer the question in the following format:
```#SQL-like: {{SQL-like question}}
#SQL: {{SQL}}```

#SQL-like:"""

new_prompt_wo_hint_new_sqllike_wodb="""{fewshot}

#Based on the database schema and the question, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. #candidate values represent the actual values that exist in the database; Give SQL relies on these values. #column represent the candidate columns of SQL.
3. #SELECT is query result set of SQL SELECT content, do not SELECT other content to SQL
4. When USE COUNT, avoid using COUNT(*)

Please rewrite the question to SQL-like question in the format: "SELECT xxx, WHERE condition is xxx , Group by/Order By xxx, LIMIT xxx. Here are 3 example: 

#SQL-like: SELECT id of cards, WHERE users' spend > 100, order by spend, LIMIT 5
#SQL: SELECT id FROM cards WHERE spend > 100 ORDER BY spend LIMIT 5

#SQL-like: SELECT the number of PaperAuthor.Name, Where publish years = 0
#SQL: SELECT COUNT(T2.Name) FROM Paper AS T1 INNER JOIN PaperAuthor AS T2 ON T1.Id = T2.PaperId WHERE T1.Year = 0

#SQL-like: SELECT Author's name, WHERE Affiliation of them = 'University of Oxford', ORDER BY Author.Name
#SQL: SELECT Name FROM Author WHERE Affiliation = 'University of Oxford' ORDER BY Name ASC

/* Answer the following: {question} */
{key_col_des}

Please answer the question in the following format:
```#SQL-like: {{SQL-like question}}
#SQL: {{SQL}}```

#SQL-like:"""

new_prompt_wo_hint_standQ_newsqllike="""{fewshot}

/* Database schema */
{db_info}

#Based on the database schema and the question, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. #candidate values represent the actual values that exist in the database; Give SQL relies on these values. #column represent the candidate columns of SQL.
3. #SELECT is query result set of SQL SELECT content, do not SELECT other content to SQL
4. When ORDER BY COUNT, it is preferable to use COUNT(table.column) to avoid using COUNT(*)

Please rewrite the question to Standardization and SQL-like question in the format: "SELECT xxx, WHERE condition is xxx , Group by/Order By xxx, LIMIT xxx. Here are 3 example: 

##Standardization: Show id of cards, the condition is the spend belong to top 5
#SQL-like: SELECT id of cards, WHERE users' spend > 100, order by spend, LIMIT 5
#SQL: SELECT id FROM cards WHERE spend > 100 ORDER BY spend LIMIT 5

##Standardization:show the number of Author, the condition is who have not publish book
#SQL-like: SELECT the number of PaperAuthor.Name, Where publish years = 0
#SQL: SELECT COUNT(T2.Name) FROM Paper AS T1 INNER JOIN PaperAuthor AS T2 ON T1.Id = T2.PaperId WHERE T1.Year = 0

##Standardization: Show the Author's name on order, the condition is affiliation is 'University of Oxford',
#SQL-like: SELECT Author's name, WHERE Affiliation = 'University of Oxford', ORDER BY Author.Name
#SQL: SELECT Name FROM Author WHERE Affiliation = 'University of Oxford' ORDER BY Name ASC

/* Answer the following: {question} */
{key_col_des}

Please answer the question in the following format:
```#Standardization:{{Standardization question}}
#SQL-like: {{SQL-like question}}
#SQL: {{SQL}}```

#Standardization:"""

new_prompt_wo_hint_standQ="""{fewshot}

/* Database schema */
{db_info}

#Based on the database schema and the question, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. #candidate values represent the actual values that exist in the database; Give SQL relies on these values. #column represent the candidate columns of SQL.
3. #SELECT is query result set of SQL SELECT content, do not SELECT other content to SQL
4. When ORDER BY COUNT, it is preferable to use COUNT(table.column) to avoid using COUNT(*)

/* Answer the following: {question} */
{key_col_des}

Please rewrite the question in a standardized format that more clearly outlines the corresponding SQL elements of SELECT, WHERE, and GROUP BY. Here are 3 examples: 

#Standardization: Show id of cards, the condition is the spend belong to top 5
#SQL: SELECT id FROM cards WHERE spend > 100 ORDER BY spend LIMIT 5

##Standardization:show the number of Author, the condition is who have not publish book
#SQL: SELECT COUNT(T2.Name) FROM Paper AS T1 INNER JOIN PaperAuthor AS T2 ON T1.Id = T2.PaperId WHERE T1.Year = 0

#Standardization: Show the Author's name on order, the condition is affiliation is 'University of Oxford',
#SQL: SELECT Name FROM Author WHERE Affiliation = 'University of Oxford' ORDER BY Name ASC

Please answer the question in the following format:
```#Standardization:{{standardized question}}
#SQL: {{SQL}}```

#Standardization:"""

new_prompt_wo_hint_no_sqllike="""{fewshot}

/* Database schema */
{db_info}

#Based on the database schema and the question, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. #candidate values represent the actual values that exist in the database; Give SQL relies on these values. #column represent the candidate columns of SQL.
3. #SELECT is query result set of SQL SELECT content, do not SELECT other content to SQL
4. When ORDER BY COUNT, it is preferable to use COUNT(table.column) to avoid using COUNT(*)

/* Answer the following: {question} */
{key_col_des}
#SQL:"""

new_prompt_sql_part="""{fewshot}

/* Database schema */
{db_info}

*******
#Based on the database schema and the question, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. #values display the closest values obtained from querying the database, formatted as "Queried Value: similar Value in Database"; #column represent the candidate columns of SQL. Please ignore the unnecessary #values and #column.
3. #SELECT is query result set of SQL SELECT content, please only respond with the required information in this question, without providing explanations or any other non-requested information.

Please rewrite the question to SQL-like question in the format: "Show #SELECT (table.column), WHERE condition are xxx (refer to #column and #values), Group by/Order By (refer to columns). Here are 3 example: 

#SQL-like: Show top 5 cards.id, where condition is cards.spend>100, order by cards.spend. 
#SQL: SELECT id FROM cards WHERE spend > 100 ORDER BY spend LIMIT 5

#SQL-like: Show Count(PaperAuthor.Name), Where condition is Paper.Year = 0
#SQL: SELECT COUNT(T2.Name) FROM Paper AS T1 INNER JOIN PaperAuthor AS T2 ON T1.Id = T2.PaperId WHERE T1.Year = 0

#SQL-like: Show Author.Name, Where condition is Author.Affiliation = 'University of Oxford', Order By Author.Name
#SQL: SELECT Name FROM Author WHERE Affiliation = 'University of Oxford' ORDER BY Name ASC

/* Answer the following: {question} */
{key_col_des}

Please answer the question in the following format:
```#SQL-like: {{SQL-like question}}
#SQL: {{SQL}}```

Please display all the nouns and phrases in the sentence and their corresponding parts in SQL, written after #Part. Then, provide the SQL code after #SQL. Please respond in the following format:
#Part:
#SQL-like:
#SQL:"""

noun_prompt="""Please extract all nouns and phrases from the following sentence, separating the results directly with a comma( format: "noun_1", "noun_2","phrases" ):
{raw_question}"""

soft_prompt="""Your task is to perform a simple evaluation of the SQL.

The database system is SQLite. The SQL you need to evaluation is:
#question: {question}
#SQL: {SQL}

Answer in the following format: 
{{
"Judgment": true/false,
"SQL":If SQL is wrong, please correct SQL directly. else answer ""
}}"""

prompts_fewshot_parse="""/* extract and rewrite example */
#question: Please give the name of the course in which most numbers of the students got an A. Also, list the full name of the students who got an A in this course.
evidence:  most number of students got an A refers MAX(COUNT(student_id WHERE grade = 'A')); full name = f_name, l_name; got an A refers to grade = 'A';
SQL: SELECT T3.name, T2.f_name, T2.l_name FROM registration AS T1 INNER JOIN student AS T2 ON T1.student_id = T2.student_id INNER JOIN course AS T3 ON T1.course_id = T3.course_id WHERE T1.grade = 'A' GROUP BY T3.name ORDER BY COUNT(T1.student_id) DESC LIMIT 1
#reason: The question requires display in order: "name of the course", "full name"."A" is filtering condition.
#SELECT: course.name, student.f_name, student.l_name
#columns: course.name, student.f_name, student.l_name, registration.grade, registration.student_id
#values: A
#Standardization question: Show the name of course and full name of students, the condition is the course which most students got an A.
#SQL-like question: Show course.name, student.f_name, student.l_name, where registration.grade = 'A' , group by course.name, order by the number of T1.student_id

/* extract and rewrite example */
#question:How much more votes for episode 1 than for episode 5?
evidence: more votes refers to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
SQL: SELECT SUM(CASE WHEN T1.episode = 1 THEN T2.votes ELSE 0 END) - SUM(CASE WHEN T1.episode = 5 THEN T2.votes ELSE 0 END) AS diff FROM Episode AS T1 INNER JOIN Vote AS T2 ON T2.episode_id = T1.episode_id;
#reason: The question requires display in order: "How much more vote". The definition of "more vote" is SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)). 1, 5 are filtering conditions.
#SELECT: SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
#columns: Episode.episode, Vote.votes
#values:1, 5
#Standardization question: Show the number of votes by which the total votes for episode 1 exceed the total votes for episode 5.
#SQL-like question: Show SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))

/* extract and rewrite example */
#question: What is the average score of the movie "The Fall of Berlin" in 2019? */
evidence: Average score refers to Avg(rating_score);
SQL: SELECT SUM(T1.rating_score) / COUNT(T1.rating_id) FROM ratings AS T1 INNER JOIN movies AS T2 ON T1.movie_id = T2.movie_id WHERE T1.rating_timestamp_utc LIKE '2019%' AND T2.movie_title LIKE 'The Fall of Berlin'
#reason: The question requires display in order: "average score". Average score is Avg(rating_score), "The Fall of Berlin",2019 are filtering conditions.
#SELECT: Avg(rating_score)
#columns: ratings.rating_score, ratings.rating_id, ratings.rating_timestamp_utc, movies.movie_title
#values: The Fall of Berlin, 2019
#Standardization question: Show the average score of the movie "The Fall of Berlin" in 2019?
#SQL-like question: Show Avg(rating_score), where ratings.rating_timestamp_utc = 2019 and movies.movie_title = 'The Fall of Berlin'

/* extract and rewrite example */
#question: How many distinct orders were there in 2003 when the quantity ordered was less than 30?
evidence: "year(orderDate) = '2003'; quantityOrdered < 30;"
SQL: SELECT COUNT(DISTINCT T1.orderNumber) FROM orderdetails AS T1 INNER JOIN orders AS T2 ON T1.orderNumber = T2.orderNumber WHERE T1.quantityOrdered < 30 AND STRFTIME('%Y', T2.orderDate) = '2003'
#reason:  The question requires display in order: "How many distinct orders"." in 2003", "less than 30" are filtering conditions.
#SELECT: COUNT(DISTINCT orderdetails.orderNumber)
#columns: orderdetails.orderNumber, orderdetails.quantityOrdered, orders.orderDate
#values: 30, 2003
#Standardization question: Show the number of distinct orders, the condition is time in 2003 and quantity ordered was less than 30
#SQL-like question: Show COUNT(DISTINCT orderdetails.orderNumber), where orders.orderDate = 2003 and orderdetails.quantityOrdered < 30

#Now, you need to process the question content based on the evidence and SQL:
1. Standardize the question into a format that aligns more closely with SQL, in order to clearly reflect components: SELECT, WHERE, GROUP BY, ORDER BY, etc.
2. provide the SQL query result set (the SELECT part in SQL, requested columns by the question), candidate columns for the question, and extract all values from the query according to the database information. Please list the query result set in the format of table.column after "#SELECT", list relevant candidate columns in the format of table.field after "#columns". List the values the question want to query after "#values". Use a comma "," to separate values and columns, and separate columns and values with a tab. The text format you will receive is ```question: {{question}}\evidence:{{define or evidence}}\nSQL:{{SQL}}\n#answer:```, and the output format you need to provide is #reason:{{why pick query, columns and values}}\n#SELECT:{{which to SELECT}}\n#columns:{{related columns}}\n#values:{{values}} #Standardization question:{{}}\n#SQL-like: SQL-like statements that ignore join conditions
Now, you need to process the following text:

#question: {question}
evidence: {evidence}
SQL: {sql}
#answer:
"""

prompts_fewshot_parse2="""/* extract and rewrite example */
#question: Please give the name of the course in which most numbers of the students got an A. Also, list the full name of the students who got an A in this course. most number of students got an A refers MAX(COUNT(student_id WHERE grade = 'A')); full name = f_name, l_name; got an A refers to grade = 'A';
SQL: SELECT T3.name, T2.f_name, T2.l_name FROM registration AS T1 INNER JOIN student AS T2 ON T1.student_id = T2.student_id INNER JOIN course AS T3 ON T1.course_id = T3.course_id WHERE T1.grade = 'A' GROUP BY T3.name ORDER BY COUNT(T1.student_id) DESC LIMIT 1
#reason: The question requires display in order: "name of the course", "full name"."A" is filtering condition.
#columns: course.name, student.f_name, student.l_name, registration.grade, registration.student_id
#SELECT: "name of the course" refer to course.name, "full name" refer to student.f_name, student.l_name
#values: got an A refers to registration.grade = 'A'
#SQL-like: Show course.name, student.f_name, student.l_name, where registration.grade = 'A' , group by course.name, order by the number of T1.student_id

/* extract and rewrite example */
#question:How much more votes for episode 1 than for episode 5? more votes refers to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
SQL: SELECT SUM(CASE WHEN T1.episode = 1 THEN T2.votes ELSE 0 END) - SUM(CASE WHEN T1.episode = 5 THEN T2.votes ELSE 0 END) AS diff FROM Episode AS T1 INNER JOIN Vote AS T2 ON T2.episode_id = T1.episode_id;
#reason: The question requires display in order: "How much more vote". The definition of "more vote" is SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)). 1, 5 are filtering conditions.
#columns: Episode.episode, Vote.votes
#SELECT: more votes for episode 1 than for episode 5 refer to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
#values:  episode 1 refer to Episode.episode = 1,  episode 5 refer to Episode.episode = 5
#SQL-like: Show SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))

/* extract and rewrite example */
#question: What is the average score of the movie "The Fall of Berlin" in 2019? Average score refers to Avg(rating_score);
SQL: SELECT SUM(T1.rating_score) / COUNT(T1.rating_id) FROM ratings AS T1 INNER JOIN movies AS T2 ON T1.movie_id = T2.movie_id WHERE T1.rating_timestamp_utc LIKE '2019%' AND T2.movie_title LIKE 'The Fall of Berlin'
#reason: The question requires display in order: "average score". Average score is Avg(rating_score), "The Fall of Berlin",2019 are filtering conditions.
#columns: ratings.rating_score, ratings.rating_id, ratings.rating_timestamp_utc, movies.movie_title
#SELECT: average score refer to Avg(rating_score)
#values: 'The Fall of Berlin' refer to movies.movie_title = 'The Fall of Berlin', 2019 refer to ratings.rating_timestamp_utc = 2019
#SQL-like: Show Avg(rating_score), where ratings.rating_timestamp_utc = 2019 and movies.movie_title = 'The Fall of Berlin'

/* extract and rewrite example */
#question: How many distinct orders were there in 2003 when the quantity ordered was less than 30? "year(orderDate) = '2003'; quantityOrdered < 30;"
SQL: SELECT COUNT(DISTINCT T1.orderNumber) FROM orderdetails AS T1 INNER JOIN orders AS T2 ON T1.orderNumber = T2.orderNumber WHERE T1.quantityOrdered < 30 AND STRFTIME('%Y', T2.orderDate) = '2003'
#reason:  The question requires display in order: "How many distinct orders". " in 2003", "less than 30" are filtering conditions.
#columns: orderdetails.orderNumber, orderdetails.quantityOrdered, orders.orderDate
#SELECT: How many distinct orders refer to COUNT(DISTINCT orderdetails.orderNumber)
#values: 30 refer to quantityOrdered < 30, 2003 refer to year(orderDate) = '2003'
#SQL-like: Show COUNT(DISTINCT orderdetails.orderNumber), where orders.orderDate = 2003 and orderdetails.quantityOrdered < 30

#Please provide answer based on the requirements below using the provided questions and SQL:
1. After #reason, follow the example above to analyze how to generate SQL based on question.
2. After #columns, Provide candidate columns for the question generate SQL
3. After #SELECT, provide the content that SQL should display in order
4. After #values, provide the filtering conditions that exist in SQL
5. After #SQL-like, rewrite the question to SQL-like in the format: "Show #SELECT (table.column), WHERE condition are xxx (refer to #values), Group by/Order By (refer to columns)
6. The text format you will receive is:
```
#question: {{question}}\nSQL:{{SQL}}\n#answer:
```
Please respond in the following format without any other content:
``` 
#reason: Analyze how to generate SQL based on the question.
#columns: All columns ultimately used in SQL
#SELECT: the content that SQL should display in order
#values: the filtering conditions that exist in SQL 
#SQL-like: SQL-like statements that ignore join conditions
```

Now, you need to process the following text:
#question: {question}
SQL: {sql}
#answer:
"""

prompts_fewshot_parse3="""/* extract and rewrite example */
#question: Please give the name of the course in which most numbers of the students got an A. Also, list the full name of the students who got an A in this course. most number of students got an A refers MAX(COUNT(student_id WHERE grade = 'A')); full name = f_name, l_name; got an A refers to grade = 'A';
SQL: SELECT T3.name, T2.f_name, T2.l_name FROM registration AS T1 INNER JOIN student AS T2 ON T1.student_id = T2.student_id INNER JOIN course AS T3 ON T1.course_id = T3.course_id WHERE T1.grade = 'A' GROUP BY T3.name ORDER BY COUNT(T1.student_id) DESC LIMIT 1
#reason: The question requires display in order: "name of the course", "full name"."A" is filtering condition.
#SELECT: course.name, student.f_name, student.l_name
#columns: course.name, student.f_name, student.l_name, registration.grade, registration.student_id
#values: A
#Standardization: Show the name of course and full name of students, the condition is the course which most students got an A.
#SQL-like: Show course.name, student.f_name, student.l_name, where registration.grade = 'A' , group by course.name, order by the number of T1.student_id

/* extract and rewrite example */
#question:How much more votes for episode 1 than for episode 5? more votes refers to SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
SQL: SELECT SUM(CASE WHEN T1.episode = 1 THEN T2.votes ELSE 0 END) - SUM(CASE WHEN T1.episode = 5 THEN T2.votes ELSE 0 END) AS diff FROM Episode AS T1 INNER JOIN Vote AS T2 ON T2.episode_id = T1.episode_id;
#reason: The question requires display in order: "How much more vote". The definition of "more vote" is SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5)). 1, 5 are filtering conditions.
#SELECT: SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))
#columns: Episode.episode, Vote.votes
#values:1, 5
#Standardization: Show the number of votes by which the total votes for episode 1 exceed the total votes for episode 5.
#SQL-like: Show SUBTRACT(SUM(votes when episode = 1), SUM(votes when episode = 5))

/* extract and rewrite example */
#question: What is the average score of the movie "The Fall of Berlin" in 2019? Average score refers to Avg(rating_score);
SQL: SELECT SUM(T1.rating_score) / COUNT(T1.rating_id) FROM ratings AS T1 INNER JOIN movies AS T2 ON T1.movie_id = T2.movie_id WHERE T1.rating_timestamp_utc LIKE '2019%' AND T2.movie_title LIKE 'The Fall of Berlin'
#reason: The question requires display in order: "average score". Average score is Avg(rating_score), "The Fall of Berlin",2019 are filtering conditions.
#SELECT: Avg(rating_score)
#columns: ratings.rating_score, ratings.rating_id, ratings.rating_timestamp_utc, movies.movie_title
#values: The Fall of Berlin, 2019
#Standardization: Show the average score of the movie "The Fall of Berlin" in 2019?
#SQL-like: Show Avg(rating_score), where ratings.rating_timestamp_utc = 2019 and movies.movie_title = 'The Fall of Berlin'

/* extract and rewrite example */
#question: How many distinct orders were there in 2003 when the quantity ordered was less than 30? "year(orderDate) = '2003'; quantityOrdered < 30;"
SQL: SELECT COUNT(DISTINCT T1.orderNumber) FROM orderdetails AS T1 INNER JOIN orders AS T2 ON T1.orderNumber = T2.orderNumber WHERE T1.quantityOrdered < 30 AND STRFTIME('%Y', T2.orderDate) = '2003'
#reason:  The question requires display in order: "How many distinct orders"." in 2003", "less than 30" are filtering conditions.
#SELECT: COUNT(DISTINCT orderdetails.orderNumber)
#columns: orderdetails.orderNumber, orderdetails.quantityOrdered, orders.orderDate
#values: 30, 2003
#Standardization: Show the number of distinct orders, the condition is time in 2003 and quantity ordered was less than 30
#SQL-like: Show COUNT(DISTINCT orderdetails.orderNumber), where orders.orderDate = 2003 and orderdetails.quantityOrdered < 30

#Now, you need to process the question content based on the evidence and SQL:
1. Standardize the question into a format that aligns more closely with SQL, in order to clearly reflect components: SELECT, WHERE, GROUP BY, ORDER BY, etc.
2. provide the SQL query result set (the SELECT part in SQL, requested columns by the question), candidate columns for the question, and extract all values from the query according to the database information. Please list the query result set in the format of table.column after "#SELECT", list relevant candidate columns in the format of table.field after "#columns". List the values the question want to query after "#values". Use a comma "," to separate values and columns, and separate columns and values with a tab. The text format you will receive is ```question: {{question}}\evidence:{{define or evidence}}\nSQL:{{SQL}}\n#answer:```, and the output format you need to provide is #reason:{{why pick query, columns and values}}\n#SELECT:{{which to SELECT}}\n#columns:{{related columns}}\n#values:{{values}} #Standardization:{{standardize question}} #SQL-like:{{SQL-like question}}
Now, you need to process the following text:

#question: {question}
SQL: {sql}
#answer:
"""


select_prompt="""现在我们定义一个问句的语法原子单元如下:
Q: 询问词: 如 calculate\ Include\ List\ List out\ List all\ give\ state\ Name\ In which\ How many\  which\ what\ who\ when\ provide\ Tally\ identify\ Find\ mention\ write等
J: 判断词： 如 Do\ Did\ If\ Is\ Are等
I: 查询内容: 查询的主体内容, 如: name, ID, date, location, item, biggest city.
C: 条件句: 通过介词和连词引入的查询的要求或属性, 如大于、等于、排序、聚合等. 介词和连词有: of\ have\ with\ that\ by. 条件句的形式例子有: with condition\ have condition\ of attribute\ that was condition


一个问题通过这些原子串联起来。常见的串联方式有
QIC(询问句): List the student with score more than 80: Q: 'List' I: 'the student' C: 'with score more than 80'
JC(判断句): State if Tom is a Cat? : J: 'State if C: is a Cat?'
C(条件句): For all people in Beijing
现在请你针对下面的问题, 把问题中的内容按照上述原子定义提取出来
问题如下: {question}

请按照下面的json格式进行回答:

```json
[{{"Type":"类型(QIC,JC,C)",
"Extract":{{//不存在的填null
    "Q":"询问词",
    "J":"判断词",
    "I":['查询内容a', '查询内容b'],//只有查询内容用and或alongside连接时,才分成多个实体填入List
    "C":["条件句a","属性b"]
}}}},
{{}}]
```"""

vote_prompt="""现在有问题如下:
#question: {question}
对应这个问题有如下几个SQL,请你从中选择最接近问题要求的SQL:
{sql}

请在上面的几个SQL中选择最符合题目要求的SQL, 不要回复其他内容:
#SQL:"""