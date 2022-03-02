//Program Name: cmartires_ShellScript.c
//Author: Colin Martires
//Purpose: Programming Assignment 1

//TODO:
// - batch mode !!!!
// - input stream file pointer needs to be set equal to input from terminal - potentially use fgets with stdin?

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

#define HOST_NAME_MAX 64

void promptUser(bool isBatch);
void printError();
int parseInput(char *input, char *splitwords[]);
char *redirectCommand(bool *isRedirect, char *tokens[], int numTokens);
char *executeCommand(char *cmd, bool *isRedirect, char* tokens[], char* outputTokens[], bool *isExits);
//char getLetter(char *str, int index);
void printHelp(char *tokens[], int numTokens);
bool exitProgram(char *tokens[], int numTokens);
void launchProcesses(char *tokens[], int numTokens, bool *status);
void changeDirectories(char *tokens[], int numTokens);

int main(int argc, char *argv[])
{
	bool batchmode, exit;

	//???
	FILE *outputFS = NULL;
	FILE *inputFS = NULL;
	FILE *redirectionFS = NULL;

	char *parsed[100], *cmdWhole, *outFileName;
	char *outputTokens[100]; //???
	char userCmds[100];
	int numArgs;
	bool isRe, isExit;
	pid_t shellPID = getpid();

	if(argc == 1)										//interactive mode
	{
		batchmode = false;

		while(true)														//loop until user exits
		{
			promptUser(batchmode);										//prompt user
			fgets(userCmds, 100, stdin);									//read in user's commands
			cmdWhole = strdup(userCmds);							//save commands before parsing
			numArgs = parseInput(userCmds, parsed);						//parse commands
			// printf("\nEntered Commands: %s\n", cmdWhole);				//----verifying input---------temporary check
			// printf("Parsed Tokens:\n");									//----verifying parsed tokens-temporary check
			// for(int i = 0; i < numArgs; i++)
			// {
			// 	printf("%s\n", parsed[i]);
			// }

			outFileName = executeCommand(cmdWhole, &isRe, parsed, outputTokens, &isExit);		//handle commands

			//exit = exitProgram(parsed, numArgs);						//check for exit command
			// ^ maybe use *isExit instead of exit

			//PROCESS KILLER
			if(isExit == true)											//exit option, kills process
			{
				printf("Exiting program with PID: %d\n", shellPID);
				kill(shellPID, SIGKILL);
			}

			//check if redirect command is called
			if(isRe == true)
			{
				printf("Successfully copied contents from %s to %s\n", parsed[1], parsed[3]);
			}

		}

		//input stream file pointer needs to be set equal to input from terminal - potentially use fgets with stdin?

//------------------------testing-------------------------------//
	

		
//--------------------------------------------------------------//
	
	}
	else if(argc == 2)									//batch mode
	{
		batchmode = true;
		if(inputFS = fopen(argv[1], "r"))				//check if file exists
		{
			char lines[150];
			while(!feof(inputFS))
			{
				fgets(lines, 150, inputFS);
				numArgs = parseInput(lines, parsed);	//parse arguments from command line
				for(int i = 0; i < numArgs; i++)
				{
					printf("%s ", parsed[i]);
				}
				printf("\n");
			}
		}
		else											//file doesn't exist
		{
			printError();
			return 1;
		}
	}
	else												//error, too many arguments
	{
		printError();
		return 1;
	} 

	return 0;
}

void promptUser(bool isBatch)
{
	if(isBatch == false)
	{
		char *user, host[HOST_NAME_MAX + 1], cwd[256];
		user = getenv("LOGNAME");
		gethostname(host, HOST_NAME_MAX + 1);
		getcwd(cwd, sizeof(cwd));
		printf("%s@%s:%s$ ", user, host, cwd);
	}
}

void printError()
{
	printf("Shell Program Error Encountered\n");
}

int parseInput(char *input, char *splitWords[])
{
	int wordInd = 0;
	splitWords[0] = strtok(input, " ");
	while(splitWords[wordInd] != NULL)
	{
		splitWords[++wordInd] = strtok(NULL, " ");
	}
	return wordInd;
}

char *executeCommand(char *cmd, bool *isRedirect, char* tokens[], char* outputTokens[], bool *isExits)
{
	char *outFileName = "";

	char* cmdDup = strdup(cmd);
	strcat(cmdDup, "\n");	
	int numTokens = parseInput(cmd, outputTokens);

	bool status;

	//printf("numTokens: %d\n", numTokens);

	//test strdup
	//printf("cmd from executeCommand: %s", cmdWhole);	//-----verify inputs-----
	//printf("cmdDup from executeCommand: %s", cmdDup);	//-----verify inputs-----

	//strcmp(tokens[1], ">") == 0  ---> this method causes a seg fault LOL
	//strchr(cmdDup, '>') != NULL

	if((strchr(cmdDup, '>') != NULL) && (strcmp(tokens[0], "cat") == 0))	//redirect command
	{
		*isRedirect = (bool)true;
		*isExits = (bool)false;
		outFileName = redirectCommand(isRedirect, tokens, numTokens);
	}
	//strstr(cmdDup, "help") != NULL
	else if(strcmp(tokens[0], "help\n") == 0)				//help command
	{
		*isRedirect = (bool)false;
		*isExits = (bool)false;
		printHelp(tokens, numTokens);
	}
	//strstr(cmdDup, "exit") != NULL
	else if(strcmp(tokens[0], "exit\n") == 0)				//exit command
	{
		*isRedirect = (bool)false;
		*isExits = exitProgram(tokens, numTokens);
	}
	//strstr(cmdDup, "cd") != NULL
	else if(strcmp(tokens[0], "cd") == 0)					//cd command
	{
		*isRedirect = (bool)false;
		*isExits = (bool)false;
		changeDirectories(tokens, numTokens);
	}
	// else if((strstr(cmdDup, "ls") != NULL) && ((strcmp(tokens[0], "ls") == 0) || (strcmp(tokens[0], "ls\n") == 0)))		//there's probably a bug here
	// {
	// 	*isRedirect = (bool)false;
	// 	*isExits = (bool)false;
	// 	launchProcesses(tokens, numTokens, isRedirect, cmdDup);
	// }
	else																	//launch processes
	{
		launchProcesses(tokens, numTokens, &status);
		*isRedirect = (bool)false;
		*isExits = (bool)false;


		//printf("status from execCmds: %d\n", status);
		if(status == 0)														//command not found
		{
			printf("Command(s) not found\n");
			printError();
		}
		else
		{
		//	printf("lp successfully executed\n");
		}
		

	}
	return outFileName;
 }

bool exitProgram(char *tokens[], int numTokens)
{
	if((strcmp(tokens[0], "exit\n") == 0) || (strcmp(tokens[0], "exit") == 0))		//check for both 'exit\n' and 'exit'
	{
		//printf("You typed exit\n");
		//printf("numTokens: %d\n", numTokens);
		if(numTokens != 1)
		{
			//printf("Too many arguments\n");
			printError();
			return false;
		}
		else return true;
	} else return false;
}

void printHelp(char *tokens[], int numTokens)
{
	if((strcmp(tokens[0], "help\n") == 0) || (strcmp(tokens[0], "help") == 0))		//check for both 'exit\n' and 'exit'
	{
		if(numTokens != 1)
		{
			printError();
		}
		else
		{
			printf("\nColin's example linux shell.\n"
					"These shell commands are defined internally.\n"
					"help -prints this screen so you can see available shell commands.\n"
					"cd -changes directories to specified path; if not given, defaults to home.\n"
					"exit -closes the example shell.\n"
					"[input] > [output] -pipes input file into output file.\n\n"
					"And more! If it's not explicitly defined here (or in the documentation for the assignment), then the command should try to be executed by launchProcesses.\n"
					"That's how we get ls -la to work here!\n\n");
		}
	}
}

char *redirectCommand(bool *isRedirect, char *tokens[], int numTokens)
{
	char *outFileName = "";	
	char contents;

	FILE *fpIN, *fpOUT;

	if(strlen(tokens[2]) != 1)										//too many >'s
	{
		printf("Too many >'s\n");
		printError();
		*isRedirect = (bool)false;
		return outFileName;
	}
	else
	{
		fpIN = fopen(tokens[1], "r");								//open input file for reading
		if(fpIN == NULL)
		{
			printf("%s: No such file or directory\n", tokens[0]);
			printError();
			*isRedirect = (bool)false;
			return outFileName;
		}

		fpOUT = fopen(tokens[3], "w");								//open output file for writing
		if(fpOUT == NULL)
		{
			printf("%s: Cannot open file\n", tokens[2]);
			printError();
			*isRedirect = (bool)false;
			return outFileName;
		}

		contents = fgetc(fpIN);										//transfer contents of input file to output file
		while(contents != EOF)
		{
			fputc(contents, fpOUT);
			contents = fgetc(fpIN);
		}

		fclose(fpIN);
		fclose(fpOUT);
	}

	outFileName = tokens[3];
	return outFileName;
}

void changeDirectories(char *tokens[], int numTokens)
{
	char *dest, cwd[100];
	int status;
	
	dest = tokens[1];
	dest[strlen(dest) - 1] = '\0';							//formatting
	status = chdir(dest);
	if(status != 0)
	{
		perror("Error");
		printError();
	}
}

void launchProcesses(char *tokens[], int numTokens, bool *status)
{
	int lpStatus;

	char *fix;									//fix last argument entry (remove '\n')
	fix = tokens[numTokens - 1];
	fix[strlen(fix) - 1] = '\0';
	tokens[numTokens - 1] = fix;
	tokens[numTokens + 1] = NULL;				//argument list must be NULL terminated

	int fd[2];						//file decriptors for pipe | fd[0] = read, fd[1] = write
	if(pipe(fd) == -1)
	{
		printError();
		printf("Pipe error\n");
	}




	int childPID = fork();							//fork child process
	if(childPID == -1)								//error checking
	{
		printError();
		printf("Forking error\n");
	}
	
	if(childPID == 0)								//in the childprocess
	{
		close(fd[0]);
		int execStatus = 0;
		//-----
		//printf("Input a number: ");
        //scanf("%d", &execStatus);
		//-----
		execStatus = execvp(tokens[0], tokens);
		if(write(fd[1], &execStatus, sizeof(int)) == -1)
		{
			printError();
			printf("writing to pipe error\n");
		}
		close(fd[1]);
	}
	else										//parent process, wait for child process to finish executing
	{
		wait(NULL);
		close(fd[1]);
		int lpStatus;
		if(read(fd[0], &lpStatus, sizeof(int)) == -1)
		{
			printError();
			printf("reading from pipe error\n");
		}
		//printf("status: %d\n", lpStatus);
		if(lpStatus == -1)
		{
			*status = (bool)false;
		}
		else
		{
			*status = (bool)true;
		}
		close(fd[0]);
	}
	//printf("Success\n");
	//kill(childPID, SIGTERM);


}





