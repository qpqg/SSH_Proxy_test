from socket import socket, AF_INET, SOCK_STREAM, error
from paramiko import SSHClient, AutoAddPolicy, AUTH_SUCCESSFUL, AUTH_FAILED,AuthenticationException

class Proxy_ssh(socket):
	def __init__(self, proxy=None, ssh_server=None, user=None, pwd=None):
		super(Proxy_ssh, self).__init__(AF_INET,SOCK_STREAM)
		self.proxy = proxy
		self.user = user
		self.password = pwd
		self.ssh_server = ssh_server
		self.payload = f"CONNECT {ssh_server} HTTP/1.0\r\n\r\n"
		self.SSHclient = SSHClient()
		
	def setProxy(self, proxy):
		self.proxy = proxy
		
	def open_connnection(self):
		proxy, port = self.proxy.split(":")
		self.connect((proxy, int(port)))
		self.sendall(self.payload.encode())
		
	def ssh_Test(self):
		ssh_host, ssh_port = self.ssh_server.split(":")
		print(ssh_host,ssh_port)
		try:
			self.SSHclient.connect(ssh_host, port=ssh_port,username=self.user, password=self.password, sock=self)
			self.SSHclient.set_missing_host_key_policy(AutoAddPolicy())
			return ("Succes", AUTH_SUCCESSFUL)
		except AuthenticationException:
			return ("Login Failed", AUTH_FAILED)
		except:
			return "SSH Error"
			
	def getResultProxy(self):
		try:
			return self.recv(1080).decode("utf-8").split("\r\n\r\n")[0]
		except Exception as e:
			return e
		
	def setSSH_server(self, server):
		self.ssh_server = server
		
	def Stop(self):
		self.close()
		self.SSHclient.close()
		
my_ssh = "128.199.151.77:443"
my_proxy = "103.3.46.19:912"		

p = Proxy_ssh()
p.setProxy(my_proxy)
p.setSSH_server(my_ssh)
p.open_connnection()
print(p.getResultProxy())
print(p.ssh_Test())
p.close()

	