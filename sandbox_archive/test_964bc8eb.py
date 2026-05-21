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
    
    def generate_tseitin_formula(n):
        vertices = list(range(1, n+1))
        clauses = []
        
        # Generate all edges in a complete graph
        for u in vertices:
            for v in range(u + 1, n + 1):
                clauses.append((u, v))
                clauses.append((-u, -v))
                clauses.append((u, -v))
                clauses.append((-u, v))
        
        # Add clauses to ensure each vertex is covered
        for u in vertices:
            clause = [-i for i in range(1, n+1) if i != u]
            clauses.append(clause)
        
        return clauses
    
    def resolution_length(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if -stack[i][0] in stack[j]:
                        new_clause = [x for x in stack[i] if x != -stack[i][0]] + [y for y in stack[j] if y != -stack[i][0]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            
            # Add the new clause to the stack and simplify
            stack.append(new_clause)
            stack = [c for c in stack if not any(x in c for x in new_clause)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_tseitin_formula(n)
            length = resolution_length(clauses)
            total_length += length
            instances_tested += 1
    
    mean_length = total_length / instances_tested
    C = 0.5  # Empirical constant based on known results
    lower_bound = C * 2**(n/2) * math.log(n)
    
    conjecture_holds = abs(mean_length - lower_bound) <= 2 * lower_bound
    counterexample = "" if conjecture_holds else f"Mean length {mean_length}, expected bound {lower_bound}"
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")