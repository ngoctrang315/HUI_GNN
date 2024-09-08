import time
from collections import defaultdict
from itertools import combinations

class ItemsetTP:
    def __init__(self):
        self.items = []
        self.utility = 0
        self.transactions_ids = set()

    def add_item(self, value):
        self.items.append(value)

    def get_items(self):
        return self.items

    def size(self):
        return len(self.items)

    def get_tidset(self):
        return self.transactions_ids

    def set_tidset(self, tidset):
        self.transactions_ids = tidset

    def increment_utility(self, increment):
        self.utility += increment

    def get_utility(self):
        return self.utility

    def __repr__(self):
        return f"Itemset(items={self.items}, utility={self.utility}, tidset={self.transactions_ids})"


class ItemsetsTP:
    def __init__(self, name):
        self.name = name
        self.levels = []

    def add_itemset(self, itemset, k):
        while len(self.levels) < k:
            self.levels.append([])
        self.levels[k-1].append(itemset)

    def get_itemsets_count(self):
        return sum(len(level) for level in self.levels)

    def decrease_count(self):
        self.levels[-1].pop()

    def get_levels(self):
        return self.levels


class MemoryLogger:
    _instance = None

    @staticmethod
    def get_instance():
        if MemoryLogger._instance is None:
            MemoryLogger._instance = MemoryLogger()
        return MemoryLogger._instance

    def reset(self):
        pass

    def check_memory(self):
        pass


class AlgoTwoPhase:
    def __init__(self):
        self.high_utility_itemsets = None
        self.database = None
        self.min_utility = None
        self.start_timestamp = None
        self.end_timestamp = None
        self.candidates_count = 0

    def run_algorithm(self, database, min_utility):
        self.database = database
        self.min_utility = min_utility
        MemoryLogger.get_instance().reset()
        self.start_timestamp = time.time()

        self.high_utility_itemsets = ItemsetsTP("HIGH UTILITY ITEMSETS")
        self.candidates_count = 0

        candidates_size1 = []
        map_item_tidsets = defaultdict(set)
        map_item_twu = defaultdict(int)
        max_item = float('-inf')

        for i, transaction in enumerate(database.transactions):
            for item_utility_obj in transaction.items:
                item = item_utility_obj.item
                if item > max_item:
                    max_item = item
                map_item_tidsets[item].add(i)
                map_item_twu[item] += transaction.transaction_utility

        for item in range(max_item + 1):
            estimated_utility = map_item_twu[item]
            if estimated_utility >= min_utility:
                itemset = ItemsetTP()
                itemset.add_item(item)
                itemset.set_tidset(map_item_tidsets[item])
                candidates_size1.append(itemset)
                self.high_utility_itemsets.add_itemset(itemset, itemset.size())

        current_level = candidates_size1
        while True:
            candidate_count = self.high_utility_itemsets.get_itemsets_count()
            current_level = self.generate_candidate_size_k(current_level, self.high_utility_itemsets)
            if candidate_count == self.high_utility_itemsets.get_itemsets_count():
                break

        MemoryLogger.get_instance().check_memory()
        self.candidates_count = self.high_utility_itemsets.get_itemsets_count()

        for level in self.high_utility_itemsets.get_levels():
            iter_itemset = iter(level)
            while True:
                try:
                    candidate = next(iter_itemset)
                except StopIteration:
                    break
                candidate_utility = 0
                for transaction in database.transactions:
                    transaction_utility = 0
                    matches_count = 0
                    for item_utility in transaction.items:
                        if item_utility.item in candidate.get_items():
                            transaction_utility += item_utility.utility
                            matches_count += 1
                    if matches_count == candidate.size():
                        candidate.increment_utility(transaction_utility)
                if candidate.get_utility() < min_utility:
                    iter_itemset = self.remove_itemset(iter_itemset)

        MemoryLogger.get_instance().check_memory()
        self.end_timestamp = time.time()

        return self.high_utility_itemsets

    def generate_candidate_size_k(self, level_k_1, candidates_htwui):
        for i, itemset1 in enumerate(level_k_1):
            for j, itemset2 in enumerate(level_k_1[i+1:], start=i+1):
                for k in range(itemset1.size()):
                    if k == itemset1.size() - 1:
                        if itemset1.get_items()[k] >= itemset2.get_items()[k]:
                            break
                    elif itemset1.get_items()[k] < itemset2.get_items()[k]:
                        continue
                    elif itemset1.get_items()[k] > itemset2.get_items()[k]:
                        break
                else:
                    missing = itemset2.get_items()[-1]
                    tidset = itemset1.get_tidset().intersection(itemset2.get_tidset())
                    twu = sum(self.database.transactions[tid].transaction_utility for tid in tidset)
                    if twu >= self.min_utility:
                        candidate = ItemsetTP()
                        candidate.items = itemset1.get_items() + [missing]
                        candidate.set_tidset(tidset)
                        candidates_htwui.add_itemset(candidate, candidate.size())
        return candidates_htwui.get_levels()[-1]

    def print_stats(self):
        print("=============  TWO-PHASE ALGORITHM - STATS =============")
        print(f" Transactions count from database : {len(self.database.transactions)}")
        print(f" Candidates count : {self.candidates_count}")
        print(f" High-utility itemsets count : {self.high_utility_itemsets.get_itemsets_count()}")
        print(f" Total time ~ {(self.end_timestamp - self.start_timestamp) * 1000} ms")
        print("===================================================")


class UtilityTransactionDatabaseTP:
    def __init__(self, transactions):
        self.transactions = transactions

    def size(self):
        return len(self.transactions)


class TransactionTP:
    def __init__(self, items, transaction_utility):
        self.items = items
        self.transaction_utility = transaction_utility

    def size(self):
        return len(self.items)


class ItemUtility:
    def __init__(self, item, utility):
        self.item = item
        self.utility = utility


def create_transaction(items, utilities):
    return TransactionTP([ItemUtility(item, utility) for item, utility in zip(items, utilities)],
                         sum(utilities))


# Example usage:
if __name__ == "__main__":
    # Creating a sample database
    transactions = [
        create_transaction([1, 2, 3], [1, 2, 3]),
        create_transaction([1, 2], [1, 2]),
        create_transaction([1, 3], [1, 3]),
        create_transaction([2, 3], [2, 3]),
    ]
    database = UtilityTransactionDatabaseTP(transactions)
    
    # Running the algorithm
    algo = AlgoTwoPhase()
    high_utility_itemsets = algo.run_algorithm(database, min_utility=2)
    
    # Printing results
    algo.print_stats()
    for level in high_utility_itemsets.get_levels():
        for itemset in level:
            print(itemset)
