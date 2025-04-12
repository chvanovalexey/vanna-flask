# vanna-flask
Web server for chatting with your database using DuckDB and OpenAI



https://github.com/vanna-ai/vanna-flask/assets/7146154/5794c523-0c99-4a53-a558-509fa72885b9



# Setup

## Set your environment variables
Create a `.env` file with the following variables:
```
# OpenAI настройки
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=1000
```

## Install dependencies
```
pip install -r requirements.txt
```

## Database
This application is configured to use a DuckDB database located at `data/retail_data.db`. The database already contains retail sales data.

## Training Vanna AI
Before using the application effectively, you should train the Vanna AI model. This can be done through the web interface after starting the application, or by using these sample Python commands:

```python
# Train on database schema
df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
plan = vn.get_training_plan_generic(df_information_schema)
vn.train(plan=plan)

# Add training examples for common questions
vn.train(question="What are the top selling products?", 
         sql="SELECT p.product_name, COUNT(*) as sold_count FROM sales s JOIN products p ON s.product_id = p.product_id GROUP BY p.product_name ORDER BY sold_count DESC LIMIT 10")

vn.train(question="What is our revenue by month?", 
         sql="SELECT strftime('%Y-%m', s.sale_date) as month, SUM(s.amount) as revenue FROM sales s GROUP BY month ORDER BY month")
```

## Run the server
```
python app.py
```

Once started, access the web interface at http://127.0.0.1:5000

Make sure you have waitress installed:
```
pip install waitress
```

### 2. Login to Heroku

### 3. Create a Heroku application

### 4. Set environment variables
Set all required environment variables on Heroku:


### 5. Deploy your application
```
git add .
git commit -m "Ready for Heroku deployment"
git push heroku main
```

### 6. Open your application
```
heroku open
```

## Important Notes for Heroku Deployment

- **Dyno Sleep**: On the free tier, Heroku dynos go to sleep after 30 minutes of inactivity. The first request after inactivity may be slow.
  
- **Memory Cache**: The current implementation uses an in-memory cache which will be cleared when dynos restart. Consider implementing a persistent cache solution if needed.
  
- **Database Access**: Make sure your Snowflake account can be accessed from Heroku's IP ranges.
  
- **Logs**: You can view application logs with the command:
  ```
  heroku logs --tail
  ```

- **Scaling**: If you need to handle more traffic, you can scale your dynos:
  ```
  heroku ps:scale web=2
  ```
  Note that this requires a paid plan.
```

