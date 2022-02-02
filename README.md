# cfgtocnf
.py, takes in Context Free Grammar and outputs a Grammar in (cleansed) Chomsky Normal Form

This python implementation of Automata theory takes in an example Context Free Grammar (CFG) and cleanses it, returning the Grammar in Chomsky Normal Form (to be used in a CYK algorithm).
This utilizes all 5 states via separate functions, checking if a function invalidates an earlier state via recursion. 
This program is rudimentary and unoptimized but robust, taking a lot of variation into account.

If a streamlined action to cleanse a grammar without recursion checks is known, please let me know via email at devinperry@usf.edu! I'd be very interested to hear a non-recursive method.
