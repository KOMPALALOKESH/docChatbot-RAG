from llama_index.core import SimpleDirectoryReader
from constants import title, description, examples
from model import query_engine
import gradio as gr
import os
import shutil

# move files to "Data" folder
def move_pdf_files():
    os.makedirs("Data", exist_ok=True)

    pdf_files = [f for f in os.listdir(source_dir) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        src_path = os.path.join("/content", pdf_file)
        dest_path = os.path.join("/content/Data", pdf_file)
        shutil.move(src_path, dest_path)
    return "success"

# generate answers
def generate(input, history):
  response = query_engine.query(input)
  return str(response)

# read directory
documents = SimpleDirectoryReader("/content/Data").load_data()

# gradio UI
with gr.Blocks() as demo:
    # file input
    file_output = gr.File()
    upload_button = gr.UploadButton("Click to Upload a File", file_types=["pdf"], file_count="multiple")
    # chat UI
    with gr.Blocks(): 
        gr.ChatInterface(
            fn=generate,
            title=title,
            description=description,
            examples=examples)

if __name__=="__main__":
    demo.launch(debug=True, share=True)
