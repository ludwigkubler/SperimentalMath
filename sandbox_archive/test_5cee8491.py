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

def run_trial(seed: int) -> dict:
    def construct_dnf_parity(n):
        dnf = []
        for i in range(1 << n):
            inputs = [j for j in range(n) if (i >> (n-1-j)) & 1]
            dnf.append(inputs)
        return dnf

    def construct_hastad_parity(n, depth):
        if depth == 2:
            return [[i] for i in range(n)]
        else:
            subcircuits = [construct_hastad_parity(n // 2, depth - 1) for _ in range(2)]
            dnf = []
            for left in subcircuits[0]:
                for right in subcircuits[1]:
                    dnf.append(left + right)
            return dnf

    def construct_random_dnf_nonparity(n, size):
        inputs = list(range(n))
        random.shuffle(inputs)
        dnf = [inputs[:size]]
        while len(dnf) < size:
            new_clause = []
            for _ in range(n):
                if random.random() < 0.5:
                    new_clause.append(random.choice(inputs))
            dnf.append(new_clause)
        return dnf

    def compute_ch(circuit, n):
        ch = set()
        for x in range(1 << n):
            output_vector = tuple(1 if circuit[i][x >> (n-1-i)] & 1 else 0 for i in range(len(circuit)))
            ch.add(output_vector)
        return len(ch)

    def log2(x):
        return math.log2(x) if x > 0 else float('-inf')

    n_values = [6, 8, 10, 12, 14, 16]
    support_threshold = Fraction(28, 30)
    total_ch = 0
    num_falsifiers = 0

    for n in n_values:
        random.seed(seed + n)
        dnf_parity = construct_dnf_parity(n)
        hastad_parity = construct_hastad_parity(n, depth=3)
        random_dnf_nonparity = construct_random_dnf_nonparity(n, size=len(dnf_parity))

        for circuit in [dnf_parity, hastad_parity]:
            ch = compute_ch(circuit, n)
            total_ch += ch
            if log2(ch) < 0.25 * n ** (1 / (3 - 1)):
                num_falsifiers += 1

        for circuit in random_dnf_nonparity:
            ch = compute_ch(circuit, n)
            total_ch += ch
            gap_ratio = log2(ch) / n ** (1 / (3 - 1))
            if gap_ratio < 0.25 * n ** (1 / (3 - 1)):
                return {
                    "metric_name": "gap_ratio",
                    "metric_value": gap_ratio,
                    "instances_tested": len(random_dnf_nonparity),
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, d=3, size={len(circuit)}, ch={ch}, seed={seed}"
                }

    mean_ch = total_ch / (2 * sum(n_values))
    support_fraction = 1 - num_falsifiers / (2 * len(n_values))

    return {
        "metric_name": "mean_ch",
        "metric_value": mean_ch,
        "instances_tested": sum(len(circuit) for circuit in [dnf_parity, hastad_parity] * len(n_values)),
        "conjecture_holds": support_fraction >= support_threshold,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_ch = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ch} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")