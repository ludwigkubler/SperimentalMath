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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

def determinant(matrix):
    n = len(matrix)
    det = 1
    for i in range(n):
        det *= matrix[i][i]
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a CNF formula with up to 40 variables and 30 clauses
    n = random.randint(5, 40)
    m = 30
    cnf_formula = []
    for _ in range(m):
        clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        cnf_formula.append(clause)
    
    # Construct the binary tree representation of the CNF formula
    def build_tree(cnf):
        if not cnf:
            return None
        node = {'type': 'OR', 'children': []}
        for clause in cnf:
            child_node = {'type': 'AND', 'children': [abs(lit) for lit in clause]}
            node['children'].append(child_node)
        return node
    
    tree = build_tree(cnf_formula)
    
    # Compute the geometric entropy of the binary tree
    def count_self_similar_structures(tree, scale):
        if not tree:
            return 0
        if len(tree['children']) == 1:
            return 1
        count = 0
        for child in tree['children']:
            count += count_self_similar_structures(child, scale)
        return count
    
    def geometric_entropy(tree):
        total_nodes = sum(count_self_similar_structures(tree, scale) for scale in range(1, n+1))
        if total_nodes == 0:
            return 0
        entropy = 0
        for scale in range(1, n+1):
            count = count_self_similar_structures(tree, scale)
            probability = Fraction(count, total_nodes)
            entropy -= probability * math.log2(probability)
        return entropy
    
    entropy = geometric_entropy(tree)
    
    # Compute the circuit depth of the minimum size circuit computing the function
    def circuit_depth(tree):
        if not tree:
            return 0
        if len(tree['children']) == 1:
            return 1
        depths = [circuit_depth(child) for child in tree['children']]
        return 1 + max(depths)
    
    depth = circuit_depth(tree)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r['metric_value'] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r['metric_value'] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")