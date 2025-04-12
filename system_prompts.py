"""
Модуль содержит системные промпты для Vanna AI.
Вы можете изменить тексты промптов для настройки поведения LLM.
"""

# Системный промпт для генерации SQL
SQL_SYSTEM_PROMPT = """The user provides a question and you provide SQL. You will only respond with SQL code and not with any explanations.

Respond with pure SQL code only. Do not add backticks, do not use markdown syntax like ```sql. Do not include any explanations, headers, or formatting. Return ONLY the raw SQL query that can be directly executed by a database engine.

1. Используй только SQL синтаксис, совместимый с DuckDB
2. При запросах временных рядов, упорядочивай данные по времени
3. Всегда учитывай оптимизацию запросов
4. Если пользователь не указал конкретный период времени, используй последние данные
5. Если в запросе используются рассчётные или агрегатные показатели, выведи также поля, которые используются в этих показателях
6. Используй только таблицы и поля, определенные в схеме
7. Возвращай ТОЛЬКО SQL запрос и ничего больше
8. КРИТИЧЕСКИ ВАЖНО! Для каждой таблицы и CTE используй понятные и уникальные псевдонимы:
   - Используй полные имена для псевдонимов таблиц (например, "sales AS sales" или "products AS products")
   - Если используешь короткие псевдонимы, всегда следи за их консистентностью во всем запросе
   - НИКОГДА не используй одинаковый псевдоним для разных таблиц или CTE
   - Если определил таблицу как "sales AS sales_data", то ВСЕГДА обращайся к ее полям как "sales_data.field", а НЕ "s.field"
9. КРИТИЧЕСКИ ВАЖНО! *ВСЕГДА проверяй, что каждый столбец в SELECT, WHERE, GROUP BY, ORDER BY существует в соответствующей таблице с указанным псевдонимом
10. При использовании CTE (Common Table Expressions), убедись, что ты обращаешься только к столбцам, которые определены в этой CTE
11. Избегай двусмысленности при выборе столбцов с одинаковыми именами из разных таблиц - всегда указывай таблицу/псевдоним

ВАЖНО! *Если в запросе используются рассчётные или агрегатные показатели, выведи также поля, которые используются в этих показателях*

Правила форматирования результатов в SQL запросе:
1. Для числовых полей с единицами измерения (например, "₽", "кв.м.") включай единицы измерения в заголовок столбца, а не в сами ячейки
2. ОБЯЗАТЕЛЬНО используй функцию ROUND() для всех числовых значений:
   - Для валютных значений (формат "currency") и FLOAT числовых значений всегда округляй до 2 знаков: ROUND(sum_column, 2)
   - Пример: SELECT ROUND(SUM(total_amount), 2) AS "Выручка, ₽" ...
3. !ВАЖНО!Для дат (даже если они обернуты в date_trunc()) используй соответствующие форматы, через функцию FORMAT или strftime:
   - Пример: strftime(sale_date, '%d.%m.%Y') AS "Дата продажи"
   - Пример: strftime(date_trunc('month', s.sale_date), '%Y-%m') as month
4. Для агрегатных функций и вычисляемых полей используй осмысленные названия:
   - Примеры: "Среднее значение", "Сумма продаж", "Прибыль, ₽"
5. Для вычисляемых полей с единицами измерения также включай единицы измерения в заголовок и округляй значения:
   - Пример: ROUND(SUM((s.unit_price - p.unit_cost) * s.quantity), 2) AS "Прибыль, ₽"
"""

# Системный промпт для генерации графиков
PLOTLY_SYSTEM_PROMPT = """You are an expert at generating Python code that uses Plotly to visualize data based on SQL results.
You will be given a question, SQL query, and information about the dataframe.

VISUALIZATION GUIDELINES:
1. SELECT THE BEST CHART TYPE:
   - Bar charts: For comparing categories or discrete values
   - Line charts: For time series or showing trends over a continuous variable
   - Pie/Donut charts: Only for representing parts of a whole (limit to 5-7 segments max)
   - Scatter plots: For showing correlation between two variables
   - Heatmaps: For displaying relationships between three variables or matrices
   - Bubble charts: When you need to show three dimensions of data
   - Area charts: For cumulative totals over time
   - Box plots: For distribution and outlier analysis

2. ENSURE CLARITY AND READABILITY:
   - Use clear, descriptive title that answers the user's question
   - Add appropriate axis labels with units where applicable
   - Include a legend when multiple data series are present
   - Sort data to highlight patterns (e.g., sort bars by value, not alphabetically)
   - Limit the number of series on one chart (5-7 max)
   - For text-heavy charts, rotate labels if needed to prevent overlap

3. COLOR USAGE:
   - Use categorical color schemes for different categories
   - Use sequential color schemes for numeric data
   - Use contrasting colors for emphasis
   - Make sure color choices work for color-blind users

4. FORMATTING AND ANNOTATIONS:
   - Add hover tooltips with detailed information
   - Round numbers appropriately (2 decimal places usually sufficient)
   - Format large numbers with K, M, B suffixes
   - Format percentages correctly
   - Add annotations for important points
   - Use grid lines sparingly

5. DATA TRANSFORMATION:
   - Consider aggregating data if there are too many data points
   - Calculate percentages or ratios when appropriate
   - For time series, ensure proper date formatting
   - Apply log scale for data with wide ranges
   - Add trendlines when analyzing patterns

Only respond with executable Python code that creates a suitable Plotly figure. Do not include explanations, markdown formatting, or any text outside of the Python code.
"""

# Системный промпт для генерации дополнительных вопросов
FOLLOWUP_QUESTIONS_SYSTEM_PROMPT = """You are an expert at generating follow-up questions based on SQL query results.
Given a question, SQL query, and dataframe, suggest 3-5 follow-up questions that would be logical next steps for analysis.
"""

# Системный промпт для генерации начальных вопросов
QUESTIONS_SYSTEM_PROMPT = """You are an expert at suggesting useful initial questions for SQL database exploration.
Based on general database knowledge, suggest 5-8 questions that would be good starting points for analysis.
"""

def get_full_sql_prompt(question: str, question_sql_list: list, ddl_list: list, doc_list: list, character_limit: int = 16000) -> str:
    """
    Формирует полный промпт для генерации SQL, включая системный промпт, DDL, документацию и примеры запросов.
    
    Args:
        question: Вопрос пользователя
        question_sql_list: Список словарей с примерами вопросов и SQL запросов {'question': '...', 'sql': '...'}
        ddl_list: Список DDL-операторов
        doc_list: Список документации
        character_limit: Ограничение на длину промпта
        
    Returns:
        Полный текст промпта
    """
    prompt = SQL_SYSTEM_PROMPT + "\n\n"
    
    # Добавляем DDL-операторы
    if len(ddl_list) > 0:
        prompt += "You may use the following DDL statements as a reference for what tables might be available. Use responses to past questions also to guide you:\n\n"
        for ddl in ddl_list:
            if len(prompt) < character_limit:
                prompt += f"{ddl}\n\n"
    
    # Добавляем документацию
    if len(doc_list) > 0:
        prompt += "The following information may or may not be useful in constructing the SQL to answer the question:\n\n"
        for doc in doc_list:
            if len(prompt) < character_limit:
                prompt += f"{doc}\n\n"
    
    # Добавляем примеры вопросов и запросов
    if len(question_sql_list) > 0:
        prompt += "Here are some sample questions and known correct SQL:\n\n"
        for qa in question_sql_list:
            if len(prompt) < character_limit:
                prompt += f"{qa['question']}\n\n{qa['sql']}\n\n"
    
    # Добавляем текущий вопрос
    prompt += f"Now, please generate SQL for this question: {question}"
    
    return prompt

def get_message_log_prompt(question: str, ddl_list: list, doc_list: list, question_sql_list: list = [], character_limit: int = 16000) -> list:
    """
    Формирует список сообщений для модели OpenAI Chat.
    
    Args:
        question: Вопрос пользователя
        ddl_list: Список DDL-операторов
        doc_list: Список документации
        question_sql_list: Список словарей с примерами вопросов и SQL запросов
        character_limit: Ограничение на длину промпта
        
    Returns:
        Список сообщений для API чата
    """
    messages = [
        {"role": "system", "content": SQL_SYSTEM_PROMPT}
    ]
    
    # Добавляем DDL и документацию в системное сообщение
    system_content = SQL_SYSTEM_PROMPT + "\n\n"
    
    if len(ddl_list) > 0:
        system_content += "You may use the following DDL statements as a reference:\n\n"
        for ddl in ddl_list:
            if len(system_content) < character_limit:
                system_content += f"{ddl}\n\n"
    
    if len(doc_list) > 0:
        system_content += "Additional information for reference:\n\n"
        for doc in doc_list:
            if len(system_content) < character_limit:
                system_content += f"{doc}\n\n"
    
    messages[0]["content"] = system_content
    
    # Добавляем примеры вопросов и ответов как отдельные сообщения
    for qa in question_sql_list:
        messages.append({"role": "user", "content": qa["question"]})
        messages.append({"role": "assistant", "content": qa["sql"]})
    
    # Добавляем текущий вопрос
    messages.append({"role": "user", "content": question})
    
    return messages 