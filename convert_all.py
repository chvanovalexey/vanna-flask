from convert_schema_to_ddl import convert_schema_to_ddl
from convert_dictionary_to_docs import convert_dictionary_to_docs
from convert_query_examples_to_sql import convert_query_examples_to_sql
import os

def main():
    print("Начинаем преобразование файлов данных для обучения Vanna...")
    
    # Проверяем наличие всех необходимых файлов
    required_files = [
        'metadata/schema.json',
        'metadata/dictionary.json',
        'metadata/query_examples.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"Ошибка: Не найдены следующие файлы: {', '.join(missing_files)}")
        return
    
    # Создаем директорию для результатов, если она не существует
    os.makedirs('converted_training_data', exist_ok=True)
    
    # Выполняем преобразования
    print("\n1. Преобразование schema.json в DDL...")
    convert_schema_to_ddl()
    
    print("\n2. Преобразование dictionary.json в документацию...")
    convert_dictionary_to_docs()
    
    print("\n3. Преобразование query_examples.json в SQL...")
    convert_query_examples_to_sql()
    
    print("\nВсе преобразования успешно завершены!")
    print("\nРезультаты сохранены в папке 'converted_training_data':")
    print("- DDL (схема базы данных): schema_ddl.sql")
    print("- Документация (бизнес-термины): business_terms_docs.txt и папка business_terms/")
    print("- SQL (примеры запросов): all_sql_examples.sql и папка examples/")
    
    print("\nТеперь вы можете загрузить эти файлы в Vanna для обучения:")
    print("1. DDL: загрузите schema_ddl.sql")
    print("2. Documentation: загрузите файлы business_terms_docs.txt или отдельные файлы из папки business_terms/")
    print("3. SQL: загрузите all_sql_examples.sql или отдельные файлы из папки examples/")

if __name__ == "__main__":
    main() 