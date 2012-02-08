LICENSE
=======
3-clause BSD.


TODO
====
* Fix output from stderr - currently only handles stdout properly


DESCRIPTION
===========
There are two versions of the same tool (more or less), one with newer modules and one using older modules.

Typical usage:

Create a folder with "project folders", and list all of them in a file called projects.txt.

/home/user/work
	/doit.py
	/projects.txt
	/projectA
	/projectB
	/projectC
	/projectD

cat projects.txt
	projectA
	projectB
	projectC

Then run "./doit.py hg pull" and "hg pull" is run in all of projectA, B and C (D is not mentioned in projects.txt), in parallell.
