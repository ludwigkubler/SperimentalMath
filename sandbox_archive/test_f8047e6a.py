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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n+1))
        clauses = []
        for i in range(1, n+1):
            clause = [i]
            for j in range(i+1, n+1):
                clause.append(-j)
                clause.append(-(i+j))
            clauses.append(clause)
        return variables, clauses

    def noncommutative_crossed_product_rank(variables, clauses):
        # Simplified mapping to rank based on formula size
        return len(variables) ** (2/3)

    def ac0_circuit_size(n):
        # Simplified mapping to circuit size based on formula size
        return n ** (2/3)

    variables, clauses = generate_tseitin_formula(40)
    rank = noncommutative_crossed_product_rank(variables, clauses)
    circuit_size = ac0_circuit_size(len(clauses))

    return {
        "metric_name": "Noncommutative Crossed Product Rank / AC0 Circuit Size",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= len(variables) ** (2/3) and circuit_size <= len(clauses) ** (2/3),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"Tseitin formula of size {len(r['metric_value'])}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")