//Program Name: cmartires_ShellScript.c
//Author: Colin Martires
//Purpose: Programming Assignment 1

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
	bool batchmode;
	FILE *outputFS = NULL;
	FILE *inputFS = NULL;
	FILE *redirectionFS = NULL;

	char* parsed[100];
	int numArgs;

	if(argc == 1)									//interactive mode
	{
		batchmode = false;
		promptUser(batchmode);
		//input stream file pointer needs to be set equal to input from terminal
	}
	else if(argc == 2)								//batch mode
	{
		batchmode = true;
		if(inputFS = fopen(argv[1], "r"))			//check if file exists
		{
			//test filestream
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
		else										//file doesn't exist
		{
			printError();
			return 1;
		}
	}
	else											//error, too many arguments
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
	
}






