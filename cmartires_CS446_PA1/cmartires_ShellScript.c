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
char *redirectCommand(char *cmdWhole, char *line, bool *isRedirect, char *tokens[], char *outputTokens[], int numTokens);
char *executeCommand(char *cmd, bool *isRedirect, char* tokens[], char* outputTokens[], bool *isExits);
//char getLetter(char *str, int index);
void printHelp(char *tokens[], int numTokens);
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



	char *parsed[100], *cmdWhole, *outFileName;
	char *outputTokens[100]; //???
	char userCmds[30];
	int numArgs;
	bool isRe, isExit;

	if(argc == 1)										//interactive mode
	{
		batchmode = false;

		while(true)														//loop until user exits
		{
			promptUser(batchmode);										//prompt user
			fgets(userCmds, 30, stdin);									//read in user's commands
			cmdWhole = strdup(userCmds);							//save commands before parsing
			numArgs = parseInput(userCmds, parsed);						//parse commands
			printf("\nEntered Commands: %s\n", cmdWhole);				//----verifying input---------temporary check
			printf("Parsed Tokens:\n");									//----verifying parsed tokens-temporary check
			for(int i = 0; i < numArgs; i++)
			{
				printf("%s\n", parsed[i]);
			}

			outFileName = executeCommand(cmdWhole, &isRe, parsed, outputTokens, &isExit);		//handle commands
			if(isRe == true)
			{
				printf("Successfully copied contents from %s to %s\n", parsed[0], parsed[2]);
			}

			//exit = exitProgram(parsed, numArgs);						//check for exit command
			// ^ maybe use *isExit instead of exit

			//PROCESS KILLER
			if(isExit == true)											//exit option, kills process
			{
				pid_t shellPID = getpid();
				printf("Exiting program with PID: %d\n", shellPID);
				kill(shellPID, SIGKILL);
			}

			//check if redirect command is called
			if(isRe == true)
			{
				printf("Redirected (from main)\n");
			}
			else
			{
				printf("Not redirected (from main)\n");
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

	//printf("numTokens: %d\n", numTokens);

	//test strdup
	//printf("cmd from executeCommand: %s", cmdWhole);	//-----verify inputs-----
	//printf("cmdDup from executeCommand: %s", cmdDup);	//-----verify inputs-----


	if(strchr(cmdDup, '>') != NULL)						//redirect command
	{
		*isRedirect = (bool)true;
		*isExits = (bool)false;
		//printf("You typed > :)\n");
		//call redirectCommand
		outFileName = redirectCommand(cmdDup, cmdDup, isRedirect, tokens, outputTokens, numTokens);

	}
	else if(strstr(cmdDup, "help") != NULL)				//help command
	{
		*isRedirect = (bool)false;
		*isExits = (bool)false;
		printHelp(tokens, numTokens);
	}
	else if(strstr(cmdDup, "exit") != NULL)				//exit command
	{
		*isRedirect = (bool)false;
		*isExits = exitProgram(tokens, numTokens);
	}
	else if(strstr(cmdDup, "cd") != NULL)				//cd command
	{
		*isRedirect = (bool)false;
		*isExits = (bool)false;
		//call changeDirectories
	}
	else												//command not found
	{
		printf("Command(s) not found\n");
		printError();
	}
	


	/*
	else												//if strchr returns NULL
	{
		*isRedirect = (bool)false;
		if(numTokens == 0)								//if 0 tokens, return outFileName
		{
			return outFileName;
		}

		*isExits = exitProgram(tokens, numTokens);
		if(*isExits == true)
		{
			return outFileName;
		}

		//printf("you didn't type > :(\n");
	}*/
	
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

char *redirectCommand(char *cmdWhole, char *line, bool *isRedirect, char *tokens[], char *outputTokens[], int numTokens)
{
	char *outFileName = "";	
	char contents;

	FILE *fpIN, *fpOUT;

	printf("cmd from redirect: %s\n", cmdWhole);
	printf("Parsed Tokens (from Redirect):\n");									//----verifying parsed tokens-temporary check
	for(int i = 0; i < numTokens; i++)
	{
		printf("[%d] %s\n", i, tokens[i]);
	}

	if(strlen(tokens[1]) != 1)										//too many >'s
	{
		printf("Too many >'s\n");
		printError();
		*isRedirect = (bool)false;
		return outFileName;
	}
	else
	{
		

		fpIN = fopen(tokens[0], "r");								//open input file for reading
		if(fpIN == NULL)
		{
			printf("%s: Cannot open file\n", tokens[0]);
			printError();
			fclose(fpIN);
			return outFileName;
		}

		fpOUT = fopen(tokens[2], "w");								//open output file for writing
		if(fpOUT == NULL)
		{
			printf("%s: Cannot open file\n", tokens[2]);
			printError();
			fclose(fpOUT);
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

	outFileName = tokens[2];
	return outFileName;
}





