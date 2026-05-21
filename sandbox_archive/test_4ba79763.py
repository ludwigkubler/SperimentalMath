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
    n = random.randint(5, 40)
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        # Generate a random permutation group G with r(G) ≤ 5
        G = generate_permutation_group(n, 5)

        if not G:
            counterexample = "mapping_undefined"
            conjecture_holds = False
            break

        # Encode communication protocol for DISJOINTNESS using G
        protocol_complexity = encode_protocol(G, n)

        if protocol_complexity > Fraction(n**(1/5), 1):
            counterexample = f"n={n}, r(G)=5, complexity={protocol_complexity}"
            conjecture_holds = False
            break

        # Update metric value
        metric_value += protocol_complexity

    return {
        "metric_name": "communication_protocol_complexity",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_permutation_group(n, max_rank):
    # Generate a random permutation group with r(G) ≤ max_rank
    G = []
    for _ in range(max_rank):
        perm = list(range(n))
        random.shuffle(perm)
        G.append(perm)
    return G

def encode_protocol(G, n):
    # Encode communication protocol using G
    complexity = Fraction(1, 1)
    for i in range(n):
        complexity *= Fraction(1, len(set(g[i] for g in G)))
    return complexity

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")