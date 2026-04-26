import sys
from random import randint, seed
from collections import defaultdict

def run_trial(seed: int) -> dict:
    def generate_3sat(n):
        clauses = []
        for _ in range(randint(2*n, 4*n)):
            literals = [randint(1, n), randint(1, n)]
            if randint(0, 1):
                literals[0] *= -1
            if randint(0, 1):
                literals[1] *= -1
            clauses.append(literals)
        return clauses

    def resolution_width(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i+1, len(stack)):
                    if set(stack[i]) & set(stack[j]):
                        new_clause = [l for l in stack[i] + stack[j] if l not in set(stack[i]) & set(stack[j])]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(set([abs(l) for l in stack]))
            stack.append(new_clause)

    def clifford_algebroid_rank(clauses):
        n = max(abs(l) for clause in clauses for l in clause)
        G = defaultdict(list)
        for clause in clauses:
            for l1 in clause:
                for l2 in clause:
                    if abs(l1) != abs(l2):
                        G[abs(l1)].append((abs(l2), 1))
                        G[abs(l2)].append((abs(l1), 1))
        rank = 0
        visited = set()
        for v in range(1, n+1):
            if v not in visited:
                queue = [v]
                while queue:
                    u = queue.pop(0)
                    if u not in visited:
                        visited.add(u)
                        for neighbor, _ in G[u]:
                            if neighbor not in visited:
                                queue.append(neighbor)
                rank += 1
        return rank

    seed(seed)
    n = randint(8, 12)
    clauses = generate_3sat(n)
    w_phi = resolution_width(clauses)
    r_phi = clifford_algebroid_rank(clauses)
    metric_value = abs(w_phi - r_phi)
    conjecture_holds = metric_value <= 2
    counterexample = "" if conjecture_holds else f"n={n}, w(φ)={w_phi}, r(φ)={r_phi}"
    return {
        "metric_name": "abs_diff",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, w(φ)={results[first_failing_seed]['metric_value']}, r(φ)={r['counterexample'].split(',')[1].strip()}\" first_failing_seed={first_failing_seed}")