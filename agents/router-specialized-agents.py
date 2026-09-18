
import ollama
import json

MODEL = "llama3.2"

def router(request):
    prompt = f"""
Choose one route:
coding
general
career

Return JSON:
{{"route":"..."}}

Request:
{request}
"""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        format="json"
    )

    return json.loads(
        response["message"]["content"]
    )["route"]

def coding_agent(request):
    return ollama.chat(
        model=MODEL,
        messages=[
            {
                "role":"system",
                "content":"You are an expert programming assistant."
            },
            {
                "role":"user",
                "content":request
            }
        ]
    )["message"]["content"]

def career_agent(request):
    return ollama.chat(
        model=MODEL,
        messages=[
            {
                "role":"system",
                "content":"You are a career guidance assistant."
            },
            {
                "role":"user",
                "content":request
            }
        ]
    )["message"]["content"]

def general_agent(request):
    return ollama.chat(
        model=MODEL,
        messages=[
            {
                "role":"user",
                "content":request
            }
        ]
    )["message"]["content"]

request = input("YOU: ")
route = router(request=request)
print("SELECTED route: ",route)

if route == "coding":
    res = coding_agent(request=request)
elif route == "career":
    res = career_agent(request=request)    
else:
    res = general_agent(request=request)

print("\nAgent:",res)

# SELECTED route:  coding

# Agent: What do you need help with? Do you have a specific coding problem, language, or project you'd like to work on? I can assist with:

# * Syntax and semantics
# * Debugging
# * Algorithm design
# * Data structures
# * Object-Oriented Programming (OOP)
# * Functional Programming
# * Web development
# * Mobile app development
# * Machine learning and AI
# * And more!

# Let me know what's on your mind, and I'll do my best to help. What's your programming background? Are you a beginner, intermediate, or advanced programmer?
# YOU: career
# SELECTED route:  career

# Agent: A career is a long-term series of work experiences and activities that provide a person with a sense of purpose, fulfillment, and financial stability. It's a journey of self-discovery, skill development, and personal growth.

# Here are some key aspects of a career:

# 1. **Occupation**: A specific job or profession that an individual performs.
# 2. **Major**: A broader field or industry that an individual is interested in.
# 3. **Career path**: A sequence of jobs or experiences that lead to a specific occupation or industry.
# 4. **Career goals**: An individual's aspirations and objectives for their career, such as promotions, job changes, or entrepreneurship.
# 5. **Career development**: The process of acquiring new skills, knowledge, and experiences to advance in one's career.

# Some common career types include:

# 1. **Entry-level careers**: Freshly minted degrees or recent graduates may be starting out in their careers.
# 2. **Mid-career careers**: Established professionals with several years of experience may be seeking new challenges or promotions.
# 3. **Senior careers**: Experienced professionals who have reached a high level of expertise and may be in leadership positions.
# 4. **Entrepreneurial careers**: Individuals who start and run their own businesses.

# To choose a career, consider the following:

# 1. **Interests**: What activities do you enjoy doing in your free time?
# 2. **Values**: What matters most to you in a career, such as work-life balance, creativity, or making a difference?
# 3. **Skills**: What are your strengths and talents?
# 4. **Personality**: What type of work environment and culture do you thrive in?
# 5. **Job market**: What are the current job market trends and requirements?

# If you're unsure about your career path, here are some resources to help:

# 1. **Career assessments**: Online tools and tests that help identify your interests, skills, and personality traits.
# 2. **Career counseling**: One-on-one guidance from a professional to explore your career options.
# 3. **Job search platforms**: Websites and apps that connect job seekers with potential employers.
# 4. **Networking**: Attending industry events, joining professional organizations, and connecting with people in your desired field.

# What's your current career situation? Are you looking to switch careers or advance in your current field?
