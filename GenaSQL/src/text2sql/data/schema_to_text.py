from typing import Any, Dict, List, Optional



def schema_to_basic_format(
    database_name: str, schema: dict[str, Any], include_types: bool = False, include_relations: bool = False
) -> str:
    """represent schema in basic table (column, column, ...) format (following DAIL-SQL)

    this supports optional inclusion of column types and relations
    """
    output = []

    for table_name, table_info in schema["tables"].items():
        columns = []
        for col_name, col_type in table_info["columns"].items():
            col_name = str(col_name)  # Convert to string in case it's an integer
            if include_types:
                columns.append(f"{col_name} ({col_type})")
            else:
                columns.append(col_name)

        table_line = f"table '{table_name}' with columns: {' , '.join(columns)}"
        output.append(table_line)

    if include_relations:
        output.append("\nRelations:")
        for table_name, table_info in schema["tables"].items():
            if "foreign_keys" in table_info and table_info["foreign_keys"]:
                for fk_column, fk_info in table_info["foreign_keys"].items():
                    fk_column = str(fk_column)  # Convert to string in case it's an integer
                    ref_table = fk_info["referenced_table"]
                    ref_column = fk_info["referenced_column"]
                    relation = f"{table_name}.{fk_column} -> {ref_table}.{ref_column}"
                    output.append(relation)

    return "\n".join(output)


def schema_to_sql_create(database_name: str, schema: dict[str, Any]) -> str:
    """represent schema as an SQL CREATE query statement (following DAIL-SQL)"""
    output = [f"{database_name} CREATE messages:\n"]

    for table_name, table_info in schema["tables"].items():
        create_statement = [f"CREATE TABLE {table_name} ("]
        column_definitions = []
        constraints = []

        # Columns
        for col_name, col_type in table_info["columns"].items():
            col_name = str(col_name)  # Convert to string in case it's an integer
            column_definitions.append(f"    {col_name} {col_type}")

        # Primary Key
        if "keys" in table_info and table_info["keys"].get("primary_key"):
            pk_columns = ", ".join(str(col) for col in table_info["keys"]["primary_key"])
            constraints.append(f"    PRIMARY KEY ({pk_columns})")

        # Foreign Keys
        if "foreign_keys" in table_info:
            for fk_column, fk_info in table_info["foreign_keys"].items():
                fk_column = str(fk_column)  # Convert to string in case it's an integer
                ref_table = fk_info["referenced_table"]
                ref_column = fk_info["referenced_column"]
                constraints.append(f"    FOREIGN KEY ({fk_column}) REFERENCES {ref_table} ({ref_column})")

        # Combine all parts of the CREATE TABLE statement
        create_statement.extend(column_definitions)
        if constraints:
            create_statement.extend([","] + constraints)
        create_statement.append(");")

        # Join all lines of the CREATE TABLE statement
        output.append("\n".join(create_statement))
        output.append("")  # Add an empty line between tables

    return "\n".join(output)


def schema_to_datagrip_format(database_name: str, schema: dict[str, Any]) -> str:
    """generate a very detailed schema description similar to Datagrip"""
    output = [f"{database_name} schema:"]
    output.append("    + tables")

    for table_name, table_info in schema["tables"].items():
        output.append(f"        {table_name}: table")

        # Columns
        output.append("            + columns")
        for col_name, col_type in table_info["columns"].items():
            col_name = str(col_name)  # Convert to string in case it's an integer
            output.append(f"                {col_name}: {col_type}")

        # Keys
        if "keys" in table_info and table_info["keys"]:
            output.append("            + keys")
            for key_name, key_columns in table_info["keys"].items():
                if key_name == "primary_key":
                    key_name = f"{table_name}_pk"
                key_columns = [str(col) for col in key_columns]  # Convert all column names to strings
                output.append(f"                {key_name}: PK ({', '.join(key_columns)})")

        # Foreign Keys
        if "foreign_keys" in table_info and table_info["foreign_keys"]:
            output.append("            + foreign-keys")
            for fk_column, fk_info in table_info["foreign_keys"].items():
                fk_column = str(fk_column)  # Convert to string in case it's an integer
                ref_table = fk_info["referenced_table"]
                ref_column = fk_info["referenced_column"]
                fk_name = f"{table_name}_{fk_column}_fk"
                output.append(
                    f"                {fk_name}: foreign key ({fk_column}) -> {ref_table}[.{ref_table}_pk] ({ref_column})"
                )

        output.append("")  # Add an empty line between tables

    return "\n".join(output)


def get_m_schema_column_samples(
    dataset: "BaseDataset",
    database_name: str,
    schema: Dict[str, Any],
    max_examples: int = 3,
) -> Dict[str, Dict[str, List[Any]]]:
    """Get sample values for each column in the schema, following m-schema.
    
    Args:
        dataset: The dataset instance to use for querying
        database_name: Name of the database to query
        schema: Schema dictionary 
        max_examples: Maximum number of samples to return per column, default 3
        
    Returns:
        Dictionary mapping table names to column names to lists of sample values
        {
            "table1": {
                "column1": ["value1", "value2", "value3"],
                "column2": ["value4", "value5", "value6"]
            },
            ...
        }
    """
    samples = {}
    
    for table_name, table_info in schema["tables"].items():
        samples[table_name] = {}
        
        # Process each column separately to get distinct values
        for col_name, col_type in table_info["columns"].items():
            # Quote column name to handle special characters and numbers
            quoted_col = f'"{col_name}"'
            
            # Create a query to get distinct sample values for this column
            query = f'SELECT DISTINCT {quoted_col} FROM "{table_name}" WHERE {quoted_col} IS NOT NULL LIMIT {max_examples}'
            
            try:
                # Execute the query and get results
                results = dataset.query_database(database_name, query)
                
                # Collect non-None values
                col_samples = []
                for row in results:
                    if col_name in row and row[col_name] is not None:
                        col_samples.append(str(row[col_name]))  # Convert to string early
                
                # Apply m-schema example selection rules
                if col_samples:
                    # For date/time types, only show first example
                    col_type = table_info["columns"][col_name].upper()
                    if any(t in col_type for t in ['DATE', 'TIME', 'DATETIME', 'TIMESTAMP']):
                        col_samples = [col_samples[0]]
                    else:
                        # Check for long examples
                        max_len = max(len(s) for s in col_samples)
                        if max_len > 50:
                            col_samples = []
                        elif max_len > 20:
                            col_samples = [col_samples[0]]
                        else:
                            col_samples = col_samples[:max_examples]
                
                # Store the samples for this column
                samples[table_name][col_name] = col_samples
                
            except Exception as e:
                # If query fails, leave empty samples for this column
                print(f"Warning: Could not get samples for column {col_name} in table {table_name}: {str(e)}")
                samples[table_name][col_name] = []
    
    return samples


def schema_to_m_schema_format(
    database_name: str,
    schema: dict[str, Any],
    column_samples: dict[str, dict[str, list[Any]]]
) -> str:
    """represent schema in m-schema format (following m-schema.txt)
    
    Args:
        database_name: Name of the database
        schema: Schema dictionary 
        column_samples: Dictionary of sample values from get_m_schema_column_samples()
    """
    output = []
    
    # Add DB_ID header
    output.append(f"【DB_ID】 {database_name}")
    output.append("【Schema】")
    
    # Process each table
    for table_name, table_info in schema["tables"].items():
        # Add table header
        output.append(f"# Table: {table_name}")
        output.append("[")
        
        # Process each column
        column_lines = []
        for col_name, col_type in table_info["columns"].items():
            col_name = str(col_name)  # Convert to string in case it's an integer
            col_line = f"({col_name}:{col_type.upper()}"
            
            # Add primary key if applicable
            if "keys" in table_info and "primary_key" in table_info["keys"]:
                if col_name in table_info["keys"]["primary_key"]:
                    col_line += ", Primary Key"
            
            # Add examples if available
            if table_name in column_samples and col_name in column_samples[table_name]:
                samples = column_samples[table_name][col_name]
                if samples:
                    sample_str = ", ".join(str(s) for s in samples)
                    col_line += f", Examples: [{sample_str}]"
            
            col_line += ")"
            column_lines.append(col_line)
        
        # Add all column lines
        output.append(",\n".join(column_lines))
        output.append("]")
    
    # Add foreign keys section
    has_foreign_keys = False
    for table_name, table_info in schema["tables"].items():
        if "foreign_keys" in table_info and table_info["foreign_keys"]:
            has_foreign_keys = True
            break
    
    if has_foreign_keys:
        output.append("【Foreign keys】")
        for table_name, table_info in schema["tables"].items():
            if "foreign_keys" in table_info:
                for fk_column, fk_info in table_info["foreign_keys"].items():
                    fk_column = str(fk_column)  # Convert to string in case it's an integer
                    ref_table = fk_info["referenced_table"]
                    ref_column = fk_info["referenced_column"]
                    output.append(f"{table_name}.{fk_column}={ref_table}.{ref_column}")
    
    return "\n".join(output)


def get_mac_schema_column_samples(
    dataset: "BaseDataset",
    database_name: str,
    schema: Dict[str, Any],
    max_examples: int = 6,
) -> Dict[str, Dict[str, List[Any]]]:
    """Get sample values for each column in the schema, following mac-schema logic.
    
    Args:
        dataset: The dataset instance to use for querying
        database_name: Name of the database to query
        schema: Schema dictionary 
        max_examples: Maximum number of examples to return per column, default 6
        
    Returns:
        Dictionary mapping table names to column names to lists of sample values
        {
            "table1": {
                "column1": ["value1", "value2", "value3"],
                "column2": ["value4", "value5", "value6"]
            },
            ...
        }
    """
    samples = {}
    
    for table_name, table_info in schema["tables"].items():
        samples[table_name] = {}
        
        # Get primary and foreign keys for this table
        primary_keys = table_info.get("keys", {}).get("primary_key", [])
        foreign_keys = list(table_info.get("foreign_keys", {}).keys())
        
        # Process each column
        for col_name, col_type in table_info["columns"].items():
            # Skip if column is a key
            if col_name in primary_keys or col_name in foreign_keys:
                continue
                
            # Skip if column name ends with certain patterns
            if col_name.lower().endswith(('id', 'email', 'url')):
                continue
                
            # For numeric types, check if we should skip
            if col_type.upper() in ['INTEGER', 'REAL', 'NUMERIC', 'FLOAT', 'INT']:
                # Query to count distinct values
                quoted_col = f'"{col_name}"'
                count_query = f'SELECT COUNT(DISTINCT {quoted_col}) FROM "{table_name}"'
                try:
                    results = dataset.query_database(database_name, count_query)
                    unique_count = results[0][0]
                    if unique_count > 10:
                        continue
                except Exception:
                    continue
            
            # Get ALL distinct values first, sorted by frequency - EXACTLY as in agents.py
            quoted_col = f'"{col_name}"'
            query = f'SELECT {quoted_col} FROM "{table_name}" GROUP BY {quoted_col} ORDER BY COUNT(*) DESC'
            
            try:
                results = dataset.query_database(database_name, query)
                col_samples = []
                
                # Process all values first before applying filters
                for row in results:
                    if col_name in row and row[col_name] is not None:
                        value = str(row[col_name]).strip()
                        if value:
                            col_samples.append(value)
                
                # Apply filters to ALL values, not just the first N
                if col_samples:
                    # For text columns, filter out URLs and emails
                    if col_type.upper() in ['TEXT', 'VARCHAR']:
                        filtered_samples = []
                        for value in col_samples:
                            if 'https://' in value or 'http://' in value:
                                continue
                            if len(value) > 50:
                                continue
                            filtered_samples.append(value)
                        col_samples = filtered_samples
                    
                    # For date columns, only take one example
                    if col_type.upper() in ['DATE', 'TIME', 'DATETIME', 'TIMESTAMP']:
                        col_samples = col_samples[:1]
                    
                    # Store the samples if we have any
                    if col_samples:
                        # Only take up to max_examples after all filtering
                        samples[table_name][col_name] = col_samples[:max_examples]
                    
            except Exception as e:
                print(f"Warning: Could not get samples for column {col_name} in table {table_name}: {str(e)}")
    
    return samples


def schema_to_mac_schema_format(
    database_name: str,
    schema: dict[str, Any],
    column_samples: dict[str, dict[str, list[Any]]],
    table_descriptions: Optional[dict] = None
) -> str:
    """represent schema in mac-schema format (following mac-schema.txt)
    
    Args:
        database_name: Name of the database
        schema: Schema dictionary 
        column_samples: Dictionary of sample values from get_mac_schema_column_samples()
        table_descriptions: Optional dictionary containing table and column descriptions
    """
    output = []
    
    # Process each table
    for table_name, table_info in schema["tables"].items():
        # Add table header
        output.append(f"# Table: {table_name}")
        output.append("[")
        
        # Process each column
        column_lines = []
        columns = list(table_info["columns"].items())
        for i, (col_name, col_type) in enumerate(columns):
            col_name = str(col_name)  # Convert to string in case it's an integer
            
            # Start building column line
            col_line = f"  ({col_name},"
            
            # Add column description if available
            if table_descriptions:
                # Find the column in table_descriptions
                col_desc = None
                for col_idx, (tb_idx, orig_col_name) in enumerate(table_descriptions["column_names_original"]):
                    if tb_idx == table_descriptions["table_names_original"].index(table_name) and orig_col_name == col_name:
                        col_desc = table_descriptions["column_names"][col_idx][1]
                        break
                
                if col_desc:
                    col_line += f" {col_desc}."
            
            # Add examples if available
            if table_name in column_samples and col_name in column_samples[table_name]:
                samples = column_samples[table_name][col_name]
                if samples:
                    sample_str = str(samples)
                    col_line += f" Value examples: {sample_str}."
            
            col_line += ")"
            
            # Add comma if this is not the last column
            if i < len(columns) - 1:
                col_line += ","
                
            column_lines.append(col_line)
        
        # Add all column lines
        output.append("\n".join(column_lines))
        output.append("]")
    
    return "\n".join(output)
