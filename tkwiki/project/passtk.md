# Passtk #

# What is it? #

Passtk is a `python` script that can generate a `random` password


# Home Page #

[https://github.com/tankywoo/passtk](https://github.com/tankywoo/passtk)


# Usage #

It can specified the level and the length of the password

	usage: passtk [-h] [-l LEVEL] [-n LENGTH]

	optional arguments:
	  -h, --help            show this help message and exit
	  -l LEVEL, --level LEVEL
	                        The level(1-3, default is 2) of the password, higher
	                        is complex
	  -n LENGTH, --length LENGTH
	                        The length of the password



# Setup #

Use it in your Unix/Linux system:

	sudo cp passtk.py /usr/bin/passtk

And then you can use `passtk` command to use it.


# Thought #

I have seen many projects like this, but most of them don't have real randomness.

Such as:

A project has the same functions with mine. 

And it has three levels, the third level is the most higher, and can generate the complex password

He use

	$ random.sample((string.letters + string.digits + string.punctuation), pwd_length)

But This way can't ensure the randomness.

Maybe the generated password(the pwd_length characters) are all digits, or others

And another reason is that random.sample function returns a set(unique)

But, my `Passtk` can ensure the randomness

If it is the third level, the password will certainly include letters, digits and punctuation,

and the numbers of them will also be random


# License #

MIT License
