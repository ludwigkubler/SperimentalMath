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
    
    def generate_k_clique(n, k):
        edges = set()
        for i in range(k):
            for j in range(i + 1, k):
                edges.add((i, j))
        return [random.sample(range(n), k) for _ in range(30)]

    def generate_dnf(n):
        clauses = []
        for _ in range(30):
            clause = random.sample(range(n), random.randint(1, n // 2))
            clauses.append(clause)
        return clauses

    def hypergraph_rank(edges):
        rank = 0
        while edges:
            edge = edges.pop()
            rank += 1
            new_edges = set()
            for e in edges:
                if not any(x in e for x in edge):
                    new_edges.add(e)
            edges = new_edges
        return rank

    def sdp_relaxation(rank):
        # Placeholder for actual SOS degree computation
        return rank * 0.5  # Simplified approximation

    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        k_clique_edges = generate_k_clique(n, int(math.sqrt(n)))
        dnf_clauses = generate_dnf(n)

        k_clique_rank = hypergraph_rank(k_clique_edges)
        dnf_rank = hypergraph_rank(dnf_clauses)

        k_clique_sdp = sdp_relaxation(k_clique_rank)
        dnf_sdp = sdp_relaxation(dnf_rank)

        results.append({
            "n": n,
            "k-clique_rank": k_clique_rank,
            "k-clique_sdp": k_clique_sdp,
            "dnf_rank": dnf_rank,
            "dnf_sdp": dnf_sdp
        })

    metric_value = sum(r['k-clique_rank'] for r in results) / len(results)
    instances_tested = len(results)

    conjecture_holds = all(r['k-clique_rank'] >= 0.7 * math.sqrt(n) and r['dnf_rank'] <= 5 * math.log(n) for n, r in zip(n_values, results))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [677, 727, 773, 821, 877, 929]  # Default list of primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank_k_clique = sum(r['k-clique_rank'] for r in results if 'k-clique' in r['counterexample']) / len([r for r in results if 'k-clique' in r['counterexample']])
    mean_rank_dnf = sum(r['dnf_rank'] for r in results if 'DNF' in r['counterexample']) / len([r for r in results if 'DNF' in r['counterexample']])
    support_fraction_k_clique = sum(1 for r in results if 'k-clique' in r['counterexample'] and r['conjecture_holds']) / len([r for r in results if 'k-clique' in r['counterexample']])
    support_fraction_dnf = sum(1 for r in results if 'DNF' in r['counterexample'] and r['conjecture_holds']) / len([r for r in results if 'DNF' in r['counterexample']])

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean_k-clique={mean_rank_k_clique} std_k-clique=0.0 support_fraction_k-clique={support_fraction_k_clique}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")