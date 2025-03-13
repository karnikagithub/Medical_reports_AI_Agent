# # main.py
# from agents.medical_agent import create_medical_agent
# from output_parsers.medical_output_parser import parse_medical_report
# import time
# import google.api_core.exceptions
# import base64
# import os

# def invoke_with_retry(agent, input_data, max_retries=3, initial_delay=1):
#     retries = 0
#     delay = initial_delay
#     while retries < max_retries:
#         try:
#             response = agent.invoke(input_data)
#             return response
#         except google.api_core.exceptions.ResourceExhausted as e:
#             if e.code == 429:
#                 print(f"Rate limit exceeded. Retrying in {delay} seconds...")
#                 time.sleep(delay)
#                 delay *= 2
#                 retries += 1
#             else:
#                 raise e
#         raise Exception("Max retries exceeded.")

# def save_pdf(pdf_base64, filename="report.pdf"):
#     """Saves a base64 encoded PDF to a file."""
#     try:
#         pdf_bytes = base64.b64decode(pdf_base64)
#         with open(filename, "wb") as f:
#             f.write(pdf_bytes)
#         print(f"PDF saved as {filename}")
#     except Exception as e:
#         print(f"Error saving PDF: {e}")

# if __name__ == "__main__":
#     agent = create_medical_agent()
#     chat_history = []
#     user_input = "I want a summary on stage 2 lung cancer and a report of the findings."
#     response = invoke_with_retry(agent, {"input": user_input, "chat_history": chat_history})
#     print(response)

#     if 'output' in response:
#         chat_history.append((user_input, response["output"]))

#         # Check if report generation was used
#         if "pdf" in response['output'].lower():
#           try:
#             pdf_data = response['output'].split("base64,")[1] #split the returned string to get the base64 pdf data.
#             save_pdf(pdf_data)

#           except IndexError:
#             print("PDF data not correctly formatted in the response.")

#         try:
#             parsed_report = parse_medical_report(response['output'])
#             print("Parsed Report:", parsed_report)
#         except:
#             print("Could not parse report.")


#     user_input2 = "What are the common treatment options?"
#     response2 = invoke_with_retry(agent, {"input": user_input2, "chat_history": chat_history})
#     print(response2)


# from flask import Flask, render_template, request, jsonify
# from agents.medical_agent import create_medical_agent
# from output_parsers.medical_output_parser import parse_medical_report
# import time
# import google.api_core.exceptions
# import base64
# import os

# app = Flask(__name__)
# agent = create_medical_agent()

# def invoke_with_retry(agent, input_data, max_retries=3, initial_delay=1):
#     retries = 0
#     delay = initial_delay
#     while retries < max_retries:
#         try:
#             response = agent.invoke(input_data)
#             return response
#         except google.api_core.exceptions.ResourceExhausted as e:
#             if e.code == 429:
#                 print(f"Rate limit exceeded. Retrying in {delay} seconds...")
#                 time.sleep(delay)
#                 delay *= 2
#                 retries += 1
#             else:
#                 raise e
#         raise Exception("Max retries exceeded.")

# def save_pdf(pdf_base64, filename="report.pdf"):
#     """Saves a base64 encoded PDF to a file."""
#     try:
#         pdf_bytes = base64.b64decode(pdf_base64)
#         with open(filename, "wb") as f:
#             f.write(pdf_bytes)
#         print(f"PDF saved as {filename}")
#     except Exception as e:
#         print(f"Error saving PDF: {e}")

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         user_input = request.form["user_input"]
#         print(user_input,'----------user_input---------------')
#         chat_history = []
#         response = invoke_with_retry(agent, {"input": user_input, "chat_history": chat_history})
#         print(response,'------------------resppppppppppppppppppp')

#         if 'output' in response:
#             chat_history.append((user_input, response["output"]))

#             # Check if report generation was used
#             if "pdf" in response['output'].lower():
#                 try:
#                     pdf_data = response['output'].split("base64,")[1]
#                     save_pdf(pdf_data)
#                     pdf_link = "/static/report.pdf" # Link to static PDF
#                 except IndexError:
#                     pdf_link = None
#                     print("PDF data not correctly formatted in the response.")
#             else:
#                 pdf_link = None

#             try:
#                 parsed_report = parse_medical_report(response['output'])
#                 return render_template("index.html", response=response["output"], pdf_link=pdf_link, parsed_report=parsed_report)
#             except:
#                 return render_template("index.html", response=response["output"], pdf_link=pdf_link)

#         return render_template("index.html", response=response["output"])

#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)


# app.py
from flask import Flask, render_template, request, jsonify
from agents.medical_agent import create_medical_agent
import time
import google.api_core.exceptions
import base64
import os
import re  # Import the regular expression module

app = Flask(__name__)
agent = create_medical_agent()

def invoke_with_retry(agent, input_data, max_retries=3, initial_delay=1):
    retries = 0
    delay = initial_delay
    while retries < max_retries:
        try:
            response = agent.invoke(input_data)
            return response
        except google.api_core.exceptions.ResourceExhausted as e:
            if e.code == 429:
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
                retries += 1
            else:
                raise e
        raise Exception("Max retries exceeded.")

def sanitize_filename(filename):
    """Sanitizes a filename by removing or replacing invalid characters."""
    return re.sub(r'[^\w\-. ]', '_', filename).replace(" ", "_") #removes invalid characters.

# def save_pdf(pdf_base64, filename):
#     """Saves a base64 encoded PDF to a file."""
#     try:
#         pdf_bytes = base64.b64decode(pdf_base64)
#         with open(f"D:\\med_doc_AI\\medical_report_generator\\reports\\{filename}", "wb") as f:
#             f.write(pdf_bytes)
#         print(f"PDF saved as D:\\med_doc_AI\\medical_report_generator\\reports\\{filename}")
#     except Exception as e:
#         print(f"Error saving PDF: {e}")


def save_pdf(pdf_base64, filename):
    """Saves a base64 encoded PDF to a file, with validation and padding correction."""
    try:
        # Calculate padding
        missing_padding = len(pdf_base64) % 4
        if missing_padding:
            pdf_base64 += '=' * (4 - missing_padding)

        print(f"Base64 data: {pdf_base64[:100]}...")

        # Validate base64 length
        if len(pdf_base64) % 4 != 0:
            print(f"Error: Invalid base64 length: {len(pdf_base64)}")
            return  # Exit if invalid
        pdf_bytes = base64.b64decode(pdf_base64)

        print(f"Decoded PDF bytes: {pdf_bytes[:100]}...")

        pdf_bytes = base64.b64decode(pdf_base64)
        with open(f"D:\\med_doc_AI\\medical_report_generator\\reports\\{filename}", "wb") as f:
            f.write(pdf_bytes)
        print(f"PDF saved as D:\\med_doc_AI\\medical_report_generator\\reports\\{filename}")
    except Exception as e:
        print(f"Error saving PDF: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    pdf_link = None  # Initialize pdf_link outside the POST block

    if request.method == "POST":
        user_input = request.form["user_input"]
        sanitized_input = sanitize_filename(user_input) #sanitize the user input.~
        pdf_filename = f"{sanitized_input}.pdf" #create the pdf filename.
        chat_history = []
        response = invoke_with_retry(agent, {"input": user_input, "chat_history": chat_history})
        print(sanitized_input)
        print(response,'----------------ds sdvsdvsdv-----------')
        if 'output' in response:
            chat_history.append((user_input, response["output"]))
            print('======IM HEREEEEEEEEEEEEEEEEEEEEEE')

            # Check if report generation was used
            # if "pdf" in response['output'].lower():
            try:
                pdf_data = response['output']
                save_pdf(pdf_data, pdf_filename)
                pdf_link = f"{pdf_filename}" # Link to static PDF
            except Exception as e:
                pdf_link = None
                print(f"PDF data not correctly formatted in the response.{e}")
        print(pdf_link,'=============casascsacasc[=============]')
    return render_template("index.html", pdf_link=pdf_link)


if __name__ == "__main__":
    app.run(debug=True)