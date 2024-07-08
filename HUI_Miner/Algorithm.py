from itertools import combinations

def read_input_file(file_path):
    transactions = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            items = list(map(int, parts[0].split()))
            transaction_utility = int(parts[1])
            item_utilities = list(map(int, parts[2].split()))
            transactions.append((items, transaction_utility, item_utilities))
    return transactions

def calculate_utility(itemset, transaction):
    items, transaction_utility, item_utilities = transaction
    utility = 0
    for item in itemset:
        if item in items:
            index = items.index(item)
            utility += item_utilities[index]
    return utility

def find_high_utility_itemsets(transactions, min_utility):
    itemsets = {}
    
    for items, transaction_utility, item_utilities in transactions:
        for size in range(1, len(items) + 1):
            for combination in combinations(items, size):
                if combination not in itemsets:
                    itemsets[combination] = 0
                itemsets[combination] += calculate_utility(combination, (items, transaction_utility, item_utilities))
    
    high_utility_itemsets = [(itemset, utility) for itemset, utility in itemsets.items() if utility >= min_utility]
    return high_utility_itemsets

def write_output_file(file_path, high_utility_itemsets):
    with open(file_path, 'w') as file:
        for itemset, utility in high_utility_itemsets:
            line = ' '.join(map(str, itemset)) + f' #UTIL: {utility}\n'
            file.write(line)

def main():
    input_file_path = 'input.txt'
    output_file_path = 'output.txt'
    min_utility = 30
    
    transactions = read_input_file(input_file_path)
    high_utility_itemsets = find_high_utility_itemsets(transactions, min_utility)
    write_output_file(output_file_path, high_utility_itemsets)

if __name__ == '__main__':
    main()
