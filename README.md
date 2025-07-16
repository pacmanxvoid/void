🚀 VOID ATTACK LAUNCHER
VOID ATTACK is a terminal-based professional-looking launcher built with Python and C++ for educational purposes only.
It includes Layer 4 (UDP) and Layer 7 (HTTP) stress testing tools.
BEFORE WE STARTING- THIS PROJECT IS USED FOR EDUCATIONAL PURPOSE ONLY 

📦 Requirements:-
1. Make codespace on github/if you have dedicated vps so run on it for better results!

2.Install the dependencies:


sudo pacman -S python-pip gcc
pip install -r requirements.txt
Or manually:


pip install rich pyfiglet
🔨 Compile the Layer 4 C++ Binary

g++ -O3 -std=c++17 -pthread -o attack attack.cpp
Make sure the compiled attack binary is in the same folder as launcher.py.

▶️ How to Use
Step 1: Launch the tool

python launcher.py
Step 2: Register or Login

You'll be asked to create a username and password (saved locally in users.json).

📌 Available Options in Menu
Option	Description
1	Layer 4 UDP Attack via ./attack
2	Layer 7 HTTP Attack via rapist.py
3	View Logs (coming soon)
4	Exit

🌐 Running an Attack
Once logged in, choose:

Layer 4: Input IP, port, and thread count (e.g., 100)
