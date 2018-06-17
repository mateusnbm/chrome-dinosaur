# Chrome Dinosaur Game

### How to run:

1. Open a new chrome window and place it on the left side of the screen, covering about 70% of it, then, navigate to this [website](http://wayou.github.io/t-rex-runner/). Press <kbd>space</kbd> to start a new game a let the dinosaur hit the first cactus.
2. Open a new terminal window and navigate to the repository's folder. Place the window on the remaining 30% right portion of the screen.
3. Install the dependencies listed in the requirements file.
4. Run `python3 main.py`. When prompted, press enter to start. The chrome window must remain open and always visible during the whole time our program is running, since, screenshots are being captured continuously. Note that our program will be manipulating the mouse cursor, clicking and hitting keyboard keys.
6. To terminate, click on the terminal window and press <kbd>control</kbd>+<kbd>C</kbd>.


### Loading genomes:

Each program execution will create a new file in the genomes folder, it will persist every genome that was tested. To start the program with genomes from a previous training phase, replace the string attributed to the variable `genomes_filename` with the name of the desired file. The application will load the latest genomes from the specified file.

### Project Structure:

`scanner.py` stores auxiliary functions that help us capture screenshots and analyse them to extract important data, such as: game boundaries, dinosaur's bounding box and detect the game over screen.

`sensors.py` is used to abstract the sensors used to determine the obstacles distance, size and speed.

`network.py` a simple MLP implementation. It uses the sigmoid function as activation function and doesn't implement a bias for each layer.

`genetic.py` contains a class representing a genome and the implementation of some steps of the genetic algorithm.

`main.py` is the core of the program, uses all libraries mentioned above to achive our goal. Start by taking a look at it, it'll help you understand how things are tied together.

### Bugs:

1. There is a bug that may cause the program to miss the game over screen. If you face this situation: terminate, ignore the genomes file and restart. This bug is rare.

## Notes:

1. The libraries being used claim to work on multiple operating systems. Although, the program was developed and tested only on a machine running macOS. Most likely, the arrow down key won't be recognized on Linux or Windows, to fix this issue take a look [here](https://github.com/SavinaRoja/PyUserInput/issues/95). You'll need to change the arrow down key code with the one suitable for your OS.
