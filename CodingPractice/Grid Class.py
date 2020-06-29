"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
color_wheel = [WHITE,RED,           BLACK,GREEN,BLUE]            # first half of color wheel is on a rotation, second half reserved for other functions
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20
 
# This sets the margin between each cell
MARGIN = 5
 
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(False)  # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[0][0] = 0
 
# Initialize pygame
pygame.init()



# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

x, y = 0,0
grid[x][y] = 3
start = grid[0][0]
grid[9][9] =  4
print(len(grid))


def check_win(x,y):
    if grid[x][y] != 4 and x < len(grid)-1:
                x+=1
                return 2
    elif grid[x][y] != 4 and y < len(grid)-1:
                y+=1
                return 2
    else:
                pass
    if grid[x][y] == 4:
        print('SUCCESS')
        return 2


    
def win(x,y,end):
    if grid[x][y] != 4 and x < len(grid)-1:
        return x+1,y,False
    elif grid[x][y] != 4 and y < len(grid)-1:
        return x,y+1,False
    elif grid[x][y] == 4:
        print('Success')
        return x,y,True
    else:
        return x,y,True
       
    
end = False
# -------- Main Program Loop -----------
while not end:
    #end = False
    for event in pygame.event.get():  # User did something
        
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            grid[x][y] = 3
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            print(WIDTH, MARGIN)
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one
            grid[row][column] = (grid[row][column]+1) % (len(color_wheel)//2) #not grid[row][column] 
            print("Click ", pos, "Grid coordinates: ", row, column)
            #grid[row][column] = check_win(x,y)
            print(x,y,end)
            x,y,end = win(x,y,end)
            
        elif end == True:
            break
    # Set the screen background
    screen.fill(BLACK)
    #grid[x,y] = 3
    # Draw the grid
    for row in range(10):
        for column in range(10):
            
                
            
            


            
            color = color_wheel[grid[row][column]] #changes cell value to index of color wheel
            # Actually draws the rectange at the color. It redraws it every loop
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column-1 + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
            
 


    
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
