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
    random.seed(seed)
    
    def random_monotone_circuit(k, n):
        if k == 1:
            return [[random.choice([0, 1]) for _ in range(n)]]
        else:
            subcircuits = [random_monotone_circuit(random.randint(1, k-1), n) for _ in range(2)]
            return [subcircuit + [sum(subcircuit) % 2] for subcircuit in subcircuits]

    def quandle_representation(circuit):
        if len(circuit) == 1:
            return [[i] for i in circuit[0]]
        else:
            left, right = quandle_representation(circuit[:-1]), [circuit[-1]]
            result = []
            for l in left:
                new_row = [l[i] ^ r for r in right]
                result.append(new_row)
            return result

    def min_rank(quandle):
        n = len(quandle[0])
        rank = 0
        for i in range(n):
            if any(all(quandle[j][i] == quandle[k][i] for j, k in itertools.combinations(range(len(quandle)), 2)) for row in quandle):
                rank += 1
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # 5 instances per size
            k = random.randint(1, min(n // 2, 5))
            circuit = random_monotone_circuit(k, n)
            quandle = quandle_representation(circuit)
            rank = min_rank(quandle)
            results.append((n, k, rank))

    total_rank = sum(rank for _, _, rank in results)
    avg_rank = total_rank / len(results)
    
    conjecture_holds = all(rank >= 2**k for _, k, rank in results)
    counterexample = "" if conjecture_holds else "rank={}, expected=2^{}".format(min(rank for _, k, rank in results), min(k for _, k, rank in results))
    
    return {
        "metric_name": "min_rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]  # Default to first 30 primes

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **trial_result})
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean=%.2f std=%.2f support_fraction=%.2f" % (mean_value, std_dev, support_fraction))
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"%s\" first_failing_seed=%d" % (result["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")