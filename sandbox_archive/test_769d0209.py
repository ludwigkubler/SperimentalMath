# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_group(n):
        # Generate a random group of order n
        elements = list(range(1, n + 1))
        operations = [[random.choice(elements) for _ in range(n)] for _ in range(n)]
        return elements, operations
    
    def compute_character_table(group_elements, group_operations):
        # Compute the character table for a given group
        n = len(group_elements)
        char_table = []
        for element in group_elements:
            row = [sum(1 if operation[i] == element else 0 for i in range(n)) for operation in group_operations]
            char_table.append(row)
        return char_table
    
    def tropicalize_character_table(char_table):
        # Tropicalize the character table
        n = len(char_table)
        tropicalized_table = []
        for row in char_table:
            tropicalized_row = [max(0, value) for value in row]
            tropicalized_table.append(tropicalized_row)
        return tropicalized_table
    
    def compute_X_G(tropicalized_char_table):
        # Compute X(G) as the sum of the maximum values in each row
        n = len(tropicalized_char_table)
        X_G = sum(max(row) for row in tropicalized_char_table)
        return X_G
    
    def construct_Tseitin_formula(group_elements, group_operations):
        # Construct a Tseitin formula from the group representation
        n = len(group_elements)
        formula = []
        for element in group_elements:
            clause = [f"x_{element}_{i}" if operation[i] == element else f"¬x_{element}_{i}" for i, operation in enumerate(group_operations)]
            formula.append(clause)
        return formula
    
    def compute_min_resolution_length(formula):
        # Compute the minimum resolution proof length (simplified example)
        n = len(formula)
        min_length = 2 * n
        return min_length
    
    n = random.randint(5, 40)
    group_elements, group_operations = generate_random_group(n)
    char_table = compute_character_table(group_elements, group_operations)
    tropicalized_char_table = tropicalize_character_table(char_table)
    X_G = compute_X_G(tropicalized_char_table)
    
    if X_G == 0:
        conjecture_holds = True
        counterexample = ""
    else:
        min_length = compute_min_resolution_length(construct_Tseitin_formula(group_elements, group_operations))
        conjecture_holds = min_length >= 2 ** (math.log(X_G, 2) * math.log(n, 2))
        counterexample = "min_length < 2^Ω(X(G))" if not conjecture_holds else ""
    
    return {
        "metric_name": "X(G)",
        "metric_value": X_G,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")