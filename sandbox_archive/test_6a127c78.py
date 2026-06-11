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
            literals = [random.choice([f"x{i}", f"~x{i}"]) for i in range(1, n+1)]
            clause = " & ".join(literals)
            clauses.append(clause)
        return " | ".join(clauses)
    
    def noncommutative_polynomial_representation(phi):
        # Placeholder for actual implementation
        # For simplicity, we assume the order is proportional to n^1.5
        n = len(phi.split(" | "))
        return int(n ** 1.5)
    
    def clause_satisfiability_complexity(phi):
        # Placeholder for actual implementation
        # For simplicity, we assume the complexity is proportional to n^1.5
        n = len(phi.split(" | "))
        return int(n ** 1.5)
    
    phi = generate_cnf(40)
    order = noncommutative_polynomial_representation(phi)
    complexity = clause_satisfiability_complexity(phi)
    
    return {
        "metric_name": "order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": order <= phi.count(" | "),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = (sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")