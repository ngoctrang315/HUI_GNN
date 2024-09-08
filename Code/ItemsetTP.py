from decimal import Decimal, ROUND_HALF_UP

class ItemsetTP:
    def __init__(self):
        self.items = []  # List of items in the itemset
        self.utility = 0  # Utility of the itemset
        self.transactions_ids = set()  # Set of transaction IDs containing this itemset

    def get_relative_support(self, nb_object):
        return len(self.transactions_ids) / nb_object

    def get_relative_support_as_string(self, nb_object):
        # Calculate the support
        frequence = Decimal(len(self.transactions_ids)) / Decimal(nb_object)
        # Format it to use four decimals
        return str(frequence.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP))

    def get_absolute_support(self):
        return len(self.transactions_ids)

    def add_item(self, value):
        self.items.append(value)

    def get_items(self):
        return self.items

    def get(self, index):
        return self.items[index]

    def print(self):
        print(self.__str__(), end='')

    def __str__(self):
        return ' '.join(map(str, self.items)) + ' '

    def set_tidset(self, list_transaction_ids):
        self.transactions_ids = list_transaction_ids

    def size(self):
        return len(self.items)

    def get_tidset(self):
        return self.transactions_ids

    def get_utility(self):
        return self.utility

    def increment_utility(self, increment):
        self.utility += increment
