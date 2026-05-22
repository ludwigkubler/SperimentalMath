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
    
    def generate_k_clique_dnf(n, k):
        if n < k or k == 0:
            return None
        vertices = list(range(n))
        edges = random.sample(list(itertools.combinations(vertices, 2)), k * (n - k) // 2)
        dnf_formula = []
        for edge in edges:
            clause = [f"x{i+1}" if i != edge[0] else f"-x{i+1}" for i in vertices]
            dnf_formula.append(" & ".join(clause))
        return " | ".join(dnf_formula)

    def tropical_matroid_rank(dnf):
        if not dnf:
            return 0
        clauses = dnf.split(' | ')
        matroid_elements = set()
        for clause in clauses:
            literals = clause.split(' & ')
            for literal in literals:
                if literal.startswith('-'):
                    matroid_elements.add(literal[1:])
                else:
                    matroid_elements.add(literal)
        rank = 0
        for element in matroid_elements:
            if all(element not in clause for clause in clauses):
                rank += 1
        return rank

    n = random.randint(5, 40)
    dnf = generate_k_clique_dnf(n, n // 2)
    if dnf is None:
        return {
            "metric_name": "tropical_matroid_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "n too small for k-CLIQUE"
        }
    rank = tropical_matroid_rank(dnf)
    lower_bound = math.ceil(math.sqrt(n))
    
    return {
        "metric_name": "tropical_matroid_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= lower_bound,
        "counterexample": "" if rank >= lower_bound else f"Rank {rank} < {lower_bound}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank too low\" first_failing_seed={first_failing_seed}")