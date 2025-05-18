# cmdpy

First crack at a module that allows you to run shell commands more
conveniently from python with shell-like pipelines.  Commands can be
inter-mixed with python code in the pipeline by inheriting from
provided classes.

Python code runs in separate threads so that python code that fills a
pipe buffer doesn't deadlock the entire pipeline.

This doesn't yet provide a method of setting environment variables and
uses a separate shell for each command.

Command strings are not sanitized and act like they are typed into a
shell.

cmd.py is the module.

example.py shows example of its use.

testcmd.py, testgen.py, and wait.py are used to demonstrate behavior
where output fills a pipe buffer entirely.

Examples
--------

````
c=Cmd("cat *") | Cmd("wc -l")
c.exec()

c=Cmd("cat *") | Cmd("wc -l") | Result()
c.exec()
print(c.result)

c = (Cmd("ls")  | (cl:=CountLines())).exec()
print(cl.line_count)
````
