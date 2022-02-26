//Program Name: cmartires_ShellScript.c
//Author: Colin Martires
//Purpose: Programming Assignment 1

//TODO:
// - input stream file pointer needs to be set equal to input from terminal - potentially use fgets with stdin?
// - executeCommand

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
char *redirectCommand(char *special, char *line, bool *isRedirect, char *tokens[], char *outputTokens[]);
char *executeCommand(char *cmd, bool *isRedirect, char* tokens[], char* outputTokens[], bool *isExits);
char getLetter(char *str, int index);
bool exitProgram(char *tokens[], int numTokens);
void launchProcesses(char *tokens[], int numTokens, bool isRedirect);
void changeDirectories(char *tokens[], int numTokens);

int main(int argc, char *argv[])
{
	bool batchmode, exit;

	//???
	FILE *outputFS = NULL;
	FILE *inputFS = NULL;
	FILE *redirectionFS = NULL;

	char* parsed[100];
	char* outputTokens[100]; //???
	char userCmds[30];
	int numArgs;
	bool *isRe, *isExit;

	if(argc == 1)										//interactive mode
	{
		batchmode = false;

		while(true)														//loop until user exits
		{
			promptUser(batchmode);										//prompt user
			fgets(userCmds, 30, stdin);									//read in user's commands
			char *cmdWhole = strdup(userCmds);							//save commands before parsing
			numArgs = parseInput(userCmds, parsed);						//parse commands
			printf("\nEntered Commands: %s\n", cmdWhole);				//----verifying input---------temporary check
			printf("Parsed Tokens:\n");									//----verifying parsed tokens-temporary check
			for(int i = 0; i < numArgs; i++)
			{
				printf("%s\n", parsed[i]);
			}
			exit = exitProgram(parsed, numArgs);						//check for exit command

			//PROCESS KILLER
			if(exit == true)											//exit option, kills process
			{
				pid_t shellPID = getpid();
				printf("Exiting program with PID: %d\n", shellPID);
				kill(shellPID, SIGKILL);
			}



		}

		//input stream file pointer needs to be set equal to input from terminal - potentially use fgets with stdin?

//------------------------testing-------------------------------//
	
		/*executeCommand(cmdWhole, isRe, parsed, outputTokens, isExit);
		if(*isRe == true)
		{
			printf("True");
		}
		else
		{
			printf("False");
		}*/
		
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
	int numTokens = parseInput(cmd, outputTokens);

	char *outFileName = "";

	char *cmdDup = strdup(cmd);
	strcat(cmdDup, "\n");

	//test strdup
	//printf("%s", cmdDup);

	if(strchr(cmdDup, '>') != NULL)						//check if command is Redirect
	{
		*isRedirect = true;
		//call redirectCommand
	}
	else
	{
		*isRedirect = false;
		//numTokens = parseInput(cmd, outputTokens);		//parseInput, storing number of returned tokens
		if(numTokens == 0)
		{
			return outFileName;
		}
	}

	if(outFileName == NULL)
	{
		*isExits = exitProgram(tokens, numTokens);
		if(*isExits == true)
		{
			return outFileName;
		}

	}

	//otherwise, call changeDirectories, printHelp, and launchProcesses, and return the output file name
	return outFileName;
 }

bool exitProgram(char *tokens[], int numTokens)
{
	if(numTokens == 1)
	{
		if(strcmp(tokens[0], "exit\n") == 0)
		{
			printf("you typed exit!\n");
			return true;
		}
		else
		{
			printf("you didn't type exit :(\n");
			return false;
		}
	}
	else
	{
		printError();										//error, too many arguments
		return false;
	}
}







