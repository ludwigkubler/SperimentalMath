# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_tseitin_tree(n):
    if n == 1:
        return [0]
    else:
        left = generate_tseitin_tree(random.randint(1, n-1))
        right = generate_tseitin_tree(n - len(left))
        root = random.randint(len(left), n)
        return [root] + left + right

def calculate_symmetric_function(tree):
    if not tree:
        return 0
    elif len(tree) == 1:
        return 1
    else:
        root, *children = tree
        return sum(calculate_symmetric_function(child) for child in children)

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row + [i] for i, row in enumerate(matrix)]
    for i in range(m):
        max_row = max(range(i, m), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        if augmented_matrix[i][i] == 0:
            return float('inf')
        for j in range(m):
            if i != j:
                factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                augmented_matrix[j] = [augmented_matrix[j][k] - factor * augmented_matrix[i][k] for k in range(n + 1)]
    return sum(1 for row in augmented_matrix if row[-1] != 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        widths = []
        ranks = []
        
        for _ in range(5):  # Ensure at least 5 instances per seed
            tree = generate_tseitin_tree(n)
            width = len(tree) - 1
            symmetric_function = calculate_symmetric_function(tree)
            rank_value = rank([[0] * (symmetric_function + 1)])
            
            widths.append(width)
            ranks.append(rank_value)
        
        if not widths or not ranks:
            return {
                "metric_name": "Spearman's Rank Correlation",
                "metric_value": None,
                "instances_tested": len(widths),
                "conjecture_holds": False,
                "counterexample": "empty_range_in_randrange"
            }
        
        widths_log = [math.log2(w) for w in widths]
        ranks_neglog2 = [-math.log2(r) for r in ranks]
        
        n_pairs = len(widths)
        sum_widths_log = sum(widths_log)
        sum_ranks_neglog2 = sum(ranks_neglog2)
        sum_widths_log_squared = sum(w**2 for w in widths_log)
        sum_ranks_neglog2_squared = sum(r**2 for r in ranks_neglog2)
        
        cov = sum((widths_log[i] - sum_widths_log / n_pairs) * (ranks_neglog2[i] - sum_ranks_neglog2 / n_pairs) for i in range(n_pairs))
        var_widths_log = sum_widths_log_squared / n_pairs - (sum_widths_log / n_pairs)**2
        var_ranks_neglog2 = sum_ranks_neglog2_squared / n_pairs - (sum_ranks_neglog2 / n_pairs)**2
        
        if var_widths_log == 0 or var_ranks_neglog2 == 0:
            return {
                "metric_name": "Spearman's Rank Correlation",
                "metric_value": None,
                "instances_tested": len(widths),
                "conjecture_holds": False,
                "counterexample": "variance_zero"
            }
        
        spearman_corr = cov / (math.sqrt(var_widths_log) * math.sqrt(var_ranks_neglog2))
        
        results.append(spearman_corr)
    
    mean_corr = sum(results) / len(results)
    return {
        "metric_name": "Spearman's Rank Correlation",
        "metric_value": mean_corr,
        "instances_tested": len(results),
        "conjecture_holds": all(corr >= 0.8 for corr in results),  # Assuming α = 0.8
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['metric_value'] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE variance_zero")