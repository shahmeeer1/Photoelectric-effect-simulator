import pygame
from state.statemachine import StateMachine

def main():
    pygame.init()
    sim = StateMachine()
    sim.run()


if __name__ == "__main__":
    main()