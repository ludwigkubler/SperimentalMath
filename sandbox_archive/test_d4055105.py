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
    
    def generate_random_boolean_function(n, m):
        return [[random.randint(0, 1) for _ in range(m)] for _ in range(2**n)]
    
    def xor_and_tree_width(f):
        n = len(f)
        m = len(f[0])
        
        def evaluate(x, y):
            if x == y:
                return f[x][y]
            else:
                return 1
        
        def xor_and(a, b):
            result = 0
            for i in range(m):
                result |= evaluate(a, i) & evaluate(b, i)
            return result
        
        def count_ones(x):
            return bin(x).count('1')
        
        def dfs(node, visited):
            if node in visited:
                return 0
            visited.add(node)
            max_width = 0
            for child in range(m):
                if evaluate(node, child) == 1:
                    max_width = max(max_width, dfs(child, visited))
            return 1 + max_width
        
        visited = set()
        return dfs(0, visited)
    
    def count_quadratic_residues(p, values):
        residues = [i**2 % p for i in range(p)]
        return sum(value in residues for value in values)
    
    n = 40
    m = n
    f = generate_random_boolean_function(n, m)
    t_f = xor_and_tree_width(f)
    
    if t_f == 0:
        return {
            "metric_name": "XOR-AND tree width",
            "metric_value": t_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    p = next((i for i in range(t_f + 1, 2 * t_f) if all(i % j != 0 for j in range(2, int(math.sqrt(i)) + 1))), None)
    if p is None:
        return {
            "metric_name": "XOR-AND tree width",
            "metric_value": t_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    values = [f[i][j] for i in range(2**n) for j in range(m)]
    num_residues = count_quadratic_residues(p, values)
    
    return {
        "metric_name": "XOR-AND tree width",
        "metric_value": t_f,
        "instances_tested": 1,
        "conjecture_holds": t_f <= math.sqrt(p),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")