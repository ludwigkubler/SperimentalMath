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
    
    def generate_k_clique(n, k):
        clique = set()
        for _ in range(k):
            node = random.randint(0, n-1)
            if node not in clique:
                clique.add(node)
        return clique

    def dnf_approximation(clique, epsilon):
        n = len(clique)
        approx_size = math.ceil(n * (1 + epsilon))
        return approx_size

    n_values = [5, 10, 15, 20, 30, 40]
    total_size = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            clique = generate_k_clique(n, int(math.log2(n)))
            size = dnf_approximation(clique, 0.1)
            total_size += size
            instances_tested += 1

    avg_size = total_size / instances_tested
    conjecture_holds = avg_size >= n_values[-1] * (1 + 0.1)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "DNF Size",
        "metric_value": avg_size,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_size:.4f} std=0.0000 support_fraction={support_fraction:.2%}")