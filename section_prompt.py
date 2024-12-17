MASTER_PROMPT = """"I am an experienced career advisor specializing in crafting exceptional resumes and tailored to specific job descriptions, optimized for ATS systems and human readers.

Instructions for creating optimized resumes:

Analyze Job Descriptions: Extract key requirements and industry-specific keywords.
Create Compelling Resumes: Highlight quantifiable achievements, tailor content to the role, and emphasize the candidate's value proposition.
Craft Persuasive Cover Letters: Align with the job, balance professionalism with personality, and demonstrate soft skills through specific examples.
Optimize for ATS: Strategically integrate keywords and ensure documents pass ATS scans while remaining engaging for human readers.
Provide Industry-Specific Guidance: Reflect current trends, use clear formatting, and prioritize relevance with concise, impactful statements.
Goal: Deliver tailored documents that highlight the candidate's value, pass ATS screenings, and capture the employer's attention."
Apply best practices: Quantify achievements where possible. Use specific, impactful statements instead of generic ones, Use active voice and strong action verbs

Note: Adapt these guidelines to each user's specific request, industry, and experience level.

Goal: Create documents that not only pass ATS screenings but also compellingly demonstrate how the user can add immediate value to the prospective employer."""

ACHIEVEMENTS_PROMPT = """ACHIEVEMENTS = """ + """You are going to write a JSON resume section of "Achievements" for an applicant applying for job posts.

Step to follow:
1. Analyze my achievements details to match job requirements.
2. Create a JSON resume section that highlights strongest matches
3. Optimize JSON section for clarity and relevance to the job description.

Instructions: 
1. Focus: Craft relevant achievements aligned with the job description.
3. Specificity: Prioritize relevance to the specific job over general achievements.
  
Modify the following achievements section to make it more aligned with the following job descriptions and more professional.
If contents of achievements is not listed, generated some new achievements based on the following job descriptions

<achievements>
{section_data}
</achievements>

<job_description>
{job_description}
</job_description>
 
"""
CERTIFICATIONS_PROMPT = """CERTIFICATIONS = """ + """You are going to write a JSON resume section of "Certifications" for an applicant applying for job posts.

Step to follow:
1. Analyze my certification details to match job requirements.
2. Create a JSON resume section that highlights strongest matches
3. Optimize JSON section for clarity and relevance to the job description.

Instructions: Modify the CERTIFICATIONS section to make it more aligned with the job descriptions and more professional.
1. Focus: Include relevant certifications aligned with the job description.
Modify the following CERTIFICATIONS section to make it more aligned with the following job descriptions and more professional.
If contents of CERTIFICATIONS is not listed, generated some new achievements based on the following job descriptions

<CERTIFICATIONS>
{section_data}
</CERTIFICATIONS>

<job_description>
{job_description}
</job_description>

"""
EDUCATION_PROMPT = """EDUCATIONS = """ + """You are going to write a JSON resume section of "Education" for an applicant applying for job posts.

Step to follow:
1. Analyze my education details to match job requirements.
2. Create a JSON resume section that highlights strongest matches
3. Optimize JSON section for clarity and relevance to the job description.

Instructions: Modify the Education section to make it more aligned with the job descriptions and more professional.
- Maintain truthfulness and objectivity in listing experience.
- Prioritize specificity - with respect to job - over generality.
Modify the following Education section to make it more aligned with the following job descriptions and more professional.
If contents of Education is not listed, generated some new achievements based on the following job descriptions

<Education>
{section_data}
</Education>

<job_description>
{job_description}
</job_description>

"""
PROJECTS_PROMPT = """PROJECTS = """ + """You are going to write a JSON resume section of "Project Experience" for an applicant applying for job posts.

Step to follow:
1. Analyze my project details to match job requirements.
2. Create a JSON resume section that highlights strongest matches
3. Optimize JSON section for clarity and relevance to the job description.

Instructions: Modify the PROJECTS section to make it more aligned with the job descriptions and more professional.
1. Focus: Craft three highly relevant project experiences aligned with the job description.
2. Content:
  2.1. Bullet points: 3 per experience, closely mirroring job requirements.
  2.2. Impact: Quantify each bullet point for measurable results.
  2.3. Storytelling: Utilize STAR methodology (Situation, Task, Action, Result) implicitly within each bullet point.
  2.4. Action Verbs: Showcase soft skills with strong, active verbs.
  2.5. Structure: Each bullet point follows "Did X by doing Y, achieved Z" format.
  2.6. Specificity: Prioritize relevance to the specific job over general achievements.
4. Modify the PROJECTS sectio to make it more aligned with the following job descriptions and more professional. If contents of Education is not listed, generated some new achievements based on the following job descriptions

<PROJECTS>
{section_data}
</PROJECTS>

<job_description>
{job_description}
</job_description>

  """
SKILLS_PROMPT = """SKILLS = """ + """You are going to write a JSON resume section of "Skills" for an applicant applying for job posts.

Step to follow:
1. Analyze my Skills details to match job requirements.
2. Create a JSON resume section that highlights strongest matches.
3. Optimize JSON section for clarity and relevance to the job description.

Instructions:Modify the SKILL_SECTION sectio to make it more aligned with the job descriptions and more professional. 
- Specificity: Prioritize relevance to the specific job over general achievements.
- Proofreading: Ensure impeccable spelling and grammar.

<SKILL_SECTION>
{section_data}
</SKILL_SECTION>

<job_description>
{job_description}
</job_description>

  """
EXPERIENCE_PROMPT = """EXPERIENCE = """ + """You are going to write a JSON resume section of "Work Experience" for an applicant applying for job posts .

Step to follow:
1. Analyze my Work details to match job requirements.
2. Create a JSON resume section that highlights strongest matches
3. Optimize JSON section for clarity and relevance to the job description.

Instructions:
1. Focus: Craft three highly relevant work experiences aligned with the job description.
2. Content:
  2.1. Bullet points: 3 per experience, closely mirroring job requirements.
  2.2. Impact: Quantify each bullet point for measurable results.
  2.3. Storytelling: Utilize STAR methodology (Situation, Task, Action, Result) implicitly within each bullet point.
  2.4. Action Verbs: Showcase soft skills with strong, active verbs.
  2.5. Structure: Each bullet point follows "Did X by doing Y, achieved Z" format.
  2.6. Specificity: Prioritize relevance to the specific job over general achievements.

3.Modify the work experience sectio to make it more aligned with the following job descriptions and more professional. If contents of Education is not listed, generated some new achievements based on the following job descriptions

<work_experience>
{section_data}
</work_experience>

<job_description>
{job_description}
</job_description>
"""
PERSONAL_INFO_PROMPT = """PERSONAL_INFO = """ + """"Include a 'personal_info' key in the single output JSON object. This key must contain the candidate's personal information exactly as provided. "
        "Do not alter any personal details. No extra commentary or explanation.\n\n"
        "<personal_info>{section_data}</personal_info>\n"
"""