class ItemsetTP:
    def __init__(self, items, support, utility):
        self.items = items  # List of items in the itemset
        self.support = support  # Support of the itemset
        self.utility = utility  # Utility of the itemset

    def print(self):
        print("{" + ", ".join(map(str, self.items)) + "}", end="")

    def get_absolute_support(self):
        return self.support

    def get_utility(self):
        return self.utility

    def __str__(self):
        return "{" + ", ".join(map(str, self.items)) + "}"


class ItemsetsTP:
    def __init__(self, name):
        self.levels = [[]]  # List containing itemsets ordered by size
        self.itemsets_count = 0  # The number of itemsets
        self.name = name  # A name given to those itemsets

    def print_itemsets(self, transaction_count):
        print(f" ------- {self.name} -------")
        pattern_count = 0
        for level_count, level in enumerate(self.levels):
            print(f"  L{level_count} ")
            for itemset in level:
                print(f"  pattern {pattern_count}  ", end="")
                itemset.print()
                print(f" #SUP: {itemset.get_absolute_support()}", end="")
                print(f" #UTIL: {itemset.get_utility()}")
                pattern_count += 1
        print(" --------------------------------")

    def save_results_to_file(self, output, transaction_count):
        with open(output, 'w') as writer:
            for level in self.levels:
                for itemset in level:
                    writer.write(str(itemset))
                    writer.write(f" #SUP: {itemset.get_absolute_support()}")
                    writer.write(f" #UTIL: {itemset.get_utility()}\n")

    def add_itemset(self, itemset, k):
        while len(self.levels) <= k:
            self.levels.append([])
        self.levels[k].append(itemset)
        self.itemsets_count += 1

    def get_levels(self):
        return self.levels

    def get_itemsets_count(self):
        return self.itemsets_count

    def decrease_count(self):
        self.itemsets_count -= 1
