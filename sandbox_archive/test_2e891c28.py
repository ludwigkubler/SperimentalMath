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
    
    def quine_mccluskey(f):
        n = len(f)
        minterms = [i for i in range(2**n) if f[i]]
        prime_implicants = []
        essential_prime_implicants = []
        
        while True:
            if not minterms:
                break
            
            # Find prime implicants
            new_prime_implicants = set()
            for term1 in minterms:
                covered = False
                for term2 in minterms:
                    if term1 != term2 and all((term1 >> i) & 1 == (term2 >> i) & 1 for i in range(n)):
                        covered = True
                        break
                if not covered:
                    new_prime_implicants.add(term1)
            
            prime_implicants.extend(new_prime_implicants)
            minterms = [m for m in minterms if any((m >> i) & 1 != (pi >> i) & 1 for pi in new_prime_implicants)]
        
        # Find essential prime implicants
        for term in minterms:
            covered = False
            for pi in prime_implicants:
                if all((term >> i) & 1 == (pi >> i) & 1 for i in range(n)):
                    covered = True
                    break
            if covered:
                essential_prime_implicants.append(term)
        
        return len(essential_prime_implicants)

    def build_lattice(prime_implicants, literals):
        n = len(literals)
        lattice = {}
        for pi in prime_implicants:
            lattice[pi] = set()
            for literal in literals:
                if all((pi >> i) & 1 == (literal >> i) & 1 for i in range(n)):
                    lattice[pi].add(literal)
        
        return lattice

    def hasse_diagram(lattice):
        nodes = list(lattice.keys())
        edges = []
        for u in nodes:
            for v in nodes:
                if u != v and all(u & v == 0) and any(v & x > 0 for x in lattice[u]):
                    edges.append((u, v))
        
        return nodes, edges

    def max_antichain_size(nodes, edges):
        graph = {node: set() for node in nodes}
        for u, v in edges:
            graph[u].add(v)
        
        visited = [False] * len(nodes)
        antichains = []
        
        def dfs(node, chain):
            if visited[node]:
                return
            visited[node] = True
            chain.append(node)
            
            for neighbor in graph[node]:
                dfs(neighbor, chain)
            
            antichains.append(chain[:])
            chain.pop()
            visited[node] = False
        
        for node in nodes:
            dfs(node, [])
        
        max_size = 0
        for antichain in antichains:
            if all(all(antichain[i] & antichain[j] == 0 for j in range(i + 1, len(antichain))) for i in range(len(antichain))):
                max_size = max(max_size, len(antichain))
        
        return max_size

    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        pivot_cols = [False] * m
        
        for col in range(m):
            if all(pivot_cols[j] for j in range(n)):
                continue
            
            row = next((i for i in range(rank, n) if matrix[i][col]), None)
            if row is None:
                continue
            
            pivot_cols[col] = True
            rank += 1
            
            for i in range(row + 1, n):
                factor = -matrix[i][col] / matrix[row][col]
                for j in range(col, m):
                    matrix[i][j] += factor * matrix[row][j]
        
        return rank

    def build_implicant_context(f):
        n = len(f)
        literals = [1 << i for i in range(n)] + [-1 << i for i in range(n)]
        prime_implicants = quine_mccluskey(f)
        lattice = build_lattice(prime_implicants, literals)
        nodes, edges = hasse_diagram(lattice)
        return max_antichain_size(nodes, edges)

    def sigma_dnf(f):
        n = len(f)
        minterms = [i for i in range(2**n) if f[i]]
        
        def set_cover(minterms, literals):
            cover = []
            while minterms:
                selected_literal = None
                for literal in literals:
                    covered = all((m & literal > 0) for m in minterms)
                    if not covered and (selected_literal is None or sum(1 for m in minterms if (m & selected_literal > 0)) < sum(1 for m in minterms if (m & literal > 0))):
                        selected_literal = literal
                cover.append(selected_literal)
                minterms = [m for m in minterms if all((m & literal == 0) for literal in cover)]
            return len(cover)
        
        literals = [1 << i for i in range(n)] + [-1 << i for i in range(n)]
        return set_cover(minterms, literals)

    n_values = [3, 4]
    if seed % 2 == 0:
        n_values.append(5)
    
    results = []
    for n in n_values:
        f = [random.choice([0, 1]) for _ in range(2**n)]
        
        sigma_dnf_value = sigma_dnf(f)
        implicant_width = build_implicant_context(f)
        
        if implicant_width < sigma_dnf_value:
            return {
                "metric_name": "implicant_width",
                "metric_value": implicant_width,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, f={f}, σ_DNF(f)={sigma_dnf_value}, w(f)={implicant_width}"
            }
        
        if implicant_width > 2 * n * sigma_dnf_value:
            return {
                "metric_name": "implicant_width",
                "metric_value": implicant_width,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, f={f}, σ_DNF(f)={sigma_dnf_value}, w(f)={implicant_width}"
            }
        
        results.append((sigma_dnf_value, implicant_width))
    
    min_ratio = min(w / sigma for sigma, w in results)
    max_ratio = max(w / sigma for sigma, w in results)
    
    return {
        "metric_name": "implicant_width",
        "metric_value": (min_ratio + max_ratio) / 2,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 2 * n * sigma_dnf([random.choice([0, 1]) for _ in range(2**n)]) for n in [3, 4]) / len(results)
    
    if all(r <= 2 * n * sigma_dnf([random.choice([0, 1]) for _ in range(2**n)]) for r in results for n in [3, 4]):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > 2 * n * sigma_dnf([random.choice([0, 1]) for _ in range(2**n)]) for r in results for n in [3, 4]):
        print(f"RESULT: FALSIFIED counterexample='upper_bound_violation' first_failing_seed={seeds[results.index(max(results))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")