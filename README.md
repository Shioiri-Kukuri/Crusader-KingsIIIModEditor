Welcome to CKIII Mod Editor!
Introduction
CKIII Mod Editor is a graphical editing tool tailored for Crusader Kings III mod creators, streamlining the mod development process and enabling non-programmers to customize game content with ease. The editor provides an intuitive interface for visually editing character attributes, traits, and more, eliminating the need for direct code manipulation and significantly enhancing mod creation efficiency and enjoyment.

Key Features
1. User-Friendly Graphical Interface
Clean & Intuitive GUI: Features "Crusader Kings III Mod Editor" as its title, with menus for "File", "Edit", and "Help" for easy navigation.
File Management: One-click opening or saving of Mod files located in the "game\history\characters" directory, with validation to ensure correct paths.
Customization Options: Under "Edit", adjust editor preferences such as font size, color themes, and image cache location.
2. Visually Rich Editing Experience
Code-to-Graphics Conversion: Automatically interprets Mod text for character names, traits, and presents them graphically with clear text and images.
Trait Image Display: Matches trait names to corresponding images, automatically loading visuals for enhanced editing feedback.
Character Properties Grid: Converts character data into editable grids, supporting numerical changes and trait selection, with real-time file updates.
3. Efficient Paging and Search
Virtual Paging: Loads all character data into memory at once, allowing for swift paging without constant file access, mindful of memory optimization.
Character Lookup: Quickly find characters by their "name" attribute through a search function, enhancing editing speed.
4. Data Validation and Saving
Pre-Save Verification: Validates data integrity and format before saving, ensuring outputted Mod files adhere to game engine standards.
Technical Stack
Programming Language: Python, leveraging its extensive community support and rich libraries.
GUI Toolkit: Tkinter or PyQt for cross-platform graphical user interface development.
File & Path Handling: Utilizes os and pathlib modules for precise file operations.
Text Parsing: Employs regular expressions or dedicated parsing libraries for efficient Mod file parsing.
Image Processing: Handles image loading, display, and caching with Pillow (PIL’s modern version).
Data Binding & Persistence: Implements data binding to keep UI and data models in sync, ensuring modifications are saved back as textual code.
Installation & Launch
Environment Setup: Ensure Python 3.x is installed on your system.
Clone the Project: Download the source code from the GitHub repository.
Install Dependencies: Run pip install -r requirements.txt in the project root directory.
Run the Editor: Execute python main.py from the command line to start CKIII Mod Editor.
User Support
Consult the "Help" menu's "ReadMe" for detailed instructions, shortcut keys, update logs, and troubleshooting advice.
Report any issues or suggest features via GitHub Issues or contribute directly to the project.
Future Developments
Enhanced Functionality: Ongoing exploration of features like a tree-view navigator, advanced search and sorting, to further refine the user experience.
Performance Enhancements: Incorporating more efficient parsing and image handling techniques to boost overall editor performance.
Embark on your Crusader Kings III mod creation journey! Join us in expanding the game's possibilities.
