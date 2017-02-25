import os
import time
from IPython.core.display import HTML, display
import subprocess
process = False

def start_tensorboard(logdir, iframe=True):
  "Starts tensorboard on public web port for session."  
  cmd = ["/opt/conda/bin/python", "/home/sense/.local/bin/tensorboard",
    "--logdir=" + logdir, "--port=8080"]
  global process
  if not process:
    process = subprocess.Popen(cmd)
    time.sleep(3)    
  url = "http://{id}.consoles.{domain}".format(id=os.environ['SENSE_DASHBOARD_ID'], domain=os.environ['SENSE_DOMAIN'])
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