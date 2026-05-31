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
    
    def generate_kcnf(k, n):
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = set()
            while len(clause) < k:
                literal = random.choice(literals)
                if -literal not in clause:
                    clause.add(literal)
            clauses.append(tuple(sorted(clause)))
        return clauses

    def noncrossing_partition_size(n):
        if n == 0: return 1
        dp = [0] * (n + 1)
        dp[0] = 1
        for i in range(1, n + 1):
            dp[i] = sum(dp[j] * dp[i - j - 1] for j in range(i)) % 1000003
        return dp[n]

    k = random.randint(2, 5)
    n = random.randint(5, 40)
    clauses = generate_kcnf(k, n)

    local_index = noncrossing_partition_size(n) * math.log(n)

    return {
        "metric_name": "local_index",
        "metric_value": local_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 * n * math.log(n) <= local_index <= 1.5 * n * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unexpected_behavior")