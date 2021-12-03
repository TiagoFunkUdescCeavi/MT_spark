#include <stdio.h>
#include <string>

using namespace std;

int main(int argc, char *argv[]){
	int a = stoi( argv[ 1 ] );
	printf("%d\n", a*a );
	return 0;
}
