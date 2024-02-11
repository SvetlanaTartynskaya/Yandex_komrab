import pygame
import requests
import sys

STATIC_API_SERVER = "https://static-maps.yandex.ru/1.x/"


def get_map_from_coords(coords, spn, type_in=str):
    params = {
        "ll": coords if type_in is str else ",".join(coords),
        "spn": f"{spn[0]},{spn[1]}",
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
        self.label_font = pygame.font.SysFont('Arial', 24)
        self.draw_label()
        pygame.display.flip()
        self.coords = input('ВВЕДИТЕ КООРДИНАТЫ В ФОРМАТЕ (ШИРОТА,ДОЛГОТА): ').replace(' ', '').split(',')
        self.spn = (0.05, 0.05)
        self.scale = 1.1

    def search(self, coords):
        image = get_map_from_coords(coords, self.spn, type_in=list)
        if image:
            self.map = pygame.image.load(image)
            self.map = pygame.transform.scale(self.map, self.screen.get_size())

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.map, (0, 0))

    def draw_label(self):
        label_text = "Введите координаты в консоль Python"
        label_surface = self.label_font.render(label_text, True, (0, 0, 0))
        self.screen.blit(label_surface, (10, 10))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    print(1)
                    if self.scale < 2:
                        self.scale += 0.1
                    self.spn = (self.spn[0] * self.scale, self.spn[1] * self.scale)
                    self.search(self.coords)
                    self.draw()
                    pygame.display.flip()
                if event.key == pygame.K_PAGEDOWN:
                    if self.scale > 1:
                        self.scale -= 0.1
                    self.spn = (self.spn[0] * (self.scale % 1), self.spn[1] * (self.scale % 1))
                    self.search(self.coords)
                    self.draw()
                    pygame.display.flip()

    def run(self):
        self.search(self.coords)
        while True:
            self.update()
            self.draw()
            pygame.display.flip()


widget = Map()
widget.run()
