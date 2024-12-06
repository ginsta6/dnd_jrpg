from character import Character

def main():
    print("Welcome to the Dungeos And Dragons Japaneese Role Playing Game Combat Encounter Player System 3000\nor DNDJRPGCEPS3000, for short\n")

    monster = Character.create_monster(2)
    print(monster)
    player = Character.create_player("./data/berserker.json")
    print(player)

    player.actions[0].use_action(monster)

    print(monster)

if __name__ == "__main__":
    main()