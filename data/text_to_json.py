import openai
import json

# Set up your OpenAI API key
openai.api_key = "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"

def generate(input_text):
    """
    Function to interact with OpenAI's GPT-4 model to extract information based on the input prompt.
    """
    try:
        # Call the OpenAI GPT-4 model
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts information from resumes."},
                {"role": "user", "content": input_text}
            ],
            max_tokens=1000,
            temperature=0.3,
        )
        # Extract and return the assistant's reply
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating text: {e}")
        return ""

def summarize_resume(resume_text):
    """
    Function to summarize a resume into predefined sections using prompts and GPT-4.
    """
    sections = {
        "Employment History": "",
        "Skills": "",
        "Education": "",
        "Certifications": "",
        "Projects": ""
    }

    prompts = {
        "Employment History": "Extract the employment history from the following resume: ",
        "Skills": "List the skills mentioned in the following resume: ",
        "Education": "Extract the education details from the following resume: ",
        "Certifications": "List any certifications mentioned in the following resume: ",
        "Projects": "Extract any projects mentioned with details in the following resume: "
    }

    for section, prompt in prompts.items():
        input_text = prompt + resume_text
        sections[section] = generate(input_text)

    return sections

def process_resumes_from_json(json_file_path, summarized_json_file_path):
    """
    Function to process resumes from a JSON file, summarize them, and save the output to another JSON file.
    """
    try:
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            resumes = json.load(json_file)

        summarized_resumes = {}

        for filename, resume_text in resumes.items():
            print(f"Processing {filename}...")
            summarized_resumes[filename] = summarize_resume(resume_text)
            print(f"Summarized {filename}")

        with open(summarized_json_file_path, "w", encoding="utf-8") as output_json_file:
            json.dump(summarized_resumes, output_json_file, indent=4, ensure_ascii=False)
        print(f"All resumes summarized and saved to {summarized_json_file_path}")
    except Exception as e:
        print(f"Error processing resumes: {e}")

# File paths
json_file_path = "data_set/input_json_folder/extracted_resumes.json"  # Replace with the actual path to your JSON file
summarized_json_file_path = "data_set/output_json_folder/summarized_resumes.json"  # Output file path

# Run the script
process_resumes_from_json(json_file_path, summarized_json_file_path)