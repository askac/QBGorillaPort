# QB Gorilla Python Port

This repository contains a modern Python port of the classic QBasic game **GORILLA.BAS**, originally published with MS-DOS 5.0 by Microsoft Corporation in 1990. In the spirit of preserving retro game history, this project aims to replicate the original gameplay – throwing explosive bananas between two gorillas perched on a skyline – while modernizing the code for better readability, modular design, and ease of extension.

## Features

- **Modern Python**: Uses Python 3 (with Pygame) for graphics, sound, and input.  
- **Modular & OOP**: Separates logic into classes (Gorilla, Banana, CityScape, etc.), simplifying maintenance and expansions.  
- **Classic Gameplay**: Includes original angle/power mechanics, collisions, cityscape generation, and the signature “banana throw” physics.  
- **Configurable Input**: Choose between keyboard-based power charging or mouse-based dragging for angle and velocity.  
- **Optional Expansions**: Explosions that damage buildings, sun’s shocked face, and more “modern" features while staying faithful to the original QBasic version.  
- **Sound Support (Not Yet Tested)**: The sound system is implemented but lacks test files. If missing, the game will display warnings but continue running.

## Getting Started

1. **Clone This Repo**  
   ```bash
   git clone https://github.com/YourUserName/QBGorillaPort.git
   cd QBGorillaPort
   ```

2. **Install Dependencies**  
   - Python 3.8+ recommended  
   - [Pygame](https://www.pygame.org/) for graphics & audio  
   ```bash
   pip install -r requirements.txt
   # or
   pip install pygame
   ```

3. **(Optional) Add Sound Files**  
   The game includes a sound system, but test sound files are currently missing.  
   If you wish to enable sound effects, add the following files inside `assets/sounds/`:
   ```
   assets/sounds/throw.wav
   assets/sounds/explosion.wav
   assets/sounds/victory.wav
   ```
   If these files are missing, the game will still run, but sound effects will be disabled.

4. **Run the Game**  
   ```bash
   python game.py
   ```
   The main game window should launch, featuring two gorillas on randomly generated buildings.

## Repository Structure

- **game.py**  
  Main game loop and overall orchestration (initialization, update, render).
- **gorilla.py**  
  Class for Gorilla sprites, including arm positions and victory dance logic.
- **banana.py**  
  Physics and drawing for the thrown banana (angle, velocity, collisions).
- **cityscape.py**  
  Procedures for generating and drawing random buildings, plus optional demolition.
- **graphics.py**  
  Handles sun drawing, banana sprite decoding (EGA style), and explosion animations.
- **sound.py**  
  Plays sound effects (throw, explosion, victory). *(Not tested due to missing sound files)*
- **utils.py**  
  Constants, color palettes, random number helpers, unit conversions, etc.
- **throw_controller.py**  
  An optional controller class for angle/power input (keyboard or mouse).
- **qbdraw.py**  
  A small helper that mimics QBasic’s line, circle, and other drawing operations.

## Legal & Copyright

- **Original Game**  
  The original QBasic GORILLA.BAS was released by IBM Corporation around 1991. All rights to the original artwork, naming, and code structure remain with their respective owners.  
- **This Port**  
  This Python version is an **unofficial fan project** intended for educational and historical purposes. It does not imply any sponsorship or endorsement by IBM or its affiliates.
- **Usage**  
  You are free to explore and modify this code base. However, you may not distribute the original QBasic code or assets in a manner that infringes on existing copyrights.

If in doubt about reuse of names, characters, or references from the original GORILLA.BAS, please consult your local laws or seek appropriate permissions.

## Contributing

Contributions and pull requests are very welcome. Whether you want to fix bugs, introduce new gameplay mechanics, or improve the code structure, please feel free to open an issue or PR on GitHub.

## License

Unless stated otherwise, the code in this repository is made available under the MIT License. See [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Microsoft (1990)** for the original GORILLA.BAS game concept and code.
- The QBasic and retro coding communities for continued enthusiasm that keeps classic games alive.
- [Pygame](https://www.pygame.org/) for making Python game development accessible and fun.

Enjoy bananas in the sky! If you have any questions or suggestions, feel free to open an issue or discussion. Happy throwing!
