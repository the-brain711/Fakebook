# Table of Contents
- [Table of Contents](#table-of-contents)
- [Objective](#objective)
- [Installation](#installation)
- [Description](#description)
- [Features](#features)
- [Front-End](#front-end)
- [Back-End](#back-end)
- [Team Members](#team-members)

# Objective
Our objective is to create a home-grown facebook-like application that will allow users to create, manage, and post from their accounts.

# Installation
1. Clone the Fakebook repo.
    
    `git clone https://github.com/the-brain711/Fakebook.git`

2. Make a virtual environment to manage dependencies
   
   `cd Fakebook`

   `py -3 -m venv .venv`

   `.venv\Scripts\activate`

3. Install all dependencies for Fakebook

   `pip install -e .` 

4. Run Fakebook App (debug flag is optional)

   `flask --app Fakebook run --debug`

# Description
Fakebook is a facebook-like application with a focus on communication and interactivity. Our program will allow those wishing to interact 
with their peers to use our service to put forth ideas as well as responses to said ideas. Our focus will be realized through a rich timeline
system that is complete with post response abilities.

# Features 
User account management- users will be able to create accounts, modify personal details/settings, login/logout, and delete accounts

User timelines- users will have access to personal feed of posts (timeline) as well as feeds of friends

Friend requests- users will be able to send and accept friend requests between other users

Post interaction- users will be able to interact with friends posts in the following ways: like, commment, and share

# Front-End
* Flask(Python)

# Back-End
* AWS Elastic Beanstalk
* AWS RDS (MySQL)

# Team Members
Brian Nguyen(the-brain711): Developer

Caleb Hickman-Thomas(CaramelHeaven1): Developer

Christian Johnson(CJhonson1234): Developer 

Connor White(TheConnorGW): Developer

Manolo Diaz(manny23diaz): Developer
