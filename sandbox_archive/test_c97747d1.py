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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = set(random.sample(range(1, n + 1), 2))
            if len(clause) == 2 and clause not in clauses:
                clauses.append(clause)
        return clauses
    
    def dpll_refutation_depth(clauses):
        literals = list(range(1, n + 1))
        stack = []
        
        def backtrack():
            if not literals:
                return 0
            literal = literals.pop()
            stack.append(literal)
            new_clauses = [c for c in clauses if literal not in c]
            if not new_clauses:
                return len(stack)
            depth = backtrack()
            if depth > 0:
                return depth
            literals.append(literal)
            stack.pop()
            new_clauses = [c for c in clauses if -literal not in c]
            if not new_clauses:
                return len(stack)
            depth = backtrack()
            if depth > 0:
                return depth
            literals.append(-literal)
            stack.pop()
            return 0
        
        return backtrack()
    
    def entropic_complexity(clauses):
        truth_table_size = 2 ** n
        entropy = 0
        for i in range(truth_table_size):
            count = sum(1 for clause in clauses if all((i >> (n - var)) & 1 == val for var, val in enumerate(bin(i)[2:].zfill(n), start=1)))
            p = count / truth_table_size
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    n = random.randint(5, 40)
    k = int(0.3 * n)  # Clause-to-variable ratio of 0.3
    clauses = generate_kcnf(n, k)
    
    refutation_depth = dpll_refutation_depth(clauses)
    entropic_complexity_value = entropic_complexity(clauses)
    
    c1 = 1.0
    c2 = 2.0
    
    if refutation_depth == 0:
        return {
            "metric_name": "entropic_complexity",
            "metric_value": entropic_complexity_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL refutation depth is zero, cannot compute relationship."
        }
    
    expected_range = c1 * math.log2(2 ** refutation_depth + 1)
    margin = 0.03
    
    if not (expected_range * (1 - margin) <= entropic_complexity_value <= expected_range * (1 + margin)):
        return {
            "metric_name": "entropic_complexity",
            "metric_value": entropic_complexity_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Deviation from expected range: {abs(entropic_complexity_value - expected_range):.4f}"
        }
    
    return {
        "metric_name": "entropic_complexity",
        "metric_value": entropic_complexity_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")