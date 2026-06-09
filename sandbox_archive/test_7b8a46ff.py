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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_search_tree(cnf):
        if not cnf:
            return 1
        literals = set(abs(lit) for lit in cnf[0])
        if len(literals) == 1:
            return 2 ** (len(cnf) - 1)
        else:
            return sum(dpll_search_tree([lit for lit in clause if lit != literal] for clause in cnf if literal in clause) 
                       + dpll_search_tree([lit for lit in clause if lit != -literal] for clause in cnf if -literal in clause) 
                       for literal in literals)
    
    def entropy(n):
        return n.bit_length() - 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    entropies = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        tree_size = dpll_search_tree(cnf)
        entropies.append(entropy(tree_size))
    
    mean_entropy = sum(entropies) / len(entropies)
    std_dev = math.sqrt(sum((x - mean_entropy) ** 2 for x in entropies) / len(entropies))
    
    log_n_values = [Fraction(n).log() for n in n_values]
    log_n_minus_3_values = [log_n - Fraction(3).log() for log_n in log_n_values]
    log_2n_values = [log_n + Fraction(1).log() for log_n in log_n_values]
    
    conjecture_holds = all(log_n >= log_n_minus_3 <= entropy_value <= log_2n 
                           for log_n, log_n_minus_3, log_2n, entropy_value 
                           in zip(log_n_values, log_n_minus_3_values, log_2n_values, entropies))
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")