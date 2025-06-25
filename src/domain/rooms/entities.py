from enum import Enum

class RoomType(Enum):
    STANDARD = 50
    SUPERIOR = 100
    SUITE = 200

    def description(self) -> list[str]:
        descriptions = {
            RoomType.STANDARD: ["1 Single Bed", "WiFi", "TV"],
            RoomType.SUPERIOR: ["1 Double Bed", "WiFi", "Flat TV", "Minibar", "AC"],
            RoomType.SUITE: ["1 Double Bed", "WiFi", "Flat TV", "Minibar", "AC", "Bathtub", "Terrace"],
        }
        return descriptions[self]

    def display_info(self):
        print(f"{self.name.capitalize()} Room: {self.value}€ per night")
        for item in self.description():
            print(f" - {item}")
