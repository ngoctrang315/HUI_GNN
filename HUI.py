def read_input_file(input_file):
    transactions = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(':')
                items = list(map(int, parts[0].split()))
                transaction_utility = int(parts[1])
                item_utilities = list(map(int, parts[2].split()))
                transactions.append((items, transaction_utility, item_utilities))
    return transactions

def write_output_file(output_file, high_utility_itemsets):
    with open(output_file, 'w') as f:
        for itemset, utility in high_utility_itemsets:
            f.write(' '.join(map(str, itemset)) + f' #UTIL: {utility}\n')

def find_high_utility_itemsets(transactions, min_utility):
    high_utility_itemsets = []
    item_utility_sum = {}
    
    for transaction in transactions:
        items, transaction_utility, item_utilities = transaction
        
        # Calculate total utility of each item in the transaction
        for item, utility in zip(items, item_utilities):
            if item in item_utility_sum:
                item_utility_sum[item] += utility
            else:
                item_utility_sum[item] = utility
        
        # Check itemsets with minimum utility
        for item in sorted(item_utility_sum.keys()):
            if item_utility_sum[item] >= min_utility:
                high_utility_itemsets.append(([item], item_utility_sum[item]))
    
    return high_utility_itemsets

# Example usage:
if __name__ == '__main__':
    input_file = 'input.txt'
    output_file = 'output.txt'
    min_utility = 30
    
    transactions = read_input_file(input_file)
    high_utility_itemsets = find_high_utility_itemsets(transactions, min_utility)
    write_output_file(output_file, high_utility_itemsets)
