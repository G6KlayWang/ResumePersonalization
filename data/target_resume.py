import csv
import json
import os
import math
import time
import openai
import backoff
import tiktoken
import pandas as pd
from multiprocessing import Pool

# ---------------- CONFIGURATION ----------------
openai.api_key = "Your API key"
MODEL_NAME = "gpt-4o"
NUM_PROCESSES = 5
CHECKPOINT_INTERVAL = 100  # Save results every 100 rows
INPUT_CSV = "E:/01_NYU/2024/2024 Fall/DL System/ResumePersonalization/data/data_set/DATA_chunk.csv"    # CSV with columns: id, extracted_job_details, summarized_sections
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MASTER_PROMPT = (
    "I am a highly experienced career advisor and resume writing expert with 15 years of specialized experience.\n\n"
    "Primary role: Craft exceptional resumes and cover letters tailored to specific job descriptions, optimized for both ATS systems and human readers.\n\n"
    "# Instructions for creating optimized resumes and cover letters:\n"
    "1. Analyze the given job description:\n"
    "   - Extract key requirements and keywords.\n"
    "   - Adapt analysis based on the industry and role.\n\n"
    "2. Create compelling resumes:\n"
    "   - Highlight quantifiable achievements.\n"
    "   - Tailor content to the specific job and company.\n"
    "   - Emphasize the candidate's unique value proposition.\n\n"
    "3. Craft persuasive cover letters:\n"
    "   - Align content with the targeted position.\n"
    "   - Use a professional tone, while reflecting the candidate's personality.\n"
    "   - Incorporate a strong opening statement.\n"
    "   - Highlight both hard and soft skills valued for the target role.\n\n"
    "4. Optimize for Applicant Tracking Systems (ATS):\n"
    "   - Integrate industry-specific keywords.\n"
    "   - Ensure content is both ATS-friendly and engaging for human readers.\n\n"
    "5. Provide industry-specific guidance:\n"
    "   - Incorporate current hiring trends.\n"
    "   - Highlight critical information to pass the '6-second rule.'\n"
    "   - Maintain clear, consistent formatting.\n\n"
    "6. Apply best practices:\n"
    "   - Quantify achievements where possible.\n"
    "   - Use specific, impactful statements instead of generic ones.\n"
    "   - Keep content updated based on latest industry standards.\n"
    "   - Use active voice and strong action verbs.\n\n"
    "IMPORTANT: Do not remove, change, anonymize, or alter any personal identifying details (e.g., name, email, city) provided in the candidate's input. All personal information must appear verbatim as given in the input resume. Preserve the exact spelling, punctuation, and formatting.\n\n"
    "Your goal is to produce a single, valid JSON object that includes all sections as top-level keys. The JSON must contain:\n"
    "- 'personal_info'\n"
    "- 'achievements'\n"
    "- 'certifications'\n"
    "- 'education'\n"
    "- 'projects'\n"
    "- 'skill_section'\n"
    "- 'work_experience'\n\n"
    "Do not add any commentary or explanations. Do not use code fences. Just produce one valid JSON object with all sections combined."
)

SECTIONS_PROMPT = {
    "personal_info": (
        "Include a 'personal_info' key in the single output JSON object. This key must contain the candidate's personal information exactly as provided. "
        "Do not alter any personal details. No extra commentary or explanation.\n\n"
        "<personal_info>{candidate_personal_info}</personal_info>\n"
        "<job_description>{job_description}</job_description>"
    ),
    "achievements": (
        "Include an 'achievements' key in the single output JSON object. "
        "Align achievements with the job, preserve personal info, no extra commentary.\n\n"
        "<achievements>{candidate_achievements}</achievements>\n"
        "<job_description>{job_description}</job_description>"
    ),
    "certifications": (
        "Include a 'certifications' key in the single output JSON object. "
        "Align with the job, preserve personal info, no extra commentary.\n\n"
        "<certifications>{candidate_certifications}</certifications>\n"
        "<job_description>{job_description}</job_description>"
    ),
    "education": (
        "Include an 'education' key in the single output JSON object. "
        "Preserve education details as is, no extra commentary.\n\n"
        "<education>{candidate_education}</education>\n"
        "<job_description>{job_description}</job_description>"
    ),
    "projects": (
        "Include a 'projects' key in the single output JSON object. It should contain 3 projects aligned with the job. "
        "Each with name, dates, and 3 bullet points. Preserve personal info, no extra commentary.\n\n"
        "<projects>{candidate_projects}</projects>\n"
        "<job_description>{job_description}</job_description>"
    ),
    "skills": (
        "Include a 'skill_section' key in the single output JSON object. "
        "Group related skills. Preserve personal info, no extra commentary.\n\n"
        "<skills>{candidate_skills}</skills>\n"
        "<job_description>{job_description}</job_description>"
    ),
    "experience": (
        "Include a 'work_experience' key in the single output JSON object. It should contain 3 roles aligned with the job, each with 3 bullet points. "
        "Preserve personal info, no extra commentary.\n\n"
        "<experience>{candidate_experience}</experience>\n"
        "<job_description>{job_description}</job_description>"
    ),
}

def create_combined_prompt(job_details, resume_sections):
    # Build a prompt instructing the model to create one single JSON object
    sections_prompt_str = (
        SECTIONS_PROMPT["personal_info"].format(
            candidate_personal_info=resume_sections.get("personal_information", ""),
            job_description=job_details
        ) + "\n\n" +
        SECTIONS_PROMPT["achievements"].format(
            candidate_achievements=resume_sections.get("achievements", ""),
            job_description=job_details
        ) + "\n\n" +
        SECTIONS_PROMPT["certifications"].format(
            candidate_certifications=resume_sections.get("certificate", ""),
            job_description=job_details
        ) + "\n\n" +
        SECTIONS_PROMPT["education"].format(
            candidate_education=resume_sections.get("education", ""),
            job_description=job_details
        ) + "\n\n" +
        SECTIONS_PROMPT["projects"].format(
            candidate_projects=resume_sections.get("projects", ""),
            job_description=job_details
        ) + "\n\n" +
        SECTIONS_PROMPT["skills"].format(
            candidate_skills=resume_sections.get("skills", ""),
            job_description=job_details
        ) + "\n\n" +
        SECTIONS_PROMPT["experience"].format(
            candidate_experience=resume_sections.get("experience", ""),
            job_description=job_details
        )
    )

    # Append the instruction again at the end of the prompt:
    # "Return one single JSON object with all the keys included."
    final_instruction = (
        "\n\nAll of the above sections must be combined into a single, valid JSON object. "
        "No extra commentary, no separate code blocks. Just return one JSON object containing all sections."
    )

    full_prompt = MASTER_PROMPT + sections_prompt_str + final_instruction
    return full_prompt

def truncate_prompt_for_token_limit(prompt_text, max_tokens=8000):
    """
    Truncate the prompt if it exceeds a certain token limit using tiktoken.
    """
    enc = tiktoken.encoding_for_model(MODEL_NAME)
    token_ids = enc.encode(prompt_text)
    if len(token_ids) > max_tokens:
        token_ids = token_ids[:max_tokens]
        prompt_text = enc.decode(token_ids)
    return prompt_text

@backoff.on_exception(backoff.expo, openai.error.RateLimitError, max_time=60)
def call_openai_api(prompt):
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

count = 0
def process_chunk(chunk, start_index):
    global count
    count += 1
    print(f"Processing chunk {count} starting from row {start_index}...")

    results = {}

    # The sections we expect to be present in the returned JSON
    required_sections = [
        "personal_info", 
        "achievements", 
        "certifications", 
        "education", 
        "projects", 
        "skill_section", 
        "work_experience"
    ]

    for i, (row_index, job_details, resume_json_str) in enumerate(chunk):
        print(f"Processing row {row_index}...")
        # Parse resume JSON
        resume_sections = json.loads(resume_json_str)
        # Create prompt
        prompt = create_combined_prompt(job_details, resume_sections)
        prompt = truncate_prompt_for_token_limit(prompt)

        # Try up to 3 times to get a valid and complete response
        attempts = 0
        improved_resume = None
        while attempts < 3:
            attempts += 1
            try:
                improved_resume = call_openai_api(prompt)
                #print(improved_resume)
                #print(type(improved_resume))
                # Attempt to parse the improved_resume as JSON
                resume_data = json.loads(improved_resume)

                # Check if all required sections are present
                if all(section in resume_data for section in required_sections):
                    # All sections present and valid JSON
                    break
                else:
                    print(f"Missing one or more required sections on attempt {attempts}. Retrying...")
            except json.JSONDecodeError:
                print(f"JSON decode error on attempt {attempts}. Retrying...")
            except Exception as e:
                print(f"Unexpected error on attempt {attempts}: {e}")

            # If we're here, either JSON parse failed or sections missing, retry
            time.sleep(2)  # small delay before retrying

        # If after attempts still not valid, proceed with what we have
        if improved_resume is None:
            # Could not get a valid response even after 3 attempts
            print(f"Failed to produce a valid complete resume for row {row_index} after 3 attempts.")
            results[row_index] = None
        else:
            results[row_index] = improved_resume

        # Checkpointing every 100 rows
        if (i + 1) % CHECKPOINT_INTERVAL == 0:
            checkpoint_path = os.path.join(OUTPUT_DIR, f"checkpoint_{start_index+i}.json")
            with open(checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

    # Final save for this chunk
    last_index = start_index + len(chunk) - 1
    checkpoint_path = os.path.join(OUTPUT_DIR, f"checkpoint_final_{last_index}.json")
    with open(checkpoint_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results

def main():
    # Read CSV using pandas
    df = pd.read_csv(INPUT_CSV)
    #print(df["summarized_sections"][0])
    
    # Ensure columns "id", "extracted_job_details", and "summarized_sections" exist
    data = []
    for i, row in df.iterrows():
        idx = row["ID"]  # Or use i if id not present.
        job_details = row["extracted_job_details"]
        resume = row["summarized_sections"]
        
        data.append((idx, job_details, resume))
    data.sort(key=lambda x: x[0])

    # Split data into chunks
    chunk_size = math.ceil(len(data) / NUM_PROCESSES)
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    # Prepare tasks for pool: (chunk, start_index)
    tasks = []
    start = 0
    for c in chunks:
        tasks.append((c, start))
        start += len(c)

    # Use multiprocessing Pool
    with Pool(NUM_PROCESSES) as pool:
        results_list = pool.starmap(process_chunk, tasks)

    # Combine all results
    all_results = {}
    for res in results_list:
        all_results.update(res)

    final_path = os.path.join(OUTPUT_DIR, "combined_results_v2.json")
    with open(final_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print("Processing complete. Results saved to output directory.")

if __name__ == "__main__":
    main()
