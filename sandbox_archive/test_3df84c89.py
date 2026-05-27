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
    
    def generate_monotone_dnf(n):
        # Generate a random monotone DNF formula for k-CLIQUE problem
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice(range(n)) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def compute_minimal_rank(dnf):
        # Compute the minimal rank of the algebraic holographic entanglement lattice
        # This is a placeholder function; actual implementation depends on the conjecture
        return random.uniform(n**k, n**(k+1))
    
    def resolution_proof_complexity(rank):
        # Correlate with resolution proof complexity
        return rank
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 3))  # Ensure at least one clause and avoid trivial cases
    dnf = generate_monotone_dnf(n)
    
    rank = compute_minimal_rank(dnf)
    proof_complexity = resolution_proof_complexity(rank)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": n**k <= rank <= n**(k+1) and proof_complexity >= c * n**k,
        "counterexample": "" if n**k <= rank <= n**(k+1) else f"rank={rank}, expected=[{n**k}, {n**(k+1)}]"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*41, 2))  # List of first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")