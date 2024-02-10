import pygame
import requests
import sys

STATIC_API_SERVER = "https://static-maps.yandex.ru/1.x/"


def get_map_from_coords(coords, type_in=str):
    params = {
        "ll": coords if type_in is str else ",".join(coords),
        "spn": "0.05,0.05",
        "l": "map"
    }
    res = requests.request(method="GET", url=STATIC_API_SERVER, params=params)
    if res.status_code == 200:
        with open('map_image.png', 'wb') as f:
            f.write(res.content)
        return 'map_image.png'
    return None


class Map:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 400))
        self.map = pygame.Surface((400, 400))
        self.coords = input().replace(' ', '').split(',')

    def search(self, coords):
        image = get_map_from_coords(coords, type_in=list)
        if image:
            self.map = pygame.image.load(image)
            self.map = pygame.transform.scale(self.map, self.screen.get_size())

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.map, (0, 0))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        self.search(self.coords)
        while True:
            self.update()
            self.draw()
            pygame.display.flip()


widget = Map()
widget.run()