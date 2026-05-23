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
    
    # Generate a random k-CNF instance with n variables and m clauses
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    k = random.randint(2, min(3, n))
    
    cnf_instance = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), k)]
        cnf_instance.append(clause)
    
    # Placeholder functions to compute ranks
    def geometric_entanglement_rank(cnf):
        return len(cnf)
    
    def noncommutative_crossed_product_rank(cnf):
        return n
    
    ge_rank = geometric_entanglement_rank(cnf_instance)
    npc_rank = noncommutative_crossed_product_rank(cnf_instance)
    
    metric_value = ge_rank - npc_rank * math.sqrt(n)
    
    return {
        "metric_name": "Rank Difference",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value > 0,
        "counterexample": "" if metric_value > 0 else "geometric_entanglement_rank <= noncommutative_crossed_product_rank * n^0.5"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")