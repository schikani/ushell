from ushell.terminal import Terminal

# Define a variable to call terminal from repl. In this case it is 'terminal',
# NOTE: If you change the variable 'terminal', 
#	then you will also need to change all the occurrence of 'terminal' in install.py


terminal = Terminal("root", "MicroPython")  # Enter the username for terminal prefix
terminal._prompt(run_pre_prompt_script=True)  # Get the terminal prompt