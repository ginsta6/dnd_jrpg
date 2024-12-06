from random import randint
import re

class Dice():

    @classmethod
    def roll_dice(cls, dice_input: str = "1d20", amount: int = None, sides: int = None) -> int:
        """Rolls dice based on input.
        
        Args:
            dice_input (str): A string in the format 'XdY' (e.g., '2d6').
            amount (int): The number of dice to roll (optional).
            sides (int): The sides of dice to roll (optional).
        
        Returns:
            int: The total result of the dice rolls.
        """
        # If amount and sides are provided, use them
        if amount is not None and sides is not None:
            return sum(randint(1, sides) for _ in range(amount))
        
        # Parse dice_input for 'XdY+Z' or 'XdY-Z' format
        match = re.fullmatch(r"(\d+)d(\d+)([+-]\d+)?", dice_input.strip())
        if not match:
            raise ValueError("Invalid dice format. Use 'XdY+Z' or 'XdY-Z' (e.g., '2d6+4').")
        
        amount = int(match.group(1))  # Number of dice
        sides = int(match.group(2))   # Dice sides
        modifier = int(match.group(3)) if match.group(3) else 0  # Modifier (if present)
        
        # Roll the dice and add the modifier
        total = sum(randint(1, sides) for _ in range(amount))

        print(f"Rolled {total + modifier}")
        return total + modifier