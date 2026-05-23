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

def geometric_quantization_matrix(boolean_algebra):
    n = len(boolean_algebra)
    quantization_matrix = []
    for x in boolean_algebra:
        row = []
        for y in boolean_algebra:
            if all((x & (1 << i)) == (y & (1 << i)) for i in range(n)):
                row.append(1)
            else:
                row.append(0)
        quantization_matrix.append(row)
    return quantization_matrix

def communication_protocol_efficiency(boolean_algebra):
    n = len(boolean_algebra)
    if n <= 1:
        return 0
    return math.ceil(math.log2(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    boolean_algebra = tuple(random.getrandbits(1) for _ in range(n))
    
    quantization_matrix = geometric_quantization_matrix(boolean_algebra)
    rank = sum(1 for row in quantization_matrix if any(row))
    
    cp_efficiency = communication_protocol_efficiency(boolean_algebra)
    
    return {
        "metric_name": "Minimal Rank of Geometric Quantization Matrix",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= cp_efficiency * math.log2(n),
        "counterexample": "" if rank <= cp_efficiency * math.log2(n) else f"Counterexample for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='First failing seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")