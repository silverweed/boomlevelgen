BOOM Random Level Generator
============
Random Level Generator for Factor Software's BOOM videogame 

Preamble
============
BOOM is an arcade game from Factor Software, similar to Bomberman, but with slightly different (and, IMHO, better) game mechanics. If you never heard of it, I suggest you looking here: http://www.factor-software.com/boom.php?lang=en. You can buy the game for about 10$ or download it free: in the latter case you'll still have access to all the levels of the game (which are 80), you just won't be able to save the game (but, hey, for hardcore gamers this is actually a good thing!). I definitely suggest you try it.

**UPDATE**: the original game is not available anymore from the original site. You can either search it in abandonware sites or [download my open source clone BOOM: Remake](https://silverweed.github.io/boom/) for free (it works on Windows, Linux and Mac). If you wish to generate levels for *BOOM: Remake* you'll need to pass the `-l` flag to `boomlevelgen.py`, as it uses a different level format.

About this program
=============
BOOM levels are cool and all, but after the 10th time you finish them, you may get a little bored. There is a handy program called BOOMEdit which allows to create customized (non-random) levels (available for free here: http://www.factor-software.com/boom.php?lang=us#BOOMLevelEditor). However, creating 80 levels by hand may be kinda frustrating. If you want to go a step further, why not generating levels in a randomized way?

boomlevelgen.py is a Python script which generates a random series of levels, allowing you to use them instead of the original ones, with virtually infinite different configurations. All the levels are guaranteed to be solve-able: this means that no unreachable spot is allowed to exist in a level. This ensures you won't get stuck in an impossible level in the middle of a game.

The script features several generation algorithms which are used alternately to create sufficiently different levels: it sometimes uses a regular base grid (like the regular game levels), but may also use a random-walk-like generation, or a fully randomized one; also, it may choose to generate an axially symmetric, center-symmetric or non-symmetric level, to increase levels differentiation.

At the moment, the choice of difficulty is quite primitive: there is a standard mode in which levels are pretty hard since the beginning, and an easy mode that should spawn less enemies. If you want to fine-tune the level's difficulty, all you have to do is change the formula returned by the BOOMLevel.probEnemy() function.

How to use
==============
Usage is pretty simple:
<pre>python boomlevelgen.py [opts] > MyLevels.plist</pre>

The script works both with Python 2 and 3.

The available <code>opts</code> are:
<ul>
  <li>-t, --faithfulThemes: tells the script to use the original game level themes, which change every 10 levels. By default, this option is False, and the theme for the level is chosen at random;</li>
  <li>-e, --faithfulEnemies: by default, all the possible enemies may spawn in each level. If this option is passed, the script will only spawn "viable" enemies for each level, i.e. only Soldiers, Sgt. Cool and Thick Lizzy will spawn in the first 10 levels, then the Mean-O-Taur will also spawn since level 11, and so on.</li>
  <li>-v, --verbose: outputs on STDERR some additional information and the layout of each generated level.</li>
  <li>-l, --lifish: outputs levels in Lifish format (needed to make it work with *BOOM: Remake*).</li>
</ul>

The levels are output on STDOUT, so you just need to redirect it to a file with the <code>> MyLevels.plist</code> directive. This will create a <code>MyLevels.plist</code> file, which you'll need to copy in the Resources path of your BOOM app (back up the original levels first!)
You can do this from the terminal:
<pre>
mv MyLevels.plist /path/to/Boom\ v2.0.6/BOOM.app/Contents/Resources/BOOM\ Levels.plist
</pre>
or from graphics environment:
<ol>
  <li>Go to the BOOM folder</li>
  <li>Right-click on BOOM and select "Show package content"</li>
  <li>Go in Contents -> Resources</li>
  <li>Backup BOOM Levels.plist somewhere else</li>
  <li>Move your generated levels file here and rename it to BOOM Levels.plist.</li>
</ol>

Next time you'll open BOOM, it will use the new levels. You can revert back to the original levels by doing the same steps descripted above, this time moving the original levels into BOOM.app/Resources/Contents.

Requires
=============
Requires Python3.

BOOM is only available on MacOS, though running this program only requires Python.

License
=============
    boomlevelgen.py
    Copyright (C) 2022 silverweed

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
