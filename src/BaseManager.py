class BaseManager:
    connection = None
 
    @classmethod
    def set_connection(cls, database_settings):
        connection = sql.connect(**database_settings)
        connection.autocommit = True
        cls.connection = connection
 
    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()
 
    @classmethod
    def _execute_query(cls, query, params=None):
        cursor = cls._get_cursor()
        cursor.execute(query, params)
 
    def __init__(self, model_class):
        self.model_class = model_class
 
    def select(self, *field_names, limit=10):
        # Build SELECT query
        fields_format = ', '.join(field_names)
        query = f"SELECT {fields_format} FROM {self.model_class.table_name}"
 
        # Execute query
        cursor = self._get_cursor()
        cursor.execute(query)
 
        # Retrieve Data
        model_objects = list()
        result = cursor.fetchall()
        for row_values in result[:limit]:
            keys, values = field_names, row_values
            row_data = dict(zip(keys, values))
            model_objects.append(self.model_class(**row_data))

        return model_objects
 
    def insert(self, rows: list):
        field_names = rows[0].keys()

        fields_format = ", ".join(field_names)
        values_placeholder_format = ", ".join([f'({", ".join(["%s"] * len(field_names))})'] * len(rows))

        query = f"INSERT INTO {self.model_class.table_name} ({fields_format}) " \
                f"VALUES {values_placeholder_format}"

        params = list()
        for row in rows:
            row_values = [row[field_name] for field_name in field_names]
            params += row_values

        self._execute_query(query, params)
 
    def update(self, new_data: dict):
        field_names = new_data.keys()
        placeholder_format = ', '.join([f'{field_name} = %s' for field_name in field_names])
        query = f"UPDATE {self.model_class.table_name} SET {placeholder_format}"
        params = list(new_data.values())
        self._execute_query(query, params)
 
    def delete(self):
        query = f"DELETE FROM {self.model_class.table_name}"
        self._execute_query(query)