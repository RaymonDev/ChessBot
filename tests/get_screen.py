import pygame
import mss
import pyautogui
from PIL import Image
from PIL import ImageDraw

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Screen Area Selector")

# Initialize some variables
is_selecting = False
start_pos = (0, 0)
end_pos = (0, 0)
selected_area = None

# Define the clock
clock = pygame.time.Clock()

def capture_screen_area(region):
    with mss.mss() as sct:
        screen_shot = sct.grab(region)
        img = Image.frombytes('RGB', (screen_shot.width, screen_shot.height), screen_shot.rgb)
        return img

def draw_selection(screen, start_pos, end_pos):
    rect_width = end_pos[0] - start_pos[0]
    rect_height = end_pos[1] - start_pos[1]
    pygame.draw.rect(screen, (255, 0, 0), (start_pos[0], start_pos[1], rect_width, rect_height), 2)

def display_image(screen, img):
    mode = img.mode
    size = img.size
    data = img.tobytes()
    image = pygame.image.fromstring(data, size, mode)
    screen.blit(image, (0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                is_selecting = True
                start_pos = event.pos
                end_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                is_selecting = False
                end_pos = event.pos
                selected_area = {
                    'left': min(start_pos[0], end_pos[0]),
                    'top': min(start_pos[1], end_pos[1]),
                    'width': abs(end_pos[0] - start_pos[0]),
                    'height': abs(end_pos[1] - start_pos[1])
                }
        elif event.type == pygame.MOUSEMOTION:
            if is_selecting:
                end_pos = event.pos

    screen.fill((0, 0, 0))

    if selected_area:
        img = capture_screen_area(selected_area)

        # Get mouse position
        mouse_x, mouse_y = pyautogui.position()
        relative_mouse_x = mouse_x - selected_area['left']
        relative_mouse_y = mouse_y - selected_area['top']

        # Draw the mouse cursor on the image
        draw = ImageDraw.Draw(img)
        cursor_size = 10  # Size of the cursor
        draw.ellipse(
            (relative_mouse_x - cursor_size, relative_mouse_y - cursor_size,
             relative_mouse_x + cursor_size, relative_mouse_y + cursor_size),
            outline='red', width=2
        )

        display_image(screen, img)

    if is_selecting:
        draw_selection(screen, start_pos, end_pos)

    print(selected_area)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()


