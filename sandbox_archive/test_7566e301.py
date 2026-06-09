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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i+1, len(clause))):
                clauses.append(clause)
        return clauses
    
    def dpll_search_tree(cnf):
        if not cnf:
            return 0
        literals = set()
        for clause in cnf:
            for literal in clause:
                literals.add(literal)
        literals = list(literals)
        n = len(literals)
        
        def backtrack(assignment, level):
            if level == n:
                return 1
            literal = literals[level]
            if literal not in assignment and -literal not in assignment:
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                count_true = backtrack(new_assignment, level + 1)
                new_assignment[literal] = False
                new_assignment[-literal] = True
                count_false = backtrack(new_assignment, level + 1)
                return count_true + count_false
            elif literal in assignment:
                return backtrack(assignment, level + 1)
            else:
                return 0
        
        return backtrack({}, 0)
    
    def entropy(n):
        if n == 0:
            return 0
        p = Fraction(1, n)
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    
    n_values = [5, 10, 15, 20, 30, 40]
    entropies = []
    for n in n_values:
        cnf = generate_cnf(n)
        tree_size = dpll_search_tree(cnf)
        if tree_size == 0:
            return {"metric_name": "entropy", "metric_value": None, "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "empty_tree"}
        entropies.append(entropy(n))
    
    mean_entropy = sum(entropies) / len(entropies)
    std_dev = math.sqrt(sum((x - mean_entropy) ** 2 for x in entropies) / len(entropies))
    log_n_values = [math.log(n) for n in n_values]
    correlation_coefficient = sum((entropies[i] - mean_entropy) * (log_n_values[i] - sum(log_n_values) / len(log_n_values)) for i in range(len(entropies))) / (len(entropies) * std_dev * math.sqrt(sum((x - sum(log_n_values) / len(log_n_values)) ** 2 for x in log_n_values)))
    
    all_within_range = all(log_n <= ent <= log_n + math.log(2) for n, log_n, ent in zip(n_values, log_n_values, entropies))
    
    return {
        "metric_name": "entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(entropies),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all_within_range,
        "counterexample": "" if correlation_coefficient >= 0.8 and all_within_range else f"correlation={correlation_coefficient}, range_check={all_within_range}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'] and r['counterexample'] != 'mapping_undefined')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_seeds_support")