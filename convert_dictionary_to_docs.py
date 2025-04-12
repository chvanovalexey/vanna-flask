import json
import os

def convert_dictionary_to_docs():
    try:
        # Загрузка JSON словаря бизнес-терминов
        with open('metadata/dictionary.json', 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
            
        business_terms = dictionary.get('business_terms', [])
        
        # Создаем директорию для результатов, если она не существует
        os.makedirs('converted_training_data', exist_ok=True)
        
        # Файл для вывода документации
        with open('converted_training_data/business_terms_docs.txt', 'w', encoding='utf-8') as docs_file:
            docs_file.write("# Словарь бизнес-терминов для системы аналитики розничной торговли\n\n")
            
            # Обрабатываем каждый бизнес-термин
            for term in business_terms:
                term_name = term.get('term', '')
                definition = term.get('definition', '')
                sql_repr = term.get('sql_representation', '')
                related_columns = term.get('related_columns', [])
                
                # Формируем запись о термине в человекочитаемом формате
                docs_file.write(f"## Бизнес-термин: {term_name}\n")
                docs_file.write(f"Определение: {definition}\n")
                docs_file.write(f"SQL-представление: {sql_repr}\n")
                
                if related_columns:
                    docs_file.write(f"Связанные колонки: {', '.join(related_columns)}\n")
                
                docs_file.write("\n")
                
        # Создаем отдельные файлы для каждого термина (для лучшей модульности обучения)
        os.makedirs('converted_training_data/business_terms', exist_ok=True)
        
        for idx, term in enumerate(business_terms):
            term_name = term.get('term', '')
            definition = term.get('definition', '')
            sql_repr = term.get('sql_representation', '')
            related_columns = term.get('related_columns', [])
            
            # Формируем имя файла из термина
            file_name = f"converted_training_data/business_terms/term_{idx+1}_{term_name}.txt"
            
            with open(file_name, 'w', encoding='utf-8') as term_file:
                term_file.write(f"# Бизнес-термин: {term_name}\n\n")
                term_file.write(f"Определение: {definition}\n\n")
                term_file.write(f"SQL-представление: ```{sql_repr}```\n\n")
                
                if related_columns:
                    term_file.write(f"Связанные колонки: {', '.join(related_columns)}\n")
            
        print(f"Преобразование словаря в документацию завершено. Результаты сохранены в converted_training_data/business_terms_docs.txt и в папке converted_training_data/business_terms/")
    
    except Exception as e:
        print(f"Ошибка при конвертации dictionary.json: {e}")

if __name__ == "__main__":
    convert_dictionary_to_docs() 