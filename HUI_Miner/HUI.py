def read_input_file(input_file):
    transactions = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                items_part, transactions_utility, utilities_part = line.split(':')
                items = list(map(int, items_part.split()))
                transaction_utility = int(transactions_utility)
                item_utilities = list(map(int, utilities_part.split()))
                transactions.append((items, transaction_utility, item_utilities))
   # print(f"Transactions: {transactions}------read")  # Debug print
    return transactions

def construct_utility_list(P_UL, Px_UL, Py_UL):
    Pxy_UL = []
    for Ex in Px_UL:
        for Ey in Py_UL:
            if Ex[0] == Ey[0]:  # Check if same transaction ID
                if P_UL:
                    E = next((E for E in P_UL if E[0] == Ex[0]), None)
                    if E:
                        Exy = (Ex[0], Ex[1] + Ey[1] - E[1], Ey[2])
                    else:
                        Exy = (Ex[0], Ex[1] + Ey[1], Ey[2])
                else:
                    Exy = (Ex[0], Ex[1] + Ey[1], Ey[2])
                Pxy_UL.append(Exy)
    print(f"Constructed Utility List: {Pxy_UL}----Pxy")  # Debug print
    return Pxy_UL

def huiminer(P_UL, ULs, minutil, high_utility_itemsets):
    for X in ULs:
        if all(len(Ex) > 1 for Ex in X):  # Ensure all elements have at least two parts
            sum_iutils = sum(Ex[1] for Ex in X)
           # print(f"Sum of item utilities: {sum_iutils}----util")  # Debug print
            if sum_iutils >= minutil:
                for Ex in X:
                    print(f"{Ex[0]} #UTIL: {Ex[1]}")
                    high_utility_itemsets.append((Ex[0], Ex[1]))
            sum_total_utils = sum(Ex[1] for Ex in X) + sum(sum(Ex[2]) for Ex in X)
           # print(f"Sum of total utilities: {sum_total_utils}")  # Debug print

            if sum_total_utils >= minutil:
                exULs = []
                for Y in ULs[ULs.index(X)+1:]:
                    exULs.extend(construct_utility_list(P_UL, X, Y))
                huiminer(X, exULs, minutil, high_utility_itemsets)
            
def write_output_file(output_file, itemsets):
    with open(output_file, 'w') as f:
        for itemset in itemsets:
            items = ' '.join(map(str, itemset[0]))
            utility = itemset[1]
            f.write(f"{items} #UTIL: {utility}\n")

if __name__ == "__main__":
    input_file = 'input.txt'
    output_file = 'output.txt'
    min_utility = 30
    
    transactions = read_input_file(input_file)
    
    # Implement HUI-Miner algorithm to find high utility itemsets
    P_UL = []
    ULs = []
    for transaction in transactions:
        items, transaction_utility, item_utilities = transaction
        P_UL.append((items, transaction_utility, item_utilities))
        extension_UL = [(items[i:], transaction_utility, item_utilities[i:]) for i in range(len(items))]
        ULs.append(extension_UL)
    
    high_utility_itemsets = []
    huiminer(P_UL, ULs, min_utility, high_utility_itemsets)
    
    # Write results to output file
    write_output_file(output_file, high_utility_itemsets)
    print(f"High utility itemsets found and written to '{output_file}'")
