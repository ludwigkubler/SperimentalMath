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
    
    def generate_k_cnf(n, k):
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(k):
            clause = random.sample(literals + [-l for l in literals], 2)
            clauses.append(clause)
        return clauses
    
    def support_of_cnf(cnf):
        support = set()
        for clause in cnf:
            for literal in clause:
                if literal.startswith('x'):
                    support.add(int(literal[1:]))
                else:
                    support.add(-int(literal[1:]))
        return sorted(support)
    
    def geometric_lattice_size(support):
        n = len(support)
        if n == 0:
            return 1
        lattice = [set([i]) for i in range(n)]
        for i in range(1, n):
            new_elements = set()
            for subset in lattice:
                for j in support[i:]:
                    new_subset = subset | {j}
                    if len(new_subset) == i + 1 and all(j not in s for s in lattice):
                        new_elements.add(new_subset)
            lattice.extend(new_elements)
        return len(lattice)
    
    def frege_proof_length(cnf):
        n = len(cnf)
        m = sum(len(clause) for clause in cnf)
        return 2 * (n + m - 1)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        k = random.randint(1, min(n * (n - 1), 100))
        cnf = generate_k_cnf(n, k)
        support = support_of_cnf(cnf)
        lattice_size = geometric_lattice_size(support)
        proof_length = frege_proof_length(cnf)
        results.append((lattice_size, proof_length))
    
    if not results:
        return {
            "metric_name": "L(C)/f(k)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    lattice_sizes, proof_lengths = zip(*results)
    mean_lattice_size = sum(lattice_sizes) / len(lattice_sizes)
    mean_proof_length = sum(proof_lengths) / len(proof_lengths)
    correlation_coefficient = 0.0
    if len(set(proof_lengths)) > 1:
        numerator = sum((l - mean_lattice_size) * (p - mean_proof_length) for l, p in results)
        denominator = math.sqrt(sum((l - mean_lattice_size) ** 2 for l in lattice_sizes)) * math.sqrt(sum((p - mean_proof_length) ** 2 for p in proof_lengths))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "L(C)/f(k)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(support_of_cnf(generate_k_cnf(40, 100))) for _ in range(5)),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_lattice_size <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")