# __Mario Bros. — Game & Watch (Python + Pyxel)__
### *Project Report — Object-Oriented Programming*

---

## **Authors**
**Razvan Iuliu Ilea Sirb & Aliaksei Yafremau**  
Group: **16**  
Course: **Programming Group 89**  
UC3M  

---

## **Abstract**

This document presents the design, implementation, and evaluation of our *Mario Bros. — Game & Watch* project written in Python using the Pyxel game engine.  
The report includes an overview of the object-oriented architecture, the main algorithms used, the functionalities implemented, and a complete user manual describing how to play the game. The project follows strong OOP principles taught in class, using encapsulation, inheritance, composition, polymorphism, and clean architecture separation between *domain* and *presentation* layers.  
We conclude with a reflection on the development process, challenges faced, and future improvements.

---

# **Index**

1. [Introduction](#introduction)  
2. [Class Architecture](#class-architecture)  
   1. [Domain Layer](#domain-layer)  
   2. [Presentation Layer](#presentation-layer)  
   3. [Object Relationships Diagram](#object-relationships-diagram)  
3. [Main Algorithms](#main-algorithms)  
4. [Work Performed](#work-performed)  
   1. [Implemented Features](#implemented-features)  
   2. [Unimplemented or Simplified Features](#unimplemented-or-simplified-features)  
   3. [Additional Features Beyond Requirements](#additional-features-beyond-requirements)  
5. [User Manual](#user-manual)  
6. [Conclusions](#conclusions)  
   1. [Final Summary](#final-summary)  
   2. [Main Problems Encountered](#main-problems-encountered)  
   3. [Personal Evaluation and Improvements](#personal-evaluation-and-improvements)

---

# 1. **Introduction**

The goal of this project was to faithfully reproduce the classic *Mario Bros. — Game & Watch* handheld videogame using Python and the Pyxel retro game engine.  
We were required to apply object-oriented design principles throughout the entire codebase, organizing the project into domain entities, presentation abstractions, and game logic controllers.

Our focus was to:

- Build a clean OOP architecture  
- Separate concerns between logic, rendering, and user interaction  
- Implement fully documented classes  
- Use encapsulation and properties for validation  
- Create a working and enjoyable game  

This document describes the resulting system.

---

# 2. **Class Architecture**

The project is divided into two main layers:

- **Domain layer** — pure game logic, no rendering  
- **Presentation layer** — sprites, screens, frames, controllers, and Pyxel integration  

This structure ensures modularity, testability, and clarity.

---

## 2.1 **Domain Layer**

### **Element (Base Class)**
- Represents a static object in the world.
- Attributes:  
  `x`, `y`, `length`, `height`  
- Enforces **non-negative coordinates** and **positive sizes**.

### **MotionElement (Derived Class)**
- Adds movement capability:  
  `.move()`, `.move_x()`, `.move_y()`

### **Player**
- Movable character (Mario/Luigi).  
- Can pick up, carry, and place packages.  
- Includes sprite-change flags and state tracking.

### **Conveyor**
- Moves packages horizontally.  
- Manages falling logic and staged animation changes.

### **Package and PackageState**
- Represents deliverable items.  
- Tracks state (`ON_CONVEYOR`, `PICKED`, `FALLING`, `ON_TRUCK`).  
- Includes staged sprite transformation.

### **PackageFactory**
- Creates packages of configurable size.  
- Sends them to a target conveyor.

### **Truck**
- Collects delivered packages.  
- Has movement logic for “leaving → turning → returning.”  

### **Floor**
- Represents valid positions for players on vertical levels.

### **Door & Boss**
- Triggered when a package is dropped incorrectly.  
- Boss enters the screen and briefly appears as punishment.

### **Game**
- Central game state manager.  
- Handles:
  - Collision and movement  
  - Player actions  
  - Package creation  
  - Truck logic  
  - Score, lives, and deliveries  
  - Difficulty scaling  

---

## 2.2 **Presentation Layer**

### **Frame**
Stores sprite location inside Pyxel tilesets.

### **PyxelElement**
Binds a domain `Element` to its visual representation.

### **PyxelStaticElement**
Used for decorations — background stairs, platforms, etc.

### **BoardedPyxelElement**
Decorator for adding borders.

### **Window**
Stores game window dimensions, obtained from `Difficulty`.

### **Controllers**
Maps keyboard events to game actions.  
Examples: `MoveUpPlayer`, `MoveDownPlayer`.

### **Screens**
- `DifficultySelectorScreen`  
- `GameApp` (main gameplay loop)  
- `GameOverScreen`

### **GUI elements**
- `PointsCounter`  
- `LivesCounter`  
- `DeliveriesCounter`  

---

## 2.3 **Object Relationships Diagram**

The following diagram summarizes the architecture:

<img width="961" height="601" alt="Untitled Diagram drawio" src="https://github.com/user-attachments/assets/ec460b2f-6e53-4c48-acdf-cc636c3c589e" />
**Fig 1.** *Classes Design scheme*

---

# 3. **Main Algorithms**

This section describes the most relevant algorithms.

### **Conveyor Package Movement**
The conveyor shifts each package horizontally by its velocity.  
If a package reaches the edge:
1. Check whether a player stands on the adjacent floor  
2. If yes, player may automatically pick up the package  
3. If not, package begins to fall; triggering the corresponding sound, boss appearance, and life loss

### **Player Picking Up and Placing Packages**
1. When a package aligns with the player, `.pick_package()` attempts pickup  
2. Package is centered in player hands  
3. After a time threshold, `.put_package()` moves the package to another conveyor or the truck  
4. Score/lives counters update accordingly

### **Truck Movement Algorithm**
The truck:
1. Moves left off-screen  
2. Turns around  
3. Returns to original position  
4. Resets delivery state

### **Package Creation Algorithm**
Frequency dynamically adjusts:
- Based on difficulty’s `belts` and `increase` parameters  
- Based on current score  
- Ensures minimum on-screen package count
- Ensures fairness with cooldowns and even package spacing

### **Boss Door**
After certain triggers (like losing a package or resting too long):
- The door opens  
- The boss appears for a short timed interval  
- The event resets automatically

---

# 4. **Work Performed**

## 4.1 **Implemented Features**
✔ Complete domain model  
✔ Player movement for 2-player support  
✔ Package generation, pickup, transfer, delivery  
✔ Conveyor mechanics with multiple belts  
✔ Full truck movement animation  
✔ Dynamic difficulty scaling  
✔ Score, lives, and delivery counters  
✔ Player and resting animations
✔ Boss animation with door event  
✔ Sound integration  
✔ Full Pyxel rendering system  
✔ Difficulty selector and game-over screens  
✔ Object-oriented architecture with encapsulation and validation  
✔ Custom property setters for all relevant attributes  
✔ Game setup factory and main launcher  

---

## 4.2 **Unimplemented or Simplified Features**
- No high-score storage  
- No advanced animations beyond sprite changes  
- Collision detection simplified to coordinate matching  
- Background music not included  

---

## 4.3 **Additional Features Beyond Requirements**
- Fully dynamic difficulty system  
- Automatic truck animation reset  
- Boss entrance punishment mechanic  
- Expanded GUI elements with digit-splitting  
- Window resizing based on difficulty  
- Sound effects for certain in-game events  
- Clean architecture separation (domain vs presentation)

---

# 5. **User Manual**

## **Objective**
Deliver as many packages as possible without dropping them.  
Avoid losing all three lives.

## **Controls**

### **General**
- **ESC** - Quiting the game

### **Mario**
- **UP arrow** – Move up  
- **DOWN arrow** – Move down  

### **Luigi**
- **W** – Move up  
- **S** – Move down  

(Controls may be reversed depending on difficulty mode.)

## **Rules**
- Catch packages before they fall from their conveyor  
- Pass them down through each conveyor until reaching the truck  
- Dropping a package costs a life  
- Filling the truck fully grants bonus points  
- Boss appears if you drop a package or rest too long  

## **Difficulty Selection**
On the start screen:
- Press **1** → Easy  
- Press **2** → Medium  
- Press **3** → Extreme  
- Press **4** → Crazy  

## **Game Over**
On the lose screen:
- Press **ESC** → Quit  
- Press **SPACE** → Play Again  

## **Game Screenshots**

We've provided some screenshots of the game for reference.

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/4b6b949c-5af7-4644-bbce-1a360c4eb74e" />
 **Fig 2.** *Difficulty Selection Screen*



<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/29eb6f35-6cb7-4ed9-b71b-a07f3f8ee657" />
 **Fig 3.** *Playing the game*



<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/3fb5c1d5-daa8-4688-b1fb-a9f493ba3aa4" />
 **Fig 4.** *Game Over Screen*


---

# 6. **Conclusions**

## 6.1 **Final Summary**
We successfully recreated the *Mario Bros. — Game & Watch* game using Python and Pyxel while following strict object-oriented principles. The project uses a clean two-layer architecture, strong encapsulation, class-based modularity, and proper domain separation. Teamwork was implemented through `git` and **Github**, which facilitated development by working through different branches and pull requests, a tool which (like it was mentioned in the given report example) we believe is extremely important for proper programming.

## 6.2 **Main Problems Encountered**
- Managing sprite alignment across different resolutions 
- Relaunching of the game with a new resolution based on the selected difficulty
- Timing issues between player pickup logic and conveyor movement  
- Handling Pyxel’s limitations (no floats in drawing, no native resolution change functionality, etc)
- Ensuring code readability and project scalability
- Debugging the truck’s off-screen movement due to coordinate restrictions  

## 6.3 **Personal Evaluation and Improvements**
We are satisfied with the final project. The game is playable, visually clear, and structurally sound.  
For future versions, we would like to add:

- High-score system  
- More animations and sound effects  
- Better error handling  
- A pause menu  
- Smoother sprite transitions  
- A more robust screen system  

---
