from dotenv import load_dotenv
load_dotenv()

from functools import wraps
from flask import Flask, jsonify, Response, request, redirect, url_for
import flask
import os
import duckdb
import time
from cache import MemoryCache
import system_prompts  # Импортируем наш модуль с промптами

app = Flask(__name__, static_url_path='')

# SETUP
cache = MemoryCache()
# Global variable to store current LLM provider
current_llm_provider = 'openai'
current_llm_model = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')

# Setup Vanna with different LLM providers
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore

# Импортируем дополнительные LLM провайдеры
try:
    from vanna.anthropic import Anthropic_Chat
except ImportError:
    Anthropic_Chat = None
    print("Anthropic provider not available")

try:
    from vanna.mistral import Mistral_Chat
except ImportError:
    Mistral_Chat = None
    print("Mistral provider not available")

# Словарь доступных моделей с их настройками
AVAILABLE_MODELS = {
    'openai': {
        'gpt-4o-mini': 'GPT-4o mini',
        'gpt-4o': 'GPT-4o',
        'o1-preview': 'o1-preview',
        'o3-mini': 'o3-mini'
    },
    'anthropic': {
        'claude-3-7-sonnet-20250219': 'Claude 3.7 Sonnet'
    },
    'mistral': {
        'codestral-2405': 'Codestral'
    }
}

# Базовый класс для всех провайдеров LLM с дополнительной функциональностью
class OpenAI_Vanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)
    
    def generate_sql(self, question, **kwargs):
        """
        Переопределяем метод generate_sql для использования наших системных промптов.
        """
        # Получаем релевантные данные для промпта
        related_ddl = self.get_related_ddl(question, **kwargs)
        related_docs = self.get_related_documentation(question, **kwargs)
        related_questions = self.get_similar_question_sql(question, **kwargs)
        
        # Собираем все данные в структуру для формирования промпта
        class RelatedData:
            def __init__(self, ddl, documentation, questions):
                self.ddl = ddl
                self.documentation = documentation
                self.questions = questions
        
        related_data = RelatedData(
            ddl=related_ddl,
            documentation=related_docs,
            questions=related_questions
        )
        
        # Формируем промпт с использованием нашей функции из system_prompts
        messages = system_prompts.get_message_log_prompt(
            question=question,
            ddl_list=related_data.ddl,
            doc_list=related_data.documentation,
            question_sql_list=related_data.questions
        )
        
        # Отправляем запрос к LLM
        sql = self.submit_prompt(messages)
        
        return sql

# Класс для Anthropic, если доступен
if Anthropic_Chat:
    class Anthropic_Vanna(ChromaDB_VectorStore, Anthropic_Chat):
        def __init__(self, config=None):
            ChromaDB_VectorStore.__init__(self, config=config)
            Anthropic_Chat.__init__(self, config=config)
        
        def generate_sql(self, question, **kwargs):
            """
            Переопределяем метод generate_sql для использования наших системных промптов.
            """
            # Получаем релевантные данные для промпта
            related_ddl = self.get_related_ddl(question, **kwargs)
            related_docs = self.get_related_documentation(question, **kwargs)
            related_questions = self.get_similar_question_sql(question, **kwargs)
            
            # Собираем все данные в структуру для формирования промпта
            class RelatedData:
                def __init__(self, ddl, documentation, questions):
                    self.ddl = ddl
                    self.documentation = documentation
                    self.questions = questions
            
            related_data = RelatedData(
                ddl=related_ddl,
                documentation=related_docs,
                questions=related_questions
            )
            
            # Формируем промпт с использованием нашей функции из system_prompts
            messages = system_prompts.get_message_log_prompt(
                question=question,
                ddl_list=related_data.ddl,
                doc_list=related_data.documentation,
                question_sql_list=related_data.questions
            )
            
            # Отправляем запрос к LLM
            sql = self.submit_prompt(messages)
            
            return sql

# Класс для Mistral, если доступен
if Mistral_Chat:
    class Mistral_Vanna(ChromaDB_VectorStore, Mistral_Chat):
        def __init__(self, config=None):
            ChromaDB_VectorStore.__init__(self, config=config)
            Mistral_Chat.__init__(self, config=config)
        
        def generate_sql(self, question, **kwargs):
            """
            Переопределяем метод generate_sql для использования наших системных промптов.
            """
            # Получаем релевантные данные для промпта
            related_ddl = self.get_related_ddl(question, **kwargs)
            related_docs = self.get_related_documentation(question, **kwargs)
            related_questions = self.get_similar_question_sql(question, **kwargs)
            
            # Собираем все данные в структуру для формирования промпта
            class RelatedData:
                def __init__(self, ddl, documentation, questions):
                    self.ddl = ddl
                    self.documentation = documentation
                    self.questions = questions
            
            related_data = RelatedData(
                ddl=related_ddl,
                documentation=related_docs,
                questions=related_questions
            )
            
            # Формируем промпт с использованием нашей функции из system_prompts
            messages = system_prompts.get_message_log_prompt(
                question=question,
                ddl_list=related_data.ddl,
                doc_list=related_data.documentation,
                question_sql_list=related_data.questions
            )
            
            # Отправляем запрос к LLM
            sql = self.submit_prompt(messages)
            
            return sql

# Функция для создания экземпляра соответствующего класса Vanna
def create_vanna_instance(llm_provider='openai', model=None):
    global current_llm_provider, current_llm_model
    
    # Сохраняем текущие значения провайдера и модели
    current_llm_provider = llm_provider
    if model:
        current_llm_model = model
    
    # Создаем конфигурацию в зависимости от провайдера
    config = {}
    
    if llm_provider == 'openai':
        model_name = model or os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
        config = {
            'api_key': os.environ['OPENAI_API_KEY'],
            'model': model_name,
            'temperature': float(os.environ['OPENAI_TEMPERATURE']),
            'max_tokens': int(os.environ['OPENAI_MAX_TOKENS'])
        }
        return OpenAI_Vanna(config=config)
    
    elif llm_provider == 'anthropic' and Anthropic_Chat:
        model_name = model or os.environ.get('ANTHROPIC_MODEL', 'claude-3-7-sonnet-20250219')
        config = {
            'api_key': os.environ['ANTHROPIC_API_KEY'],
            'model': model_name,
            'temperature': float(os.environ['ANTHROPIC_TEMPERATURE']),
            'max_tokens': int(os.environ['ANTHROPIC_MAX_TOKENS'])
        }
        return Anthropic_Vanna(config=config)
    
    elif llm_provider == 'mistral' and Mistral_Chat:
        model_name = model or os.environ.get('MISTRAL_MODEL', 'codestral-2405')
        config = {
            'api_key': os.environ['MISTRAL_API_KEY'],
            'model': model_name,
            'temperature': float(os.environ['MISTRAL_TEMPERATURE']),
            'max_tokens': int(os.environ['MISTRAL_MAX_TOKENS'])
        }
        return Mistral_Vanna(config=config)
    
    else:
        # Если провайдер не поддерживается, возвращаемся к OpenAI
        current_llm_provider = 'openai'
        model_name = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
        config = {
            'api_key': os.environ['OPENAI_API_KEY'],
            'model': model_name,
            'temperature': float(os.environ['OPENAI_TEMPERATURE']),
            'max_tokens': int(os.environ['OPENAI_MAX_TOKENS'])
        }
        return OpenAI_Vanna(config=config)

# Инициализируем Vanna с OpenAI по умолчанию
vn = create_vanna_instance(llm_provider='openai')

# Connect to DuckDB
try:
    db_path = 'data/retail_data.db'
    vn.connect_to_duckdb(url=db_path, read_only=True)
    print(f"Successfully connected to DuckDB at {db_path} in read-only mode")
except Exception as e:
    print(f"Error connecting to DuckDB in read-only mode: {str(e)}")
    # If we can't connect even in read-only mode, we have a more serious problem
    # Try one more time with normal mode as a fallback
    try:
        vn.connect_to_duckdb(url=db_path)
        print(f"Successfully connected to DuckDB in normal mode")
    except Exception as e:
        print(f"Failed to connect to DuckDB: {str(e)}")

# NO NEED TO CHANGE ANYTHING BELOW THIS LINE
def requires_cache(fields):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            id = request.args.get('id')

            if id is None:
                return jsonify({"type": "error", "error": "No id provided"})
            
            for field in fields:
                if cache.get(id=id, field=field) is None:
                    return jsonify({"type": "error", "error": f"No {field} found"})
            
            field_values = {field: cache.get(id=id, field=field) for field in fields}
            
            # Add the id to the field_values
            field_values['id'] = id

            return f(*args, **field_values, **kwargs)
        return decorated
    return decorator

@app.route('/api/v0/generate_questions', methods=['GET'])
def generate_questions():
    return jsonify({
        "type": "question_list", 
        "questions": vn.generate_questions(),
        "header": "Here are some questions you can ask:"
        })

@app.route('/api/v0/generate_sql', methods=['GET'])
def generate_sql():
    question = flask.request.args.get('question')

    if question is None:
        return jsonify({"type": "error", "error": "No question provided"})

    id = cache.generate_id(question=question)
    sql = vn.generate_sql(question=question)

    cache.set(id=id, field='question', value=question)
    cache.set(id=id, field='sql', value=sql)

    return jsonify(
        {
            "type": "sql", 
            "id": id,
            "text": sql,
        })

@app.route('/api/v0/run_sql', methods=['GET'])
@requires_cache(['sql'])
def run_sql(id: str, sql: str):
    try:
        df = vn.run_sql(sql=sql)

        cache.set(id=id, field='df', value=df)

        return jsonify(
            {
                "type": "df", 
                "id": id,
                "df": df.head(10).to_json(orient='records'),
            })

    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/download_csv', methods=['GET'])
@requires_cache(['df'])
def download_csv(id: str, df):
    csv = df.to_csv()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 f"attachment; filename={id}.csv"})

@app.route('/api/v0/generate_plotly_figure', methods=['GET'])
@requires_cache(['df', 'question', 'sql'])
def generate_plotly_figure(id: str, df, question, sql):
    try:
        code = vn.generate_plotly_code(question=question, sql=sql, df_metadata=f"Running df.dtypes gives:\n {df.dtypes}")
        fig = vn.get_plotly_figure(plotly_code=code, df=df, dark_mode=False)
        fig_json = fig.to_json()

        cache.set(id=id, field='fig_json', value=fig_json)

        return jsonify(
            {
                "type": "plotly_figure", 
                "id": id,
                "fig": fig_json,
            })
    except Exception as e:
        # Print the stack trace
        import traceback
        traceback.print_exc()

        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/get_training_data', methods=['GET'])
def get_training_data():
    df = vn.get_training_data()

    return jsonify(
    {
        "type": "df", 
        "id": "training_data",
        #"df": df.head(25).to_json(orient='records'),
        "df": df.to_json(orient='records'),
    })

@app.route('/api/v0/remove_training_data', methods=['POST'])
def remove_training_data():
    # Get id from the JSON body
    id = flask.request.json.get('id')

    if id is None:
        return jsonify({"type": "error", "error": "No id provided"})

    if vn.remove_training_data(id=id):
        return jsonify({"success": True})
    else:
        return jsonify({"type": "error", "error": "Couldn't remove training data"})

@app.route('/api/v0/train', methods=['POST'])
def add_training_data():
    question = flask.request.json.get('question')
    sql = flask.request.json.get('sql')
    ddl = flask.request.json.get('ddl')
    documentation = flask.request.json.get('documentation')

    try:
        id = vn.train(question=question, sql=sql, ddl=ddl, documentation=documentation)

        return jsonify({"id": id})
    except Exception as e:
        print("TRAINING ERROR", e)
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/generate_followup_questions', methods=['GET'])
@requires_cache(['df', 'question', 'sql'])
def generate_followup_questions(id: str, df, question, sql):
    followup_questions = vn.generate_followup_questions(question=question, sql=sql, df=df)

    cache.set(id=id, field='followup_questions', value=followup_questions)

    return jsonify(
        {
            "type": "question_list", 
            "id": id,
            "questions": followup_questions,
            "header": "Here are some followup questions you can ask:"
        })

@app.route('/api/v0/load_question', methods=['GET'])
@requires_cache(['question', 'sql', 'df', 'fig_json', 'followup_questions'])
def load_question(id: str, question, sql, df, fig_json, followup_questions):
    try:
        return jsonify(
            {
                "type": "question_cache", 
                "id": id,
                "question": question,
                "sql": sql,
                "df": df.head(10).to_json(orient='records'),
                "fig": fig_json,
                "followup_questions": followup_questions,
            })

    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/get_question_history', methods=['GET'])
def get_question_history():
    return jsonify({"type": "question_history", "questions": cache.get_all(field_list=['question']) })

# Новый API эндпоинт для получения доступных моделей
@app.route('/api/v0/get_available_models', methods=['GET'])
def get_available_models():
    return jsonify({
        "type": "available_models",
        "current_provider": current_llm_provider,
        "current_model": current_llm_model,
        "models": AVAILABLE_MODELS
    })

# Новый API эндпоинт для смены модели
@app.route('/api/v0/change_model', methods=['POST'])
def change_model():
    global vn
    
    data = flask.request.json
    provider = data.get('provider')
    model = data.get('model')
    
    if not provider or provider not in AVAILABLE_MODELS:
        return jsonify({"type": "error", "error": "Invalid provider"})
    
    if not model or model not in AVAILABLE_MODELS[provider]:
        return jsonify({"type": "error", "error": "Invalid model for the selected provider"})
    
    try:
        # Создаем новый экземпляр Vanna с выбранной моделью
        vn = create_vanna_instance(llm_provider=provider, model=model)
        
        # Переподключаемся к базе данных
        try:
            db_path = 'data/retail_data.db'
            vn.connect_to_duckdb(url=db_path, read_only=True)
        except Exception as e:
            # В случае ошибки пробуем подключиться в обычном режиме
            try:
                vn.connect_to_duckdb(url=db_path)
            except Exception as e:
                return jsonify({"type": "error", "error": f"Failed to connect to database: {str(e)}"})
        
        return jsonify({
            "type": "success",
            "message": f"Successfully changed model to {model} from provider {provider}",
            "provider": provider,
            "model": model
        })
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
