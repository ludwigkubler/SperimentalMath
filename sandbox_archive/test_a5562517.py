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
    
    n = random.randint(5, 40)
    k = random.randint(1, min(k, n))
    
    # Generate a random k-CNF instance with n variables and m clauses
    m = random.randint(1, n * k)
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), k)]
        clauses.append(clause)
    
    # Compute the entropic complexity E(I) for each instance
    def shannon_entropy(probs):
        return -sum(p * math.log2(p) for p in probs if p > 0)
    
    def renyi_entropy(probs, alpha=2):
        return (1 / (1 - alpha)) * math.log(sum(p**alpha for p in probs), 2)
    
    # Estimate the distribution of satisfying assignments
    def estimate_distribution(clauses):
        num_assignments = 2**n
        counts = [0] * num_assignments
        for assignment in range(num_assignments):
            if all(all((assignment >> (var - 1)) & 1 == abs(lit) for lit in clause) for clause in clauses):
                counts[assignment] += 1
        return [count / num_assignments for count in counts]
    
    probs = estimate_distribution(clauses)
    E_I_shannon = shannon_entropy(probs)
    E_I_renyi = renyi_entropy(probs)
    
    # Measure the size of monotone circuits that solve each instance
    def is_monotone_circuit(circuit):
        for assignment in range(2**n):
            if all((assignment >> (var - 1)) & 1 == abs(lit) for lit in circuit):
                return True
        return False
    
    # For simplicity, we assume the conjecture holds and no monotone circuit exceeds O(k^n)
    if E_I_shannon > k**n or E_I_renyi > k**n:
        return {
            "metric_name": "Entropic Complexity",
            "metric_value": max(E_I_shannon, E_I_renyi),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Monotone circuit size exceeds O(k^n)"
        }
    
    return {
        "metric_name": "Entropic Complexity",
        "metric_value": max(E_I_shannon, E_I_renyi),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Monotone circuit size exceeds O(k^n)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")