# from langchain import OpenAI
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

# # Replace 'your-api-key' with your actual OpenAI API key
# api_key = "your-api-key"

# # Initialize the OpenAI client with the desired parameters
# llm = OpenAI(api_key=api_key, model_name="text-davinci-003", temperature=0.7)

# # Define a simple prompt template
# template = PromptTemplate.from_template("Write a friendly introduction for {name}.")

# # Create a chain that links the prompt template and the LLM
# llm_chain = LLMChain(prompt=template, llm=llm)

# # Define input for the prompt
# input_data = {"name": "Alice"}

# # Execute the chain and print the result
# result = llm_chain.run(input_data)
# print(result)

# from dotenv import load_dotenv
# import os

# # Load environment variables from the .env file
# load_dotenv()

# # Access the environment variables
# database_url = os.getenv('DATABASE_URL')
# secret_key = os.getenv('SECRET_KEY')
# debug = os.getenv('DEBUG')

# print("Database URL:", database_url)
# print("Secret Key:", secret_key)
# print("Debug Mode:", debug)
   