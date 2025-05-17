#!/usr/bin/python3

import sys
import os
import subprocess


class Cmd:
    """Cmd("<shell cmd>").exec() to run
c = Cmd("<shell cmd>") | Cmd("<shell cmd2>")
c.exec()

pipes the output from <shell cmd> to <shell cmd2>.
"""
    def __init__(self, *args):
        self.args = args
        self.cmd = " ".join(self.args)
        self.next_pipeline_cmd = None
        self.capture_output = False
        self.cwd_path = None
        self.prev_pipeline_cmd = None
        self.encoding = 'utf-8'
        self.resultcode = None
    # end def

    def enc(self, encoding):
        """encoding to use for IO, a text value like 'utf-8' or None"""
        self.encoding = encoding
        return self
    # end def


    def cwd(self, path):
        self.cwd_path = path
        return self
    # end def

    # in order to chain the |-operator properly, we have to pass back
    # the last operation (rightmost), but we want to start execution
    # from beginning of the pipeline so we fix that up
    def exec(self):
        self.resultcode = self.get_first().run()
        return self
    # end def

    def __or__(self, other):
        self.next_pipeline_cmd = other
        self.capture_output = True
        other.set_prev_pipeline_cmd(self)
        return other
    # end def

    def set_prev_pipeline_cmd(self, lhs):
        self.prev_pipeline_cmd = lhs
    # end def

    def get_first(self):
        prev = self
        while (prev.prev_pipeline_cmd != None):
            prev = prev.prev_pipeline_cmd
        # end while
        return prev
    # end def

    def run(self, input=None):
        stdout_arg=None
        if (self.next_pipeline_cmd):
            stdout_arg=subprocess.PIPE
        # end if
        ret = subprocess.Popen(self.cmd,
                               stdin=input,
                               stdout=stdout_arg,
                               cwd=self.cwd_path,
                               #capture_output=self.capture_output,
                               env=None,
                               encoding=self.encoding,
                               shell=True)

        if (self.next_pipeline_cmd):
            res = self.next_pipeline_cmd.run(ret.stdout)
            ret.wait()
            return res
        else:
            ret.wait()
            return ret.returncode
        # end if
    # end def

    def __repr__(self):
        return self.cmd
    # end def
# end class

class Filter(Cmd):
    """Base class to derive filters"""
    def run(self, input=None):
        stdout = sys.stdout
        stderr = sys.stderr
        if (self.next_pipeline_cmd):
            (outpipe_r,outpipe_w) = os.pipe()
            stdout = os.fdopen(outpipe_w, "w")
            stdout_r = os.fdopen(outpipe_r)
        # end if
        self.process(input, stdout, stderr)

        if (self.next_pipeline_cmd):
            stdout.close()
            return self.next_pipeline_cmd.run(stdout_r)
        else:
            return 0
        # end if
    # end def

    def process(self, stdin, stdout, stderr):
        """override this method to do work
- stdin, stdout, and stderr are file handles
        """
        pass
    # end
# end class

class LineFilter(Cmd):
    """Base class to derive line-oriented filters"""
    def run(self, input=None):
        stdout = sys.stdout
        stderr = sys.stderr
        if (self.next_pipeline_cmd):
            (outpipe_r,outpipe_w) = os.pipe()
            stdout = os.fdopen(outpipe_w, "w")
            stdout_r = os.fdopen(outpipe_r)
        # end if
        self.process(input.readlines(), stdout, stderr)

        if (self.next_pipeline_cmd):
            stdout.close()
            return self.next_pipeline_cmd.run(stdout_r)
        else:
            return 0
        # end if
    # end def

    def process(self, lines, stdout, stderr):
        """override this method to do work
- lines is the result of stdin.readlines()
- stdout and stderr are file handles
        """
        pass
    # end
# end class


class CountLines(Filter):
    """Filter that counts the number of lines input to it and writes the result to stdout.  The result can also be accessed after the pipeline runs by reading the variable line_count"""
    def process(self, stdin, stdout, stderr):
        self.line_count = 0
        while 1:
            line = stdin.readline()
            if (line == ''):
                break
            # end if
            self.line_count+=1
        # end while
        stdout.write(f"{self.line_count}\n")
    # end
# end class


class Result(Filter):
    """Filter that can be put at the end of pipelines to collect the output which can be accessed later in the member variable self.result as text"""
    def process(self, stdin, stdout, stderr):
        self.result = stdin.read()
    # end
# end class

class LResult(LineFilter):
    """Filter that can be put at the end of pipelines to collect the output which can be accessed later in the member variable self.result as a list of text lines"""
    def process(self, lines, stdout, stderr):
        self.result = lines
    # end
# end class


if __name__ == "__main__":
    c = Cmd("ls")  | (cl:=CountLines())
    c.exec()
    print(cl.line_count)
# end if
