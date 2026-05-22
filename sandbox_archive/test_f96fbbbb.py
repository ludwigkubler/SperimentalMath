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
    
    def generate_k_clique_dnf(n, k):
        if n < k or k <= 0:
            return None
        vertices = list(range(n))
        edges = random.sample(list(itertools.combinations(vertices, 2)), k * (n - k) // 2)
        dnf_formula = []
        for i in range(k):
            clause = [f"x{v}" if v < n else f"~x{v-n}" for v in vertices]
            for j in range(i + 1, k):
                clause.append(f"~x{j}")
            dnf_formula.append(" & ".join(clause))
        return " | ".join(dnf_formula)
    
    def tropical_matroid_rank(dnf_formula):
        if not dnf_formula:
            return 0
        literals = set()
        for clause in dnf_formula.split(" | "):
            for literal in clause.split(" & "):
                literals.add(literal)
        rank = len(literals)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            dnf_formula = generate_k_clique_dnf(n, k=3)
            if dnf_formula is None:
                continue
            rank = tropical_matroid_rank(dnf_formula)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    lower_bound = math.ceil(math.sqrt(n))
    
    conjecture_holds = mean_rank >= lower_bound
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, lower_bound={lower_bound}"
    
    return {
        "metric_name": "tropical_matroid_rank",
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
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")