# ResumePersonalization

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

## Introduction

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

We train the model with 4 epochs and a learning rate of 2e-4

## Evaluation

## Future Work

# Project

## Installation


## Directory Structure

Key Notebooks:

Project Structure:
```
├── backtesting                          # Scripts for backtesting trained models
├── data                                 # Various datasets used in the project
│   ├── nexis_news_data_cleaned          # Cleaned news data from Nexis
│   ├── price_history                    # Historical price data for stocks
│   ├── sentiments                       # Sentiment data for stocks
│   └── technical_indicators             # Technical indicators for stocks

```
<br>

> **Note:** This project is for academic research. Do not use for commercial purposes, including Our Evaluation and Training Data.

<hr>

## Reference
