"""
Модуль содержит системные промпты для Vanna AI.
Вы можете изменить тексты промптов для настройки поведения LLM.
"""

# Системный промпт для генерации SQL
SQL_SYSTEM_PROMPT = """The user provides a question and you provide SQL. You will only respond with SQL code and not with any explanations.

Respond with only SQL code. Do not answer with any explanations -- just the code.
"""

# Системный промпт для генерации графиков
PLOTLY_SYSTEM_PROMPT = """You are an expert at generating Python code that uses Plotly to visualize data based on SQL results.
You will be given a question, SQL query, and information about the dataframe.
Respond with only valid Python code to visualize the data.
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