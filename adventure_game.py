#imports
import random
import json
import numpy as np

# Configuration
MAX_HEALTH = 100
STARTING_INVENTORY = {"Gold": 10, "Potion": 1}
ENEMY_TYPES = ["Goblin", "Orc", "Troll", "Skeleton"]
LOOT_ITEMS = ["Gold", "Potion", "Magic Sword"]
SAVE_FILE = "game_progress.json"

# Helper Functions
def save_progress(players):
    with open(SAVE_FILE, "w") as file:
        json.dump([player.__dict__ for player in players], file)
    print("\nProgress saved!\n")

def load_progress():
    try:
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)
            players = []
            for player_data in data:
                player_class = globals()[player_data.pop("class_name")]
                players.append(player_class(**player_data))
            return players
    except FileNotFoundError:
        return None

# Base Player Class
class Player:
    def __init__(self, name, health, inventory, base_damage):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.base_damage = base_damage

    def show_status(self):
        print(f"\n{self.name}'s Status:")
        print(f"Health: {self.health}/{MAX_HEALTH}")
        print("Inventory:", self.inventory)

    def attack(self):
        return random.randint(self.base_damage - 5, self.base_damage + 5)

    def use_potion(self):
        if self.inventory.get("Potion", 0) > 0:
            self.health = min(self.health + 30, MAX_HEALTH)
            self.inventory["Potion"] -= 1
            print(f"\n{self.name} used a Potion! Health restored.\n")
        else:
            print("\nNo Potions left!\n")

# Specialized Classes
class Warrior(Player):
    def __init__(self, name, health=120, inventory=STARTING_INVENTORY.copy(), base_damage=20):
        super().__init__(name, health, inventory, base_damage)
        self.class_name = "Warrior"

    def special_ability(self):
        print("\n[Special Ability: Shield Block] You block the next attack completely!")

class Mage(Player):
    def __init__(self, name, health=80, inventory=STARTING_INVENTORY.copy(), base_damage=25):
        super().__init__(name, health, inventory, base_damage)
        self.class_name = "Mage"

    def special_ability(self):
        print("\n[Special Ability: Fireball] You deal a massive 50 damage!")
        return 50

class Rogue(Player):
    def __init__(self, name, health=90, inventory=STARTING_INVENTORY.copy(), base_damage=15):
        super().__init__(name, health, inventory, base_damage)
        self.class_name = "Rogue"

    def special_ability(self):
        print("\n[Special Ability: Critical Strike] You deal double damage on your next attack!")
        return self.attack() * 2

# Enemy Class
class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

    def attack(self):
        return random.randint(5, self.damage)

# Game Functions
def encounter_enemy(players):
    enemy_name = random.choice(ENEMY_TYPES)
    enemy_health = random.randint(50, 100)
    enemy_damage = random.randint(15, 25)
    enemy = Enemy(enemy_name, enemy_health, enemy_damage)

    print(f"\nA wild {enemy.name} appeared! It has {enemy.health} HP.")

    while enemy.health > 0 and any(player.health > 0 for player in players):
        for player in players:
            if player.health <= 0:
                continue  # Skip players with 0 health

            print(f"\n{player.name}'s Turn:")
            print("Choose your action:")
            print("1. Attack")
            print("2. Use Potion")
            print("3. Use Special Ability")
            print("4. Pass")

            action = input("> ").strip()
            if action == "1":
                damage = player.attack()
                enemy.health -= damage
                print(f"\n{player.name} dealt {damage} damage to the {enemy.name}. Its health is now {enemy.health}.")
            elif action == "2":
                player.use_potion()
            elif action == "3":
                if isinstance(player, Mage):
                    damage = player.special_ability()
                    enemy.health -= damage
                elif isinstance(player, Rogue):
                    damage = player.special_ability()
                    enemy.health -= damage
                    print(f"\nCritical Strike! {player.name} dealt {damage} damage.")
                elif isinstance(player, Warrior):
                    player.special_ability()
                    continue  # Skip enemy attack
            elif action == "4":
                print(f"\n{player.name} passed their turn.")

            if enemy.health <= 0:
                print(f"\nYou defeated the {enemy.name}!")
                loot = random.choice(LOOT_ITEMS)
                player.inventory[loot] = player.inventory.get(loot, 0) + 1
                print(f"\nYou found {loot} in the loot!")
                return

            # Enemy attacks after each player's turn
            player.health -= enemy.attack()
            print(f"The {enemy.name} attacked {player.name}! Their health is now {player.health}.")

            if player.health <= 0:
                print(f"\n{player.name} has been defeated!")

    if all(player.health <= 0 for player in players):
        print("\nYour entire team has been defeated! Game over.")
        exit()

def explore(players):
    print("\nYou are exploring the Mystic Lands...")
    if random.random() < 0.6:  # 60% chance of encounter
        encounter_enemy(players)
    else:
        event = random.choice(["treasure", "trap", "nothing"])
        if event == "treasure":
            player = random.choice(players)
            loot = random.choice(LOOT_ITEMS)
            player.inventory[loot] = player.inventory.get(loot, 0) + 1
            print(f"\n{player.name} found a {loot}!")
        elif event == "trap":
            player = random.choice(players)
            damage = random.randint(10, 20)
            player.health -= damage
            print(f"\n{player.name} triggered a trap and lost {damage} health!")
        else:
            print("\nYou found nothing this time.")

def choose_class(name):
    print("\nChoose your class:")
    print("1. Warrior - High health and decent attack.")
    print("2. Mage - Low health but powerful spells.")
    print("3. Rogue - Balanced stats with critical strikes.")

    while True:
        choice = input("> ").strip()
        if choice == "1":
            return Warrior(name)
        elif choice == "2":
            return Mage(name)
        elif choice == "3":
            return Rogue(name)
        else:
            print("\nInvalid choice. Try again.")

def main():
    print("Welcome to Legends of the Mystic Lands!")

    # Load progress or create new game
    players = load_progress()
    if players:
        print("\nSaved progress found! Loading game...\n")
    else:
        print("\nNo saved progress found. Starting a new game...\n")
        players = []
        for i in range(2):
            name = input(f"Enter Player {i + 1}'s name: ")
            players.append(choose_class(name))

    # Game loop
    while True:
        for player in players:
            player.show_status()

        print("\nWhat would you like to do?")
        print("1. Explore")
        print("2. Save Progress")
        print("3. Exit")

        choice = input("> ").strip()
        if choice == "1":
            explore(players)
        elif choice == "2":
            save_progress(players)
        elif choice == "3":
            print("\nGoodbye, adventurers!")
            break
        else:
            print("\nInvalid choice. Try again.")

# Start the game
if __name__ == "__main__":
    main()
