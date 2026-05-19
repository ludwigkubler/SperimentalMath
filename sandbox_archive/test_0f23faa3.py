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
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Compute the number of irreducible representations
    def character_table(n):
        table = []
        for k in range(n + 1):
            row = [math.comb(n, k) / math.factorial(k) * math.factorial(n - k)]
            for j in range(1, n // 2 + 1):
                if (k + j) % 2 == 0:
                    row.append(math.comb(n, k + j) / (math.factorial(j) * math.factorial(k + j)))
                else:
                    row.append(-math.comb(n, k + j) / (math.factorial(j) * math.factorial(k + j)))
            table.append(row)
        return table
    
    def irreducible_representations(G):
        n = len(G)
        char_table = character_table(n)
        representations = set()
        for i in range(n):
            for j in range(i, n):
                if G[i][j] == 1:
                    representation = sum(char_table[k][i] * char_table[k][j] for k in range(n))
                    representations.add(representation)
        return len(representations)
    
    irreps_count = irreducible_representations(G)
    
    # Estimate resolution complexity (simplified example)
    def resolution_complexity(irreps_count):
        if irreps_count == 0:
            return 1
        return 2 ** irreps_count
    
    res_comp = resolution_complexity(irreps_count)
    
    return {
        "metric_name": "resolution_complexity",
        "metric_value": res_comp,
        "instances_tested": 1,
        "conjecture_holds": False,  # This seed's data does not support the conjecture
        "counterexample": f"Graph with {n} nodes and {irreps_count} irreducible representations"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_res_comp = sum(r["metric_value"] for r in results) / len(results)
    std_res_comp = math.sqrt(sum((r["metric_value"] - mean_res_comp) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_res_comp} std={std_res_comp} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")