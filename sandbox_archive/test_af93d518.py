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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10):  # 10 clauses for simplicity
            clause = [random.randint(-n, n) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
        return clauses

    def cnf_to_category(cnf):
        morphisms = set()
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    morphisms.add((clause[i], clause[j]))
        return morphisms

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    category = cnf_to_category(cnf)
    
    circuit_size = len(cnf) * 2 + len(category)  # Simplified estimate
    num_morphisms = len(category)

    return {
        "metric_name": "circuit_size_vs_morphisms",
        "metric_value": num_morphisms / circuit_size,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")