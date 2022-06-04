class DictNode(object):
    """
    Class the represents a node in LinkedDict.

    Attributes:
        hmap (dict): data that is being held by the node.
        prev (DictNode): the next node / next highest scope.
    """

    def __init__(self, prev):
        self.hmap = {}
        self.prev = prev


class LinkedDict(object):
    """
    Class that represents a data structure that is a singly linked list of hashmaps. Each node in the
    singly linked list contains a hashmap that maps variable names to their respective values in the current
    scope. To search through higher scopes, traverse up the nodes in the linked list.

    Attributes:
        top (DictNode): the node at the top of the stack.
        bottom (DictNode): the node at the bottom of the stack.
    """

    def __init__(self):
        """Inits LinkedDict class."""
        self.top = DictNode(DictNode(None))
        self.bottom = self.top

    def get(self, key) -> object:
        """
        Gets the value corresponding to a key from the data structure. In case of duplicates,
        this function returns the value corresponding to the key with the lowest scope.
        Args:
            key (object): the key.
        Returns:
            object: the value corresponding to the key.
        Raises:
            KeyError: if the provided key is not present.
        """
        # Begins with the lowest scope.
        curr = self.top

        # Keeps looping until you reach the highest scope.
        while curr.prev != None:
            # If the key is present in the scope, return the corresponding value.
            if key in curr.hmap:
                return curr.hmap[key]

            # Otherwise, go to the next highest scope.
            curr = curr.prev

        # Throws an error if the key is not present.
        raise KeyError(str(key))

    def set(self, key, value) -> None:
        """
        Sets the value for a key that is already present in the map. In case of duplicates, 
        this function sets the value corresponding to the key with the lowest scope.
        Args:
            key (object): the key.
            value (object): the value.
        Raises:
            KeyError: if the provided key is not present.
        """
        # Begins with the lowest scope.
        curr = self.top

        # Keeps looping until you reach the highest scope.
        while curr.prev != None:
            # If the key is present in the scope, set the corresponding value and return.
            if key in curr.hmap:
                curr.hmap[key] = value
                return

            # Otherwise, go to the next highest scope.
            curr = curr.prev

        # Throws an error if the key is not present.
        raise KeyError(str(key))

    def insert(self, key, value) -> None:
        """
        Inserts a key and its corresponding value into the lowest scope.
        Args:
            key (object): the key.
            value (object): the value.
        Raises:
            Exception: if the provided key is already present in the lowest scope.
        """
        # Throw an exception if the key is already present.
        if key in self.top.hmap:
            raise Exception(f"{str(key)} in dict")

        # Otherwise insert it into the hashmap.
        self.top.hmap[key] = value

    def push(self) -> None:
        """Creates a scope beneath the currently lowest scope."""
        self.top = DictNode(self.top)

    def pop(self) -> None:
        """Removes the scope beneath the currently lowest scope."""
        self.top = self.top.prev

    def peek(self) -> dict:
        """Returns a dict of the lowest scope."""
        return self.top.hmap

    def __contains__(self, key) -> bool:
        """Checks if a value is present in the data structure."""
        # Begins with the lowest scope.
        curr = self.top

        # Keeps looping until you reach the highest scope.
        while curr.prev != None:
            # If the key is present in the scope, return True.
            if key in curr.hmap:
                return True

            # Otherwise go to the next highest scope.
            curr = curr.prev

        # If it is not present, return False.
        return False

    def __str__(self) -> str:
        """String representation of the data structure."""
        # List of all the hashmaps
        l = []

        # Begins with the lowest scope.
        curr = self.top

        # Keeps looping until you reach the highest scope.
        while curr.prev != None:
            # Append the current scope to the list.
            l.append(curr.hmap)

            # Otherwise go to the next highest scope.
            curr = curr.prev

        # Reverse the list - we want the highest scope to be first in the list.
        l.reverse()

        # Return a string representation of the list.
        return str(l)
