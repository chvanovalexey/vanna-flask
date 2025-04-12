import json
import os

def convert_query_examples_to_sql():
    try:
        # Загрузка JSON с примерами запросов
        with open('metadata/query_examples.json', 'r', encoding='utf-8') as f:
            query_examples = json.load(f)
            
        examples = query_examples.get('examples', [])
        
        # Создаем директорию для результатов, если она не существует
        os.makedirs('converted_training_data', exist_ok=True)
        os.makedirs('converted_training_data/examples', exist_ok=True)
        
        # Файл для объединенного вывода всех SQL запросов
        with open('converted_training_data/all_sql_examples.sql', 'w', encoding='utf-8') as sql_file:
            sql_file.write("-- Примеры SQL-запросов для розничной аналитики\n\n")
            
            # Обрабатываем каждый пример запроса
            for idx, example in enumerate(examples):
                question = example.get('question', '')
                sql = example.get('sql', '')
                
                # Добавляем пример в общий файл с комментарием
                sql_file.write(f"-- Запрос {idx+1}: {question}\n")
                sql_file.write(f"{sql};\n\n")
        
        # Создаем отдельные файлы для каждого примера (для лучшей модульности обучения)
        for idx, example in enumerate(examples):
            question = example.get('question', '')
            sql = example.get('sql', '')
            
            # Формируем имя файла из номера примера и короткого описания запроса
            short_name = question[:20].replace(' ', '_').replace('?', '').lower()
            file_name = f"converted_training_data/examples/example_{idx+1}_{short_name}.sql"
            
            with open(file_name, 'w', encoding='utf-8') as example_file:
                example_file.write(f"-- Запрос: {question}\n\n")
                example_file.write(f"{sql};\n")
            
            # Также создаем файл с вопросом и ответом для улучшения контекста обучения
            qa_file_name = f"converted_training_data/examples/qa_{idx+1}_{short_name}.txt"
            
            with open(qa_file_name, 'w', encoding='utf-8') as qa_file:
                qa_file.write(f"# Вопрос: {question}\n\n")
                qa_file.write(f"SQL-запрос для решения:\n")
                qa_file.write(f"```sql\n{sql}\n```\n")
            
        print(f"Преобразование примеров запросов в SQL завершено. Результаты сохранены в converted_training_data/all_sql_examples.sql и в папке converted_training_data/examples/")
    
    except Exception as e:
        print(f"Ошибка при конвертации query_examples.json: {e}")

if __name__ == "__main__":
    convert_query_examples_to_sql() 