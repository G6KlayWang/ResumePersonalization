import openai
import pandas as pd
import json
import numpy as np
import time
import tiktoken
import random
import multiprocessing as mp
import os

# Set up your OpenAI API key
openai.api_key = "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"

# Model configuration
MODEL_NAME = "gpt-4o"  # Ensure you have access to gpt-4; otherwise use gpt-3.5-turbo
MAX_INPUT_TOKENS = 3000
MAX_RETRIES = 5
BASE_SLEEP = 1

encoding = tiktoken.encoding_for_model("gpt-4o")

def count_tokens(text):
    return len(encoding.encode(text))

def truncate_input(system_prompt, user_prompt, max_tokens=MAX_INPUT_TOKENS):
    system_tokens = count_tokens(system_prompt)
    allowed_user_tokens = max_tokens - system_tokens
    allowed_user_tokens = max(allowed_user_tokens, 0)

    user_tokens = encoding.encode(user_prompt)
    if len(user_tokens) > allowed_user_tokens:
        user_tokens = user_tokens[:allowed_user_tokens]
    truncated_user_prompt = encoding.decode(user_tokens)
    return truncated_user_prompt

def generate(input_text, max_retries=MAX_RETRIES, base_sleep=BASE_SLEEP):
    system_prompt = (
        "You are an assistant that extracts structured information from resumes. "
        "Return only the requested data in a single line. "
        "Do not include phrases like 'Here is' or 'Here are'. "
        "Do not use bullets, dashes, or asterisks. "
        "Do not include newlines in your output. "
        "Do not provide explanations. "
        "Do not include extra words or formatting. "
        "Just return the relevant data."
    )

    truncated_user_input = truncate_input(system_prompt, input_text, MAX_INPUT_TOKENS)

    for attempt in range(max_retries):
        try:
            # Exponential backoff with randomness
            sleep_time = base_sleep * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(sleep_time)

            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": truncated_user_input}
                ],
                temperature=0.7
            )
            return response.choices[0].message['content'].strip()

        except openai.error.RateLimitError:
            if attempt < max_retries - 1:
                continue
            else:
                return ""
        except Exception:
            if attempt < max_retries - 1:
                continue
            else:
                return ""

def summarize_resume(resume_text, max_retries=5):
    sections = {
        "personal_information": "Extract personal information (name, email, phone, address) from the following resume. Only return raw data in one line, no extra words or formatting: ",
        "achievements": "Extract achievements from the following resume. Only return raw data in one line, no extra words or formatting: ",
        "certificate": "Extract certificates from the following resume. Only return raw data in one line, no extra words or formatting: ",
        "education": "Extract education details from the following resume. Only return raw data in one line, no extra words or formatting: ",
        "projects": "Extract project details from the following resume. Only return raw data in one line, no extra words or formatting: ",
        "skills": "Extract skills from the following resume. Only return raw data in one line, no extra words or formatting: ",
        "experience": "Extract employment/experience history from the following resume. Only return raw data in one line, no extra words or formatting: "
    }

    summarized_data = {}
    for section, prompt in sections.items():
        input_text = prompt + resume_text
        result = generate(input_text, max_retries=max_retries)
        cleaned_result = result.strip()
        if not cleaned_result or cleaned_result.lower() in ["none", "no information", "no data"]:
            summarized_data[section] = None
        else:
            summarized_data[section] = cleaned_result

    return summarized_data
count = 0
def process_row(row_dict):
    global count
    count += 1
    print(f"Processing row {count}...")
    # row_dict is a dictionary representing a single row
    resume_text = row_dict["resume_combined"]
    summary = summarize_resume(resume_text)
    row_dict["summarized_sections"] = json.dumps(summary)
    return row_dict

def main():
    input_csv_path = "data/data_set/DATA3.csv"  # Replace with your input path
    output_csv_path = "data/data_set/summarized_resumes3.csv"  # Output path
    resume_column_name = "resume_combined"

    df = pd.read_csv(input_csv_path)

    if resume_column_name not in df.columns:
        raise ValueError(f"The column '{resume_column_name}' does not exist in the provided CSV.")

    df[resume_column_name] = df[resume_column_name].astype(str)

    # Convert the DataFrame rows to a list of dictionaries
    rows = df.to_dict(orient="records")

    num_processes = 4  # Adjust as needed
    with mp.Pool(num_processes) as pool:
        processed_rows = pool.map(process_row, rows)

    # Convert processed rows back to DataFrame
    final_df = pd.DataFrame(processed_rows)
    final_df.to_csv(output_csv_path, index=False)
    print(f"Processing complete. Results saved to {output_csv_path}")

if __name__ == "__main__":
    main()
