import openai
import pandas as pd
import json
import numpy as np
import multiprocessing as mp
import tiktoken
import time

'''
Extract job details from job descriptions using OpenAI's GPT-4 model.

'''

# Set your OpenAI API key
openai.api_key = ""

JOB_DETAILS_EXTRACTOR = """ 
<task>
Identify the key details from a job description and company overview to create a structured JSON output. Focus on extracting the most crucial and concise information that would be most relevant for tailoring a resume to this specific job.
</task>

<job_description>
{job_description}
</job_description>

Note: The "keywords", "job_duties_and_responsibilities", and "required_qualifications" sections are particularly important for resume tailoring. Ensure these are as comprehensive and accurate as possible.  
"""

execution_count = 0

# Setup the tokenizer
encoding = tiktoken.encoding_for_model("gpt-4")

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

def extract_job_details(description):
    global execution_count
    execution_count += 1
    print(f"Processing job description {execution_count}...")
    print(description[:10])

    # Format the prompt
    prompt = JOB_DETAILS_EXTRACTOR.format(job_description=description)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    # Calculate token usage for the messages
    total_message_content = "".join([msg["content"] for msg in messages])
    token_count = count_tokens(total_message_content)
    
    print(f"Token count for this prompt before truncation: {token_count}")

    # We plan to have a max of 8000 tokens total. 1500 for completion.
    # So messages should not exceed 6500 tokens.
    max_total_tokens = 8000
    completion_tokens = 1500
    max_message_tokens = max_total_tokens - completion_tokens  # 6500

    if token_count > max_message_tokens:
        # Truncate the user prompt to fit into 6500 tokens
        print(f"Truncating prompt from {token_count} tokens to {max_message_tokens} tokens...")
        
        # Encode, truncate, and decode
        encoded_tokens = encoding.encode(total_message_content)
        truncated_tokens = encoded_tokens[:max_message_tokens]
        truncated_content = encoding.decode(truncated_tokens)
        
        system_content = messages[0]["content"]
        user_content = prompt
        system_token_count = count_tokens(system_content)

        # Re-encode to separate
        system_encoded = encoding.encode(system_content)
        # The remainder of the tokens belong to the user prompt
        user_start_index = len(system_encoded)  # user prompt starts after system tokens
        
        if len(truncated_tokens) > user_start_index:
            truncated_user_tokens = truncated_tokens[user_start_index:]
            truncated_user_content = encoding.decode(truncated_user_tokens)
        else:
            # If the truncation cut into the system message (unlikely, but let's be safe),
            # just truncate the user content to empty.
            truncated_user_content = ""
        
        # Reassign the truncated content to the user message
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": truncated_user_content}
        ]

        # Recalculate token count after truncation
        total_message_content = system_content + truncated_user_content
        token_count = count_tokens(total_message_content)
        print(f"Token count after truncation: {token_count}")

    max_retries = 5
    backoff_delay = 5  # initial delay in seconds

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=completion_tokens,
                temperature=0
            )
            
            content = response.choices[0].message["content"]
            try:
                extracted_data = json.loads(content)
            except json.JSONDecodeError:
                extracted_data = content
            
            return extracted_data
        
        except openai.error.RateLimitError:
            # If rate limit is hit, wait and try again
            print(f"Rate limit reached (Attempt {attempt+1}/{max_retries}). Waiting {backoff_delay} seconds before retrying...")
            time.sleep(backoff_delay)
            backoff_delay *= 1.5

    # If we get here, all retries have failed
    print("Rate limit error persists after maximum retries.")
    return {"error": "Rate limit exceeded after multiple retries"}

def process_chunk(df_chunk):
    df_chunk["extracted_job_details"] = df_chunk["description"].apply(extract_job_details)
    return df_chunk

if __name__ == "__main__":
    # Load your DataFrame
    df = pd.read_csv("E:/01_NYU/2024/2024 Fall/DL System/ResumePersonalization/data/job_5.csv")
    
    num_processes = mp.cpu_count()
    print(f"Number of processes: {num_processes}")
    df_chunks = np.array_split(df, num_processes)

    with mp.Pool(processes=num_processes) as pool:
        result_chunks = pool.map(process_chunk, df_chunks)
    
    final_df = pd.concat(result_chunks, ignore_index=True)
    final_df.to_csv("output_jobs_with_details5.csv", index=False)

    print(f"Number of job descriptions processed: {len(final_df)}")