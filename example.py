#!/usr/bin/python3


from collections import namedtuple
from cmd import Cmd, CountLines, Filter, LineFilter, Result, LResult


c=Cmd("cat *") | Cmd("wc -l")
c.exec()

c=Cmd("cat *") | Cmd("wc -l") | Result()
c.exec()
print(c.result)

c = (Cmd("ls")  | (cl:=CountLines())).exec()
print(cl.line_count)

c = (Cmd("ls")  | LResult()).exec()
print(c.result)

print((Cmd("ls")  | LResult()).exec().result)

class mount_filter(LineFilter):
    def process(self, lines, stdout, stderr):
        self.some_mounts = []
        Mount = namedtuple('Mount', ['dev', 'mountpoint', 'type', 'options'])
        for line in lines:
            res = line.split()
            fs_type = res[4]
            m = Mount(dev=res[0], mountpoint=res[2],
                      type=res[4], options=res[5])
            if (m.type in ["ext2", "ext3", "ext4","nfs","ntfs","btrfs",
                           "fat", "vfat", "exfat"]):
                stdout.write (line)
                self.some_mounts.append(m)
            # end if
        # end for
    # end
# end class

c = Cmd("mount") | (mf:=mount_filter()) | Cmd("grep vfat") | Result()
c.exec()
print(c.result)

print("-------")
for m in mf.some_mounts:
    print(f"{m.dev}\t{m.type}\t{m.mountpoint}")
# end for
print("-------")


c = Cmd("cat *.py") | Cmd("hexdump -C")
c.exec()


(Cmd("netstat -na") | Cmd("wc -l")).exec()

# c is a reference to the last cmd in the pipeline Results()
c = Cmd("uname -a") | Result()
c.exec()
print(c.result.split())
print(c.resultcode)


c = (Cmd("uname -a") | Result()).exec()
print(c.result.split())
print(c.resultcode)
