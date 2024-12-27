def action_on_target(player, enemy):
    return player.use_action(0, enemy) + f" against {enemy.character._name}"
    

def heal_target(target):
    target.status_tracker.heal(15)