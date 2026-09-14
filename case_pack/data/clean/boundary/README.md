# Movement review: threshold test cases

Nine small cases for the period-on-period movement check (C09).

The rule warns only when **both** tests pass, and both use a strict `>`:

    abs(current - prior) > 100.00   AND   abs((current - prior) / abs(prior)) > 0.20

Two cases sit exactly on a threshold and must **not** warn. Two sit just past it and must.
Two have a prior value of zero: the percentage is `not_comparable`, never infinity and
never invented. One is large enough to warn as new activity, one is not.

The amounts are small on purpose. Decide which of the nine cases should warn, and why,
before you run any code.
