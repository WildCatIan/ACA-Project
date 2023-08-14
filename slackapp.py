import logging
import os

import string
import requests
from pytz import timezone

from datetime import datetime
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.INFO)
load_dotenv()

SLACK_BOT_TOKEN = os.environ["user_oauth_token"]
SLACK_APP_TOKEN = os.environ["socket_mode_token"]

app = App(token=SLACK_BOT_TOKEN)

# Database of ten companies chosen for program
company_info = {
    "adobe": {
        "address": "345 Park Ave, San Jose, California, USA",
        "timezone": "America/Los_Angeles",
        "weather": None,
        "core_values": "Create the future, Own the outcome, Raise the bar, and Be genuine — represent who we are, how we show up in the world, and how we’ll define our future success.",
        "internship_website": "https://careers.adobe.com/us/en/search-results?qkexperienceLevel=University%20Intern",
        "interview_questions": [
            "What are your short- and long-term goals?",
            "Tell me about some of your recent goals and what you did to achieve them.",
            "Tell me about an idea you implemented; what was the impact?",
            "Tell me about a time you went above and beyond for a customer.",
            "How would a coworker describe you?",
            "Tell me about a time when you needed feedback from a client and they were not responsive?",
            "Why do you want to work for Adobe?",
            "What has been your biggest success or failure?",
            "Describe a challenging problem you faced and how you solved it.",
            "How do you handle working in a team? \n\nFor more information about the hiring process, visit: https://www.adobe.com/careers/interviewing-at-adobe.html",
        ],
        "summary": "Adobe Inc., originally called Adobe Systems Incorporated, is an American multinational computer software company incorporated in Delaware and headquartered in San Jose, California. It has historically specialized in software "+
        "for the creation and publication of a wide range of content, including graphics, photography, illustration, animation, multimedia/video, motion pictures, and print. Its flagship products include Adobe Photoshop image editing software; "+
        "Adobe Illustrator vector-based illustration software; Adobe Acrobat Reader and the Portable Document Format (PDF); and a host of tools primarily for audio-visual content creation, editing and publishing. Adobe offered a bundled solution "+
        "of its products named Adobe Creative Suite, which evolved into a subscription software as a service (SaaS) offering named Adobe Creative Cloud. The company also expanded into digital marketing software and in 2021 was considered one of "+
        "the top global leaders in Customer Experience Management (CXM).",
        "ceo": "Shantanu Narayen",
        "founded": "December 1982",
        "founder": "John Warnock and Charles Geschke",
    },
    "google": {
        "address": "1600 Amphitheatre Pkwy, Mountain View, California, USA",
        "timezone": "America/Los_Angeles",
        "weather": None,
        "core_values": "Focus on the user and all else will follow, It’s best to do one thing really, really well, Fast is better than slow, Democracy on the web works, You can make money without doing evil, There’s always more information out there, "+
        "The need for information crosses all borders, You can be serious without a suit, Great just isn’t good enough.",
        "internship_website": "https://careers.google.com/students/",
        "interview_questions": [
            "What is your favorite Google product, and how would you improve it?",
            "What projects have you worked on that you're most proud of?",
            "How do you handle working in a team?",
            "How do you stay accountable?",
            "Describe a time when you faced a difficult technical challenge and how you resolved it.",
            "Why do you want to join Google?",
            "Tell me about a time when you demonstrated leadership skills.",
            "Tell me about a time when you set and achieved a goal?",
            "What would you want to do if you didn't have to work?",
            "What is Googleyness?",
        ],
        "summary": "Google LLC is an American multinational technology company focusing on artificial intelligence, online advertising, search engine technology, cloud computing, computer software, quantum computing, e-commerce, and consumer "+
        "electronics. It has been referred to as 'the most powerful company in the world' and as one of the world's most valuable brands due to its market dominance, data collection, and technological advantages in the field of artificial "+
        "intelligence. Google's parent company Alphabet Inc. is one of the five Big Tech companies, alongside Amazon, Apple Inc., Meta Platforms, and Microsoft.",
        "ceo": "Sundar Pichai",
        "founded": "September 1998",
        "founder": "Larry Page and Sergey Brin",
    },
    "apple": {
        "address": "1 Apple Park Way, Cupertino, California, USA",
        "timezone": "America/Los_Angeles",
        "weather": None,
        "core_values": "A healthy respect for well-being. Putting the personal in personalization. Keeping it green. And clean. Growing roles into careers. Helping people grow in their own direction.",
        "internship_website": "https://jobs.apple.com/en-us/search?team=Internships-STDNT-INTRN",
        "interview_questions": [
            "Where do you see yourself in five years?",
            "Tell me about a time you completely failed. How did you bounce back from it?",
            "Tell me about a time you disagreed with your manager. How did you handle it? What was the outcome?",
            "How have you dealt with a difficult customer?",
            "Share about a time when you went above and beyond for a customer.",
            "Tell me about a time when you had to work under a tight deadline.",
            "How do you stay motivated during challenging projects?",
            "Describe a situation where you had to solve a complex problem with limited resources.",
            "Why do you want to work at Apple?",
            "What are your favorite Apple products and why?",
        ],
        "summary": "Apple Inc. is an American multinational technology company headquartered in Cupertino, California. Apple is the world's largest technology company by revenue, with US$394.3 billion in 2022 revenue. As of March 2023, Apple "+
        "is the world's biggest company by market capitalization. As of June 2022, Apple is the fourth-largest personal computer vendor by unit sales and the second-largest mobile phone manufacturer in the world. It is considered one of the Big "+
        "Five American information technology companies, alongside Alphabet (parent company of Google), Amazon, Meta Platforms, and Microsoft.",
        "ceo": "Tim Cook",
        "founded": "April 1976",
        "founder": "Steve Jobs, Steve Wozniak, and Ronald Wayne",
    },
    "microsoft": {
        "address": "1 Microsoft Way, Redmond, Washington, USA",
        "timezone": "America/Los_Angeles",
        "weather": None,
        "core_values": "Innovation, Diversity and inclusion, Corporate social responsibility, Trustworthy computing",
        "internship_website": "https://careers.microsoft.com/students/us/en/internship",
        "interview_questions": [
            "What do you think are the 3 qualities to work at Microsoft?",
            "Tell me about a when you took risk at work.",
            "What interests you most about working at Microsoft?",
            "Tell me about a time when you had to work with a difficult team member and how you handled it.",
            "How do you approach solving problems collaboratively?",
            "Why do you want to be part of Microsoft?",
            "Describe a project where you had to learn new technologies quickly.",
            "Do you use Microsoft products or services? If so, which is your favorite, and why?",
            "How do you build and maintain functional relationships with colleagues working in other locations?",
            "What steps do you take to keep your skills current?",
        ],
        "summary": "Microsoft Corporation is an American multinational technology corporation headquartered in Redmond, Washington. Microsoft's best-known software products are the Windows line of operating systems, the Microsoft 365 suite of "+
        "productivity applications, and the Internet Explorer and Edge web browsers. Its flagship hardware products are the Xbox video game consoles and the Microsoft Surface lineup of touchscreen personal computers. Microsoft ranked No. 14 in the "+
        "2022 Fortune 500 rankings of the largest United States corporations by total revenue; it was the world's largest software maker by revenue as of 2022. It is considered one of the Big Five American information technology companies, alongside "+
        "Alphabet (parent company of Google), Amazon, Apple, and Meta Platforms (formerly Facebook, Inc.).",
        "ceo": "Satya Nadella",
        "founded": "April 1975",
        "founder": "Bill Gates and Paul Allen",
    },
    "intel": {
        "address": "2200 Mission College Blvd, Santa Clara, California, USA",
        "timezone": "America/Los_Angeles",
        "weather": None,
        "core_values": "Customer First, Fearless Innovation, Results Driven, Inclusion, Quality, Integrity",
        "internship_website": "https://jobs.intel.com/en/search-jobs",
        "interview_questions": [
            "What skills do you believe are essential for success in a technical role at Intel?",
            "Tell me about a time when you had to adapt to a new technology or programming language quickly.",
            "Describe a project you worked on that required both technical and interpersonal skills.",
            "Why do you want to intern at Intel?",
            "How do you handle working in a fast-paced environment?",
            "Why should we hire you?",
            "Where do you see yourself five years from now?",
            "Who has inspired you in your life and how?",
            "What kind of work environment do you dislike working in?",
            "Do you think honesty is always the best policy? \n\nFor more interview tips, visit https://jobs.intel.com/en/interview-tips",
        ],
        "summary": "Intel Corporation (commonly known as Intel) is an American multinational corporation and technology company headquartered in Santa Clara, California. It is one of the world's largest semiconductor chip manufacturer by revenue, "+
        "and is one of the developers of the x86 series of instruction sets found in most personal computers (PCs). Incorporated in Delaware, Intel ranked No. 45 in the 2020 Fortune 500 list of the largest United States corporations by total "+
        "revenue for nearly a decade, from 2007 to 2016 fiscal years. Intel supplies microprocessors for computer system manufacturers such as Acer, Lenovo, HP, and Dell. Intel also manufactures motherboard chipsets, network interface controllers "+
        "and integrated circuits, flash memory, graphics chips, embedded processors and other devices related to communications and computing.",
        "ceo": "Patrick Gelsinger",
        "founded": "July 1968",
        "founder": "Robert Noyce and Gordon Moore",
    },
    "nvidia": {
        "address": "2788 San Tomas Expressway, Santa Clara, California, USA",
        "timezone": "America/Los_Angeles",
        "weather": None,
        "core_values": "Take risks, learn fast. Seek truth, learn from mistakes, share learnings. Learn, adapt, shape the world. Maintain the highest standards.",
        "internship_website": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?workerSubType=0c40f6bd1d8f10adf6dae42e46d44a17&workerSubType=ab40a98049581037a3ada55b087049b7",
        "interview_questions": [
            "How do you approach solving complex problems?",
            "How do you prioritize tasks in a busy schedule?",
            "What has been the most challenging project you have worked on so far?",
            "Tell me about a time when you had to work on a project with tight deadlines.",
            "How do you handle receiving constructive feedback on your work?",
            "How do you believe you would benefit Nvidia?",
            "What are the three qualities that make you an ideal fit for this position?",
            "What are the most important aspects of enhancing productivity at the workplace?",
            "Describe a situation where you contributed to a successful team project.",
            "What would you do to handle a conflict with a coworker?",
        ],
        "summary": "Nvidia Corporation is an American multinational technology company incorporated in Delaware and based in Santa Clara, California. It is a software and fabless company which designs graphics processing units (GPUs), application "+
        "programming interface (APIs) for data science and high-performance computing as well as system on a chip units (SoCs) for the mobile computing and automotive market. Nvidia is a dominant supplier of artificial intelligence hardware and "+
        "software. Its professional line of GPUs are used in workstations for applications in such fields as architecture, engineering and construction, media and entertainment, automotive, scientific research, and manufacturing design.",
        "ceo": "Jensen Huang",
        "founded": "April 1993",
        "founder": "Jensen Huang, Chris Malachowsky, and Curtis Priem",
    },
    "facebook": {
        "address": "1 Hacker Way, Menlo Park, California, USA",
        "timezone": "America/Los_Angeles",
        "weather": None,
        "core_values": "Focus on impact, Move fast, Live in the future, Build awesome things",
        "internship_website": "https://www.metacareers.com/careerprograms/students/?p[teams][0]=Internship%20-%20Engineering%2C%20Tech%20%26%20Design&p[teams][1]=Internship%20-%20Business&p[teams][2]=Internship%20-%20PhD&p[teams][3]=University%20Grad%20-%20PhD%20%26%20Postdoc&p[teams][4]=University%20Grad%20-%20Engineering%2C%20Tech%20%26%20Design&p[teams][5]=University%20Grad%20-%20Business&teams[0]=Internship%20-%20Engineering%2C%20Tech%20%26%20Design&teams[1]=Internship%20-%20Business#openpositions",
        "interview_questions": [
            "Tell me about a time you made a mistake.",
            "Tell me about a time you dealt with a conflict with others.",
            "Describe a time when your project or a project you helped with failed.",
            "How do you earn the trust of your team members?",
            "What product are you most proud of working on and why?",
            "Tell me about yourself and your background.",
            "Why are you interested in interning at Meta?",
            "How do you handle working in a team?",
            "Describe a time when you demonstrated leadership skills.",
            "What do you think is the biggest challenge facing Meta in the next five years?",
        ],
        "summary": "Meta Platforms, Inc., doing business as Meta, and formerly named Facebook, Inc., and TheFacebook, Inc., is an American multinational technology conglomerate based in Menlo Park, California. The company owns and operates "+
        "Facebook, Instagram, Threads, and WhatsApp, among other products and services. Meta is one of the world's most valuable companies and among the ten largest publicly traded corporations in the United States. It is considered one of the "+
        "Big Five American information technology companies, alongside Google's parent company Alphabet, Amazon, Apple, and Microsoft. In addition to Facebook, Instagram, Threads and WhatsApp, Meta has also acquired Oculus.",
        "ceo": "Mark Zuckerberg",
        "founded": "January 2004",
        "founder": "Mark Zuckerberg, Andrew McCollum, Eduardo Saverin, Chris Hughes, and Dustin Moskovitz",
    },
    "ibm": {
        "address": "1 New Orchard Road, Armonk, New York, USA",
        "timezone": "America/New_York",
        "weather": None,
        "core_values": "Diversity and inclusion, innovation, being yourself, and focusing on change.",
        "internship_website": "https://www.ibm.com/employment/internship/",
        "interview_questions": [
            "Why do you want to work at IBM?",
            "Tell me about a time when you worked on a complex project.",
            "How do you handle change and uncertainty?",
            "Describe your experience working in a diverse team.",
            "What technical skills do you possess that would be valuable at IBM?",
            "Tell me about a time when you solved a problem creatively?",
            "Give me an example of a time you went out of your way for a customer or client?",
            "If a member of your team was not pulling his or her weight, what would you do?",
            "How would you resolve a team conflict? Can you provide some examples of when you’ve done this?",
            "What is one thing IBM has done recently that impressed you?",
        ],
        "summary": "The International Business Machines Corporation (IBM), nicknamed Big Blue, is an American multinational technology corporation headquartered in Armonk, New York and is present in over 175 countries. It specializes in computer "+
        "hardware, middleware, and software, and provides hosting and consulting services in areas ranging from mainframe computers to nanotechnology. IBM is the largest industrial research organization in the world, with 19 research facilities "+
        "across a dozen countries, and has held the record for most annual U.S. patents generated by a business for 29 consecutive years from 1993 to 2021.",
        "ceo": "Arvind Krishna",
        "founded": "June 1911",
        "founder": "Herman Hollerith, Charles Ranlett Flint, and Thomas J. Watson, Sr.",
    },
    "oracle": {
        "address": "2300 Oracle Way, Austin, Texas, USA",
        "timezone": "America/Chicago",
        "weather": None,
        "core_values": "Integrity, customer satisfaction, mutual respect, quality, teamwork, fairness, communication, compliance, innovation, and ethics",
        "internship_website": "https://www.oracle.com/careers/students-grads/internships/",
        "interview_questions": [
            "Why do you want to intern at Oracle?",
            "What are your expectations for this position?",
            "How do your values align with our company values?",
            "Do you prefer to work individually or in a team setting?",
            "Where do you see yourself in five years?",
            "How do you resolve conflicts with fellow employees?",
            "How do you prioritize your work tasks and projects?",
            "How do you handle working on multiple projects simultaneously?",
            "Describe a time when you had to persuade others to adopt your ideas.",
            "What interests you the most about Oracle's products and services?",
        ],
        "summary": "Oracle Corporation is an American multinational computer technology company headquartered in Austin, Texas, United States. In 2020, Oracle was the third-largest software company in the world by revenue and market "+
        "capitalization. The company sells database software and technology (particularly its own brands), cloud engineered systems, and enterprise software products, such as enterprise resource planning (ERP) software, human capital management "+
        "(HCM) software, customer relationship management (CRM) software (also known as customer experience), enterprise performance management (EPM) software, and supply chain management (SCM) software.",
        "ceo": "Safra Catz",
        "founded": "June 1977",
        "founder": "Larry Ellison, Bob Miner, and Ed Oates",
    },
    "tesla": {
        "address": "1 Tesla Rd, Austin, Texas, USA",
        "timezone": "America/Chicago",
        "weather": None,
        "core_values": "Doing the best, taking risks, respect, constant learning, and environmental consciousness.",
        "internship_website": "https://www.tesla.com/careers/search/?type=3&site=US",
        "interview_questions": [
            "Why do you want to intern at Tesla?",
            "Describe a time when you worked on an innovative project.",
            "What makes you passionate about sustainable energy?",
            "How do you deal with tight deadlines and multiple priorities?",
            "Where do you see yourself in the next five years?",
            "What makes you a good fit for this role here at Tesla?",
            "What qualities and traits are needed to work for Tesla?",
            "When have you failed, and how did you learn from it?",
            "Tell us about a time you had to solve a problem with little to no information.",
            "How would you contribute to Tesla's mission to accelerate the world's transition to sustainable energy?",
        ],
        "summary": "Tesla, Inc. is an American multinational automotive and clean energy company headquartered in Austin, Texas. Tesla designs and manufactures electric vehicles (cars and trucks), stationary battery energy storage devices from "+
        "home to grid-scale, solar panels and solar roof tiles, and related products and services. Tesla is one of the world's most valuable companies and, as of 2023, is the world's most valuable automaker. In 2022, the company led the battery "+
        f"electric vehicle market, with 18% share. Its subsidiary Tesla Energy develops and is a major installer of photovoltaic systems in the United States. Tesla Energy is one of the largest global suppliers of battery energy storage systems "+
        "with 6.5 gigawatt-hours (GWh) installed in 2022.",
        "ceo": "Elon Musk",
        "founded": "July 2003",
        "founder": "Martin Eberhard and Marc Tarpenning",
    },
}

def get_weather(city):
    # Replace 'your_weather_api_key' with your actual API key from https://openweathermap.org/api (each key has sixty calls a day)
    weather_api_key = "your_weather_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=imperial"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"{weather_description.capitalize()}. Temperature: {temperature}°F"
    return None

def get_current_time_in_timezone(timezone_str):
    # Get current time at headquarters
    tz = timezone(timezone_str)
    current_time = datetime.now(tz)
    return current_time

def format_datetime(dt):
    # Format date and time as "mm/dd/yyyy HH:MM AM/PM"
    return dt.strftime("%m/%d/%Y %I:%M %p").lstrip("0").replace(" 0", " ").replace("AM", "am").replace("PM", "pm")

@app.event("app_mention")
def mention_handler(body, say, logger):
    # Get the text and split it into words
    request = body["event"]["text"]
    words = request.split()

    # Check if the mention includes the company name
    if len(words) >= 2:
        # Extract the company name (second word) and clean it up
        company_name = strip_request(words[1])
        company_name_lower = company_name.lower()

        # Check if the company exists in the company_info dictionary
        if company_name_lower in company_info:
            company_details = company_info[company_name_lower]
            location = company_details["address"].split(',', 1)[1].strip()
            city = location.split(',')[0].strip()

            # Fetch weather information
            weather_info = get_weather(city)
            if weather_info:
                company_details["weather"] = weather_info

            # Get current time in the company's timezone
            current_time = get_current_time_in_timezone(company_details["timezone"])

            # Format the current time
            current_time_formatted = format_datetime(current_time)

            # Prepare the response with all company information
            response = f"- *Company:* {company_name_lower.capitalize()}\n------------------------\n"
            response += f"- *Headquarters (HQ) Address:* {company_details['address']}\n"
            response += f"- *Current Time at HQ:* {current_time_formatted}\n"
            response += f"- *Current Weather at HQ:* {company_details['weather']}\n"
            response += f"- *Internship Website:* {company_details['internship_website']}\n\n\n"
            response += f"- *Summary:* {company_details['summary']}\n\n\n"
            response += f"- *Core Values:* {company_details['core_values']}\n"
            response += f"- *CEO:* {company_details['ceo']}\n"
            response += f"- *Founded:* {company_details['founded']}\n"
            
            # Add the founder information
            founder = company_details.get("founder")
            if founder:
                response += f"- *Founded by:* {founder}\n"

            # Add the interview questions section
            response += f"\n\n- *Interview Questions:*\n----------------------------\n"
            for i, question in enumerate(company_details['interview_questions'], start=1):
                response += f"{i}. {question}\n"

            # Send the response
            say(response)
        else:
            say(f"Sorry, I don't have information on the company *{company_name.capitalize()}*.")
    else:
        say('''Welcome to *InternBot*! \n\nType @InternBot, then the name of the company you'd like to intern at:\n
1) Adobe
2) Apple
3) Microsoft
4) Google
5) Facebook
6) Tesla
7) Nvidia
8) Intel
9) Oracle
10) IBM
            ''')

def strip_request(request):
    # Remove any punctuation from the request
    request = request.translate(str.maketrans("", "", string.punctuation))
    # Remove any whitespace from the request
    request = request.strip()
    # Make the request lowercase
    request = request.lower()
    # Return the stripped request as a string
    return request

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()