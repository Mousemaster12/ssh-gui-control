import paramiko
import threading
import sys
# necessary inputs for ssh
domain = input("Input server IP: \n")
serveruser = input("Input Server User: \n")
passwd = input("Input password: \n")
port = input("Enter port:\n")

ssh_client = paramiko.SSHClient()

# ssh connection function
def connection():
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=domain, username=serveruser, password=passwd, port=int(port))
    print(f"Connected to {serveruser}@{domain}")

# static shell emulator function
def commands():
    command = ""
    while command != "stop":
        command = input("Enter a command to run:\n ")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        cmd_output = (stdout.read() + stderr.read()).decode('utf-8')
        cmd_output = cmd_output.replace('"', '').replace('\\n', '\n').rstrip('\n')
        print(cmd_output)


connection()



#commands
def echotest():
    stdin, stdout, stderr = ssh_client.exec_command("echo hi")
    cmd_output = (stdout.read() + stderr.read()).decode('utf-8')
    cmd_output = cmd_output.replace('"', '').replace('\\n', '\n').rstrip('\n')
    print(cmd_output)

#File Transfer
ssh_client.open_sftp()
sftp = ssh_client.open_sftp()
def sftp():
    remotepath = r"C:\Users\VMtest\Desktop"
    sftp.put(f"~/Documents/testfile.txt",{remotepath})


#GUI
import dearpygui.dearpygui as dpg
def gui():
    dpg.create_context()
    dpg.create_viewport(title='SSH Command Center', width=1920, height=1080)

    import TabOpener
    with dpg.window(label="Control center"):
        dpg.add_text("Python scripts") 
        dpg.add_text(f"Connected to {serveruser}@{domain}")
        dpg.add_button(label="command one", callback = echotest)
        dpg.add_button(label="OpenerTab", callback = TabOpener)
        dpg.add_button(label='File Transfer', callback = sftp)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

guithread = threading.Thread(target=gui)
commandthread = threading.Thread(target=commands)
commandthread.start()
guithread.start()