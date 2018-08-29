"""Doc."""
import time
import subprocess

p = subprocess.Popen([". ./runjob.sh"], shell=True)
# time.sleep(10)
# p.terminate()
# for i in range(10):
while p.returncode is None:
    p.poll()
    print(p.pid, p.returncode)
    time.sleep(1)
