import jenkins
from tkinter import messagebox
import webbrowser
from models.config import Config

def printf(txt:str, status:bool):
    if status:
        print(txt)

def glength(group_channels:str) -> int:
    counter = 0
    for line in group_channels:
        try:
            n = int(line)
        except Exception:
            counter += 1
    return counter

def autoPopulateJenkins(content, config:Config):
    
    J_SERVER = jenkins.Jenkins(config.jenkins_url, config.user, config.psw)    
    try:
       b = bool(J_SERVER.job_exists(config.jenkis_job))        
    except Exception as e:
        printf("$ AUTH ERROR IN JENKINS $", config.logs)
        messagebox.showerror(message="Auth error 🥺, check your user configs at configs/config.json", title="Jenkins Auth")
        return

    printf("$ Connected to Jenkins. 👍", config.logs)

    for j, group in enumerate(content):        
        _parameters = config.build_parameters(group)
        if config.run:
            J_SERVER.build_job(config.jenkins_job, _parameters, token=config._TOKEN)
        printf(group, config.logs)
        printf(f"--> Build {j} load. ", config.logs)
    
    messagebox.showinfo(message=f"We sent {config.mod*(len(content)-1)+glength(content[-1])} contents in \
                                 {len(content)} builds 😀 You'll be redirected to Jenkins to see the progress...⏳")    
    webbrowser.open(config.get_jenkins_job_url())

def str_group_content(ls) -> str:
    ## Given a group of ids it returns them with propper Jenkins arg format (str)
    out = ""
    for ch in ls:
        out += str(ch) + "\n"
    return out

def split_content(content, mod) -> list:
    ### It returns the list of group ids splitted according to mod selected
    str_content = []    
    start_point = 0
    min_groups = (len(content) // mod) 
    
    for i in range (min_groups):
        group_i = content[start_point:(i+1)*mod]
        str_content.append(str_group_content(group_i))
        start_point += mod
    
    final_group = content[min_groups*mod:] 
    if len(final_group) != 0:
        str_content.append(str_group_content(final_group))

    return str_content