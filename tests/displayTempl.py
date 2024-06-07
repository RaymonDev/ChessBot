


import cv2
import numpy as np
import mss
import pyautogui

# Define the screen region to capture
screen_region = {'left': 260, 'top': 184, 'width': 741, 'height': 743}

def capture_screen(region):
    with mss.mss() as sct:
        screen_shot = sct.grab(region)
        img = np.array(screen_shot)
        return img

def draw_cursor(image, region):
    # Get mouse position
    mouse_x, mouse_y = pyautogui.position()
    relative_mouse_x = mouse_x - region['left']
    relative_mouse_y = mouse_y - region['top']
    
    # Draw a red circle at the mouse cursor's position
    cursor_size = 10  # Size of the cursor
    cv2.circle(image, (relative_mouse_x, relative_mouse_y), cursor_size, (0, 0, 255), 2)
    return image


def main():
    while True:
        # Capture the screen region
        frame = capture_screen(screen_region)
        
        # Draw mouse cursor on the frame
        frame = draw_cursor(frame, screen_region)
                
        # Display the frame
        cv2.imshow('Screen Capture', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
