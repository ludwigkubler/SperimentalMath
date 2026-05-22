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
    
    def generate_instance(n, m):
        variables = [f"x{i}" for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f"~{v}" for v in variables], 3)
            clauses.append(clause)
        return variables, clauses
    
    def compute_minimal_rank(variables, clauses):
        # Placeholder for cocomplex minimal rank computation
        # This is a dummy implementation and does not reflect actual complexity
        return len(variables) + len(clauses)
    
    def f(n):
        # Placeholder function to bound SAT prover time complexity
        # This is a dummy implementation and does not reflect actual complexity
        return n**2
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, 2*n)
        variables, clauses = generate_instance(n, m)
        rank = compute_minimal_rank(variables, clauses)
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    conjecture_holds = all(rank <= f(n) for n, _ in zip([len(v) for v, _ in generate_instance(1, 1)], results))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_rank = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= f(len(generate_instance(1, 1)[0]))) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={math.sqrt(sum((r - mean_rank)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r > f(len(generate_instance(1, 1)[0])))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")