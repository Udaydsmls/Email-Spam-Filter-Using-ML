# Email-Spam-Filter-Using-ML

## A Spam Filter which will highlight all the spam mails, and add suspicious email-id to blacklist.

Dataset Used: https://www.kaggle.com/datasets/shantanudhakadd/email-spam-detection-dataset-classification

### How the Mail Box will Look after running the spam filter

![Screenshot 2024-08-22 192944](https://github.com/user-attachments/assets/ed080b50-a7d0-437c-b6fb-28e3a4d28848)

There are different types of categorization associated with various colors, depending on the type of spam.

Additionally, there is a blacklist and a whitelist. The purpose of the whitelist is to ensure that emails from important addresses bypass the spam filter, preventing these emails from being marked as spam. The blacklist serves a similar function, but in this case, all emails from the specified addresses will be considered spam.

### How to setup your gmail account with Spam Filter:

1) Login to https://console.cloud.google.com/ to let python access gmail, for this purpose we will need to create credentials.json for the system to work as intended.
2) Now create a new project and name it accordingly. 
![image](https://github.com/user-attachments/assets/3c666984-85c1-4ee1-827b-83ff21e6c5d1)

3) After creating a new project, access under projects and search for Gmail API and enable it.
![image](https://github.com/user-attachments/assets/cdf37876-3635-4e7d-9da3-41c314bc2728)

4) After enabling it click on the option to generate credentials
![image](https://github.com/user-attachments/assets/2c7a1c39-9ead-4892-ab1d-63fd9884ac46)

5) Now under credential type under Gmail API select User data.
![image](https://github.com/user-attachments/assets/c6e5ba35-dba1-4e17-83f2-b2bdb172ca83)

6) Now under the OAuth consent screen, enter the details as per the requirement.
![image](https://github.com/user-attachments/assets/f60a5d18-27d3-4222-9429-7dd3ddaa260a)

7) There is no need to fill scopes.
8) Now in OAuth Client ID, select Desktop App and there is no need to change the name.
![image](https://github.com/user-attachments/assets/06dcd660-e716-4321-a935-7ad4467cf6e4)

9) Now Click on create and you should get your credentials.
![image](https://github.com/user-attachments/assets/dc62e1a6-c271-4956-8f28-167fa895c367)

10) Now go to OAuth consent Screen and add test users, enter the mail from which
you would access the account.
![image](https://github.com/user-attachments/assets/495ab838-4c8f-47e5-bc62-f7e5dfde5ddf)

11) Make sure to rename this file to credentials.json and move it to the same
directory as the python program.
12) Make sure to have all the right files in the directory, token.pickle is createdwhen the program is executed for the first time.

13) For the python program to work correctly make sure to install necessary modules and the ML model.
14) When you run the program, you will ask to login to provide the consent to use the application to access the gmail server. Make sure to choose the right gmail account.
15) You will see the following screen click on continue if the app is not yet verified.
16) Now click on continue and make sure to check the permissions you are providing to the application, if you don’t consent with something make sure you don’t allow it.
17) You should get a message "The authentication flow has completed. You may close this window." after you have correctly authenticated.
18) Now the program should run and check all the unread mails and categorise on the basis if they are spam or not.

