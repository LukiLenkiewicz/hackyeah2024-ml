TEMPLATE = """
 I have a list of tuples containing information about subsites of some website in
 format (subsite_url, description, link_title) and a question given by user
 "{question}". Sort these subsites by 
 relevance to user question:
 {content}

 Return ONLY the list of subsites SORTED BY RELEVANCE TO THE USER QUESTION.
 Return output in JSON format. Don't write any additional text or comments. 
 Don't explain your responing. Don't define any additional structures.
"""
