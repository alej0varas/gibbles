Gibbles
=======

nibbles like game. much more fun, moves on all directions and jump, can be played with mouse.

You can get the code at https://github.com/alej0varas/gibbles or visit http://gibbles.alej0.tk

Requirements
============

pygame 1.9, visit http://www.pygame.org/install.html

Running the Game
----------------

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py


How to Play the Game
--------------------

+-------+--------------------------------------+
|  Key  |                Action                |
+-------+--------------------------------------+
| Mouse |           Move left/right            |
+-------+--------------------------------------+
| Space |                 Jump                 |
+-------+--------------------------------------+
|  Esc  |                 Exit                 |
+-------+--------------------------------------+

Development notes 
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app
