from collections import Counter


def feedback(code, guess):
    exact = sum(c == g for c, g in zip(code, guess))

    unmatched_code = [c for c, g in zip(code, guess) if c != g]
    unmatched_guess = [g for c, g in zip(code, guess) if c != g]

    code_counts = Counter(unmatched_code)
    guess_counts = Counter(unmatched_guess)

    partial = sum(min(guess_counts[k], code_counts[k]) for k in guess_counts)

    return exact, partial
