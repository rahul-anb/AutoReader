from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_task():
    llm = OpenAI(temperature=0.6)
    
    prompt = """you are a Task list creation aiding tool who will take in a input detail and give out an output in a specific format to aid in generating tasks and subtask for a project.
    Generated tasks should be very project specific and include specialized tasks in them.
    Create only 4 to 6 main headings unless specifically asked to.
    Create a task list for inventory management system. Let numbering for main headings be numbers and numbering for subheadings be alphabets."""
    name = llm(prompt)
    
    return name

if __name__ == "__main__":
    text_generated= generate_task()
    print(text_generated)
    text_file = open("data.txt", "w")
    text_file.write(text_generated)
    text_file.close()