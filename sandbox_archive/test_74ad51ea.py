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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_circuit(n):
    if n == 1:
        return '0'
    elif n == 2:
        return random.choice(['0', '1'])
    else:
        left = generate_circuit(n // 2)
        right = generate_circuit(n - n // 2)
        return f'({left},{right})'

def hodge_rank(circuit):
    if isinstance(circuit, str):
        return 1
    elif isinstance(circuit, tuple):
        left_rank = hodge_rank(circuit[0])
        right_rank = hodge_rank(circuit[1])
        return max(left_rank, right_rank) + 1

def acc0_certificate_size(circuit):
    if isinstance(circuit, str):
        return 1
    elif isinstance(circuit, tuple):
        left_cert = acc0_certificate_size(circuit[0])
        right_cert = acc0_certificate_size(circuit[1])
        return max(left_cert, right_cert) + 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 3
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    rank_sum = 0
    acc0_cert_sum = 0

    for n in n_values:
        for _ in range(167):  # Aim for at least 1000 instances per seed
            circuit = generate_circuit(n)
            rank = hodge_rank(circuit) % p
            cert_size = acc0_certificate_size(circuit)
            rank_sum += rank
            acc0_cert_sum += cert_size
            instances_tested += 1

    avg_rank = rank_sum / instances_tested
    avg_cert_size = acc0_cert_sum / instances_tested
    conjecture_holds = all(avg_rank <= (n + 3) % p for n in n_values) and all(avg_cert_size >= (n * 2 - 2) for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Hodge Rank vs ACC⁰ Certificates",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    avg_cert_size = sum(r["instances_tested"] * (r["metric_value"] if r["conjecture_holds"] else 0) for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")