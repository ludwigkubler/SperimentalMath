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
    
    def generate_truth_table(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def quine_mccluskey(prime_implicants):
        # Simplify using Quine–McCluskey algorithm
        while True:
            new_pi = set()
            for pi1 in prime_implicants:
                for pi2 in prime_implicants:
                    if pi1 != pi2 and pi1[:-1] == pi2[:-1] and pi1[-1] != pi2[-1]:
                        new_pi.add(pi1[:-1])
            if not new_pi:
                break
            prime_implicants = new_pi
        return prime_implicants
    
    def set_cover(prime_implicants, n):
        # Find minimum cover using branch-and-bound
        def backtrack(cover, remaining):
            if not remaining:
                return len(cover)
            min_cover = float('inf')
            for pi in prime_implicants:
                if all(pi[i] == 1 for i in range(n) if remaining[i]):
                    new_remaining = [r ^ pi[i] for r in remaining]
                    min_cover = min(min_cover, backtrack(cover + [pi], new_remaining))
            return min_cover
        
        return backtrack([], [1] * n)
    
    def build_lattice(prime_implicants):
        lattice = set()
        for pi in prime_implicants:
            lattice.add(tuple(pi))
        while True:
            new_elements = set()
            for x in lattice:
                for y in lattice:
                    if all(x[i] <= y[i] for i in range(n)):
                        new_elements.add(y)
            if not new_elements:
                break
            lattice.update(new_elements)
        return lattice
    
    def antichain_width(lattice):
        # Compute the size of the largest antichain using Hasse diagram and König's theorem
        adj = {x: set() for x in lattice}
        for x in lattice:
            for y in lattice:
                if all(x[i] <= y[i] for i in range(n)) and not any(y[i] < x[i] for i in range(n)):
                    adj[x].add(y)
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    stack.extend(adj[node])
            
            return len(visited)
        
        max_antichain_size = 0
        for x in lattice:
            visited = set()
            dfs(x, visited)
            max_antichain_size = max(max_antichain_size, len(visited))
        
        return max_antichain_size
    
    def sigma_DNF(prime_implicants):
        # Count the number of prime implicants
        return len(prime_implicants)
    
    n_values = [3, 4, 5]
    results = []
    
    for n in n_values:
        if n == 5:
            truth_tables = [generate_truth_table(n) for _ in range(30 * 34)]
        else:
            truth_tables = [generate_truth_table(n) for _ in range(2**(2**n))]
        
        for tt in truth_tables:
            prime_implicants = quine_mccluskey([tt[i] << i for i in range(n)])
            sigma_dnf = sigma_DNF(prime_implicants)
            lattice = build_lattice(prime_implicants)
            w_f = antichain_width(lattice)
            
            if w_f < sigma_dnf:
                return {
                    "metric_name": "w(f)",
                    "metric_value": w_f,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"sigma_DNF={sigma_dnf}, w(f)={w_f}"
                }
            if w_f > 2 * n * sigma_dnf:
                return {
                    "metric_name": "w(f)",
                    "metric_value": w_f,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"sigma_DNF={sigma_dnf}, w(f)={w_f}"
                }
    
    min_ratio = min(w / sigma for _, w, sigma in results)
    max_ratio = max(w / sigma for _, w, sigma in results)
    
    return {
        "metric_name": "w(f)/sigma_DNF",
        "metric_value": (min_ratio + max_ratio) / 2,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")