# Resume Personalization

<div align="center">
<h3>Authors</h3>
<table>
  <tr>
    <td>Charles Wang</td>
    <td><a href="mailto:mw4899@nyu.edu">mw4899@nyu.edu</a></td>
  </tr>
    <tr>
    <td>Yue Han</td>
    <td><a href="mailto:yh5404@nyu.edu">yh5404@nyu.edu</a></td>
  </tr>
</table>
</div>

## Procedure

Our approach involves:

1. **Data Collection and Preprocessing**: We collected resume data and job description data from various sources, including scrapping and collecting manually.We extracted the key information from the job descriptions and categoried the origina resume data into seven sections. 
2. **Prompt Engineering**: We have two parts: master prompt and section prompt. We redesign the content of the prompt based on the Resumeflow to make more fit for data generation and finetuning.
3. **Model Finetuning and Evaluation**: We implement PEFT to finetuning a LLama 3.1 8B model, significantly reduced the finetuning cost.
4. **Evaluation**: We use three metrics to evaluation the results produced by GPT 4o, original Llama 3.1 8B model and the finetuned Llama 3.1 8B model.

## Data Source
### Reume Data

1. Training Data:
Due the limit budget to use the GPT API, we selected the first 600 resumes data from this [github Repo](https://github.com/florex/resume_corpus) The resume data are stored in text format.
3. Evaluation Data:
We manually collected some real resume data form evaluation, mainly the people from NYU [Computational Intelligence, Vision, and Robotics Lab](https://wp.nyu.edu/cilvr/)

For privacy, I am sorry that our evaluation data is not currently available

### Job Details data
We use the [Job Spy](https://github.com/Bunsly/JobSpy?tab=readme-ov-file#output) to scrap the job details from various sources including Indeed, linkedin, glassdoor, google. We limit the job position to be within United States. We main collected job descriptions for positions including software engineer, data analyst, data scientist, data engineer, machine learning engineer. The number of job descriptions collected categorized by positions is below: Data analyst 125, data engineer 100, Data scientist 116, machine learning engineer 120, sde 120

## Data Preprocessing
1. For job descriptions, we extracted the most important information and stored as job details using GPT 4 model, including job titles, salary, skills, requirement, etc
2. For resume data, we leveraged a GPT 4o mini model to categorize the resume into seven cetegories including personal information, achievements, certificate, education, projects, skills and experience with some prompt engineering. The categorized results are stored in json format
3. As the resume in the datasets does not contain personal information, for the purpose of resume personalization, we impement GPT model to randomly generate some personal information including names, email address, education and location for each resume. 

## Target Data Generation
As finetuning the model is similar with supervised learning in our case, we need a improved version of the resume for the model to learn. As it is challenging to get two versions of a resume for the same person, we decided to use GPT 4o model to generated a polished version of the resume as the target data in the finetune. 

At the end, we prepared 532 resume data. Some data are partiled out due the token limit of the API.

## Prompt Engineering
We prepared two sets of [prompts](https://github.com/G6KlayWang/ResumePersonalization/blob/main/section_prompt.py)
1. Master prompt, general instructions for the section improvement
2. Section prompt, specific improve and generation instruction customized for each section

## Model Finetuning

We finetuned a Llama 3.1 8B model with Lora using one A800 GPU on [Autodl](https://www.autodl.com/)

In the finetuning process, we did not finetune the model with the entire resume instead our finetune data is section by section as a multitask finetuning. 

Here is a sample of our finetune data. 
```
{'prompt': '"I am an experienced career advisor specializing in crafting exceptional resumes and cover letters tailored to specific job descriptions, optimized for ATS systems and human readers.\n\n**Instructions for Optimized Resume and Cover Letter Creation:**\n1. **Analyze Job Descriptions:** Extract key requirements and industry-specific keywords from the provided job description.\n2. **Create Compelling Resumes:** Highlight quantifiable achievements, tailor content specifically to the role, and emphasize the candidate\'s value proposition.\n3. **Craft Persuasive Cover Letters:** Align the tone and content with the job, balance professionalism with personality, and showcase soft skills through specific, impactful examples.\n4. **Optimize for ATS:** Integrate keywords strategically, maintain clear formatting, and ensure the document passes ATS scans while remaining engaging for human readers.\n5. **Provide Industry-Specific Guidance:** Reflect current trends, prioritize relevance, and use concise, impactful statements.\n\n**Best Practices:**\n- Quantify achievements where possible.\n- Use specific, impactful statements instead of generic ones.\n- Maintain an active voice with strong action verbs.\n\n**Goal:** Deliver tailored documents that highlight the candidate\'s value, ensure ATS compatibility, and capture the employer\'s attention.\n\n\nACHIEVEMENTS = You are going to write a JSON resume section of "Achievements" for an applicant applying for job posts.\n\nStep to follow:\n1. Analyze my achievements details to match job requirements.\n2. Create a JSON resume section that highlights strongest matches\n3. Optimize JSON section for clarity and relevance to the job description.\n\nInstructions: Modify the achievements section to make it more aligned with the job descriptions and more professional.\n1. Focus: Craft relevant achievements aligned with the job description.\n2. Honesty: Prioritize truthfulness and objective language.\n3. Align achievements with the job, preserve personal info, no extra commentary, modify and improve the descriptions of achievements to make it aligning as close to the job descritions as possible."\n\n<achievements>\nDesigned databases to fit a variety of needs, ensured security of databases, problem-solved for back-end and front-end needs, installed and tested new database management systems, customized and installed applications, monitored performance for smooth front-end experience, administered and maintained over 150 database servers, ensured SOX compliance for code changes, migrated data using ETL, upgraded servers from SQL Server 2005 to 2014, provided 24/7 on-call support, executed migration/decommission plan for over 500 databases within 4 months.\n</achievements>\n\n<job_description>\n{\'job_title\': \'Data Analyst\', \'job_type\': [\'Full-time\', \'Part-time\'], \'salary\': \'From $40.00 per hour\', \'location\': \'Remote\', \'keywords\': [\'AI chatbots\', \'Data Science\', \'Applied Math\', \'Computer Science\', \'arithmetic\', \'algebra\', \'geometry\', \'calculus\', \'probability\', \'statistics\', \'inductive/deductive reasoning\'], \'job_duties_and_responsibilities\': [\'Give AI chatbots diverse and complex mathematics problems and evaluate their outputs\', \'Evaluate the quality produced by AI models for correctness and performance\'], \'required_qualifications\': [\'Fluency in English (native or bilingual level)\', \'Detail-oriented\', \'Proficient in data science, arithmetic, algebra, geometry, calculus, probability, statistics, and inductive/deductive reasoning\', \'A current, in progress, or completed Masters and/or PhD is preferred but not required\'], \'benefits\': [\'This is a full-time or part-time REMOTE position\', \'You’ll be able to choose which projects you want to work on\', \'You can work on your own schedule\', \'Projects are paid hourly starting at $40+ per hour, with bonuses on high-quality and high-volume work\'], \'payment_method\': \'PayPal\', \'expected_hours_per_week\': \'1 – 40\'}\n</job_description>\n \n',
 'Output': '<|output starts|>"Developed and optimized data-driven solutions, enhancing database security and performance. Successfully administered and maintained over 150 database servers, ensuring SOX compliance and smooth operation. Executed a comprehensive migration plan for over 500 databases within a 4-month timeframe, enhancing data accessibility and system efficiency."\n<|out ends|>'}
```
Finally, we have 3675 data entries in sections

We trained the model with 2, 3 and 4 epochs respectively and a learning rate of 2e-4 and achieved a loss of 0.067300 at the end. The finetuning took around 1 hour on one A800 GPU.

## Inference and Evaluation

We found out the the 4 epochs finetuning version has the best performance in terms of extracting and improving the content for each section in the resume. 

We evaluation the model with the real world resume data seperated in different sections combined with the job descriptions in terms of user personalization, job alignment and model hallucination.

The results is shown below: 


## Future Work
1. Finetune the model with more data. We are only able to process 500+ resumes due to the budget limit
2. Merge our finetuned model into resumeflow to generate a resume in pdf directly
3. handle the challenge that the llama model includes prompt and input both in the generated output

# Project

## Installation
1. Requestion the access to the Llama model from Huggingface.
```
from huggingface_hub import login
login(token = 'Your token')

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
```
3. Get the login token for huggingface and the GPT API key
4. Install the following package
```
pip install datasets transformers, evaluate, re
```

## Tutorial
### Training
1. Downlaod the raw resume data from [the resume corpus github Repo](https://github.com/florex/resume_corpus) and scraping some job descriptions using the scrapper in the [notebootk](https://github.com/G6KlayWang/ResumePersonalization/blob/main/data/jd_scrap.ipynb)

2. Use the code in notebook [data_preprocess](https://github.com/G6KlayWang/ResumePersonalization/blob/main/data_preprocess.ipynb) to preprocess the resume data and the data returned by the job scrapper and generate some simulated personal information using GPT API.

3. Leverage script [jd_detail.py](https://github.com/G6KlayWang/ResumePersonalization/blob/main/data/jd_detail.py) to extract key information from the full text of job descriptions and [resume_section.py](https://github.com/G6KlayWang/ResumePersonalization/blob/main/data/resume_section.py) to categorize the resume data into seven sections. 

4. Once had the job details extracted and resume categorized, you can save these two data in to csv file in seperate columns. Then use the [target_resume.py](https://github.com/G6KlayWang/ResumePersonalization/blob/main/data/target_resume.py) to generate the target data using GPT API. The simulated resume will be stored in a json file. 

5. Once had the input data ina csv file and output data in json file, you can use the [Llama31_finetune](https://github.com/G6KlayWang/ResumePersonalization/blob/main/Llama31_finetune.ipynb) notebook to finetune the model, you can adjust the configuration for different number of epochs. In the notebook, you can directly run a test using the finetuned model.
```
training_args = TrainingArguments(
    output_dir="./finetuned-llama-lora",
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    learning_rate=2e-4,
    num_train_epochs=2,
    logging_steps=300,
    save_steps=3000,
    #save_total_limit=1,
    gradient_accumulation_steps=1,
    fp16=True if torch.cuda.is_available() else False,
    eval_strategy="no",
    #eval_steps=300,
    logging_dir="./logs"
)
```

### Inferencing and testing
1. If your resume data is in pdf format, you can use [pdf_extract.py](https://github.com/G6KlayWang/ResumePersonalization/blob/main/data/pdf_extract.py) to convert all the content in your pdf to text. Then use the [resume_section.py](https://github.com/G6KlayWang/ResumePersonalization/blob/main/data/resume_section.py) to categorize the resume data into seven sections. 

2. Job descriptions collection and data preprocssing are the same with the first three steps in training.

3. Using the [Evaluation_realworld_rg.ipynb](https://github.com/G6KlayWang/ResumePersonalization/blob/main/Evaluation_realworld_rg.ipynb) to evaluate the results and generate the new resume content in a json format


## Directory Structure

Key Notebooks:
1. **Evaluation_realworld_rg.ipynb**: Evaluate the GPT 4o, original Llama, finetuned Llama model using some real resume and job description data using metrics including job alignment, user alignment, model hallucination and Rouge-Lsum.
2. **Evaluation.ipynb**: Evaluate the GPT 4o, original Llama, finetuned Llama model using evaluation data splited from the generated dataset in output folder with the evaluation results
3. **Llama31_finetune.ipynb**: The process of finetuning the Llama 3.1 8B model including prompt, data prepration and a inference demo


Project Structure:
```
├── Backup_Notebook                      # Scripts for backtesting trained models
├── Resumeflow_source                    # source code for the resumeflow tool to generate resume in pdf
├── data                                 # Data collection, preprocessing and trainig and evaluation data
│   ├── first_600_resumes.txt            # raw resume data
│   ├── data_set                         # raw and processed job description and resume data
│   ├── jd_detail.py                     # Extract key information from the full text of job descritpion
│   ├── jd_scrap.ipybn                   # Scrapping job descriptions
│   |── pdf_extract.py                   # Extract all the content in a pdf in the format of text
│   |── resume_section.py                # Split the full text of resume into different sections
│   |── resume_text.ipynb                # process of data cleaning, preprocssing
│   |── target_resume.py                 # generate resume as target data using GPT 4o and save all results into a json file
│   |── text_process.py                  # split the resume into 6 sections without personal information
│   |── text_to_json.py                  # save the categorized resume content into a json file
│   |── updated_resumes_combined.csv     # resume data with simulated personal information
├── output                               # a folder contains the output data of target_resume.py
├── eval.py                              # Evaluation metrics impelementation
├── section_prompt.py                    # the master and section prompts for training and inferencing
```
<br>

> **Note:** This project is for academic research. Do not use for commercial purposes, including Our Evaluation and Training Data.

<hr>

## Reference

1. [ResumeFlow: An LLM-facilitated Pipeline for Personalized Resume Generation and Refinement](https://github.com/Ztrimus/ResumeFlow)

2. [JobSpy](https://github.com/Bunsly/JobSpy?tab=readme-ov-file#output)

3. [resume_corpus](https://github.com/florex/resume_corpus)

4. [Meta Llama 3.1 8B](https://huggingface.co/meta-llama/Llama-3.1-8B)

5. [OpenAI API](https://platform.openai.com/docs/overview)

6. [Autodl](https://www.autodl.com/)