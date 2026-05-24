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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hodge_rank(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        H = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    H[i][j] = Fraction((circuit[i] - circuit[j]) * (i - j), n)
        rank = 0
        for row in H:
            if any(val != 0 for val in row):
                rank += 1
        return rank
    
    def acc0_certificate(circuit):
        n = len(circuit)
        if n == 1:
            return [circuit[0]]
        certificates = []
        for i in range(n):
            cert = [circuit[i]]
            for j in range(i+1, n):
                cert.append((cert[-1] + circuit[j]) % 2)
            certificates.append(cert)
        return certificates
    
    p = 2
    d_max = 40
    instances_tested = 0
    hodge_ranks = []
    acc0_sizes = []
    
    for n in range(5, d_max+1):
        for _ in range(20):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n)
            rank = hodge_rank(circuit)
            certificates = acc0_certificate(circuit)
            if rank > p:
                return {
                    "metric_name": "hodge_rank",
                    "metric_value": rank,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Hodge rank {rank} exceeds p={p}"
                }
            hodge_ranks.append(rank)
            acc0_sizes.append(len(certificates))
            instances_tested += 1
    
    if len(hodge_ranks) < 1000:
        return {
            "metric_name": "hodge_rank",
            "metric_value": sum(hodge_ranks) / len(hodge_ranks),
            "instances_tested": len(hodge_ranks),
            "conjecture_holds": False,
            "counterexample": "Insufficient data"
        }
    
    mean_rank = sum(hodge_ranks) / len(hodge_ranks)
    std_rank = math.sqrt(sum((x - mean_rank)**2 for x in hodge_ranks) / len(hodge_ranks))
    mean_size = sum(acc0_sizes) / len(acc0_sizes)
    std_size = math.sqrt(sum((x - mean_size)**2 for x in acc0_sizes) / len(acc0_sizes))
    
    support_fraction = sum(1 for rank, size in zip(hodge_ranks, acc0_sizes) if rank <= p and size >= 3 * (len(circuit) ** 0.5)) / len(hodge_ranks)
    
    return {
        "metric_name": "hodge_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30*len(sys.argv), 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")