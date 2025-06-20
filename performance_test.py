import pygame
import time

# Simple performance test
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Test drawing performance
start_time = time.time()
frames = 0

for i in range(300):  # Test 300 frames
    screen.fill((0, 0, 0))
    
    # Draw some rectangles (simulating cars)
    for j in range(10):
        pygame.draw.rect(screen, (255, 0, 0), (j * 50, j * 30, 30, 50))
        pygame.draw.rect(screen, (0, 255, 0), (j * 50 + 10, j * 30 + 5, 20, 10))
    
    pygame.display.flip()
    clock.tick(60)
    frames += 1

end_time = time.time()
elapsed = end_time - start_time
fps = frames / elapsed

print(f"Performance test: {fps:.1f} FPS average over {frames} frames")
print(f"Time elapsed: {elapsed:.2f} seconds")

pygame.quit()
