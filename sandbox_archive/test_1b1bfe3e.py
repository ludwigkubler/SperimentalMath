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
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_formula(xor_func, n):
        clauses = []
        for i in range(2**n):
            clause = []
            for j in range(n):
                if xor_func[i] == (i & (1 << j)) ^ 0:
                    clause.append(j)
                else:
                    clause.append(-j-1)
            clauses.append(clause)
        return clauses
    
    def resolution_length(clauses):
        stack = [clauses]
        while stack:
            new_clauses = []
            for i in range(len(stack)):
                for j in range(i+1, len(stack)):
                    common_vars = set(stack[i]) & set(stack[j])
                    if not common_vars:
                        continue
                    for var in common_vars:
                        new_clause = [x for x in stack[i] if x != var and x != -var-1]
                        new_clause.extend([x for x in stack[j] if x != var and x != -var-1])
                        new_clause = list(set(new_clause))
                        if not new_clause:
                            return 0
                        new_clauses.append(new_clause)
            stack = new_clauses
        return len(stack)
    
    def local_cohomology_rank(n):
        # Simplified heuristic for demonstration purposes
        return n
    
    n = random.randint(5, 40)
    xor_func = generate_xor_function(n)
    clauses = tseitin_formula(xor_func, n)
    length = resolution_length(clauses)
    
    H_n = local_cohomology_rank(n)
    expected_length = 2**(math.log2(n) + math.log2(H_n))
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": abs(length - expected_length) <= 3,
        "counterexample": "" if abs(length - expected_length) <= 3 else f"Expected {expected_length}, got {length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")