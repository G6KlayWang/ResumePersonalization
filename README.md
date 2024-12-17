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

## Target Data Generation
As finetuning the model is similar with supervised learning in our case, we need a improved version of the resume for the model to learn. As it is challenging to get two versions of a resume for the same person, we decided to use GPT 4o model to generated a polished version of the resume as the target data in the finetune. 

## Prompt Engineering
We prepared two sets of prompts
1. Master prompt, 

## Model Finetuning

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
