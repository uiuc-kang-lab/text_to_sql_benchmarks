import datetime
import decimal
import json
import re
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union
from typing import Sequence as _typing_Sequence

import sqlalchemy
from sqlalchemy import MetaData, Table, create_engine, insert, inspect, select, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import OperationalError, ProgrammingError


@sqlalchemy.util.preload_module("sqlalchemy.engine.reflection")
def reflect(
    self,
    bind: Union[Engine, Connection],
    schema: Optional[str] = None,
    views: bool = False,
    only: Union[
        _typing_Sequence[str], Callable[[str, MetaData], bool], None
    ] = None,
    extend_existing: bool = False,
    autoload_replace: bool = True,
    resolve_fks: bool = True,
    **dialect_kwargs: Any,
) -> None:
    with sqlalchemy.inspection.inspect(bind)._inspection_context() as insp:
        reflect_opts: Any = {
            "autoload_with": insp,
            "extend_existing": extend_existing,
            "autoload_replace": autoload_replace,
            "resolve_fks": resolve_fks,
            "_extend_on": set(),
        }

        reflect_opts.update(dialect_kwargs)

        if schema is None:
            schema = self.schema

        if schema is not None:
            reflect_opts["schema"] = schema

        kind = sqlalchemy.util.preloaded.engine_reflection.ObjectKind.TABLE
        available: sqlalchemy.util.OrderedSet[str] = sqlalchemy.util.OrderedSet(
            insp.get_table_names(schema)
        )
        if views:
            kind = sqlalchemy.util.preloaded.engine_reflection.ObjectKind.ANY
            available.update(insp.get_view_names(schema))
            try:
                available.update(insp.get_materialized_view_names(schema))
            except NotImplementedError:
                pass

        if schema is not None:
            available_w_schema: sqlalchemy.util.OrderedSet[str] = sqlalchemy.util.OrderedSet(
                [f"{schema}.{name}" for name in available]
            )
        else:
            available_w_schema = available

        current = set(self.tables)

        if only is None:
            load = [
                name
                for name, schname in zip(available, available_w_schema)
                if extend_existing or schname not in current
            ]
        elif callable(only):
            load = [
                name
                for name, schname in zip(available, available_w_schema)
                if (extend_existing or schname not in current)
                and only(name, self)
            ]
        else:
            missing = [name for name in only if name not in available]
            if missing:
                s = schema and (" schema '%s'" % schema) or ""
                missing_str = ", ".join(missing)
                raise sqlalchemy.exc.InvalidRequestError(
                    f"Could not reflect: requested table(s) not available "
                    f"in {bind.engine!r}{s}: ({missing_str})"
                )
            load = [
                name
                for name in only
                if extend_existing or name not in current
            ]
        # pass the available tables so the inspector can
        # choose to ignore the filter_names
        _reflect_info = insp._get_reflection_info(
            schema=schema,
            filter_names=load,
            available=available,
            kind=kind,
            scope=sqlalchemy.util.preloaded.engine_reflection.ObjectScope.ANY,
            **dialect_kwargs,
        )
        reflect_opts["_reflect_info"] = _reflect_info

        for name in load:
            try:
                Table(name, self, **reflect_opts)
            except sqlalchemy.exc.UnreflectableTableError as uerr:
                sqlalchemy.util.warn(f"Skipping table {name}: {uerr}")
            except Exception as uerr:
                sqlalchemy.util.warn(f"Skipping table {name}: {uerr}")


class SQLDatabase:
    def __init__(
        self,
        engine: Engine,
        schema: Optional[str] = None,
        metadata: Optional[MetaData] = None,
        ignore_tables: Optional[List[str]] = None,
        include_tables: Optional[List[str]] = None,
        sample_rows_in_table_info: int = 3,
        indexes_in_table_info: bool = False,
        custom_table_info: Optional[dict] = None,
        view_support: bool = False,
        max_string_length: int = 300,
    ):
        """Create engine from database URI."""
        self._engine = engine
        self._schema = schema
        if include_tables and ignore_tables:
            raise ValueError("Cannot specify both include_tables and ignore_tables")

        self._inspector = inspect(self._engine)

        # including view support by adding the views as well as tables to the all
        # tables list if view_support is True
        self._all_tables = set(
            self._inspector.get_table_names(schema=schema)
            + (self._inspector.get_view_names(schema=schema) if view_support else [])
        )

        self._include_tables = set(include_tables) if include_tables else set()
        if self._include_tables:
            missing_tables = self._include_tables - self._all_tables
            if missing_tables:
                raise ValueError(
                    f"include_tables {missing_tables} not found in database"
                )
        self._ignore_tables = set(ignore_tables) if ignore_tables else set()
        if self._ignore_tables:
            missing_tables = self._ignore_tables - self._all_tables
            if missing_tables:
                raise ValueError(
                    f"ignore_tables {missing_tables} not found in database"
                )
        usable_tables = self.get_usable_table_names()
        self._usable_tables = set(usable_tables) if usable_tables else self._all_tables

        if not isinstance(sample_rows_in_table_info, int):
            raise TypeError("sample_rows_in_table_info must be an integer")

        self._sample_rows_in_table_info = sample_rows_in_table_info
        self._indexes_in_table_info = indexes_in_table_info

        self._custom_table_info = custom_table_info
        if self._custom_table_info:
            if not isinstance(self._custom_table_info, dict):
                raise TypeError(
                    "table_info must be a dictionary with table names as keys and the "
                    "desired table info as values"
                )
            # only keep the tables that are also present in the database
            intersection = set(self._custom_table_info).intersection(self._all_tables)
            self._custom_table_info = {
                table: info
                for table, info in self._custom_table_info.items()
                if table in intersection
            }

        self._max_string_length = max_string_length

        self._metadata = metadata or MetaData()
        # Money patch reflect function
        reflect(
            self._metadata,
            views=view_support,
            bind=self._engine,
            only=list(self._usable_tables),
            schema=self._schema,
        )

    @property
    def engine(self) -> Engine:
        """Return SQL Alchemy engine."""
        return self._engine

    @property
    def metadata_obj(self) -> MetaData:
        """Return SQL Alchemy metadata."""
        return self._metadata

    @classmethod
    def from_uri(
        cls, database_uri: str, engine_args: Optional[dict] = None, **kwargs: Any
    ) -> "SQLDatabase":
        """Construct a SQLAlchemy engine from URI."""
        _engine_args = engine_args or {}
        return cls(create_engine(database_uri, **_engine_args), **kwargs)

    @property
    def dialect(self) -> str:
        """Return string representation of dialect to use."""
        return self._engine.dialect.name

    def get_usable_table_names(self) -> Iterable[str]:
        """Get names of tables available."""
        if self._include_tables:
            return sorted(self._include_tables)
        return sorted(self._all_tables - self._ignore_tables)

    def get_table_columns(self, table_name: str) -> List[Any]:
        """Get table columns."""
        return self._inspector.get_columns(table_name)

    def get_single_table_info(self, table_name: str) -> str:
        """Get table info for a single table."""
        # same logic as table_info, but with specific table names
        template = "Table '{table_name}' has columns: {columns}, "
        try:
            # try to retrieve table comment
            table_comment = self._inspector.get_table_comment(
                table_name, schema=self._schema
            )["text"]
            if table_comment:
                template += f"with comment: ({table_comment}) "
        except NotImplementedError:
            # get_table_comment raises NotImplementedError for a dialect that does not support comments.
            pass

        template += "{foreign_keys}."
        columns = []
        for column in self._inspector.get_columns(table_name, schema=self._schema):
            if column.get("comment"):
                columns.append(
                    f"{column['name']} ({column['type']!s}): "
                    f"'{column.get('comment')}'"
                )
            else:
                columns.append(f"{column['name']} ({column['type']!s})")

        column_str = ", ".join(columns)
        foreign_keys = []
        for foreign_key in self._inspector.get_foreign_keys(
            table_name, schema=self._schema
        ):
            foreign_keys.append(
                f"{foreign_key['constrained_columns']} -> "
                f"{foreign_key['referred_table']}.{foreign_key['referred_columns']}"
            )
        foreign_key_str = (
            foreign_keys
            and " and foreign keys: {}".format(", ".join(foreign_keys))
            or ""
        )
        return template.format(
            table_name=table_name, columns=column_str, foreign_keys=foreign_key_str
        )

    def insert_into_table(self, table_name: str, data: dict) -> None:
        """Insert data into a table."""
        table = self._metadata.tables[table_name]
        stmt = insert(table).values(**data)
        with self._engine.begin() as connection:
            connection.execute(stmt)

    def truncate_word(self, content: Any, *, length: int, suffix: str = "...") -> str:
        """
        Truncate a string to a certain number of words, based on the max string
        length.
        """
        if not isinstance(content, str) or length <= 0:
            return content

        if len(content) <= length:
            return content

        return content[: length - len(suffix)].rsplit(" ", 1)[0] + suffix

    def run_sql(self, command: str) -> Tuple[str, Dict]:
        """Execute a SQL statement and return a string representing the results.

        If the statement returns rows, a string of the results is returned.
        If the statement returns no rows, an empty string is returned.
        """
        with self._engine.begin() as connection:
            try:
                if self._schema:
                    command = command.replace("FROM ", f"FROM {self._schema}.")
                    command = command.replace("JOIN ", f"JOIN {self._schema}.")
                cursor = connection.execute(text(command))
            except (ProgrammingError, OperationalError) as exc:
                raise NotImplementedError(
                    f"Statement {command!r} is invalid SQL.\nError: {exc.orig}"
                ) from exc
            if cursor.returns_rows:
                result = cursor.fetchall()
                # truncate the results to the max string length
                # we can't use str(result) directly because it automatically truncates long strings
                truncated_results = []
                for row in result:
                    # truncate each column, then convert the row to a tuple
                    truncated_row = tuple(
                        self.truncate_word(column, length=self._max_string_length)
                        for column in row
                    )
                    truncated_results.append(truncated_row)
                return str(truncated_results), {
                    "result": truncated_results,
                    "col_keys": list(cursor.keys()),
                }
        return "", {}


def is_email(string):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    match = re.match(pattern, string)
    if match:
        return True
    else:
        return False


def examples_to_str(examples: list) -> list[str]:
    """
    from examples to a list of str
    """
    values = examples
    for i in range(len(values)):
        if isinstance(values[i], datetime.date):
            values = [values[i]]
            break
        elif isinstance(values[i], datetime.datetime):
            values = [values[i]]
            break
        elif isinstance(values[i], decimal.Decimal):
            values[i] = str(float(values[i]))
        elif is_email(str(values[i])):
            values = []
            break
        elif "http://" in str(values[i]) or "https://" in str(values[i]):
            values = []
            break
        elif values[i] is not None and not isinstance(values[i], str):
            pass
        elif values[i] is not None and ".com" in values[i]:
            pass

    return [str(v) for v in values if v is not None and len(str(v)) > 0]


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


class MSchema:
    def __init__(self, db_id: str = "Anonymous", schema: Optional[str] = None):
        self.db_id = db_id
        self.schema = schema
        self.tables = {}
        self.foreign_keys = []

    def add_table(self, name, fields={}, comment=None):
        self.tables[name] = {
            "fields": fields.copy(),
            "examples": [],
            "comment": comment,
        }

    def add_field(
        self,
        table_name: str,
        field_name: str,
        field_type: str = "",
        primary_key: bool = False,
        nullable: bool = True,
        default: Any = None,
        autoincrement: bool = False,
        comment: str = "",
        examples: list = [],
        **kwargs,
    ):
        self.tables[table_name]["fields"][field_name] = {
            "type": field_type,
            "primary_key": primary_key,
            "nullable": nullable,
            "default": default if default is None else f"{default}",
            "autoincrement": autoincrement,
            "comment": comment,
            "examples": examples.copy(),
            **kwargs,
        }

    def add_foreign_key(
        self, table_name, field_name, ref_schema, ref_table_name, ref_field_name
    ):
        self.foreign_keys.append(
            [table_name, field_name, ref_schema, ref_table_name, ref_field_name]
        )

    def get_field_type(self, field_type, simple_mode=True) -> str:
        if not simple_mode:
            return field_type
        else:
            return field_type.split("(")[0]

    def has_table(self, table_name: str) -> bool:
        if table_name in self.tables.keys():
            return True
        else:
            return False

    def has_column(self, table_name: str, field_name: str) -> bool:
        if self.has_table(table_name):
            if field_name in self.tables[table_name]["fields"].keys():
                return True
            else:
                return False
        else:
            return False

    def get_field_info(self, table_name: str, field_name: str) -> Dict:
        try:
            return self.tables[table_name]["fields"][field_name]
        except:
            return {}

    def single_table_mschema(
        self,
        table_name: str,
        selected_columns: List = None,
        example_num=3,
        show_type_detail=False,
    ) -> str:
        table_info = self.tables.get(table_name, {})
        output = []
        table_comment = table_info.get("comment", "")
        if (
            table_comment is not None
            and table_comment != "None"
            and len(table_comment) > 0
        ):
            if self.schema is not None and len(self.schema) > 0:
                output.append(f"# Table: {self.schema}.{table_name}, {table_comment}")
            else:
                output.append(f"# Table: {table_name}, {table_comment}")
        else:
            if self.schema is not None and len(self.schema) > 0:
                output.append(f"# Table: {self.schema}.{table_name}")
            else:
                output.append(f"# Table: {table_name}")

        field_lines = []
        # 处理表中的每一个字段
        for field_name, field_info in table_info["fields"].items():
            if (
                selected_columns is not None
                and field_name.lower() not in selected_columns
            ):
                continue

            raw_type = self.get_field_type(field_info["type"], not show_type_detail)
            field_line = f"({field_name}:{raw_type.upper()}"
            if field_info["comment"] != "":
                field_line += f", {field_info['comment'].strip()}"
            else:
                pass

            ## 打上主键标识
            is_primary_key = field_info.get("primary_key", False)
            if is_primary_key:
                field_line += f", Primary Key"

            # 如果有示例，添加上
            if len(field_info.get("examples", [])) > 0 and example_num > 0:
                examples = field_info["examples"]
                examples = [s for s in examples if s is not None]
                examples = examples_to_str(examples)
                if len(examples) > example_num:
                    examples = examples[:example_num]

                if raw_type in ["DATE", "TIME", "DATETIME", "TIMESTAMP"]:
                    examples = [examples[0]]
                elif len(examples) > 0 and max([len(s) for s in examples]) > 20:
                    if max([len(s) for s in examples]) > 50:
                        examples = []
                    else:
                        examples = [examples[0]]
                else:
                    pass
                if len(examples) > 0:
                    example_str = ", ".join([str(example) for example in examples])
                    field_line += f", Examples: [{example_str}]"
                else:
                    pass
            else:
                field_line += ""
            field_line += ")"

            field_lines.append(field_line)
        output.append("[")
        output.append(",\n".join(field_lines))
        output.append("]")

        return "\n".join(output)

    def to_mschema(
        self,
        selected_tables: List = None,
        selected_columns: List = None,
        example_num=3,
        show_type_detail=False,
    ) -> str:
        """
        convert to a MSchema string.
        selected_tables: 默认为None，表示选择所有的表
        selected_columns: 默认为None，表示所有列全选，格式['table_name.column_name']
        """
        output = []

        output.append(f"【DB_ID】 {self.db_id}")
        output.append(f"【Schema】")

        if selected_tables is not None:
            selected_tables = [s.lower() for s in selected_tables]
        if selected_columns is not None:
            selected_columns = [s.lower() for s in selected_columns]
            selected_tables = [s.split(".")[0].lower() for s in selected_columns]

        # 依次处理每一个表
        for table_name, table_info in self.tables.items():
            if selected_tables is None or table_name.lower() in selected_tables:
                cur_table_type = table_info.get("type", "table")
                column_names = list(table_info["fields"].keys())
                if selected_columns is not None:
                    cur_selected_columns = [
                        c.lower()
                        for c in column_names
                        if f"{table_name}.{c}".lower() in selected_columns
                    ]
                else:
                    cur_selected_columns = selected_columns
                output.append(
                    self.single_table_mschema(
                        table_name, cur_selected_columns, example_num, show_type_detail
                    )
                )

        # 添加外键信息，选择table_type为view时不展示外键
        if self.foreign_keys:
            output.append("【Foreign keys】")
            for fk in self.foreign_keys:
                ref_schema = fk[2]
                table1, column1, _, table2, column2 = fk
                if selected_tables is None or (
                    table1.lower() in selected_tables
                    and table2.lower() in selected_tables
                ):
                    if ref_schema == self.schema:
                        output.append(f"{fk[0]}.{fk[1]}={fk[3]}.{fk[4]}")

        return "\n".join(output)

    def dump(self):
        schema_dict = {
            "db_id": self.db_id,
            "schema": self.schema,
            "tables": self.tables,
            "foreign_keys": self.foreign_keys,
        }
        return schema_dict

    def save(self, file_path: str):
        schema_dict = self.dump()
        write_json(file_path, schema_dict)

    def load(self, file_path: str):
        data = read_json(file_path)
        self.db_id = data.get("db_id", "Anonymous")
        self.schema = data.get("schema", None)
        self.tables = data.get("tables", {})
        self.foreign_keys = data.get("foreign_keys", [])


class SchemaEngine(SQLDatabase):
    def __init__(
        self,
        engine: Engine,
        schema: Optional[str] = None,
        metadata: Optional[MetaData] = None,
        ignore_tables: Optional[List[str]] = None,
        include_tables: Optional[List[str]] = None,
        sample_rows_in_table_info: int = 3,
        indexes_in_table_info: bool = False,
        custom_table_info: Optional[dict] = None,
        view_support: bool = False,
        max_string_length: int = 300,
        mschema: Optional[MSchema] = None,
        db_name: Optional[str] = "",
    ):
        super().__init__(
            engine,
            schema,
            metadata,
            ignore_tables,
            include_tables,
            sample_rows_in_table_info,
            indexes_in_table_info,
            custom_table_info,
            view_support,
            max_string_length,
        )

        self._db_name = db_name
        self._usable_tables = [
            table_name
            for table_name in self._usable_tables
            if self._inspector.has_table(table_name, schema)
        ]
        self._dialect = engine.dialect.name
        if mschema is not None:
            self._mschema = mschema
        else:
            self._mschema = MSchema(db_id=db_name, schema=schema)
            self.init_mschema()

    @property
    def mschema(self) -> MSchema:
        """Return M-Schema"""
        return self._mschema

    def get_pk_constraint(self, table_name: str) -> Dict:
        return self._inspector.get_pk_constraint(table_name, self._schema)[
            "constrained_columns"
        ]

    def get_table_comment(self, table_name: str):
        try:
            return self._inspector.get_table_comment(table_name, self._schema)["text"]
        except:  # sqlite不支持添加注释
            return ""

    def default_schema_name(self) -> Optional[str]:
        return self._inspector.default_schema_name

    def get_schema_names(self) -> List[str]:
        return self._inspector.get_schema_names()

    def get_foreign_keys(self, table_name: str):
        return self._inspector.get_foreign_keys(table_name, self._schema)

    def get_unique_constraints(self, table_name: str):
        return self._inspector.get_unique_constraints(table_name, self._schema)

    def fectch_distinct_values(
        self, table_name: str, column_name: str, max_num: int = 5
    ):
        table = Table(table_name, self.metadata_obj, autoload_with=self._engine)
        # 构建 SELECT DISTINCT 查询
        query = select(table.c[column_name]).distinct().limit(max_num)
        values = []
        with self._engine.connect() as connection:
            result = connection.execute(query)
            distinct_values = result.fetchall()
            for value in distinct_values:
                if value[0] is not None and value[0] != "":
                    values.append(value[0])
        return values

    def init_mschema(self):
        for table_name in self._usable_tables:
            table_comment = self.get_table_comment(table_name)
            table_comment = "" if table_comment is None else table_comment.strip()
            self._mschema.add_table(table_name, fields={}, comment=table_comment)
            pks = self.get_pk_constraint(table_name)

            fks = self.get_foreign_keys(table_name)
            for fk in fks:
                referred_schema = fk["referred_schema"]
                for c, r in zip(fk["constrained_columns"], fk["referred_columns"]):
                    self._mschema.add_foreign_key(
                        table_name, c, referred_schema, fk["referred_table"], r
                    )

            fields = self._inspector.get_columns(table_name, schema=self._schema)
            for field in fields:
                field_type = f"{field['type']!s}"
                field_name = field["name"]
                if field_name in pks:
                    primary_key = True
                else:
                    primary_key = False

                field_comment = field.get("comment", None)
                field_comment = "" if field_comment is None else field_comment.strip()
                autoincrement = field.get("autoincrement", False)
                default = field.get("default", None)
                if default is not None:
                    default = f"{default}"

                try:
                    examples = self.fectch_distinct_values(table_name, field_name, 5)
                except:
                    examples = []
                examples = examples_to_str(examples)

                self._mschema.add_field(
                    table_name,
                    field_name,
                    field_type=field_type,
                    primary_key=primary_key,
                    nullable=field["nullable"],
                    default=default,
                    autoincrement=autoincrement,
                    comment=field_comment,
                    examples=examples,
                )

# db_path = "data/test_databases/formula_1/formula_1.sqlite"
# db_engine = create_engine(f"sqlite:///{db_path}")
# print(SchemaEngine(engine=db_engine, db_name="new_schema").mschema.to_mschema())

# db_path = "data/sqlite_repro/test.db"
# db_engine = create_engine(f"sqlite:///{db_path}")
# print(SchemaEngine(engine=db_engine, db_name="new_schema").mschema.to_mschema())
