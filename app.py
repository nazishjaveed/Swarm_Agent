import pygame
import random
import math

# Screen dimensions
WIDTH, HEIGHT = 800, 600
# Boid settings
NUM_BOIDS = 50
MAX_SPEED = 4
MAX_FORCE = 0.1
NEIGHBOR_RADIUS = 50
SEPARATION_RADIUS = 20

class Boid:
    def __init__(self, x, y):
        # Initialize position and velocity
        self.position = pygame.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * MAX_SPEED
        self.acceleration = pygame.Vector2(0, 0)

    def update(self):
        # Update velocity and position
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.position += self.velocity
        self.acceleration *= 0

        # Screen wrapping
        if self.position.x > WIDTH: self.position.x = 0
        elif self.position.x < 0: self.position.x = WIDTH
        if self.position.y > HEIGHT: self.position.y = 0
        elif self.position.y < 0: self.position.y = HEIGHT

    def apply_force(self, force):
        self.acceleration += force

    def align(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < NEIGHBOR_RADIUS:
                steering += boid.velocity
                total += 1
        if total > 0:
            steering /= total
            steering = (steering.normalize() * MAX_SPEED) - self.velocity
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering

    def cohesion(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < NEIGHBOR_RADIUS:
                steering += boid.position
                total += 1
        if total > 0:
            steering /= total
            steering = (steering - self.position).normalize() * MAX_SPEED - self.velocity
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering

    def separation(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < SEPARATION_RADIUS:
                diff = self.position - boid.position
                if distance != 0:
                    diff /= distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
        if steering.length() > 0:
            steering = steering.normalize() * MAX_SPEED - self.velocity
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering

    def flock(self, boids):
        # Apply the three main forces
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        # Weigh the forces
        self.apply_force(alignment * 1.0)
        self.apply_force(cohesion * 1.0)
        self.apply_force(separation * 1.5)

    def draw(self, screen):
        # Draw a simple triangle for the boid
        angle = math.atan2(self.velocity.y, self.velocity.x)
        points = [
            self.position + pygame.Vector2(math.cos(angle) * 10, math.sin(angle) * 10),
            self.position + pygame.Vector2(math.cos(angle + 2.5) * 10, math.sin(angle + 2.5) * 10),
            self.position + pygame.Vector2(math.cos(angle - 2.5) * 10, math.sin(angle - 2.5) * 10),
        ]
        pygame.draw.polygon(screen, (255, 255, 255), points)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Swarm Simulation")
    clock = pygame.time.Clock()

    # Create boids
    boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BOIDS)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Update and draw boids
        for boid in boids:
            boid.flock(boids)
            boid.update()
            boid.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
