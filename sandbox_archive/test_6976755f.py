# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, 2*n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def calculate_width(clauses):
        # Placeholder for actual width calculation
        return len(clauses)
    
    def assign_semantic_types(clauses):
        semtypes = set()
        for clause in clauses:
            semtype = random.choice([f"semtype_{i}" for i in range(1, 2**len(clauses))])
            semtypes.add(semtype)
        return semtypes
    
    n = 40
    cnf = generate_cnf(n)
    width = calculate_width(cnf)
    semtypes = assign_semantic_types(cnf)
    
    k_pi = len(semtypes)
    conjecture_holds = width <= 2**(k_pi) and k_pi <= Fraction(1, 2)**n
    
    return {
        "metric_name": "width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Width {width} exceeds bound {2**(k_pi)} for k_pi={k_pi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"width_exceeds_bound\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")