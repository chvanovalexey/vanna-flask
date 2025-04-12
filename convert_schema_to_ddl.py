import json
import os

def convert_schema_to_ddl():
    try:
        # Загрузка JSON схемы
        with open('metadata/schema.json', 'r', encoding='utf-8') as f:
            schema = json.load(f)
            
        tables = schema.get('tables', [])
        relationships = schema.get('relationships', [])
        
        # Создаем директорию для результатов, если она не существует
        os.makedirs('converted_training_data', exist_ok=True)
        
        # Файл для вывода DDL
        with open('converted_training_data/schema_ddl.sql', 'w', encoding='utf-8') as ddl_file:
            # Добавляем комментарий для каждой секции
            ddl_file.write("-- DDL для базы данных розничной торговли\n\n")
            
            # Конвертируем каждую таблицу
            for table in tables:
                table_name = table['name']
                description = table.get('description', '')
                columns = table.get('columns', [])
                
                # Начало CREATE TABLE
                ddl_file.write(f"-- {description}\n")
                ddl_file.write(f"CREATE TABLE {table_name} (\n")
                
                # Добавляем колонки
                column_defs = []
                for column in columns:
                    col_name = column['name']
                    col_type = column['type']
                    col_description = column.get('description', '')
                    
                    # Составляем определение колонки
                    column_def = f"    {col_name} {col_type}"
                    
                    # Добавляем комментарий
                    column_def += f" -- {col_description}"
                    column_defs.append(column_def)
                
                # Объединяем все колонки через запятую
                ddl_file.write(",\n".join(column_defs))
                ddl_file.write("\n);\n\n")
            
            # Добавляем внешние ключи на основе отношений
            if relationships:
                ddl_file.write("-- Определения внешних ключей\n\n")
                for rel in relationships:
                    from_table = rel['from']['table']
                    from_column = rel['from']['column']
                    to_table = rel['to']['table']
                    to_column = rel['to']['column']
                    rel_type = rel['type']
                    
                    ddl_file.write(f"-- Отношение типа {rel_type}\n")
                    ddl_file.write(f"ALTER TABLE {from_table} ADD CONSTRAINT fk_{from_table}_{from_column}_{to_table} \n")
                    ddl_file.write(f"    FOREIGN KEY ({from_column}) REFERENCES {to_table}({to_column});\n\n")
            
        print(f"Преобразование схемы в DDL завершено. Результат сохранен в converted_training_data/schema_ddl.sql")
    
    except Exception as e:
        print(f"Ошибка при конвертации schema.json: {e}")

if __name__ == "__main__":
    convert_schema_to_ddl() 