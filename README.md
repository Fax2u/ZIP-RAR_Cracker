# ZIP-RAR_Cracker
ZIP-RAR Cracker using dictionary file
In order to crack rar files faster, download unrar.exe from rarlab.com!
https://www.rarlab.com/rar_add.htm
or press the link below for direct download!
https://www.rarlab.com/rar/unrarw64.exe
Be sure to extract it!

Place UnRAR.exe in the folder with the python file. 
Run dependencies.py before running the cracker to install the necessary libraries!

This python project utilizes 3 different libraries for cracking purposes. 
zipfile library for cracking and extracting zip files. 
patoolib library for cracking and extracting rar files.
rarfile library for cracking and extracting rar files.

rarfile library requires the addition of unrar.exe as its tool. 
patoolib has its own tool but will echo to console thus slowing the process drastically. 
zipfile works extremely fast compared to the above, but only suitable for zip files. 

The other libraries are:
multiprocessing - used to split the load between all cores and expedite the process.
time - for a single wait command after a successful password attempt in order to have enough time to kill other processes and not get overwritten. 
os - used to manage all the file paths.

Basic order of operation:
A welcome screen is printed. 

The program asks for the user to enter 3 paths:
Path to archive, or an archive name if the .py file is in the same folder.
Path to password dictionary, or a file name if the .py file is in the same folder.
Path to extract to. A folder with the archive name will be made in the path.
After receiving said values, a password queue is started, the archive type is determined by the file header,and the passwords are put into the password queue.

A start screen is printed which indicates the process start. 

A progress bar is started and the main process starts. 

At the end you will receive an output, either a successful extraction and the password 
or a failed extraction. 


Code Commentary:
Lines 1 - 7   # Import necessary libraries and modules.
Line 8 	        # set the rar tool used with rarfile.
Line 11        # define a “global” printing function with mode, strings and line length.
Line 12        # compares the line length of the function to the length of the string inputted.
Line 13        # if one of the input strings is longer than line length then it is the new line length.
           Used a max() function to select the maximum value between the inputted values.
Line 15        # if the mode is ‘begin’ then print the welcome screen.
Lines 16-17 # define variables for the welcome screen so they could be changed later with ease
Lines 18-21 # use line length and the string length to print the strings in the center.
Lines 23-29 # prints a screen that shows you the paths you’ve entered and returns their length.
Lines 31-35 # prints a screen that shows the results password after a successful crack.
Lines 37-40 # prints a screen that shows the user the cracking failed. 
Lines 42-43 # prints a screen to indicate cleanup before terminating the code. 
Line 46        # define a progress bar printer function.
Line 47        # define a variable with string formatting to display percentage of process complete. 
Line 48        # define a var with an int that indicates the length of the bar to fill. 
Line 49        # define a progress bar to print with filled section and empty section decided by %.
Line 51        # if the function doesn’t have the attribute (var) ‘rolling_index’.
Line 52        # make new variable for function and define it at 0.
Line 53        # set a list of signs for the rolling index to go through in a loop. 
Line 54        # set the rolling indicator integer by modulus of the length of signs (5).
Line 56        # if the number of iterations == to the number of total iterations.
Line 57        # print a full bar, 100%, and end message.
Line 58-59   # else print the bar and percentages accordingly.
Line 60        # add +1 to the rolling index so the indicator would “rotate”. 
Line 63        # define a function for a process to operate the progress bar.
Line 64        # if we haven't completed all the parts it would continue printing the bar.
Line 65-67   # if a process has raised a flag that it finished, print 100% bar and complete. 
Line 68-69   # if the flag isn’t raised, print the progress bar. 
Line 70        # sleep for 1 second. (timeout for process bar to prevent unnecessary updates).
Line 73        # define a function to check archive file type. Zip or rar. 
Line 74-75   # bit headers for each file for later use. 
Line 76-79   # try to open the archive file, read it as bits and store as var. close file at end. 
Line 80-81   # if the zip signature == to file bits at length of zip signature. Then it’s ZIP. 
Line 82-83   # if the rar signature == to file bits at length of rar signature. Then it’s RAR. 
Line 84-85   # if none of the above return none. 
Line 86-87   # raise Exception for any reason if any of the operations weren’t successful. 
Line 90        # define a function to read and split password dictionary file. 
Line 91-93   # Try to open file and data = read lines. Ignore errors, encoding utf8.
Line 95-97   # for every line in data, strip ‘\n’ and append to list.
99-101	        # if the list length is 100 then append the list to the process queue. (FIFO)
103 -104      # if a list is less than 100 words, append it to the end of the queue.
Line 105      # return the length of all the data for the progress bar % calculation.  
106-107       # raise Exception for any reason if any of the operations weren’t successful. 
Line 110      # Define a process function to crack the archive. 
Lines 111     # While not stop flag means that if a stop flag is raised it stops the process. 
112-115       # try to get a password list from queue and if it’s empty after 5 sec stop the process.
Line 117      # if archive type is zip then do zip cracking:
	 118 # define var as the zip file
	 119 # for every password in the password list
	 120 # try to:
      121-122 # check if process stop flag is raised. If so, break process.
	 124 # get file info for file number 0 from the zip file.
	 125 # get the file name for file number  0. 
	 126 # try to extract file number 0 to the directory with the python program. 
	 127 # if the code reached this line it means extract was successful and save the password to a process shared variable.
	 128 # raise a stop flag in a process shared variable.
	 129 # wait one second for all the processes to stop.
	 130 # get the path for the extracted file number 0. 
     131-134 # try to remove file number 0 from the directory. If error then pass. 
     135-136 # Extract all the zip file contents into the output directory selected and close zip.
	 137 # break the process because we have got our password and extracted the rar.
     138-139 # if for any reason we didn’t succeed in the operations above, skip to next password
Line 141     # if archive type is rar then do rar cracking: 
	 142 # for every password in the password list
	 143 # try to:
     144-145 # check if process stop flag is raised. If so, break process.
	 147 # if the tool is patool then:
      148-152 # use patool to extract archive and arguments needed.(verbose always on…)
	 153 # if the code reached this line it means extract was successful and save the password to a process shared variable.
 154 # raise a stop flag in a process shared variable.  
	 155 # wait one second for all the processes to stop.
	 157 # if the tool is unrar then:
	 158 # define var as the rarfile 
	 159 # set password to the rarfile
	 160 # get file info for file number 0 from the rar file. 
 	 161 # get the file name for file number  0. 
 162 # try to extract file number 0 to the directory with the python program. 
 163 # if the code reached this line it means extract was successful and save the password to a process shared variable.
 164 # raise a stop flag in a process shared variable. 
 165 # wait one second for all the processes to stop.
 166 # get the path for the extracted file number 0.
      167-170 # try to remove file number 0 from the directory. If error then pass. 	
      171-172 # Extract all the rar file contents into the output directory selected and close rar.
.	 173 # break process since we got the rarfile password. Either with unrar or patool.
     174-175 # if for any reason we didn’t succeed in the operations above, skip to next password
	 176 # add the length of password list to the parts complete variable for progress bar.
    	 179 # Define a user selection function. (only function to get inputs from user).
	 180 # get input for archive file name and strip “ because copy as path pastes with “. 
	 181 # get input for passwords file name and strip “ because copy as path pastes with “. 
	 182 # get input for Extract path and strip “ because copy as path pastes with “.
	 184 # create a new folder name by use of archive name
      185-186 # if user didn’t input extract path then create one with the new folder in program dir. 
      187-189 # else attach the new folder name to the path the user entered.
	 191 # get archive type with the zip_or_rar function 
	 192 # set rar tool to blank in order to not cause errors when zip cracking
      193-204 # a loop that starts if the archive type is rar and asks the user to input 0 or 1 for patool or unrar accordingly. If the input is invalid it asks for an input again until the input is valid. 
	 206 # return data collected in this function for variables in the main function. 
	 209 # define main function. This function runs once and is the order of the program. 
	 210 # call printing function to print a welcome screen.
	 211 # start a queue variable from multiprocessing library in order to load passwords to it.
	 212 # get the variables from user selections function. Archive path etc…
	 213 # get password list length and load passwords to queue with open pass function. 
	 214 # call for printing function to print start screen and return length of line printed. 
	 216 # initialize a manager for shared memory cells. 
     217-219 # initialize shared memory cells between processes and set them. 
     	 221 # define a process for multiprocessing. 
     222-229 # add arguments and number of processes according to number of cpus (threads).
	 231 # define a process for progress bar to be simultaneous with the cracking process.
      232-235 # arguments for progress bar process. 
	 236 # Start progress bar process
     238-240 # start all processes if the stop flag isn’t raised.
     242-245 # wait for stop flag value, if it’s raised then check if a process is alive and kill it.
     247-248 # wait for all the processes to finish in order to continue the code.
     250-251 # kill the progress bar process and wait for it to join.
     253-254 # if the returned password is not blank then print the end screen with the password.
     255-254 # else print a failed screen. 
	 258 # if there are some more passwords in the queue:
	 259 # print a cleanup screen (indication the code hasn’t finished).
	 260 # a loop to get all the passwords out of the queue. 
      261-264 # try to get an item from the queue. If the queue is empty then break.
   265-269 # handle other exceptions and check if the queue is empty with a function then break.
   271-272 # close the queue (can be done only when empty) and join queue to main program
   275-276 # if the window name is main then run the program. Else do nothing.

