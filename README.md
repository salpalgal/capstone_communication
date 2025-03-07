# Company Communication App
Company Communication App is created with a thought of having a email system with access to all employees within a company. 
## Features
nav bar that contains:
- sign up
  - creates user in database
- log in/out
  - authentication that only allows access to users in database
  - data from interaction with app is specfic to each user 
- root page
  - landing page for the public 
- homepage
  - welcome user when logged in, can click on employees list to access all employees in the database  
- name list
   - list of all employees
- user page
  - shows user profile and option to send the user an email
- email
   -  email form that once filled out will send a gmail to that user 
## User Flow
From the landing site, users can either sign up to create a new user or log in to existing account. Once logged in, the user will come to the homepage. From here, user can click on list of employees to find co-worker to send an gmail to.Clicking on the names of the employees list will lead to that user's profile page. From there, the send email button leads to a email form. Once filled out, the user can send a gmail to the co-worker they wish to communicate with. To logout, click on logout button. Once again, user will be back to the landing page.
## Links
- [smtp server](smtp.gmail.com)
- [site url](https://company-communication-app-7a8b5e846acd.herokuapp.com/)
## Technology 
- python flask
- postgresql
- wtforms
- bootstrap
