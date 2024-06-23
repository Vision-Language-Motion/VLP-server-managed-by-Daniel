import os
import paramiko
import tempfile
from dotenv import load_dotenv
load_dotenv()

def daily_ssh_task():
    if not os.environ.get('SSH_PRIVATE_KEY'):
        print("No SSH Key found")
        return "No SSH Key found"
    else:
        private_key = os.environ.get('SSH_PRIVATE_KEY')



    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    with tempfile.NamedTemporaryFile(delete=True) as key_file:
        key_file.write(private_key.encode())
        key_file.flush()

    

        key = paramiko.RSAKey.from_private_key_file(key_file.name)
        # ssh.connect('XXXX', username='XXXXXX', pkey=key)

    #stdin, stdout, stderr = ssh.exec_command('path_to_your_script')
    #output = stdout.read()
    ssh.close()
    print("SSH connection closed")
    
    # Optional: log the output or handle it as needed
    # print(output)

if __name__ == '__main__':
    daily_ssh_task()