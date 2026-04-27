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
    def rle_encoding(s):
        encoded = []
        count = 1
        for i in range(1, len(s)):
            if s[i] == s[i-1]:
                count += 1
            else:
                encoded.append((s[i-1], count))
                count = 1
        encoded.append((s[-1], count))
        return encoded

    def h_rle(f):
        tt = ''.join('1' if f(i) else '0' for i in range(2**n))
        rle = rle_encoding(tt)
        entropy = sum(count * math.log2(length + 1) for _, length in rle)
        return entropy

    def dnf_min(f):
        n_vars = n
        prime_implicants = []
        covered = [False] * (2**n)

        def quine_mccluskey(vars, minterms):
            if not minterms:
                return []

            minterms = sorted(minterms)
            active = minterms[:]
            while len(active) > 1:
                next_level = []
                for i in range(len(active)):
                    for j in range(i + 1, len(active)):
                        diff = sum(1 for k in range(n_vars) if (active[i] & (1 << k)) != (active[j] & (1 << k)))
                        if diff == 1:
                            next_level.append(active[i] ^ active[j])
                active = list(set(next_level))

            prime_implicants.extend(active)

        def cover_minterms(minterms, implicants):
            covered = [False] * len(minterms)
            for implicant in implicants:
                for i, minterm in enumerate(minterms):
                    if not covered[i] and (implicant & minterm) == implicant:
                        covered[i] = True
            return all(covered)

        def greedy_set_cover(minterms, implicants):
            cover = []
            while minterms:
                best_implicant = None
                max_covered = 0
                for implicant in implicants:
                    covered = sum(1 for minterm in minterms if (implicant & minterm) == implicant)
                    if covered > max_covered:
                        max_covered = covered
                        best_implicant = implicant
                cover.append(best_implicant)
                minterms = [minterm for minterm in minterms if (best_implicant & minterm) != best_implicant]
            return cover

        quine_mccluskey(list(range(2**n)), list(range(2**n)))
        prime_implicants = sorted(prime_implicants, key=lambda x: -sum(1 << i for i in range(n_vars) if (x & (1 << i)) != 0))
        cover = greedy_set_cover(list(range(2**n)), prime_implicants)
        return len(cover)

    def random_boolean_function(n):
        return lambda x: random.choice([True, False])

    def structured_boolean_function(n, t, width):
        terms = []
        for _ in range(t):
            term = 0
            for _ in range(width):
                var = random.randint(0, n-1)
                if random.choice([True, False]):
                    term |= (1 << var)
            terms.append(term)
        return lambda x: any(all((x & term) == term for term in terms))

    def density_to_minterms(density, n):
        minterms = []
        for i in range(2**n):
            if random.random() < density:
                minterms.append(i)
        return minterms

    n = 6
    random.seed(seed)

    results = []
    densities = [1/4, 1/2, 3/4]
    num_samples = 200
    num_structured = 100

    for density in densities:
        for _ in range(num_samples):
            f = lambda x: random.choice([True, False])
            results.append((density, f))

    for t in range(1, 9):
        for _ in range(num_structured):
            f = structured_boolean_function(n, t, n)
            results.append((None, f))

    for density, f in results:
        if density is not None:
            minterms = density_to_minterms(density, n)
            f = lambda x: any(minterm & x == minterm for minterm in minterms)
        else:
            minterms = list(range(2**n))

        h_rle_val = h_rle(f)
        dnf_min_val = dnf_min(f)
        slack = (n + 1) * dnf_min_val - 2 ** h_rle_val

        results.append((f, h_rle_val, dnf_min_val, slack))

    total_slack = sum(slack for _, _, _, slack in results)
    median_slack = sorted([slack for _, _, _, slack in results])[len(results) // 2]

    conjecture_holds = all(slack >= 0 for _, _, _, slack in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "slack",
        "metric_value": median_slack,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    total_slack = sum(result["metric_value"] for result in results)
    median_slack = sorted([result["metric_value"] for result in results])[len(results) // 2]
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_slack/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")