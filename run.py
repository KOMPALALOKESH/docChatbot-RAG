from llama_index.core import SimpleDirectoryReader
import os
import shutil

# move files to "Data" folder
def move_pdf_files(source_dir, destination_dir):
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

documents = SimpleDirectoryReader("/content/Data").load_data()
