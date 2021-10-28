import pygame

# Global Constants
FPS = 60
WIN_DIMENSION = (1280,720)

# Game Global
WIN = pygame.display.set_mode(WIN_DIMENSION)


# Setup window
pygame.display.set_caption("Bounce Classic")

# Draw
def draw():

  # Background
  WIN.fill((255,255,255))
  # Refresh
  pygame.display.update()

# Game Loop
def main():
  pygame.init()
  clock = pygame.time.Clock()
  
  run = True
  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    draw()

  pygame.quit()

if __name__ == "__main__":
  main()