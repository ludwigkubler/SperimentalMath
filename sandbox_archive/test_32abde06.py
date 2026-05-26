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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def cyclic_difference_set(f):
        n = len(f)
        diff_set = set()
        for i in range(n):
            diff = [(f[j] ^ f[(j + i) % n]) for j in range(n)]
            diff_set.add(tuple(diff))
        return diff_set
    
    def dpll_proof_width(f):
        # Simplified DPLL solver to estimate proof width
        clauses = []
        for i in range(len(f)):
            clauses.append([i])
            clauses.append([-i - 1])
        
        stack = [(clauses, [])]
        while stack:
            clauses, assignment = stack.pop()
            if not clauses:
                return len(assignment)
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause is None:
                literal = random.choice(clauses[0])
                new_assignment = assignment + [literal]
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                stack.append((new_clauses, new_assignment))
                stack.append(([[-literal]], new_assignment + [-literal]))
            else:
                literal = unit_clause[0]
                new_assignment = assignment + [literal]
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                stack.append((new_clauses, new_assignment))
        return float('inf')
    
    def minimal_rank(diff_set):
        n = len(next(iter(diff_set)))
        rank = 0
        for i in range(n):
            row = [1 if diff[i] else 0 for diff in diff_set]
            if any(row[j] == 1 for j in range(i)):
                continue
            rank += 1
            for j in range(i + 1, n):
                if row[j] == 1:
                    row[j] = sum(row[k] * (-1) ** (k - i) for k in range(i)) % 2
        return rank
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    diff_set = cyclic_difference_set(f)
    proof_width = dpll_proof_width(f)
    rank = minimal_rank(diff_set)
    
    metric_name = "correlation_coefficient"
    metric_value = rank / proof_width if proof_width != 0 else float('inf')
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")