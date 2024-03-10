from llama_index.core import VectorStoreIndex, ServiceContext, SimpleDirectoryReader
from constants import title, description, examples
from model import service_context
import gradio as gr
import os
import shutil

# move files to "Data" folder
def move_pdf_files(files_paths):
    if os.path.exists('/content/assignment/Data/'):
        shutil.rmtree('/content/assignment/Data/')
      
    os.makedirs("Data", exist_ok=True)
    dst = "/content/assignment/Data/"

    for src in files_paths:
        shutil.copy2(src, dst)
    return "successfully loaded files."

flag = False
query_engine = None
# generate answers
def generate(input, history):
    global flag
    global query_engine
    if flag==False:
        # read directory
        documents = SimpleDirectoryReader("/content/assignment/Data").load_data()
        # indexing
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        # query engine
        query_engine = index.as_query_engine()
        # set flag=True
        flag=True
    # else:   
    response = query_engine.query(input)
    return str(response)

file_paths = None
def upload_file(files):
    global file_paths
    file_paths = [file.name for file in files]
    move_pdf_files(file_paths)
    return file_paths

# gradio UI
with gr.Blocks() as demo:
    # file input
    file_output = gr.File()
    upload_button = gr.UploadButton("Click to Upload a File", file_types=["pdf"], file_count="multiple")
    upload_button.upload(upload_file, upload_button, file_output)
    
    # chat UI
    with gr.Blocks(): 
        gr.ChatInterface(
            fn=generate,
            title=title,
            description=description,
            examples=examples)

if __name__=="__main__":    
    demo.launch(debug=True, share=True)
