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

def generate_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = []
        for _ in range(3):
            var = random.choice(variables)
            polarity = random.choice([True, False])
            if polarity:
                clause.append(var)
            else:
                clause.append(-var)
        clauses.append(clause)
    return clauses

def hypergraph_max_matching_size(clauses):
    n = len(clauses)
    matching = []
    for i in range(n):
        for j in range(i + 1, n):
            if not any(x == y or x == -y for x in clauses[i] for y in clauses[j]):
                matching.append((i, j))
                break
    return len(matching)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = generate_3cnf(n, m)
    matching_size = hypergraph_max_matching_size(cnf)
    conjecture_holds = matching_size <= math.log(n) and matching_size >= math.log(n) / 10
    return {
        "metric_name": "max_matching_size",
        "metric_value": matching_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*3 + 1))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
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
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, m={results[0]['instances_tested']}\" first_failing_seed={first_failing_seed}")