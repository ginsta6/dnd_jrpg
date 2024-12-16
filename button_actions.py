awaiting_target = False

def action_on_target(player, enemy):
    player.use_action(0, enemy)
    player.apply_condition("Blinded")
    print(player.get_status())

def heal_target(target):
    target.status_tracker.heal(15)