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
	int fd[2];
	if(pipe(fd) == -1)
	{
		return 1;
	}



	char* argument_list[] = {"s", NULL}; // NULL terminated array of char* strings

	int childPID = fork();

	if(childPID == 0)
	{
		close(fd[0]);
		int CHILDstatus;
		printf("In the CHILD PROCESS\n");
		CHILDstatus = execvp(argument_list[0], argument_list);
		printf("if not command, this will print\n"
				"execvp returns: %d\n", CHILDstatus);
		write(fd[1], &CHILDstatus, sizeof(int));
		close(fd[1]);
	}
	else
	{
		wait(NULL);
		int statFromChild;
		close(fd[1]);
		printf("In the PARENT PROCESS\n");
		read(fd[0], &statFromChild, sizeof(int));
		printf("execvp return from child: %d\n", statFromChild);
		close(fd[0]);
	}

	return 0;
}