# #!/usr/bin/python
# # only for python2
# import pexpect
# import os
#
# 这个脚本不支持python3，在我机器上会编译出错，不过在2下面可以用
#
# def ssh_command(cmd,password):
#     ssh_newkey = 'Are you sure you want to continue connecting'
#     child = pexpect.spawn(cmd)
#     i = child.expect([pexpect.TIMEOUT, ssh_newkey, '.assword: '])
#     if i == 0: # Timeout
#         print 'ERROR!'
#         print 'SSH could not login. Here is what SSH said:'
#         print child.before, child.after
#         return None
#     if i == 1: # SSH does not have the public key. Just accept it.
#         child.sendline ('yes')
#         i = child.expect([pexpect.TIMEOUT, '.assword: '])
#         if i == 0: # Timeout
#             print 'ERROR!'
#             print 'SSH could not login. Here is what SSH said:'
#             print child.before, child.after
#             return None
#     child.sendline(password)
#     return child
#
# if __name__ == "__main__":
#     user="xxxx"
#     host="xx.xx.xx.xx"
#     password="xxxxxx"
#     print "Delete war on remote server..."
#     child = ssh_command("ssh -l %s %s rm -rf /home/admin/wmac/target/wmac.war"%(user,host),password)
#     child.expect(pexpect.EOF)
#     print child.before;
#     print "Copy war to remote server..."
#     child = ssh_command("scp /home/admin/wmac/target/wmac.tgz %s@%s:/home/admin/wmac/target/"%(user,host),password)
#     child.expect(pexpect.EOF)
#     print child.before
#     print "Restart remote web server..."
#     child = ssh_command("ssh -l %s %s /home/admin/wmac/bin/jbossctl restart"%(user,host),password)
#     child.expect([pexpect.EOF,pexpect.TIMEOUT])
#     print "OK!"