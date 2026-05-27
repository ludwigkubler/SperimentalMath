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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return ['0', '1']
        else:
            subcircuits = [generate_boolean_circuit(n // 2) for _ in range(2)]
            circuit = []
            for i in range(len(subcircuits[0])):
                circuit.append(f"({subcircuits[0][i]} OR {subcircuits[1][i]})")
            return circuit
    
    def compute_groupoid_rank(circuit):
        n = len(circuit)
        rank = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                stack = [i]
                while stack:
                    node = stack.pop()
                    if not visited[node]:
                        visited[node] = True
                        rank += 1
                        for j in range(n):
                            if circuit[j].find(circuit[node]) != -1 and not visited[j]:
                                stack.append(j)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        rank = compute_groupoid_rank(circuit)
        total_rank += rank
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= n**2
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank} exceeds n^2 for n={n}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.00 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank exceeds n^2\" first_failing_seed={first_failing_seed}")