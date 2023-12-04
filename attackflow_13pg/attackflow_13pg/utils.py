import openai
import tempfile
from django.contrib.staticfiles import finders
# common generator
def generator(prompt:str)-> str:
    """
    This function utilizes the OpenAI service for convert code.
    
    To replace the API key:

    1. Visit the official website of OpenAI and sign in to your account.
    2. Go to the API key section and generate a new key if you don't have one already.
    3. Copy the new API key.
    4. Replace the value of openai.api_key variable with the new API key.
    5. Save the file and ensure the updated API key is used in subsequent API calls.
    """
    openai.api_key = "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" # private API key
    model_engine = "gpt-3.5-turbo-16k"  # Specify the model engine to use
    temperature = 0.5
    max_tokens = 5000 # maximum char length
    generated_text = ''
    content = []
    # for i in range(0, len(prompt), max_prompt_tokens):
    #     chunk = prompt[i:i+max_prompt_tokens]

    #     response = openai.Completion.create(
    #         engine=model_engine,
    #         prompt=chunk,
    #         temperature=temperature,
    #         max_tokens=max_tokens
    #     )
    #     generated_text += response.choices[0].text.strip()
    # return content

    # Send the API request and print the generated text
    # response = openai.Completion.create(
    #     engine=model_engine,
    #     prompt=prompt,
    #     temperature=temperature,
    #     max_tokens=max_tokens
    # )
    # generated_text = response.choices[0].text.strip()

    # Send the API request using the ChatCompletion endpoint
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that converts incident reports into a specified JSON format."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    generated_text = response['choices'][0]['message']['content'].strip()
    return generated_text


# check if raw_code is fromLanguage
def checker(raw_code:str, fromLanguage: str) -> str:
    print(fromLanguage)
    prompt = "is the following code written in "+ fromLanguage + " ? reply \'Yes\' or \'No\' and reason \n" + raw_code
    return generator(prompt)

'''
*Description:
Use openai API to convert code into target coding language 

*args:
    string raw_code : origianl code in string format
    string toLanguge : coding language to be converted
*ret:
    string generated_text : converted code in string format
'''
def converter(raw_code:str, toLanguage:str) -> str:
    prompt = "convert this code \n" +raw_code+ "\n to "+ toLanguage
    return generator(prompt)

def analysis(incident_report:str, example:str) -> str:
    #prompt = "replace info from this report: \n" +incident_report+ "\n into the following format: "+ example
    prompt = "把这个报告:\n" + incident_report + "\n根据这个例子替换对应信息: \n"+ example
    return generator(prompt)

def textToTxt(text:str) -> str:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    # Write the text to the temporary file
    temp_file.write(text.encode('utf-8'))
    temp_file.close()
    print(f"Temp file path: {temp_file.name}")
    return temp_file.name

