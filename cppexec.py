#! /usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (c) 2013, Sebastian Bartos <sebastian.bartos@gmail.com>
#           Terms of the general public license (GPL) version 2 or later apply.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import sys
import tempfile
import subprocess

from PySide.QtCore    import *
from PySide.QtGui     import *
from PySide.QtUiTools import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TARGET_C99      = '-std=c99'
TARGET_CPP98    = '-std=c++98'
OPT_WALL        = '-Wall'

class Control:

    def __init__(self, wmain, initargs):

        self.wmain = wmain

        shortcut = QShortcut('Ctrl+w', wmain)
        shortcut.activated.connect(wmain.close)

        if initargs.target_c99:
            wmain.c99.setChecked(True)
        if initargs.target_cpp98:
            wmain.cpp98.setChecked(True)
        if initargs.opt_wall:
            wmain.opt_wall.setChecked(True)
        if initargs.opt_debug:
            wmain.opt_g.setChecked(True)
        if initargs.opt_optimize:
            wmain.opt_o2.setChecked(True)

        wmain.btn_compile_run.clicked.connect(self.compile_run)

        wmain.show()

    def compile_run(self):

        cmd = ['/usr/bin/gcc']
        wmain = self.wmain
        if wmain.c99.isChecked():
            cmd.append(TARGET_C99)
        if wmain.cpp98.isChecked():
            cmd.append(TARGET_CPP98)
        if wmain.opt_wall.isChecked():
            cmd.append(OPT_WALL)

        if wmain.line_include_path.text():
            cmd.append('-i')
            cmd.append(wmain.line_include_path.text())
        if wmain.line_library_path.text():
            cmd.append('-L')
            cmd.append(wmain.line_library_path.text())
        if wmain.line_library.text():
            cmd.append('-l')
            cmd.append(wmain.line_library.text())

        wmain.line_compile_exit.clear()
        wmain.txt_compile_output.clear()
        wmain.line_run_exit.clear()
        wmain.txt_run_output.clear()

        with tempfile.TemporaryDirectory() as tmpdirname:

            #### compile code ####

            sourcefilepath = os.path.join(tmpdirname, 'code.c')
            cmd.append(sourcefilepath)
            oldpath = os.getcwd()
            os.chdir(tmpdirname)

            with open(sourcefilepath, 'w') as f:
                f.write(wmain.txt_input.toPlainText())

            proc = subprocess.Popen(
                cmd,
                cwd=tmpdirname,
                shell=False,
                close_fds=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
                )

            while proc.poll() is None:

                lines = proc.stdout.readlines()
                proc.stdout.flush()
                if lines:
                    txt = wmain.txt_compile_output.toHtml()
                    for line in lines:
                        txt += line.decode('utf-8') + '<br>'
                    wmain.txt_compile_output.clear()
                    wmain.txt_compile_output.setHtml(txt)

                lines = proc.stderr.readlines()
                proc.stderr.flush()
                if lines:
                    txt = wmain.txt_compile_output.toHtml()
                    for line in lines:
                        txt += '<span style="color:red">{}</span>'.format(line.decode('utf-8')) + '<br>'
                    wmain.txt_compile_output.clear()
                    wmain.txt_compile_output.append(txt)

            ret = proc.wait()
            wmain.line_compile_exit.setText(str(ret))

            if ret == 0:

                #### run executable ####

                cmd = os.path.join(tmpdirname, 'a.out')
                proc = subprocess.Popen(
                    cmd,
                    cwd=tmpdirname,
                    shell=False,
                    close_fds=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                    )

                while proc.poll() is None:

                    lines = proc.stdout.readlines()
                    proc.stdout.flush()
                    if lines:
                        txt = wmain.txt_run_output.toHtml()
                        for line in lines:
                            txt += line.decode('utf-8') + '<br>'
                        wmain.txt_run_output.clear()
                        wmain.txt_run_output.setHtml(txt)

                    lines = proc.stderr.readlines()
                    proc.stderr.flush()
                    if lines:
                        txt = wmain.txt_run_output.toHtml()
                        for line in lines:
                            txt += '<span style="color:red">{}</span>'.format(line.decode('utf-8')) + '<br>'
                        wmain.txt_run_output.clear()
                        wmain.txt_run_output.append(txt)

                ret = proc.wait()
                wmain.line_run_exit.setText(str(ret))

            os.chdir(oldpath)

    def fromclipboard(self):

        proc = subprocess.Popen(['/usr/bin/xsel', '--clipboard'],
                             shell = False, stdout = subprocess.PIPE)

        while proc.poll() is None:

            lines = proc.stdout.readlines()
            proc.stdout.flush()
            if lines:
                for line in lines:
                    txt = line.decode('utf-8')
                    if txt[-1] == '\n':
                        txt = txt[:-1]
                    wmain.txt_input.appendPlainText(txt)

        proc.wait()

        self.compile_run()
        wmain.showMaximized()

if __name__ == '__main__':

    class initargs:
        target_c99   = False
        target_cpp98 = False
        opt_wall     = False
        opt_debug    = False
        opt_optimize = False

    if '-std=c++98' in sys.argv:
        initargs.target_cpp98 = True
    else:
        initargs.target_c99   = True

    if '-Wall' in sys.argv:
        initargs.opt_wall     = True

    app = QApplication(sys.argv)

    loader = QUiLoader()
    uifile = QFile('root.ui')
    uifile.open(QFile.ReadOnly)
    wmain = loader.load(uifile)
    uifile.close()

    ctrl = Control(wmain, initargs)

    if '-xclip' in sys.argv:

        ctrl.fromclipboard()

    sys.exit(app.exec_())

