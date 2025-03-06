import json
import unicodedata
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm


def process_post(raw_file_path, process_file_path="data/processed_posts.json"):
    enriched_posts = []

    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)

        for post in posts:
            clean_text = sanitize_text(post['text']) 
            metadata = extract_metadata(clean_text)
            post_with_metadata = {**post, **metadata}  
            enriched_posts.append(post_with_metadata)

    cleaned_posts = json.dumps(enriched_posts, ensure_ascii=False, indent=4)
    cleaned_posts = cleaned_posts.encode("utf-8", "ignore").decode("utf-8") 

    with open(process_file_path, "w", encoding="utf-8") as file:
        file.write(cleaned_posts)

    print(f"Processed {len(enriched_posts)} posts. Data saved to {process_file_path}")
    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(process_file_path,encoding='utf-8',mode = 'w') as file:
        json.dump(enriched_posts,file, indent=4)




def get_unified_tags(enriched_posts):
    unique_tags = set()
    for post in enriched_posts:
        unique_tags.update(post['tags'])

    unique_tags_list = ', '.join(unique_tags)

    
    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
    Here is the list of tags: 
    {tags}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    try:
        response = chain.invoke(unique_tags_list) 
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except Exception as e:
        print(f"Error unifying tags: {e}")
        res = {}
    
    return res










def sanitize_text(text):
    """Normalize text and remove surrogate characters (e.g., emojis causing encoding errors)."""
    if not isinstance(text, str):
        return ""  
    return text.encode("utf-8", "ignore").decode("utf-8") 


def extract_metadata(text):
    """Extract metadata from a LinkedIn post using an LLM."""
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post, and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language, and tags. 
    3. tags is an array of text tags. Extract a maximum of two tags.
    4. Language should be English or Hinglish (Hinglish means Hindi + English).
    
    Here is the actual post on which you need to perform this task:  
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm 
    try:
        response = chain.invoke(text) 
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        res = {"line_count": 0, "language": "Unknown", "tags": []}  

    return res


if __name__ == "__main__":
    process_post("data/raw_posts.json", "data/processed_posts.json")
    # print(enric)

