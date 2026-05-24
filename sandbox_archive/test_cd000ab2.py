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
    
    def generate_tseitin_formula(n, m):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(m):
            clause = random.choice(variables)
            if random.choice([True, False]):
                clause = f"~{clause}"
            clauses.append(clause)
        return variables, clauses
    
    def derive_equations(clauses):
        equations = set()
        for clause in clauses:
            if "~" in clause:
                equations.add(f"{clause[2:]} = 0")
            else:
                equations.add(f"{clause} = 1")
        return equations
    
    def compute_minimal_rank(equations):
        n = len(equations)
        rank = 0
        for i in range(n):
            if all(equations[j] != equations[i] for j in range(i+1, n)):
                rank += 1
        return rank
    
    def compute_resolution_proof_width(clauses):
        width = 0
        for clause in clauses:
            width = max(width, len(clause.split(" ")))
        return width
    
    variables, clauses = generate_tseitin_formula(40, 80)
    equations = derive_equations(clauses)
    rank = compute_minimal_rank(equations)
    proof_width = compute_resolution_proof_width(clauses)
    
    metric_name = "minimal_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= math.log(40)**2 * 80 and proof_width <= rank
    counterexample = "" if conjecture_holds else f"rank={rank}, expected>=log^2(n)*m"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")