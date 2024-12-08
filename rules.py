class Ruleset():
    CONDITIONS = {
        "Blinded": "Cannot see, automatically fails checks requiring sight, attack rolls against have advantage, and attacks by have disadvantage.",
        "Charmed": "Cannot attack or target charmer with harmful abilities or magic; charmer has advantage on social interactions.",
        "Deafened": "Cannot hear and automatically fails checks requiring hearing.",
        "Exhaustion": "Six levels with cumulative penalties, from disadvantage on ability checks to death.",
        "Frightened": "Cannot willingly move closer to the source of fear; has disadvantage on ability checks and attack rolls while it's in sight.",
        "Grappled": "Speed becomes 0; cannot benefit from bonuses to speed. Ends if grappler is incapacitated or moved away.",
        "Incapacitated": "Cannot take actions or reactions.",
        "Invisible": "Cannot be seen without special senses; attacks against have disadvantage, and attacks by have advantage.",
        "Paralyzed": "Incapacitated and cannot move or speak. Automatically fails Strength and Dexterity saves. Attack rolls against have advantage, and hits within 5 ft are critical.",
        "Petrified": "Transformed into stone, is incapacitated, and has resistance to all damage. Immune to poison and disease, but such effects are suspended.",
        "Poisoned": "Has disadvantage on attack rolls and ability checks.",
        "Prone": "Can only crawl unless standing up. Attack rolls against have advantage if attacker is within 5 ft; otherwise, they have disadvantage.",
        "Restrained": "Speed is 0, attacks against have advantage, and attacks by have disadvantage. Disadvantage on Dexterity saving throws.",
        "Stunned": "Incapacitated, cannot move, and can barely speak. Automatically fails Strength and Dexterity saves. Attack rolls against have advantage.",
        "Unconscious": "Incapacitated, prone, and unaware of surroundings. Drops what is holding. Automatically fails Strength and Dexterity saves. Attack rolls against have advantage, and hits within 5 ft are critical."
    }