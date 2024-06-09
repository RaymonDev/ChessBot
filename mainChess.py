
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chess
import time
import chess.engine

from playsound import playsound

err_sound_file = "./media/error.wav"
pop_sound_file = "./media/pop.wav"

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities




############################################ Selenium Config ############################################

profile = webdriver.FirefoxProfile(
    r'route to firefox profile')

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX

driver = webdriver.Firefox(firefox_profile=profile,
                           desired_capabilities=desired)


# Set the window to full screen
driver.maximize_window()





board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("./stockfish/stockfish-windows-x86-64-sse41-popcnt.exe")

# Function to convert evaluation score to probability
def eval_to_prob(score):
    # A simple heuristic to convert centipawn score to win probability
    if score > 0:
        prob = min(1.0, 0.5 + (score / 4000))
    else:
        prob = max(0.0, 0.5 + (score / 4000))
    return prob



url = "https://www.chess.com/play/online"
driver.get(url)

print("- " *20)
print("Please login to your account and open a game in chess.com")
print("Make sure you have the movements in text and not in symbols")
print("Make sure your language is English")
print("- " *20)
print("\n")
try:
    playsound(pop_sound_file)
except:
    print("\033[93m[WARNING] Error playing sound\033[0m")



enemyColor = input("\nEnter your enemy color (w/b): ")
stockFishElo = input("Enter the desired elo of AI engine (m = max & min = 1320): ")
print("\n")

# Configure the engine to limit its strength if a specific elo is provided
if stockFishElo != "m":
    engine.configure({"UCI_LimitStrength": True, "UCI_Elo": int(stockFishElo)})
    print(f"\033[94m[BOT INFO] AI engine elo set to {stockFishElo}\033[0m")
else:
    engine.configure({"UCI_LimitStrength": False})
    print("\033[94m[BOT INFO] AI engine elo set to max\033[0m")

# Define the color of the player
if enemyColor == "w":
    player_color = chess.WHITE
    # par = True
    flip_flag = True

    print("\033[94m[BOT INFO] Enemy color / Your color with AI : White \033[0m")
else:
    player_color = chess.BLACK
    # par = False
    flip_flag = False
    print("\033[94m[BOT INFO] Enemy color / Your color with AI : Black \033[0m")


# Define the list of data-node values to search for
data_node_values = {f"0-{i}" for i in range(150)}  # Adjust the range as needed

# Set to keep track of already detected elements
detected_elements = []




############################################ Mouse Control ############################################

import numpy as np
import pyautogui
import time
import keyboard


distFactor = 95

rows, cols = (8, 8)
initial_point = np.array([302.5, 887.5])

coordMatrix = np.zeros((rows, cols, 2))

for row in range(rows):
    for col in range(cols):
        coordMatrix[row, col] = initial_point + np.array([distFactor * col, -distFactor * row])


columnDict = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}


if flip_flag:
    print("- " *20)
    print("Data inverted")
    print("- " *20)
    print("\n")

    # flip the rows of coordMatrix
    coordMatrix = np.flip(coordMatrix, 0)

    # flip the columns of coordMatrix
    coordMatrix = np.flip(coordMatrix, 1)


def split_string(s, length):
    return [s[i: i +length] for i in range(0, len(s), length)]

def translatePosition(value):

    # translate value[0] with columnDict
    column = columnDict[value[0]]
    row = int(value[1]) - 1
    return row, column




def moveMouseToPosition(chessPosition):
    splitedPosition = split_string(chessPosition, 2)
    print("- " *20)
    for position in splitedPosition:
        row, col = translatePosition(position)
        print(f"Moving to row {row} and col {col}")
        pyautogui.moveTo(coordMatrix[row][col][0], coordMatrix[row][col][1])
        pyautogui.click()
        time.sleep(1)




############################################ Main Loop ############################################




# Initialize a set to keep track of already processed data-node values
processed_nodes = set()

try:
    while not board.is_game_over():
        for value in data_node_values:
            try:
                # Use JavaScript to check for the presence of the element
                element = driver.execute_script(f"""
                    return document.querySelector("div[data-node='{value}']");
                """)
                if element and value not in processed_nodes:
                    # Extract and print the content if the element is found
                    content = element.text
                    processed_nodes.add(value)  # Mark this node as processed

                    # Determine whether to process based on color and move number
                    move_number = int(value.split("-")[1])
                    if (flip_flag and move_number % 2 == 0) or (not flip_flag and move_number % 2 != 0):
                        print("\n")
                        print("- " *20)
                        print(f"\033[94mEnemy movement found in data-node={value}! Content: {content}\033[0m")
                        detected_elements.append(content)

                        # Move will be the last element of detected_elements
                        move = detected_elements[-1]

                        # Try to parse and push the move to the board
                        try:
                            move_obj = board.parse_san(move)
                            board.push(move_obj)

                        except ValueError as ve:
                            print(f"\033[91mError parsing move: {move}. Exception: {ve}\033[0m")
                            try:
                                playsound(err_sound_file)
                            except:
                                print("\033[93m[WARNING] Error playing sound\033[0m")
                            print(board)




                if board.turn != player_color:
                    # Engine's turn
                    result = engine.play(board, chess.engine.Limit(time=5.0))
                    board.push(result.move)
                    print("\033[92mEngine's move:", result.move, "\033[0m")
                    moveMouseToPosition(str(result.move))
                    print("- " *20)
                    print(board)
                    print("\n")

                    ############################################ Evaluation ############################################

                    try:
                        # Get the evaluation of the current position
                        info = engine.analyse(board, chess.engine.Limit(time=2.0))
                        score = info["score"].relative.score(mate_score=10000)

                        # Calculate the probability
                        if score is not None:
                            probability = eval_to_prob(score)
                            if score > 0:
                                print \
                                    (f"\033[94m[BOT INFO] ES: +{score} (Probability of AI winning: {probability:.2%})\033[0m")
                            else:
                                print \
                                    (f"\033[94m[BOT INFO] ES: {score} (Probability of Human Enemy winning: {probability:.2%})\033[0m")
                        else:
                            print("\033[94m[BOT INFO] Mate in {info['score'].relative.mate()}\033[0m")
                    except Exception as e:
                        print(f"\033[91mError getting evaluation: {e}\033[0m")
                        try:
                            playsound(err_sound_file)
                        except:
                            print("\033[93m[WARNING] Error playing sound\033[0m")

                    #####################################################################################################

                time.sleep(0.05)

            except Exception as e:
                # If there's any exception, print it out
                print(f"Exception encountered: {e}")
                try:
                    playsound(err_sound_file)
                except:
                    print("\033[93m[WARNING] Error playing sound\033[0m")
                continue
        # Wait for a very short period before checking again
        time.sleep(0.01)

    input("Press Enter to exit...")
    engine.quit()

except KeyboardInterrupt:
    # Exit the loop if interrupted by the user
    print("Script terminated by user.")
    try:
        playsound(err_sound_file)
    except:
        print("\033[93m[WARNING] Error playing sound\033[0m")
finally:
    # Clean up and close the browser
    driver.quit()
