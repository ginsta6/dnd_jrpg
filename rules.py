class Ruleset():
    default_attributes = {
    "can_see": True, # Cant target enemies
    "can_speak": True, # Cant cast spells 
    "can_take_actions": True, # Cant do anything
    "can_take_reactions": True, # cant react (might not implement)
    "can_be_seen": True, # Cant be targeted by others
    "attack_advantage": False, 
    "attack_disadvantage": False,
    "check_advantage": False,
    "check_disadvantage": False,
    "critical_hits": False, # Auto crits on me
    "attackers_have_advantage": False,
    "attackers_have_disadvantage": False,
    "automatic_fail_str_and_dex_saves": False,
    "resistance_to_all_damage": False,
    }

    conditions = {
        "Blinded": {
            "can_see": False,
            "attack_disadvantage": True,
            "melee_attackers_have_advantage": True,
            "ranged_attackers_have_advantage": True
        },
        "Incapacitated": {
                "can_take_actions": False,
                "can_take_reactions": False
        },
        "Invisible": {
                "can_be_seen": False,
                "attackers_have_disadvantage": True,
                "attack_advantage": True
        },
        "Paralyzed": { # Same as unconscious 
                "can_move": False,
                "can_speak": False,
                "can_take_actions": False,
                "can_take_reactions": False,
                "automatic_fail_str_and_dex_saves": True,
                "attackers_have_advantage": True,
                "critical_hits": True
        },
        "Petrified": {
                "can_move": False,
                "can_take_actions": False,
                "can_take_reactions": False,
                "resistance_to_all_damage": True,
        },
        "Poisoned": {
                "attack_disadvantage": True,
                "check_disadvantage": True
        },
        "Restrained": {
                "can_move": False,
                "attack_disadvantage": True,
                "attackers_have_advantage": True,
        },
        "Stunned": {
                "can_move": False,
                "can_speak": False,
                "can_take_actions": False,
                "can_take_reactions": False,
                "automatic_fail_str_and_dex_saves": True,
                "attackers_have_advantage": True
        }
    }
