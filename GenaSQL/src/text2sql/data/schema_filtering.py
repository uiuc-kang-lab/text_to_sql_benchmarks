def parse_mac_schema(text: str, filter_dict: dict[str, list[str]], force_keep_all=False) -> str:
    """filter a mac-schema schema description text based on dictionary of table -> columns to keep"""
    lines = text.strip().split("\n")
    current_table = None

    new_schema = []

    for line in lines:
        # Check for table declaration
        if line.startswith("# Table:"):
            current_table = line.replace("# Table:", "").strip()
            if current_table in filter_dict:
                if new_schema:
                    new_schema.append("]")
                new_schema.append(line)
                new_schema.append("[")

        if current_table not in filter_dict:
            continue

        keep_all = filter_dict[current_table] == "keep_all" or force_keep_all
        # If we're inside a table definition and line contains a column definition
        if current_table is not None and line.strip().startswith("("):
            # Extract column name from the tuple format (column_name, description)
            try:
                column_name = (
                    line.strip().strip("(),").split(",")[0].split(":")[0].strip()
                )
                if keep_all:
                    new_schema.append(line)
                elif column_name in filter_dict[current_table]:
                    new_schema.append(line)
                # print(column_name)
            except IndexError:
                pass  # Skip malformed lines
    new_schema = new_schema + ["]"]

    return "\n".join(new_schema)


def parse_m_schema(text: str, filter_dict: dict[str, list[str]], force_keep_all=False) -> str:
    """filter a m-schema schema description text based on dictionary of table -> columns to keep"""
    lines = text.strip().split("\n")
    current_table = None

    new_schema = []

    for line in lines:
        # Check for table declaration
        if line.startswith("# Table:"):
            current_table = line.replace("# Table:", "").strip()
            if current_table in filter_dict:
                if new_schema:
                    new_schema.append("]")
                new_schema.append(line)
                new_schema.append("[")

        if current_table not in filter_dict:
            continue

        keep_all = filter_dict[current_table] == "keep_all" or force_keep_all
        # If we're inside a table definition and line contains a column definition
        if current_table is not None and line.strip().startswith("("):
            # Extract column name from the tuple format (column_name, description)
            try:
                column_name = (
                    line.strip().strip("(),").split(",")[0].split(":")[0].strip()
                )
                if keep_all:
                    new_schema.append(line)
                elif column_name in filter_dict[current_table]:
                    new_schema.append(line)
                # print(column_name)
            except IndexError:
                pass  # Skip malformed lines
    new_schema = lines[:2] + new_schema + ["]"]

    new_fk = []
    if "【Foreign keys】" in text:
        fk_part = text.split("【Foreign keys】")[-1].strip().split("\n")
        for line in fk_part:
            try:
                left, right = line.split("=")
            except Exception as e:
                print(text)
                raise e
            left_table, left_col = left.split(".")
            right_table, right_col = right.split(".")

            if (
                left_table in filter_dict
                and (
                    filter_dict[left_table] == "keep_all"
                    or left_col in filter_dict[left_table]
                )
                and right_table in filter_dict
                and (
                    filter_dict[right_table] == "keep_all"
                    or right_col in filter_dict[right_table]
                )
            ):
                new_fk.append(line)

        if new_fk:
            new_schema.append("【Foreign keys】")
            new_schema += new_fk

    return "\n".join(new_schema)

def parse_sql_create(text: str, filter_dict: dict[str, list[str]], force_keep_all=False) -> str:
    """filter a SQL CREATE schema description text based on dictionary of table -> columns to keep"""
    lines = text.strip().split("\n")
    new_schema = []
    current_create = []
    in_create = False
    current_table = None
    has_columns = False

    # Keep the header line
    if lines and "CREATE messages:" in lines[0]:
        new_schema.append(lines[0])
        new_schema.append("")  # Add empty line after header
        lines = lines[1:]

    for line in lines:
        # Check for CREATE TABLE statement
        if line.strip().startswith("CREATE TABLE"):
            if current_create:
                # Add comma after columns if we have any
                if has_columns:
                    current_create.append(",")
                new_schema.extend(current_create)
                new_schema.append("")
            table_name = line.split("CREATE TABLE")[1].strip().split()[0]
            current_table = table_name
            
            if current_table in filter_dict:
                current_create = [line]
                in_create = True
                has_columns = False
            else:
                in_create = False
                current_create = []
            continue

        if not in_create:
            continue

        keep_all = filter_dict[current_table] == "keep_all" or force_keep_all

        # Handle column definitions
        if line.strip() and not line.strip().startswith("PRIMARY KEY") and not line.strip().startswith("FOREIGN KEY") and not line.strip() == "," and not line.strip() == ");":
            column_name = line.strip().split()[0]
            if keep_all or column_name in filter_dict[current_table]:
                current_create.append(line)
                has_columns = True
            continue

        # Handle comma after columns
        if line.strip() == ",":
            if has_columns:
                current_create.append(line)
            continue

        # Handle PRIMARY KEY constraint
        if line.strip().startswith("PRIMARY KEY"):
            pk_columns = line.strip().split("(")[1].split(")")[0].split(",")
            pk_columns = [col.strip() for col in pk_columns]
            if keep_all or all(col in filter_dict[current_table] for col in pk_columns):
                current_create.append(line)
            continue

        # Handle FOREIGN KEY constraint
        if line.strip().startswith("FOREIGN KEY"):
            fk_parts = line.strip().split("REFERENCES")
            fk_col = fk_parts[0].split("(")[1].split(")")[0].strip()
            ref_table = fk_parts[1].split("(")[0].strip()
            ref_col = fk_parts[1].split("(")[1].split(")")[0].strip()
            
            # Only keep foreign key if both the column and referenced column are kept
            if (keep_all or fk_col in filter_dict[current_table]) and \
               (ref_table in filter_dict and 
                (filter_dict[ref_table] == "keep_all" or ref_col in filter_dict[ref_table])):
                current_create.append(line)
            continue

        # Handle closing parenthesis
        if line.strip() == ");":
            if current_create:
                current_create.append(line)
                new_schema.extend(current_create)
                new_schema.append("")
            in_create = False
            current_create = []

    # Add any remaining CREATE statement
    if current_create:
        # Add comma after columns if we have any
        if has_columns:
            current_create.append(",")
        new_schema.extend(current_create)
        new_schema.append("")

    return "\n".join(new_schema)


from copy import deepcopy
from text2sql.data.schema_to_text import schema_to_sql_create

def filter_schema_dict(column_dict: dict, filter_dict: dict) -> tuple[dict, dict]:
    """filter the dataset schema dict based on the filter dict from schema linking"""
    column_dict = deepcopy(column_dict)  # Make a deep copy of the input dictionary
    pop_keys = []
    pop_cols = {}
    pop_fks = {}

    for table_name in column_dict["tables"]:
        if table_name not in filter_dict:
            pop_keys.append(table_name)
            continue

        pop_cols[table_name] = []
        pop_fks[table_name] = []
        if filter_dict[table_name] == "keep_all":
            continue
        for col in column_dict["tables"][table_name]["columns"]:
            if col not in filter_dict[table_name]:
                pop_cols[table_name].append(col)
        for fk_col in column_dict["tables"][table_name]["foreign_keys"]:
            if fk_col not in filter_dict[table_name]:
                pop_fks[table_name].append(fk_col)
                continue
            referenced_table = column_dict["tables"][table_name]["foreign_keys"][
                fk_col
            ]["referenced_table"]
            referenced_column = column_dict["tables"][table_name]["foreign_keys"][
                fk_col
            ]["referenced_column"]
            if referenced_table not in filter_dict:
                pop_fks[table_name].append(fk_col)
                continue
            if referenced_column not in filter_dict[referenced_table]:
                pop_fks[table_name].append(fk_col)
                continue

    for key in pop_keys:
        column_dict["tables"].pop(key)

    for table_name in pop_cols:
        for col in pop_cols[table_name]:
            column_dict["tables"][table_name]["columns"].pop(col)

    for table_name in pop_fks:
        for col in pop_fks[table_name]:
            column_dict["tables"][table_name]["foreign_keys"].pop(col)

    return column_dict


def parse_sql_create_from_source(dataset: "BaseDataset", database_name: str, filter_dict: dict[str, list[str]], force_keep_all=False) -> str:
    """filter a SQL CREATE schema description text based on dictionary of table -> columns to keep"""
    schema_dict = deepcopy(dataset.get_database_schema(database_name))
    filter_dict = deepcopy(filter_dict)
    if force_keep_all:
        for key in filter_dict.keys():
            filter_dict[key] = "keep_all"
    filtered_column_dict = filter_schema_dict(schema_dict, filter_dict)
    return schema_to_sql_create(database_name, filtered_column_dict)


def parse_basic_format(text: str, filter_dict: dict[str, list[str]], include_types: bool = False, include_relations: bool = False, force_keep_all=False) -> str:
    """filter a basic format schema description text based on dictionary of table -> columns to keep
    
    Args:
        text: The schema description text
        filter_dict: Dictionary mapping table names to lists of columns to keep
        include_types: Whether to include column types in the output
        include_relations: Whether to include foreign key relations
        force_keep_all: If True, keep all columns for tables in filter_dict
    """
    lines = text.strip().split("\n")
    new_schema = []
    relations = []
    current_table = None

    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Check if this is a table line
        if line.startswith("table '") and "' with columns:" in line:
            table_parts = line.split("'")
            current_table = table_parts[1]
            
            if current_table not in filter_dict:
                continue

            # Extract columns
            columns_part = line.split("columns:")[1].strip()
            columns = [col.strip() for col in columns_part.split(",")]
            
            # Filter columns
            keep_all = filter_dict[current_table] == "keep_all" or force_keep_all
            filtered_columns = []
            
            for col in columns:
                if include_types:
                    # Handle columns with types: "col_name (type)"
                    col_name = col.split("(")[0].strip()
                    if keep_all or col_name in filter_dict[current_table]:
                        filtered_columns.append(col)
                else:
                    # Handle columns without types
                    if keep_all or col in filter_dict[current_table]:
                        filtered_columns.append(col)

            if filtered_columns:
                new_line = f"table '{current_table}' with columns: {', '.join(filtered_columns)}"
                new_schema.append(new_line)

        # Handle relations section
        elif include_relations and "->" in line:
            left, right = line.split("->")
            left_table, left_col = left.strip().split(".")
            right_table, right_col = right.strip().split(".")

            # Only keep relation if both tables and columns are kept
            if (left_table in filter_dict and 
                right_table in filter_dict and
                (filter_dict[left_table] == "keep_all" or left_col in filter_dict[left_table]) and
                (filter_dict[right_table] == "keep_all" or right_col in filter_dict[right_table])):
                relations.append(line)

    # Add relations section if needed
    if include_relations and relations:
        new_schema.append("")
        new_schema.append("Relations:")
        new_schema.extend(relations)

    return "\n".join(new_schema)

def parse_datagrip_format(text: str, filter_dict: dict[str, list[str]], force_keep_all=False) -> str:
    """filter a datagrip format schema description text based on dictionary of table -> columns to keep
    
    The datagrip format is hierarchical with indentation and plus signs marking categories:
    - Top level: "+ tables"
    - For each table:
      - "+ columns" with column names and types
      - "+ keys" with primary keys
      - "+ foreign-keys" with foreign key relationships
    """
    lines = text.strip().split("\n")
    new_schema = []
    current_table = None
    in_table = False
    in_columns = False
    in_keys = False
    in_foreign_keys = False

    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Get indentation level
        indent = len(line) - len(line.lstrip())
        
        # Handle schema header
        if "schema:" in line:
            new_schema.append(line)
            continue

        # Handle tables section start
        if "+ tables" in line:
            new_schema.append(line)
            continue

        # Handle table declaration
        if indent == 8 and ":" in line and not line.startswith("+"):
            table_name = line.split(":")[0].strip()
            current_table = table_name
            
            if current_table in filter_dict:
                new_schema.append(line)
                in_table = True
            else:
                in_table = False
            continue

        # Skip lines if not in a kept table
        if not in_table:
            continue

        # Handle columns section
        if indent == 12 and "+ columns" in line:
            new_schema.append(line)
            in_columns = True
            in_keys = False
            in_foreign_keys = False
            continue

        # Handle keys section
        if indent == 12 and "+ keys" in line:
            new_schema.append(line)
            in_columns = False
            in_keys = True
            in_foreign_keys = False
            continue

        # Handle foreign keys section
        if indent == 12 and "+ foreign-keys" in line:
            new_schema.append(line)
            in_columns = False
            in_keys = False
            in_foreign_keys = True
            continue

        # Handle column definitions
        if in_columns and indent == 16:
            col_name = line.split(":")[0].strip()
            keep_all = filter_dict[current_table] == "keep_all" or force_keep_all
            if keep_all or col_name in filter_dict[current_table]:
                new_schema.append(line)

        # Handle primary key definitions
        if in_keys and indent == 16:
            pk_cols = line.split("(")[1].split(")")[0].split(",")
            pk_cols = [col.strip() for col in pk_cols]
            keep_all = filter_dict[current_table] == "keep_all" or force_keep_all
            if keep_all or all(col in filter_dict[current_table] for col in pk_cols):
                new_schema.append(line)

        # Handle foreign key definitions
        if in_foreign_keys and indent == 16:
            # Extract foreign key info
            fk_parts = line.split("->")
            fk_col = fk_parts[0].split("(")[1].split(")")[0].strip()
            ref_table = fk_parts[1].split("[")[0].strip()
            ref_col = fk_parts[1].split("(")[1].split(")")[0].strip()

            # Check if both tables and columns are kept
            keep_all = filter_dict[current_table] == "keep_all" or force_keep_all
            if (keep_all or fk_col in filter_dict[current_table]) and \
               (ref_table in filter_dict and 
                (filter_dict[ref_table] == "keep_all" or ref_col in filter_dict[ref_table])):
                new_schema.append(line)

    return "\n".join(new_schema)