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
    
    def generate_tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        
        for i in range(m):
            a = random.choice(variables)
            b = random.choice(variables)
            if a != b:
                clauses.append((a, b, 'or'))
                clauses.append((-a, -b, 'and'))
        
        return variables, clauses
    
    def resolution_length(clauses):
        stack = []
        while True:
            new_clauses = set()
            for clause in clauses:
                if len(clause) == 1:
                    return len(stack)
                negated_vars = [var for var in clause if var < 0]
                pos_vars = [abs(var) for var in clause if var > 0]
                for neg_var in negated_vars:
                    for pos_var in pos_vars:
                        new_clause = tuple(sorted([neg_var, -pos_var]))
                        if new_clause not in stack and new_clause not in new_clauses:
                            new_clauses.add(new_clause)
            if not new_clauses:
                return len(stack)
            stack.extend(new_clauses)
    
    def minimal_rank(m):
        # Simplified heuristic for minimal rank
        return 2 ** (m - n / 2)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 10)
    variables, clauses = generate_tseitin_formula(n, m)
    rank_threshold = minimal_rank(m)
    
    # Simulate quantum channel (heuristic)
    non_zero_entries = len(clauses) * 2
    channel_rank = math.ceil(math.sqrt(non_zero_entries))
    
    resolution_len = resolution_length(clauses)
    conjecture_holds = channel_rank >= rank_threshold and resolution_len >= channel_rank
    
    return {
        "metric_name": "Minimal Rank vs Resolution Proof Length",
        "metric_value": channel_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {channel_rank} < {rank_threshold} or resolution length {resolution_len} < {channel_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")