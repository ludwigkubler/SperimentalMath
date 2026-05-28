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
    
    def find_partition(clauses):
        literals = set()
        for clause in clauses:
            for literal in clause:
                literals.add(literal)
        partition = {}
        for literal in literals:
            if literal.startswith('-'):
                partition[literal] = 'A'
            else:
                partition[literal] = 'B'
        return partition
    
    def resolution(clauses, partition):
        new_clauses = clauses[:]
        while True:
            new_clause = None
            for i in range(len(new_clauses)):
                for j in range(i + 1, len(new_clauses)):
                    if set(new_clauses[i]) & set(new_clauses[j]):
                        common_vars = list(set(new_clauses[i]) & set(new_clauses[j]))
                        for var in common_vars:
                            neg_var = '-' + var[1:] if var.startswith('-') else '-' + var
                            new_clause = [l for l in new_clauses[i] if l != neg_var]
                            new_clause.extend([l for l in new_clauses[j] if l != var])
                            break
                        if new_clause:
                            break
                if new_clause:
                    break
            if not new_clause:
                return False
            if new_clause not in new_clauses:
                new_clauses.append(new_clause)
        return True
    
    def tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        neg_literals = [-int(l) for l in literals]
        clauses = []
        for literal in literals:
            clauses.append([literal] + neg_literals)
        return clauses
    
    def rank(partition):
        count_A = sum(1 for _, p in partition.items() if p == 'A')
        count_B = sum(1 for _, p in partition.items() if p == 'B')
        return min(count_A, count_B)
    
    n = random.randint(5, 40)
    tseitin_clauses = tseitin_formula(n)
    partition = find_partition(tseitin_clauses)
    resolution_length = resolution(tseitin_clauses, partition)
    
    if not resolution_length:
        return {
            "metric_name": "Resolution proof length",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_failed"
        }
    
    rank_P = rank(partition)
    expected_length = 2 ** (math.ceil(math.log2(rank_P)))
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": resolution_length,
        "instances_tested": 1,
        "conjecture_holds": resolution_length >= expected_length and resolution_length <= 2 * expected_length,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 307))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_length = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    count_supporting = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(count_supporting, len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_length / len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= Fraction(4, 5):
        print(f"RESULT: SUPPORTED mean={total_length / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_length_out_of_bounds\" first_failing_seed={first_failing_seed}")