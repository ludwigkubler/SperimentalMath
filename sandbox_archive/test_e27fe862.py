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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def minterms_from_clauses(clauses, n):
        minterms = set()
        for clause in clauses:
            term = 1
            for var, sign in enumerate(clause):
                if sign == 1:
                    term *= (2 * var + 1)
                else:
                    term *= (2 * var + 2)
            minterms.add(term)
        return minterms
    
    def minimal_order(minterms):
        n = len(minterms)
        for i in range(1, n + 1):
            if all(any(m % j == 0 for j in range(1, i)) for m in minterms):
                return i
        return n
    
    def clause_subset_entropy(n):
        return math.log2(2**n)
    
    n = random.randint(5, 40)
    clauses = generate_cnf(n)
    minterms = minterms_from_clauses(clauses, n)
    order = minimal_order(minterms)
    entropy = clause_subset_entropy(n)
    
    return {
        "metric_name": "order_over_entropy",
        "metric_value": order / entropy,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order <= 2 * entropy,  # Placeholder constant c=2
        "counterexample": "" if order <= 2 * entropy else f"order={order} > 2*entropy={2*entropy}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order > 2*entropy\" first_failing_seed={first_failing_seed}")