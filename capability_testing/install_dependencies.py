# install all dependencies that can't be satisfied by requirements.txt
# i.e. at least one package requires pip2 instead of pip3
import sys
import subprocess


def install_dependencies():
  print('Installing dependencies. . .')
  p = subprocess.Popen("pip2 install coinbits", shell=True,
      stdout=subprocess.PIPE)
  out, err = p.communicate()
  if out != None:
    print(out)
  if err != None:
    print(err)

  status = p.wait()
  return status


def main():
  rv = install_dependencies()
  if rv != 0:
    print('ERROR: Dependencies not sucessfully installed. Aborting. . .')
    sys.exit(1)


if __name__ == '__main__':
  main()  

