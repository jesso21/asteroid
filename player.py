import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:

        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen: pygame.Surface) -> None:
        color = "white"
        points = self.triangle()
        width = LINE_WIDTH
        pygame.draw.polygon(screen, color, points, width)

    def rotate(self, dt):
        return PLAYER_TURN_SPEED * dt
    
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.cooldown_timer -= dt

        if keys[pygame.K_a]:
            self.rotation += self.rotate(dt)
        if keys[pygame.K_d]:
            self.rotation -= self.rotate(dt)
        if keys[pygame.K_w]:
            self.position += self.move(dt)
        if keys[pygame.K_s]:
            self.position -=self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        return rotated_vector * PLAYER_SPEED * dt
    
    def shoot(self):
        if self.cooldown_timer > 0:
            pass
        else:
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            direction = pygame.Vector2(0,1)
            direction = direction.rotate(self.rotation)
            shot.velocity = direction * PLAYER_SHOOT_SPEED
            self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
