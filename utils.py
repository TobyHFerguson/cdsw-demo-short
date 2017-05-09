import os
import time
from IPython.core.display import HTML, display
import subprocess
process = False

def start_tensorboard(logdir="/tmp/tensorboard", iframe=True):
  "Starts tensorboard on public web port for session."  
  cmd = ["python", "/home/cdsw/.local/bin/tensorboard",
    "--logdir=" + logdir, "--port=8080"]
  global process
  if not process:
    process = subprocess.Popen(cmd)
    time.sleep(3)    
  url = "http://{id}.{domain}".format(id=os.environ['CDSW_ENGINE_ID'], domain=os.environ['CDSW_DOMAIN'])
  print "Starting Tensorboard at {url}...".format(url=url)
  if iframe:
    html = """
      <p><a href="{url}">Open Tensorboard</a></p>
      <iframe  width="100%" height=700px" style="border: 0" src="{url}" seamless></iframe>
    """.format(url=url)
  else:
    html = """
      <p><a href="{url}">Open Tensorboard</a></p>
    """.format(url=url)
  display(HTML(html))

def stop_tensorboard():
  "Stop tensorboard"
  global process
  if process: 
    process.terminate()
    print "Tensorboard stopped."
    process = False
  else:
    print "Tensorboard is not running."
