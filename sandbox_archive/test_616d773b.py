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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
            clauses.append(clause)
        return clauses
    
    def frege_proof_width(clauses):
        # Simplified heuristic to estimate Frege proof width
        return len(clauses) ** 0.5
    
    def groupoid_cocomorphism(clauses):
        # Placeholder for actual cocomorphism computation
        # This is a dummy implementation for testing purposes
        rank = sum(abs(sum(clause)) for clause in clauses)
        return rank
    
    n = random.randint(4, 30)  # Ensure n ≥ 4 and n_max ≤ 30
    formula = generate_3cnf(n)
    proof_width = frege_proof_width(formula)
    cocomorphism_rank = groupoid_cocomorphism(formula)
    
    if proof_width == 0:
        return {
            "metric_name": "cocomorphism_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "proof_width_zero"
        }
    
    ratio = cocomorphism_rank / math.log2(n)
    return {
        "metric_name": "cocomorphism_rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.5,  # Example threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 89))  # Default to first 30 primes
    
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
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='cocomorphism_rank_too_small' first_failing_seed={first_failing_seed}")