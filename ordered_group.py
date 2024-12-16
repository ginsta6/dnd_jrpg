import pygame

class OrderedDictGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._sprites = {}  # Internal dictionary to store sprites by string keys

    def add_with_key(self, key, sprite):
        """Add a sprite with a unique string key."""
        if key not in self._sprites:
            self._sprites[key] = sprite
            super().add(sprite)

    def __getitem__(self, key):
        """Get a sprite by its key."""
        return self._sprites[key]

    def __delitem__(self, key):
        """Remove a sprite by its key."""
        sprite = self._sprites.pop(key)
        super().remove(sprite)

    def __contains__(self, key):
        """Check if a sprite with the given key exists."""
        return key in self._sprites

    def keys(self):
        """Return the keys of the dictionary."""
        return self._sprites.keys()

    def values(self):
        """Return the sprites (values) of the dictionary."""
        return self._sprites.values()

    def items(self):
        """Return the key-value pairs of the dictionary."""
        return self._sprites.items()
