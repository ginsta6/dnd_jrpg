def action_on_target(player, enemy):
    player.use_action(0, enemy)    

def heal_target(target):
    target.status_tracker.heal(15)