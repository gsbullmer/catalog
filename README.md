# Item Catalog
This is the third project in the [Udacity Fullstack Nanodgree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) program.

This web application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

The flavor I've designed around is a board game database, much akin to http://www.boardgamegeek.com. Users can view any games in the database, sorted into categories. Once logged in, users can create new games, as well as edit and delete games they've created.

## Table of Contents
- [Installing](#installing)
- [Files](#files)
- [API Hooks](#api-hooks)
- [Upcoming Features](#upcoming-features)

## Installing
You'll use a virtual machine (VM) to run a database server and a web app that uses it. The VM is a Linux server system that runs on top of your own computer. You can share files easily between your computer and the VM.

I'm using the Vagrant software to configure and manage the VM.

Here are the tools you'll need to install to get it running:

### Git
You will need Git to install the configuration for the VM. If you don't already have Git installed, download Git from [git-scm.com](http://git-scm.com/downloads). Install the version for your operating system.

**On Windows:** Git will provide you with a Unix-style terminal and shell called **Git Bash**.  
**On Mac or Linux:** You can use the regular terminal program.

### VirtualBox
VirtualBox is the software that actually runs the VM. You can download it from [virtualbox.org](https://www.virtualbox.org/wiki/Downloads). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

**Ubuntu 14.04 Note:** If you are running Ubuntu 14.04, install VirtualBox using the **Ubuntu Software Center**, not the virtualbox.org web site. Due to a [reported bug](http://ubuntuforums.org/showthread.php?t=2227131), installing VirtualBox from the site may uninstall other software you need.

### Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download it from [vagrantup.com](https://www.vagrantup.com/downloads). Install the version for your operating system.

**Windows Note:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

### Use Git to fetch the VM configuration
**Windows:** Use **Git Bash** (installed with Git) to get a Unix-style terminal.
**Other systems:** Use your favorite terminal program.

From the terminal, run:
```
cd /folder/to/install/project
git clone https://github.com/gsbullmer/catalog.git
```
This will give you a directory named **catalog**.

### Run the virtual machine!
Using the terminal, change directory to `catalog/vagrant`, then type `vagrant up` to launch your virtual machine.

Once it is up and running, type `vagrant ssh` to log into it. This will log your terminal in to the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type `exit` at the shell prompt. To turn the virtual machine off (without deleting anything), type `vagrant halt`. If you do this, you'll need to run `vagrant up` again before you can log into it.

### Start the application
Once your vagrant box is up and running, start the application server by typing:
```
cd /vagrant/catalog
python application.py
```
Visit http://localhost:8000 to use the application.

## Files
Files installed for this project are located in the **/vagrant** directory inside the virtual machine. Everything here is automatically shared with the **vagrant** directory inside the **catalog** directory on your computer. Any code files you save into that directory from your favorite text editor will be automatically available in the VM.

#### categories.py
I've included a script to create the categories I've found to be useful for board games. This gives enough variety to categorize games without being too specific to be useful. Feel free to edit this list to meet your app's needs.

This script is already called when `vagrant up` is called for the first time, or `vagrant provision` after the vagrant box is created.

#### populate_db.py
I've created a script to generate content for the site, including categories. This is helpful for troubleshooting any edits made to the project. Running this will clear out any entries that exist in database already.

#### database_setup.py
The database classes are located in this script.

#### application.py
This is the core application script. All of the routes with their views are found in this file, as well as some utility functions and the user authentication methods.

## API Hooks
Here's a list of api endpoints available at this time:

#### /api/categories
Returns all of the Category objects in json format.

#### /api/category/<:slug>
Returns all of the Game objects in the Category object referenced by the `slug`, in json format.

#### /api/game/<:id>
Returns the details of the Game object referenced by `id`, in json format.

#### /api/recent/rss
Returns an rss feed of updates made to games.

## Upcoming Features
While this covers the basic functionality of the application, there are some features I'd like to implement in the future:

- [ ] Allow users to add their own categories.
- [ ] Hide categories with 0 games in category list.
