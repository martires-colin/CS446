#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
#include <stdbool.h>

int main()
{
	// char cwd[100];

	// printf("cwd: %s\n", getcwd(cwd, 100));
	// int status = chdir("newDir");
	// printf("status: %d\n", status);
	// printf("cwd: %s\n", getcwd(cwd, 100));

	//int execvp(const char* command, char* argv[]);
	char* argument_list[] = {"ls", NULL}; // NULL terminated array of char* strings
 
	// Ok! Will execute the command "ls -l"

	for(int i = 0; i < 3; i++)
	{
		fork();
		execvp("ls", argument_list);
		printf("\n");
		wait(NULL);
	}


	return 0;
}