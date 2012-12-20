import os
import subprocess as sp

from os.path import exists, join
from shutil import rmtree
from tempfile import mkdtemp

base = mkdtemp()
myenv = join(base, "env")

cmds = [
    (
        "conda info", 
        "info-1"
    ),
    (
        "conda list ^m.*lib$",
        "list-1"
    ),
    (
        "conda search ^m.*lib$",
        "search-1"
    ),
    (
        "conda depends numpy",
        "depends-1"
    ),
    (
        "conda info -e",
        "envs-1"
    ),
    (
        "conda create --yes -p %s sqlite" % myenv,
        "create-1"
    ),
    (
        "conda install --yes -p %s pandas=0.8.1" % myenv,
        "install-1"
    ),
    (
        "conda update --yes -p %s pandas" % myenv,
        "update-1"
    ),
    (
        "conda env --yes -ap %s numba-0.3.1-np17py27_0" % myenv,
        "activate-1"
    ),
    (
        "conda env --yes -dp %s sqlite-3.7.13-0" % myenv,
        "deactivate-1"
    ),
    (
        "conda local --yes -r zeromq-2.2.0-0",
        "remove-1"
    ),
    (
        "conda local --yes -d zeromq-2.2.0-0",
        "download-1"
    )
]

def tester(commands):
    cmds = commands
    fails = []
    for i in cmds:
        cmd = i[0]
        out = i[1]
        print "-"*120
        print "%s" % cmd 
        print "-"*120
        try:
            child = sp.Popen(cmd.split(), stdout=sp.PIPE, stderr=sp.PIPE)
            data, err = child.communicate()
            ret = child.returncode
            if ret != 0:
                print "\nFAILED\n"
                f.write("\n%s\n \n%s" % (cmd, err))
                fails.append(cmd)
            else:
                print "\nPASSED\n"
        except Exception as e:
            print e
            f.write("\nThe script had the following error running %s: %s" % (cmd, e))

    return fails


if __name__ == '__main__':
    TESTLOG="conda-testlog.txt"
    if exists(TESTLOG):
        os.remove(TESTLOG)
    f = open(TESTLOG, "w")
    fails = tester(cmds)
    f.close()
    if fails:
        print "These commands failed: \n"
        for line, fail in enumerate(fails, 1):
            print "%d: %s\n" % (line, fail)
        print "Writing failed commands to conda-testlog.txt"

    try:
        rmtree(myenv)
    except:
        pass