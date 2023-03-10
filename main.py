# @ssebas.andres | 10-03-2023 
# [ query ] -> [ elastic ] -> [ ids ] -> jenkins [ ids ]

from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import ast
from scripts.es_helper import search_content
from scripts.jenkins_helper import split_content, autoPopulateJenkins
from models.config import Config

## Load the query
with open('configs/es-query.json', 'r') as myfile:
    data=myfile.read()
QUERY = ast.literal_eval(data)

## Load configs
with open('configs/config.json', 'r') as myfile:
    data=myfile.read()
configs_json = ast.literal_eval(data)
config = Config(configs_json)

## Read Elasticsearch content
try:
    CONTENT = search_content(config.host, QUERY)  
    GROUP_CONTENT = split_content(CONTENT, config.mod)   

    ## BUILD GUI APP 
    root = Tk()  
    root.title("🤖 Elastic-to-Jenkins")

    HEIGHT = 180
    root.geometry(f"300x{HEIGHT}")  # width x height
    root.iconphoto(False, PhotoImage(file='assets/icono.png'))

    text = Label(root, text="\nAuto", font=('Arial', 20))
    text.pack()

    jenkins_func_aux = partial(autoPopulateJenkins, GROUP_CONTENT, config)
    jenkins_button = Button(root, text="Build in Jenkins", command=jenkins_func_aux, padx=10, pady=10, bg="black", fg="white")
    jenkins_button.pack()

    if len(GROUP_CONTENT) == 0:
        messagebox.showerror(title="Error connecting with Elasticsearch", message="Check the query! No content has been returned")    
    else:
        print("content_received: ", CONTENT)
        n_builds = len(CONTENT) // config.mod
        if len(CONTENT) % config.mod != 0: 
            n_builds += 1
        print()
        print(f"* We received {len(CONTENT)} contents, they are split in {n_builds} jenkins builds.")

    root.mainloop()

except Exception:
    messagebox.showerror(title="Signal Error", message="There was a problem reading elastic-search content, check if you need any vpn!") 