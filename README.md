# Battleship x Minesweaper
It is a **mix** between a **BattleShip** game and a **Minesweaper** game with a **GUI**.

The rules are simple, the main objective remains the same as in the battleship game except that here there are **mines** in addition and each missed shot gives you **insights** on the number of ships and mines in the surrounding tiles within a certain radius.

# Features
In addition to the basic rules and functionalities of the game I implemented some features that I found useful.

**Main menu**
- A Player Vs Player game mode
- A Player Vs AI game mode
- An AI Vs AI game mode
- A settings tab
	- Hint radius, corresponds to the radius in which you will have insights on the number of ships and mines in the surrounding tiles
	- Random placement, either the player places its ships and mines, or the placement is random
	- Number of ships, number of ships for each players
	- Number of mines, number of mines for each players
- A help tab
	- Gives you the color code of the game
  
 **Placement menu**
 - You have a first button to choose between placing a mine or placing a ship
 - When you hover over a tile on the board and you can place the ship/mine, it is showing up on the board
	
**Game board**
- You have a button to switch between 4 differents hint type
	- Only display hints about ships
  - Only display hints about mines
  - Display both
  - Display none
	
- Another button to switch between two types of gamebaord
  - Search grid, it's the hidden opponent grid with your shot displayed
  - Player's grid, it's the current player grid with opponent's shot displayed
- You can right click on a tile to place a flag as in the Minesweaper game
- Next button to allow time for the players to move on to the next round

**AI explanation**

At the start of every turn, it works out all possible locations that every remaining ship could fit in. In addition to that, the neighbors of the boxes containing a ship touched but not cast are highly valued. These different combinations are all added up, and every tile on the board is thus assigned a probability that it includes a ship part, based on the tiles that are already uncovered and the ones that are known to be clear.

# Requirements
As it is said in the **requirements.txt** file, **pygame** and **numpy** are mandatory to run the program.
And if you want to run some perfs test with **test_AI_perf.py** you will need to install the **click** package.

To install a new package juste run ```pip install <package>```

# How to play

To launch the game just run the **gui.py** file with ```python gui.py```

If you want to make some **performance tests**, head into the **test_AI_perf.py** file, **teak** the test settings and run ```python test_AI_perf.py```

# Ways to improve

- Add a Client/Server architecture to be able to play in multiplayer
- Improve AI by enabling it to detect and avoid mines through an algorithm using **inferences**(the same algo used in the Minesweaper game)
- Add images instead of colored shapes

# Screenshots

**Main menu**

![image](https://user-images.githubusercontent.com/75265945/194669116-e8641f08-fd4c-41be-a690-a420f764d163.png)

**Help menu**

![image](https://user-images.githubusercontent.com/75265945/194669869-547b24bf-273a-45f5-a65d-0c1202f8a113.png)

**Settings menu**

![image](https://user-images.githubusercontent.com/75265945/194669966-c283efae-6545-4cb8-bcb0-2ee0e793c726.png)

**Placement menu**

![image](https://user-images.githubusercontent.com/75265945/194670140-52d01ac4-1d2b-43aa-856b-3eb025de82b6.png)

**Game board (search board)**

![image](https://user-images.githubusercontent.com/75265945/194670692-8e94f43c-80e7-4a51-b043-c58d6359a7b6.png)

**Game board (player's board)**

![image](https://user-images.githubusercontent.com/75265945/194670597-debb600c-1179-4e74-b9b6-6f1e4db09c92.png)




