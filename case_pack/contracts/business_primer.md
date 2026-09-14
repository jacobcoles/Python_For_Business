# Business primer: Northbridge's figures worked by hand

Pre-read for session D1-S01, about ten minutes. Fictional case, no code. Every number comes from the eight-row
example in `case_pack/data/clean/tiny/`.

The goal: before anyone writes a line of Python, you can say what the right answer is, and why.

## 1. The whole idea in one sentence
A month's **operating result** is what the unit earned (**revenue**) minus what it spent
(**costs**).

It is not "profit" in the tax sense. This case has no tax, interest or depreciation. It is simply
earnings minus the costs we track.

## 2. The eight lines

Unit N01 sent eight lines for December 2025.

| Line | Account code | Report line | Amount EUR | Status | In plain words |
|---|---|---|---:|---|---|
| T001 | 0400 | revenue | 1000.00 | posted | Service work sold |
| T002 | 0410 | revenue | 500.00 | posted | Training sold |
| T003 | 0400 | revenue | -100.00 | posted | Money given back to a customer |
| T004 | 0500 | direct_cost | -400.00 | posted | Cost of delivering the work |
| T005 | 0500 | direct_cost | -200.00 | posted | Cost of delivering the work |
| T006 | 0500 | direct_cost | 20.00 | posted | Part of a cost undone |
| T007 | 0600 | overhead | -100.00 | posted | Premises cost |
| T008 | 0400 | revenue | 999.00 | **cancelled** | A sale that was called off |

Three words to know. The **report line** is the heading a line is added into: revenue,
direct cost (the cost of doing the work) or overhead (running costs such as premises).
**Posted** means the line counts. **Cancelled** means it does not.

## 3. Costs are stored as minus numbers, so the total is just addition

In the data, money in carries a plus sign and money out carries a minus sign. The "minus" in
"revenue minus costs" is already inside each cost figure.

So you never need a rule about when to subtract. You add the seven posted lines as they stand:

```
   1000.00      T001
  + 500.00      T002
  - 100.00      T003
  - 400.00      T004
  - 200.00      T005
  +  20.00      T006
  - 100.00      T007
  ---------
    720.00      operating result
```

Grouped by report line, it is the same answer:

```
revenue      1000.00 + 500.00 - 100.00   =  1400.00
direct cost  -400.00 - 200.00 + 20.00    =  -580.00
overhead                                  =  -100.00
operating result  1400.00 - 580.00 - 100.00 = 720.00
```

## 4. Why the management table then shows costs as plus numbers

Managers read "we spent 580" more easily than "we spent minus 580". So the report **displays**
costs as positive. That is a change of label, not a different number.

```
   STORED in the data              DISPLAYED in the management table
   direct_cost   -580.00   ---->   Direct cost    580.00
   overhead      -100.00   ---->   Overhead       100.00
                    (multiply by -1, and change the label)
```

The rule: add up the **stored** numbers; show the **displayed** ones. Never add a displayed
number to a stored one.

## 5. A refund: T003, −100.00 on a revenue line

We gave 100.00 back to a customer. It sits on the **revenue** line as a minus number. It is
**less revenue**, not a cost.

Why it matters: if you moved it into costs, the operating result would still be 720.00. But
revenue and direct cost would both be wrong. The budget comparison is done line by line, so
you would then blame costs for a shortfall that is really in revenue.

## 6. A cost reversal: T006, +20.00 on a cost line

A **reversal** is part of a cost undone, for example a charge corrected after it was recorded.
It sits on the cost line as a plus number, because it makes the cost smaller. It is not income.

The tempting shortcut is to treat every cost as a plain positive size and subtract the lot. Watch
what that does to T006:

```
RIGHT (keep the signs)              WRONG (make every cost positive first)
direct cost = -400 - 200 + 20       direct cost = 400 + 200 + 20 = 620
            = -580.00               result      = 1400 - 620 - 100
result      = 1400 - 580 - 100                  = 680.00
            = 720.00
```

The shortcut turns "20.00 less cost" into "20.00 more cost". The answer comes out as 680.00
instead of 720.00.

## 7. A cancelled line: T008, 999.00

T008 was called off. It is **left out of every total** and **kept in the file**, so anyone can
see it existed.

Include it by mistake and the result becomes 720.00 + 999.00 = **1719.00**.

The unit's own record agrees with leaving it out: 8 lines sent, 7 posted, posted total 720.00.

## 8. Favourable variance: how far from budget, and in which direction

The budget for the same month, stored with the same signs:

| Report line | Budget | Actual |
|---|---:|---:|
| revenue | 1500.00 | 1400.00 |
| direct cost | -600.00 | -580.00 |
| overhead | -100.00 | -100.00 |
| **operating result** | **800.00** | **720.00** |

**Favourable variance = actual − budget**, line by line, on the stored numbers. Read the sign the
same way on every line: **plus is better than budget, minus is worse.** "Favourable variance" is
the name of the measure, not a verdict, so it can be negative.

| Line | Calculation | In words | Result |
|---|---|---|---:|
| revenue | 1400.00 − 1500.00 | earned 100.00 less than planned | **−100.00** |
| direct cost | −580.00 − (−600.00) | planned to spend 600.00, spent 580.00 | **+20.00** |
| overhead | −100.00 − (−100.00) | spent exactly the plan | **0.00** |
| **total** | −100.00 + 20.00 + 0.00 | | **−80.00** |

**Cross-check:** actual result minus budget result, 720.00 − 800.00 = **−80.00**. Same answer.

The same story as a ladder from budget to actual:

```
Budget operating result          800.00
  revenue below budget          -100.00
  direct cost below budget       +20.00
  overhead on budget               0.00
                                --------
Actual operating result          720.00
```

One warning. If you subtract the *displayed* costs instead (580.00 − 600.00), the sign flips:
good news comes out with a minus. That is a different measure (overspend), and it must never
be labelled "variance".

## Key points
1. N01's December operating result is **720.00**: the seven posted lines, added as stored.
2. **1719.00** means the cancelled line was counted; **680.00** means the cost reversal was made positive.
3. "Direct cost 580.00" in a report and "−580.00" in the data are the same number with different labels.
4. A refund is less revenue, not more cost; a reversal is less cost, not more revenue.
5. We were **80.00 below budget**: revenue 100.00 short, direct cost 20.00 better, overhead on plan.
