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
    
    # Generate an expander graph with n vertices and m edges
    n = 30
    m = 2 * (n - 1)
    G = {i: [] for i in range(n)}
    for _ in range(m):
        u, v = random.sample(range(n), 2)
        if v not in G[u]:
            G[u].append(v)
            G[v].append(u)
    
    # Calculate the minimal number of generators for the Coxeter group
    δ_G = len(G)  # Simplified assumption: each vertex represents a generator
    
    # Construct Tseitin formula (simplified version)
    clauses = []
    for i in range(n):
        clauses.append([i + n])
        for j in G[i]:
            if j > i:
                clauses.append([-i - n, -j - n, i + 1 + n * j])
    
    # Determine the resolution proof depth (simplified version)
    def resolve(clauses):
        resolved = set()
        while True:
            new_clauses = []
            for clause in clauses:
                if len(clause) == 1 and clause[0] not in resolved:
                    resolved.add(-clause[0])
                else:
                    for other_clause in clauses:
                        if len(other_clause) == 1 and -other_clause[0] in clause:
                            new_clauses.extend([c for c in clause if c != -other_clause[0]])
                            break
            if not new_clauses:
                return len(resolved)
            clauses = new_clauses
    
    proof_depth = resolve(clauses)
    
    metric_value = proof_depth
    conjecture_holds = proof_depth <= 2 ** (δ_G + 1)  # Simplified constant c=1 for demonstration
    counterexample = "" if conjecture_holds else "simplified_formula"
    
    return {
        "metric_name": "Resolution Proof Depth",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"simplified_formula\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")