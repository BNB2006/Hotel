import random
import string
import time
import os

def generate_random_string():
    """Generate a random 3-character string using letters"""
    return ''.join(random.choices(string.ascii_letters, k=3))

def main():
    filename = "index.css"
    
    while True:  # Infinite loop
        try:
            # Generate and write 5 strings (5 loops)
            for loop in range(5):
                random_string = generate_random_string()
                
                # Append the string to file
                with open(filename, "a") as file:
                    file.write(random_string + "\n")
                
                print(f"Loop {loop + 1}/5: Appended '{random_string}'")
                time.sleep(5)  # Wait 5 seconds
            
            # After 5 loops, delete the file
            if os.path.exists(filename):
                os.remove(filename)
                print("\nCompleted 5 loops - File deleted")
                print("Starting new cycle...\n")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)  # Wait before retrying if there's an error

if __name__ == "__main__":
    main()  
