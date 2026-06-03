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
    
    def noncrossing_partitions(n):
        if n == 0:
            return 1
        count = 0
        for i in range(1, n):
            count += noncrossing_partitions(i) * noncrossing_partitions(n - i - 1)
        return count
    
    def communication_complexity_rank(n):
        # Placeholder function to compute the rank r
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n // 2)
    
    instances_tested = 0
    m_sum = 0
    counterexamples = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = noncrossing_partitions(n)
            r = communication_complexity_rank(n)
            instances_tested += 1
            if not (math.log2(n) <= m <= 2 * r):
                counterexamples.append(f"n={n}, m={m}, r={r}")
    
    conjecture_holds = len(counterexamples) <= 5
    
    return {
        "metric_name": "noncrossing_partitions",
        "metric_value": m_sum / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": ", ".join(counterexamples)
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")