"""Source for data/problems.json. Run: python3 tools/build_problems.py
Each problem: tests hold only inputs; expected outputs are computed from the Python reference solution,
then the JavaScript reference is checked against the same expectations (tools/check_problems.mjs)."""
import random

CATS = [
 {"id":"basics","name":"Warm-ups","icon":"zap","blurb":"Small, friendly problems for your first weeks. Loops, conditions, strings and lists.",
  "pattern":["Read the input carefully, decide what to return, then walk through the data once with a loop.","Most warm-ups are one loop plus one variable that accumulates the answer (a count, a sum, a best-so-far)."],
  "template":"def solve(items):\n    answer = 0            # the accumulator\n    for x in items:       # one pass over the data\n        if condition(x):\n            answer += 1   # update it\n    return answer"},
 {"id":"arrays","name":"Arrays & Hashing","icon":"hash","blurb":"Trade memory for speed with sets and dictionaries.",
  "pattern":["When a brute-force answer compares every pair (O(n²)), ask: what would I need to remember to answer in one pass? Usually a set of things seen or a dict from value to index or count.","Hash lookups are O(1) on average, so one pass with a dict turns many O(n²) problems into O(n)."],
  "template":"def one_pass(nums):\n    seen = {}                 # value -> index (or count)\n    for i, x in enumerate(nums):\n        if need(x) in seen:   # answer found using memory\n            return seen[need(x)], i\n        seen[x] = i\n    return None"},
 {"id":"two-pointers","name":"Two Pointers","icon":"code","blurb":"Walk inward from both ends, or chase with a fast and slow pointer.",
  "pattern":["On sorted data (or symmetric problems like palindromes) put one pointer at each end. Compare, then move the pointer that can improve the answer.","Each step discards at least one element, so the scan is O(n) with O(1) extra memory."],
  "template":"def two_pointers(a):\n    lo, hi = 0, len(a) - 1\n    while lo < hi:\n        if good(a[lo], a[hi]):\n            return lo, hi\n        if too_small(a[lo], a[hi]):\n            lo += 1\n        else:\n            hi -= 1"},
 {"id":"sliding-window","name":"Sliding Window","icon":"layers","blurb":"Grow a window on the right, shrink it on the left.",
  "pattern":["For 'longest/shortest contiguous subarray or substring such that…', keep a window [left, right]. Extend right one step at a time; while the window breaks the rule, move left forward.","Both pointers only move forward, so the total work is O(n) even though there is a loop inside a loop."],
  "template":"def window(s):\n    left = 0\n    state = {}\n    best = 0\n    for right, ch in enumerate(s):\n        add(state, ch)\n        while invalid(state):\n            remove(state, s[left])\n            left += 1\n        best = max(best, right - left + 1)\n    return best"},
 {"id":"stack","name":"Stack","icon":"layers","blurb":"Last in, first out: matching brackets, undo, and monotonic stacks.",
  "pattern":["Use a stack when the most recent unfinished thing is the one you need next: an open bracket, an operand, a day waiting for a warmer day.","A monotonic stack keeps elements in increasing or decreasing order; each element is pushed and popped at most once, so it's O(n)."],
  "template":"def next_greater(nums):\n    ans = [-1] * len(nums)\n    stack = []                       # indices, values decreasing\n    for i, x in enumerate(nums):\n        while stack and nums[stack[-1]] < x:\n            ans[stack.pop()] = x\n        stack.append(i)\n    return ans"},
 {"id":"binary-search","name":"Binary Search","icon":"target","blurb":"Halve the search space every step: O(log n).",
  "pattern":["If the data is sorted, or if the answer is monotonic (every value below some point fails and every value above passes), you can binary search it.","Keep an invariant about lo and hi and make sure each iteration shrinks the range, or you'll loop forever."],
  "template":"def first_true(lo, hi, ok):\n    # smallest x in [lo, hi] with ok(x) True\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if ok(mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo"},
 {"id":"linked-list","name":"Linked List","icon":"chain","blurb":"Rewire pointers carefully; a dummy head saves edge cases.",
  "pattern":["Draw the boxes and arrows. Most bugs are a lost reference: save `nxt = cur.next` before you overwrite `cur.next`.","A dummy node before the head means you never special-case 'the head changed'. Fast/slow pointers find middles and cycles."],
  "template":"def reverse(head):\n    prev, cur = None, head\n    while cur:\n        nxt = cur.next\n        cur.next = prev\n        prev, cur = cur, nxt\n    return prev"},
 {"id":"trees","name":"Trees","icon":"flow","blurb":"Recursion is natural: solve for the children, combine at the parent.",
  "pattern":["Most tree problems are: what does each subtree return, and how does the parent combine the two answers? Write the base case for `None` first.","Use BFS with a queue when the problem says 'level' or 'closest'; use DFS (recursion) for everything else."],
  "template":"def dfs(node):\n    if node is None:\n        return BASE\n    left = dfs(node.left)\n    right = dfs(node.right)\n    return combine(node.val, left, right)"},
 {"id":"heap","name":"Heaps","icon":"bars","blurb":"Always know the smallest (or largest) item in O(log n).",
  "pattern":["A heap answers 'give me the current minimum' quickly while items keep arriving. For the top k of something, keep a min-heap of size k: the root is the k-th best.","Python's `heapq` is a min-heap; push negatives for a max-heap. In JavaScript there is no built-in heap, so sorting is fine at these sizes."],
  "template":"import heapq\n\ndef k_largest(nums, k):\n    heap = []\n    for x in nums:\n        heapq.heappush(heap, x)\n        if len(heap) > k:\n            heapq.heappop(heap)\n    return heap[0]"},
 {"id":"backtracking","name":"Backtracking","icon":"route","blurb":"Explore every choice, undo it, try the next.",
  "pattern":["Build the answer one choice at a time. At each step: choose, recurse, un-choose. Record a copy when the partial answer is complete.","Prune early: if a partial answer can't possibly work, return before going deeper."],
  "template":"def backtrack(path, choices):\n    if complete(path):\n        result.append(path[:])\n        return\n    for c in choices:\n        if allowed(path, c):\n            path.append(c)\n            backtrack(path, next_choices(c))\n            path.pop()"},
 {"id":"graphs","name":"Graphs","icon":"globe","blurb":"Grids and networks: BFS, DFS and topological order.",
  "pattern":["Model the problem as nodes and edges. A grid is a graph where each cell links to its 4 neighbours.","BFS gives shortest paths in unweighted graphs; DFS explores components; Kahn's algorithm (in-degree queue) orders tasks and detects cycles."],
  "template":"from collections import deque\n\ndef bfs(start, neighbours):\n    seen = {start}\n    q = deque([(start, 0)])\n    while q:\n        node, dist = q.popleft()\n        for nb in neighbours(node):\n            if nb not in seen:\n                seen.add(nb)\n                q.append((nb, dist + 1))"},
 {"id":"dp","name":"Dynamic Programming","icon":"grid","blurb":"Overlapping subproblems: solve each once, reuse forever.",
  "pattern":["Define the state in words (\"dp[i] = the best answer for the first i items\"), write the transition from smaller states, then the base cases.","Start with recursion plus memoisation if the table feels hard; convert to a bottom-up loop once it works."],
  "template":"def dp_solve(n):\n    dp = [0] * (n + 1)\n    dp[0] = BASE\n    for i in range(1, n + 1):\n        dp[i] = best_of(dp[j] + cost(j, i) for j in options(i))\n    return dp[n]"},
 {"id":"greedy","name":"Greedy & Intervals","icon":"clock","blurb":"Make the locally best choice, after sorting the right way.",
  "pattern":["Sort intervals by start (to merge) or by end (to schedule the most). Then one pass decides each interval by comparing with the last kept one.","A greedy choice needs a reason it's safe: an exchange argument that any optimal answer can be rearranged to include it."],
  "template":"def merge(intervals):\n    intervals.sort()\n    out = []\n    for s, e in intervals:\n        if out and s <= out[-1][1]:\n            out[-1][1] = max(out[-1][1], e)\n        else:\n            out.append([s, e])\n    return out"},
 {"id":"bits","name":"Math & Bits","icon":"binary","blurb":"XOR tricks, counting bits and arithmetic insight.",
  "pattern":["`x ^ x == 0` and `x ^ 0 == x`, so XOR-ing everything cancels pairs. `n & (n - 1)` clears the lowest set bit.","Many 'find the missing/extra number' problems have an O(1)-memory answer with a sum formula or XOR."],
  "template":"def popcount(n):\n    count = 0\n    while n:\n        n &= n - 1   # drop lowest set bit\n        count += 1\n    return count"},
 {"id":"design","name":"Design","icon":"cube","blurb":"Build a data structure with guaranteed operation costs.",
  "pattern":["Pick the operations' target costs first, then combine structures that achieve them: a dict for O(1) lookup, a list or linked list for order, a second stack for running minimums.","Test with a sequence of operations, not single calls."],
  "template":"class Thing:\n    def __init__(self):\n        self.index = {}     # fast lookup\n        self.order = []     # keeps sequence\n\n    def op(self, x):\n        ..."}
]

R = random.Random(42)
def rints(n, lo, hi): return [R.randint(lo, hi) for _ in range(n)]

P = []
def add(**k): P.append(k)

# ------------------------------------------------------------------ WARM-UPS
add(id="fizz-buzz", title="FizzBuzz", difficulty="Easy", cat="basics", tags=["Loops","Strings"],
 desc=["Given a whole number `n`, return a list of strings for the numbers 1 to `n`.","For multiples of 3 use `\"Fizz\"`, for multiples of 5 use `\"Buzz\"`, for multiples of both use `\"FizzBuzz\"`, and otherwise use the number itself as a string."],
 constraints=["1 <= n <= 10^4"], params=["n"], fn={"py":"fizz_buzz","js":"fizzBuzz"},
 examples=[[5],[15]], tests=[[1],[3],[5],[15],[16],[30],[2],[100]],
 hints=["Check the 'both' case first, or build the string by appending 'Fizz' and 'Buzz'.","`str(i)` in Python and `String(i)` in JavaScript turn a number into text."],
 editorial=["Loop from 1 to n. A number divisible by 15 is divisible by both 3 and 5, so test that first (or build the word from two independent checks and fall back to the number if it's empty)."],
 complexity="O(n) time, O(n) space for the output.",
 py='''def fizz_buzz(n):
    out = []
    for i in range(1, n + 1):
        word = ""
        if i % 3 == 0:
            word += "Fizz"
        if i % 5 == 0:
            word += "Buzz"
        out.append(word or str(i))
    return out''',
 js='''function fizzBuzz(n) {
  const out = [];
  for (let i = 1; i <= n; i++) {
    let word = "";
    if (i % 3 === 0) word += "Fizz";
    if (i % 5 === 0) word += "Buzz";
    out.push(word || String(i));
  }
  return out;
}''')

add(id="reverse-string", title="Reverse a String", difficulty="Easy", cat="basics", tags=["Strings","Loops"],
 desc=["Return the string `s` with its characters in reverse order.","Try writing it with a loop first, then look up the one-line idiom in your language."],
 constraints=["0 <= s.length <= 10^5","s contains printable ASCII characters"], params=["s"], fn={"py":"reverse_string","js":"reverseString"},
 examples=[["hello"],["CodeLearner"]], tests=[["hello"],["CodeLearner"],[""],["a"],["racecar"],["ab"],["Hello, World!"],["12345"]],
 hints=["Start from the last index, `len(s) - 1`, and walk down to 0.","Python: `s[::-1]`. JavaScript: `[...s].reverse().join(\"\")`."],
 editorial=["Walk the indices from the end to the start and collect characters. Joining a list once is faster than adding to a string repeatedly, because strings are immutable and each `+` copies."],
 complexity="O(n) time and space.",
 py='''def reverse_string(s):
    chars = []
    for i in range(len(s) - 1, -1, -1):
        chars.append(s[i])
    return "".join(chars)''',
 js='''function reverseString(s) {
  let out = "";
  for (let i = s.length - 1; i >= 0; i--) out += s[i];
  return out;
}''')

add(id="count-vowels", title="Count the Vowels", difficulty="Easy", cat="basics", tags=["Strings","Counting"],
 desc=["Return how many vowels (`a`, `e`, `i`, `o`, `u`, in upper or lower case) appear in the string `s`."],
 constraints=["0 <= s.length <= 10^5"], params=["s"], fn={"py":"count_vowels","js":"countVowels"},
 examples=[["Hello World"],["rhythm"]], tests=[["Hello World"],["rhythm"],[""],["AEIOU"],["aeiouAEIOU"],["Programming is fun"],["xyz"],["Queueing"]],
 hints=["Lower-case the string once so you only compare against five letters.","Membership in a string or set: `ch in \"aeiou\"`."],
 editorial=["Convert to lower case, then count characters that are in the vowel set. One pass, constant extra memory."],
 complexity="O(n) time, O(1) space.",
 py='''def count_vowels(s):
    return sum(1 for ch in s.lower() if ch in "aeiou")''',
 js='''function countVowels(s) {
  let n = 0;
  for (const ch of s.toLowerCase()) if ("aeiou".includes(ch)) n++;
  return n;
}''')

add(id="largest-number", title="Largest Number in a List", difficulty="Easy", cat="basics", tags=["Arrays","Loops"],
 desc=["Return the largest number in the non-empty list `nums` without using the built-in `max` (Python) or `Math.max` (JavaScript).","The point is to practise the 'best so far' pattern you'll use in hundreds of harder problems."],
 constraints=["1 <= nums.length <= 10^5","-10^9 <= nums[i] <= 10^9"], params=["nums"], fn={"py":"largest_number","js":"largestNumber"},
 examples=[[[3,9,2,7]],[[-5,-2,-9]]], tests=[[[3,9,2,7]],[[-5,-2,-9]],[[42]],[[1,1,1]],[[0,-1]],[[5,4,3,2,1]],[[1,2,3,4,5]],[rints(2000,-10**9,10**9)]],
 hints=["Start with the first element as your best guess, not 0. Why would 0 be wrong?","Loop over the rest and replace the best when you see something bigger."],
 editorial=["Initialise `best = nums[0]` (initialising to 0 fails when every number is negative). Walk the list once and update `best` whenever an element is larger."],
 complexity="O(n) time, O(1) space.",
 py='''def largest_number(nums):
    best = nums[0]
    for x in nums[1:]:
        if x > best:
            best = x
    return best''',
 js='''function largestNumber(nums) {
  let best = nums[0];
  for (const x of nums) if (x > best) best = x;
  return best;
}''')

add(id="sum-of-digits", title="Sum of Digits", difficulty="Easy", cat="basics", tags=["Math","Loops"],
 desc=["Given a non-negative integer `n`, return the sum of its decimal digits.","Solve it with arithmetic (`%` and `//`) rather than converting to a string."],
 constraints=["0 <= n <= 10^15"], params=["n"], fn={"py":"sum_of_digits","js":"sumOfDigits"},
 examples=[[1234],[0]], tests=[[1234],[0],[9],[10],[99999],[1000000],[987654321],[505]],
 hints=["`n % 10` is the last digit.","`n // 10` (Python) or `Math.floor(n / 10)` (JavaScript) drops the last digit."],
 editorial=["Repeatedly take the last digit with `n % 10`, add it, then remove it by integer division by 10, until `n` is 0."],
 complexity="O(d) time where d is the number of digits, O(1) space.",
 py='''def sum_of_digits(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total''',
 js='''function sumOfDigits(n) {
  let total = 0;
  while (n > 0) {
    total += n % 10;
    n = Math.floor(n / 10);
  }
  return total;
}''')

add(id="factorial", title="Factorial", difficulty="Easy", cat="basics", tags=["Math","Recursion"],
 desc=["Return `n!`, the product `1 × 2 × … × n`. By definition `0! = 1`.","Write it once with a loop and once with recursion. Which one would you trust for `n = 5000`?"],
 constraints=["0 <= n <= 18 (so the answer fits in a JavaScript number exactly)"], params=["n"], fn={"py":"factorial","js":"factorial"},
 examples=[[5],[0]], tests=[[0],[1],[2],[5],[10],[12],[15],[18]],
 hints=["Start the product at 1, not 0.","Recursive version: `n! = n × (n-1)!` with base case `0! = 1`."],
 editorial=["A loop multiplying 1..n is the safest version. The recursive one is elegant but uses one stack frame per call, so very large `n` would exceed the recursion limit."],
 complexity="O(n) time, O(1) space for the loop.",
 py='''def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result''',
 js='''function factorial(n) {
  let result = 1;
  for (let i = 2; i <= n; i++) result *= i;
  return result;
}''')

add(id="leap-year", title="Is It a Leap Year?", difficulty="Easy", cat="basics", tags=["Conditions"],
 desc=["Return `true` if `year` is a leap year in the Gregorian calendar.","A year is a leap year if it is divisible by 4, except years divisible by 100, unless they are also divisible by 400. So 2000 was a leap year and 1900 was not."],
 constraints=["1 <= year <= 10^5"], params=["year"], fn={"py":"is_leap_year","js":"isLeapYear"},
 examples=[[2024],[1900],[2000]], tests=[[2024],[1900],[2000],[2023],[2100],[2400],[4],[1]],
 hints=["Combine the three rules with `and` / `or`.","`year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)`"],
 editorial=["Translate the rule directly: divisible by 400, or divisible by 4 but not by 100. Order the checks from most specific to least to keep it readable."],
 complexity="O(1).",
 py='''def is_leap_year(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)''',
 js='''function isLeapYear(year) {
  return year % 400 === 0 || (year % 4 === 0 && year % 100 !== 0);
}''')

# ------------------------------------------------------------------ ARRAYS & HASHING
big = list(range(1, 4001)); R.shuffle(big)
add(id="two-sum", title="Two Sum", difficulty="Easy", cat="arrays", tags=["Array","Hash Table"],
 desc=["Given a list of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`, as `[i, j]` with `i < j`.","Exactly one pair works, and you may not use the same element twice."],
 constraints=["2 <= nums.length <= 10^4","-10^9 <= nums[i], target <= 10^9","Exactly one valid answer exists"], params=["nums","target"], fn={"py":"two_sum","js":"twoSum"},
 examples=[[[2,7,11,15],9],[[3,2,4],6]], tests=[[[2,7,11,15],9],[[3,2,4],6],[[3,3],6],[[-1,-2,-3,-4,-5],-8],[[0,4,3,0],0],[[1,5,9,13],22],[big, big[-1]+big[-2]]],
 hints=["The brute force checks every pair: O(n²). What do you need to remember to do one pass?","For each `x`, the partner you need is `target - x`. Have you seen it before?"],
 editorial=["Walk the list once with a dictionary from value to index. For each `nums[j]`, check whether `target - nums[j]` is already in the dictionary; if so, return its index and `j`. Otherwise store `nums[j]`. Checking before storing means an element never pairs with itself."],
 complexity="O(n) time, O(n) space.",
 py='''def two_sum(nums, target):
    seen = {}
    for j, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], j]
        seen[x] = j
    return []''',
 js='''function twoSum(nums, target) {
  const seen = new Map();
  for (let j = 0; j < nums.length; j++) {
    const need = target - nums[j];
    if (seen.has(need)) return [seen.get(need), j];
    seen.set(nums[j], j);
  }
  return [];
}''')

add(id="contains-duplicate", title="Contains Duplicate", difficulty="Easy", cat="arrays", tags=["Array","Hash Set"],
 desc=["Return `true` if any value appears at least twice in `nums`, and `false` if every element is distinct."],
 constraints=["1 <= nums.length <= 10^5","-10^9 <= nums[i] <= 10^9"], params=["nums"], fn={"py":"contains_duplicate","js":"containsDuplicate"},
 examples=[[[1,2,3,1]],[[1,2,3,4]]], tests=[[[1,2,3,1]],[[1,2,3,4]],[[1]],[[1,1,1,3,3,4,3,2,4,2]],[[-1,0,1,-1]],[list(range(5000))],[list(range(5000))+[4999]]],
 hints=["A set remembers what you've seen with O(1) lookups.","Or compare `len(set(nums))` with `len(nums)`."],
 editorial=["Add elements to a set; if an element is already there, you've found a duplicate. Sorting and comparing neighbours also works in O(n log n) with less memory."],
 complexity="O(n) time, O(n) space.",
 py='''def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False''',
 js='''function containsDuplicate(nums) {
  return new Set(nums).size !== nums.length;
}''')

add(id="valid-anagram", title="Valid Anagram", difficulty="Easy", cat="arrays", tags=["String","Hash Table","Counting"],
 desc=["Return `true` if `t` is an anagram of `s`: the same letters with the same counts, possibly in a different order."],
 constraints=["1 <= s.length, t.length <= 5 × 10^4","s and t contain lowercase English letters"], params=["s","t"], fn={"py":"is_anagram","js":"isAnagram"},
 examples=[["anagram","nagaram"],["rat","car"]], tests=[["anagram","nagaram"],["rat","car"],["a","a"],["ab","a"],["listen","silent"],["aacc","ccac"],["abc","cba"]],
 hints=["Different lengths can never be anagrams.","Count letters of `s` up, letters of `t` down; every count must end at 0."],
 editorial=["Build a frequency count for each string and compare. With only 26 letters, an array of 26 counters is enough and keeps memory constant."],
 complexity="O(n) time, O(1) space (26 counters).",
 py='''def is_anagram(s, t):
    if len(s) != len(t):
        return False
    counts = {}
    for a, b in zip(s, t):
        counts[a] = counts.get(a, 0) + 1
        counts[b] = counts.get(b, 0) - 1
    return all(v == 0 for v in counts.values())''',
 js='''function isAnagram(s, t) {
  if (s.length !== t.length) return false;
  const c = new Array(26).fill(0);
  for (let i = 0; i < s.length; i++) {
    c[s.charCodeAt(i) - 97]++;
    c[t.charCodeAt(i) - 97]--;
  }
  return c.every(v => v === 0);
}''')

add(id="group-anagrams", title="Group Anagrams", difficulty="Medium", cat="arrays", tags=["String","Hash Table","Sorting"],
 desc=["Group the strings in `strs` so that anagrams are together. Return a list of groups; the order of groups and of words inside a group doesn't matter."],
 constraints=["1 <= strs.length <= 10^4","0 <= strs[i].length <= 100","lowercase English letters"], params=["strs"], fn={"py":"group_anagrams","js":"groupAnagrams"}, cmp="deep",
 examples=[[["eat","tea","tan","ate","nat","bat"]],[[""]]], tests=[[["eat","tea","tan","ate","nat","bat"]],[[""]],[["a"]],[["abc","bca","cab","xyz","zyx","q"]],[["",""]],[["ab","ba","ab"]]],
 hints=["Two words are anagrams exactly when their sorted letters are equal.","Use the sorted word as a dictionary key."],
 editorial=["Map each word to a canonical key (its letters sorted, or a tuple of 26 counts) and append the word to `groups[key]`. The dictionary's values are the answer."],
 complexity="O(n · k log k) time for n words of length up to k; O(n · k) space.",
 py='''def group_anagrams(strs):
    groups = {}
    for w in strs:
        groups.setdefault("".join(sorted(w)), []).append(w)
    return list(groups.values())''',
 js='''function groupAnagrams(strs) {
  const groups = new Map();
  for (const w of strs) {
    const k = [...w].sort().join("");
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(w);
  }
  return [...groups.values()];
}''')

add(id="top-k-frequent", title="Top K Frequent Elements", difficulty="Medium", cat="arrays", tags=["Array","Hash Table","Bucket Sort","Heap"],
 desc=["Return the `k` most frequent elements of `nums`, in any order. The answer is guaranteed to be unique."],
 constraints=["1 <= nums.length <= 10^5","1 <= k <= number of distinct elements","The answer is unique"], params=["nums","k"], fn={"py":"top_k_frequent","js":"topKFrequent"}, cmp="unordered",
 examples=[[[1,1,1,2,2,3],2],[[1],1]], tests=[[[1,1,1,2,2,3],2],[[1],1],[[4,4,4,5,5,6,6,6,6],1],[[-1,-1,2,2,2,3],2],[[7,7,8,8,8,9,9,9,9],3]],
 hints=["Count first. Then you need the k largest counts.","Bucket sort: a list where index `c` holds the values that appear `c` times."],
 editorial=["Count with a dictionary. Then either sort the distinct values by count (O(n log n)), keep a min-heap of size k (O(n log k)), or use buckets indexed by count and read from the top (O(n))."],
 complexity="O(n) time with buckets, O(n) space.",
 py='''def top_k_frequent(nums, k):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    buckets = [[] for _ in range(len(nums) + 1)]
    for x, c in count.items():
        buckets[c].append(x)
    out = []
    for c in range(len(buckets) - 1, 0, -1):
        for x in buckets[c]:
            out.append(x)
            if len(out) == k:
                return out
    return out''',
 js='''function topKFrequent(nums, k) {
  const count = new Map();
  for (const x of nums) count.set(x, (count.get(x) || 0) + 1);
  return [...count.entries()].sort((a, b) => b[1] - a[1]).slice(0, k).map(e => e[0]);
}''')

add(id="product-except-self", title="Product of Array Except Self", difficulty="Medium", cat="arrays", tags=["Array","Prefix Sum"],
 desc=["Return a list `answer` where `answer[i]` is the product of every element of `nums` except `nums[i]`.","Do it in O(n) time without using division."],
 constraints=["2 <= nums.length <= 10^5","-30 <= nums[i] <= 30","Every prefix and suffix product fits in a 32-bit integer"], params=["nums"], fn={"py":"product_except_self","js":"productExceptSelf"},
 examples=[[[1,2,3,4]],[[-1,1,0,-3,3]]], tests=[[[1,2,3,4]],[[-1,1,0,-3,3]],[[2,3]],[[0,0]],[[1,1,1,1]],[[5,0,2]],[[-2,-3,4]]],
 hints=["answer[i] = (product of everything left of i) × (product of everything right of i).","Fill the output left to right with prefix products, then sweep right to left multiplying in a running suffix product."],
 editorial=["Two passes. First, `out[i]` = product of `nums[0..i-1]`. Then walk backwards with a running product of `nums[i+1..]`, multiplying it into `out[i]`. No division, so zeros need no special case."],
 complexity="O(n) time, O(1) extra space besides the output.",
 py='''def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    for i in range(1, n):
        out[i] = out[i - 1] * nums[i - 1]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out''',
 js='''function productExceptSelf(nums) {
  const n = nums.length, out = new Array(n).fill(1);
  for (let i = 1; i < n; i++) out[i] = out[i - 1] * nums[i - 1];
  let right = 1;
  for (let i = n - 1; i >= 0; i--) {
    out[i] *= right;
    right *= nums[i];
  }
  return out;
}''')

add(id="longest-consecutive", title="Longest Consecutive Sequence", difficulty="Medium", cat="arrays", tags=["Array","Hash Set"],
 desc=["Given an unsorted list `nums`, return the length of the longest run of consecutive integers (like 4, 5, 6, 7) that can be formed from its elements.","Aim for O(n) time."],
 constraints=["0 <= nums.length <= 10^5","-10^9 <= nums[i] <= 10^9"], params=["nums"], fn={"py":"longest_consecutive","js":"longestConsecutive"},
 examples=[[[100,4,200,1,3,2]],[[0,3,7,2,5,8,4,6,0,1]]], tests=[[[100,4,200,1,3,2]],[[0,3,7,2,5,8,4,6,0,1]],[[]],[[5]],[[1,2,0,1]],[[9,1,-3,2,4,8,3,-1,6,-2,-4,7]],[big]],
 hints=["Put everything in a set.","Only start counting from a number `x` when `x - 1` is not in the set: that's the start of a run."],
 editorial=["Insert all numbers into a set. For each `x` that starts a run (no `x - 1` present), count up while `x + 1, x + 2, …` exist. Each number is visited by at most one run, so the total is O(n)."],
 complexity="O(n) time, O(n) space.",
 py='''def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:
            y = x
            while y + 1 in s:
                y += 1
            best = max(best, y - x + 1)
    return best''',
 js='''function longestConsecutive(nums) {
  const s = new Set(nums);
  let best = 0;
  for (const x of s) {
    if (!s.has(x - 1)) {
      let y = x;
      while (s.has(y + 1)) y++;
      best = Math.max(best, y - x + 1);
    }
  }
  return best;
}''')

add(id="majority-element", title="Majority Element", difficulty="Easy", cat="arrays", tags=["Array","Counting","Boyer-Moore"],
 desc=["Return the element that appears more than `n / 2` times in `nums`. It always exists.","Can you do it in O(1) extra memory?"],
 constraints=["1 <= nums.length <= 5 × 10^4","A majority element always exists"], params=["nums"], fn={"py":"majority_element","js":"majorityElement"},
 examples=[[[3,2,3]],[[2,2,1,1,1,2,2]]], tests=[[[3,2,3]],[[2,2,1,1,1,2,2]],[[1]],[[5,5,5,1,2]],[[-1,-1,-1,7,7]],[[8,9,8,9,8]]],
 hints=["Counting with a dict works in O(n) memory.","Boyer–Moore voting: keep a candidate and a counter; matching elements vote +1, others −1."],
 editorial=["Boyer–Moore: when the counter hits 0, adopt the current element as the candidate. Each non-majority element can cancel at most one majority vote, and the majority has more than half, so it survives as the final candidate."],
 complexity="O(n) time, O(1) space.",
 py='''def majority_element(nums):
    cand, count = None, 0
    for x in nums:
        if count == 0:
            cand = x
        count += 1 if x == cand else -1
    return cand''',
 js='''function majorityElement(nums) {
  let cand = null, count = 0;
  for (const x of nums) {
    if (count === 0) cand = x;
    count += x === cand ? 1 : -1;
  }
  return cand;
}''')

# ------------------------------------------------------------------ TWO POINTERS
add(id="valid-palindrome", title="Valid Palindrome", difficulty="Easy", cat="two-pointers", tags=["String","Two Pointers"],
 desc=["A phrase is a palindrome if, after lower-casing it and removing every non-alphanumeric character, it reads the same forwards and backwards.","Return `true` if `s` is a palindrome."],
 constraints=["1 <= s.length <= 2 × 10^5","printable ASCII"], params=["s"], fn={"py":"is_palindrome","js":"isPalindrome"},
 examples=[["A man, a plan, a canal: Panama"],["race a car"]], tests=[["A man, a plan, a canal: Panama"],["race a car"],[" "],["a."],["0P"],["No 'x' in Nixon"],["ab_a"],["Was it a car or a cat I saw?"]],
 hints=["Two pointers: one from each end, skipping characters that aren't letters or digits.","Python: `ch.isalnum()`. JavaScript: `/[a-z0-9]/i.test(ch)`."],
 editorial=["Move `lo` right and `hi` left, skipping non-alphanumerics, and compare lower-cased characters. Stop at the first mismatch. No cleaned copy of the string is needed."],
 complexity="O(n) time, O(1) space.",
 py='''def is_palindrome(s):
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if not s[lo].isalnum():
            lo += 1
        elif not s[hi].isalnum():
            hi -= 1
        elif s[lo].lower() != s[hi].lower():
            return False
        else:
            lo += 1
            hi -= 1
    return True''',
 js='''function isPalindrome(s) {
  const ok = c => /[a-z0-9]/i.test(c);
  let lo = 0, hi = s.length - 1;
  while (lo < hi) {
    if (!ok(s[lo])) lo++;
    else if (!ok(s[hi])) hi--;
    else if (s[lo].toLowerCase() !== s[hi].toLowerCase()) return false;
    else { lo++; hi--; }
  }
  return true;
}''')

add(id="two-sum-sorted", title="Two Sum II: Sorted Input", difficulty="Medium", cat="two-pointers", tags=["Array","Two Pointers","Binary Search"],
 desc=["`numbers` is sorted in non-decreasing order. Return the **1-based** indices `[i, j]` (`i < j`) of the two numbers that add up to `target`.","Use only constant extra space."],
 constraints=["2 <= numbers.length <= 3 × 10^4","Exactly one solution exists"], params=["numbers","target"], fn={"py":"two_sum_sorted","js":"twoSumSorted"},
 examples=[[[2,7,11,15],9],[[2,3,4],6]], tests=[[[2,7,11,15],9],[[2,3,4],6],[[-1,0],-1],[[1,2,3,4,4,9,56,90],8],[[5,25,75],100],[list(range(1,3001)),5999]],
 hints=["If the current sum is too small, which pointer should move?","Start with `lo = 0`, `hi = len - 1`."],
 editorial=["Because the array is sorted, a sum that's too small can only grow by moving `lo` right, and a sum too big can only shrink by moving `hi` left. Each step eliminates one element, so it's O(n)."],
 complexity="O(n) time, O(1) space.",
 py='''def two_sum_sorted(numbers, target):
    lo, hi = 0, len(numbers) - 1
    while lo < hi:
        s = numbers[lo] + numbers[hi]
        if s == target:
            return [lo + 1, hi + 1]
        if s < target:
            lo += 1
        else:
            hi -= 1
    return []''',
 js='''function twoSumSorted(numbers, target) {
  let lo = 0, hi = numbers.length - 1;
  while (lo < hi) {
    const s = numbers[lo] + numbers[hi];
    if (s === target) return [lo + 1, hi + 1];
    if (s < target) lo++; else hi--;
  }
  return [];
}''')

add(id="three-sum", title="3Sum", difficulty="Medium", cat="two-pointers", tags=["Array","Two Pointers","Sorting"],
 desc=["Return all **unique** triplets `[a, b, c]` from `nums` (using three different positions) such that `a + b + c == 0`.","The order of triplets and of numbers inside a triplet doesn't matter, but the same triplet must not appear twice."],
 constraints=["3 <= nums.length <= 3000","-10^5 <= nums[i] <= 10^5"], params=["nums"], fn={"py":"three_sum","js":"threeSum"}, cmp="deep",
 examples=[[[-1,0,1,2,-1,-4]],[[0,1,1]],[[0,0,0]]], tests=[[[-1,0,1,2,-1,-4]],[[0,1,1]],[[0,0,0]],[[0,0,0,0]],[[-2,0,1,1,2]],[[1,-1,-1,0]],[[-4,-2,-2,-2,0,1,2,2,2,3,3,4,4,6,6]]],
 hints=["Sort first. Fix the first number, then it's Two Sum II on the rest.","Skip a value equal to the previous one at every level to avoid duplicates."],
 editorial=["Sort. For each index `i` (skipping repeats of `nums[i]`), run two pointers on `i+1..n-1` looking for `-nums[i]`. After a hit, advance both pointers past equal values. Total O(n²), which beats the O(n³) brute force."],
 complexity="O(n²) time, O(1) extra space besides the output (sorting aside).",
 py='''def three_sum(nums):
    nums = sorted(nums)
    out = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                out.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
                hi -= 1
    return out''',
 js='''function threeSum(nums) {
  nums = [...nums].sort((a, b) => a - b);
  const out = [];
  for (let i = 0; i < nums.length - 2; i++) {
    if (i > 0 && nums[i] === nums[i - 1]) continue;
    let lo = i + 1, hi = nums.length - 1;
    while (lo < hi) {
      const s = nums[i] + nums[lo] + nums[hi];
      if (s < 0) lo++;
      else if (s > 0) hi--;
      else {
        out.push([nums[i], nums[lo], nums[hi]]);
        lo++;
        while (lo < hi && nums[lo] === nums[lo - 1]) lo++;
        hi--;
      }
    }
  }
  return out;
}''')

add(id="container-most-water", title="Container With Most Water", difficulty="Medium", cat="two-pointers", tags=["Array","Two Pointers","Greedy"],
 desc=["`height[i]` is the height of a vertical line at position `i`. Choose two lines that, together with the x-axis, hold the most water. Return that maximum area.","Area = (distance between the lines) × (height of the shorter line)."],
 constraints=["2 <= height.length <= 10^5","0 <= height[i] <= 10^4"], params=["height"], fn={"py":"max_area","js":"maxArea"},
 examples=[[[1,8,6,2,5,4,8,3,7]],[[1,1]]], tests=[[[1,8,6,2,5,4,8,3,7]],[[1,1]],[[4,3,2,1,4]],[[1,2,1]],[[2,3,4,5,18,17,6]],[[0,0]],[rints(3000,0,10**4)]],
 hints=["Start with the widest container. Moving the taller line inward can never help. Why?","Always move the shorter line."],
 editorial=["Start with pointers at both ends. The area is limited by the shorter line; moving the taller one can only shrink the width without raising that limit. So move the shorter line each step, tracking the best area."],
 complexity="O(n) time, O(1) space.",
 py='''def max_area(height):
    lo, hi, best = 0, len(height) - 1, 0
    while lo < hi:
        best = max(best, (hi - lo) * min(height[lo], height[hi]))
        if height[lo] < height[hi]:
            lo += 1
        else:
            hi -= 1
    return best''',
 js='''function maxArea(height) {
  let lo = 0, hi = height.length - 1, best = 0;
  while (lo < hi) {
    best = Math.max(best, (hi - lo) * Math.min(height[lo], height[hi]));
    if (height[lo] < height[hi]) lo++; else hi--;
  }
  return best;
}''')

add(id="move-zeroes", title="Move Zeroes", difficulty="Easy", cat="two-pointers", tags=["Array","Two Pointers","In-place"],
 desc=["Move every `0` in `nums` to the end while keeping the relative order of the non-zero elements.","Modify the list **in place**; the judge inspects `nums` after your function returns, so what you return is ignored."],
 constraints=["1 <= nums.length <= 10^4"], params=["nums"], fn={"py":"move_zeroes","js":"moveZeroes"}, inplace=0,
 examples=[[[0,1,0,3,12]],[[0]]], tests=[[[0,1,0,3,12]],[[0]],[[1,2,3]],[[0,0,1]],[[4,2,4,0,0,3,0,5,1,0]],[[1,0]]],
 hints=["Keep a `write` index for where the next non-zero belongs.","After placing all non-zeros, fill the rest with zeros (or swap as you go)."],
 editorial=["Walk with a read pointer; each time you see a non-zero, swap it into position `write` and advance `write`. Non-zeros keep their order and zeros drift to the end."],
 complexity="O(n) time, O(1) space.",
 py='''def move_zeroes(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1''',
 js='''function moveZeroes(nums) {
  let write = 0;
  for (let read = 0; read < nums.length; read++) {
    if (nums[read] !== 0) {
      [nums[write], nums[read]] = [nums[read], nums[write]];
      write++;
    }
  }
}''')

add(id="trapping-rain-water", title="Trapping Rain Water", difficulty="Hard", cat="two-pointers", tags=["Array","Two Pointers","Dynamic Programming"],
 desc=["`height` describes an elevation map where each bar has width 1. Compute how many units of rain water it traps."],
 constraints=["1 <= height.length <= 2 × 10^4","0 <= height[i] <= 10^5"], params=["height"], fn={"py":"trap","js":"trap"},
 examples=[[[0,1,0,2,1,0,1,3,2,1,2,1]],[[4,2,0,3,2,5]]], tests=[[[0,1,0,2,1,0,1,3,2,1,2,1]],[[4,2,0,3,2,5]],[[1]],[[3,0,3]],[[5,4,3,2,1]],[[2,0,2,0,2]],[[0,0,0]],[rints(2000,0,1000)]],
 hints=["Water above bar i = min(tallest bar to its left, tallest to its right) − height[i].","Two pointers: whichever side has the smaller max is the one whose water level you know for sure."],
 editorial=["Keep `left_max` and `right_max`. If `left_max <= right_max`, the water at `lo` is decided by `left_max` (there's something at least as tall on the right), so add `left_max - height[lo]` and move `lo`. Otherwise do the mirror step on `hi`."],
 complexity="O(n) time, O(1) space.",
 py='''def trap(height):
    lo, hi = 0, len(height) - 1
    left_max = right_max = water = 0
    while lo <= hi:
        if left_max <= right_max:
            left_max = max(left_max, height[lo])
            water += left_max - height[lo]
            lo += 1
        else:
            right_max = max(right_max, height[hi])
            water += right_max - height[hi]
            hi -= 1
    return water''',
 js='''function trap(height) {
  let lo = 0, hi = height.length - 1, lm = 0, rm = 0, water = 0;
  while (lo <= hi) {
    if (lm <= rm) { lm = Math.max(lm, height[lo]); water += lm - height[lo]; lo++; }
    else { rm = Math.max(rm, height[hi]); water += rm - height[hi]; hi--; }
  }
  return water;
}''')

# ------------------------------------------------------------------ SLIDING WINDOW
add(id="best-time-stock", title="Best Time to Buy and Sell Stock", difficulty="Easy", cat="sliding-window", tags=["Array","Sliding Window"],
 desc=["`prices[i]` is a stock's price on day `i`. Choose one day to buy and a later day to sell. Return the maximum profit, or 0 if no profit is possible."],
 constraints=["1 <= prices.length <= 10^5","0 <= prices[i] <= 10^4"], params=["prices"], fn={"py":"max_profit","js":"maxProfit"},
 examples=[[[7,1,5,3,6,4]],[[7,6,4,3,1]]], tests=[[[7,1,5,3,6,4]],[[7,6,4,3,1]],[[1]],[[2,4,1]],[[3,2,6,5,0,3]],[[1,2]],[rints(4000,0,10**4)]],
 hints=["For each day as the selling day, what's the best buying day?","Track the cheapest price seen so far."],
 editorial=["One pass: keep the minimum price so far and the best `price - minimum`. Selling today is only worth comparing against the cheapest earlier day."],
 complexity="O(n) time, O(1) space.",
 py='''def max_profit(prices):
    lowest, best = float("inf"), 0
    for p in prices:
        lowest = min(lowest, p)
        best = max(best, p - lowest)
    return best''',
 js='''function maxProfit(prices) {
  let lowest = Infinity, best = 0;
  for (const p of prices) {
    lowest = Math.min(lowest, p);
    best = Math.max(best, p - lowest);
  }
  return best;
}''')

add(id="longest-substring", title="Longest Substring Without Repeating Characters", difficulty="Medium", cat="sliding-window", tags=["String","Sliding Window","Hash Table"],
 desc=["Return the length of the longest substring of `s` that contains no repeated characters."],
 constraints=["0 <= s.length <= 5 × 10^4","letters, digits, symbols and spaces"], params=["s"], fn={"py":"length_of_longest_substring","js":"lengthOfLongestSubstring"},
 examples=[["abcabcbb"],["bbbbb"],["pwwkew"]], tests=[["abcabcbb"],["bbbbb"],["pwwkew"],[""],[" "],["dvdf"],["abba"],["tmmzuxt"],["abcdefghijklmnopqrstuvwxyz"*40]],
 hints=["Grow a window to the right; when a character repeats, the left edge must jump past its previous occurrence.","Store each character's last index in a dict."],
 editorial=["Keep `left` and a map `last[ch]`. When `s[right]` was seen at an index ≥ `left`, move `left` to that index + 1. The window `s[left..right]` is always repeat-free; track its maximum length."],
 complexity="O(n) time, O(min(n, alphabet)) space.",
 py='''def length_of_longest_substring(s):
    last = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best''',
 js='''function lengthOfLongestSubstring(s) {
  const last = new Map();
  let left = 0, best = 0;
  for (let r = 0; r < s.length; r++) {
    if (last.has(s[r]) && last.get(s[r]) >= left) left = last.get(s[r]) + 1;
    last.set(s[r], r);
    best = Math.max(best, r - left + 1);
  }
  return best;
}''')

add(id="character-replacement", title="Longest Repeating Character Replacement", difficulty="Medium", cat="sliding-window", tags=["String","Sliding Window"],
 desc=["You may change up to `k` characters of the uppercase string `s` to any other uppercase letter. Return the length of the longest substring that can be made of one repeated letter."],
 constraints=["1 <= s.length <= 10^5","0 <= k <= s.length"], params=["s","k"], fn={"py":"character_replacement","js":"characterReplacement"},
 examples=[["ABAB",2],["AABABBA",1]], tests=[["ABAB",2],["AABABBA",1],["A",0],["AAAA",0],["ABCDE",1],["ABBB",2],["BAAAB",2]],
 hints=["A window is fixable if (window length − count of its most common letter) ≤ k.","You never need to shrink the best count you've seen; the window just stops growing."],
 editorial=["Slide a window, counting letters and tracking the highest single-letter count `top`. If `size - top > k`, move `left` forward by one. The window never shrinks below the best size found, which is exactly the answer."],
 complexity="O(n) time, O(26) space.",
 py='''def character_replacement(s, k):
    count = {}
    left = top = best = 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        top = max(top, count[ch])
        if right - left + 1 - top > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best''',
 js='''function characterReplacement(s, k) {
  const count = {};
  let left = 0, top = 0, best = 0;
  for (let r = 0; r < s.length; r++) {
    count[s[r]] = (count[s[r]] || 0) + 1;
    top = Math.max(top, count[s[r]]);
    if (r - left + 1 - top > k) { count[s[left]]--; left++; }
    best = Math.max(best, r - left + 1);
  }
  return best;
}''')

add(id="min-window-substring", title="Minimum Window Substring", difficulty="Hard", cat="sliding-window", tags=["String","Sliding Window","Hash Table"],
 desc=["Return the shortest substring of `s` that contains every character of `t` (including duplicates). If there is none, return the empty string. The answer is unique when it exists."],
 constraints=["1 <= s.length, t.length <= 10^5","English letters"], params=["s","t"], fn={"py":"min_window","js":"minWindow"},
 examples=[["ADOBECODEBANC","ABC"],["a","a"],["a","aa"]], tests=[["ADOBECODEBANC","ABC"],["a","a"],["a","aa"],["ab","b"],["aaflslflsldkalskaaa","aaa"],["cabwefgewcwaefgcf","cae"],["bba","ab"]],
 hints=["Expand right until the window covers t, then shrink from the left while it still covers t.","Track how many required characters are currently satisfied, so 'covers t' is an O(1) check."],
 editorial=["Count what `t` needs. Extend `right`; when a character's count in the window reaches its requirement, increment `have`. While `have` equals the number of distinct needed characters, record the window and shrink from the left. Each index enters and leaves once."],
 complexity="O(|s| + |t|) time, O(alphabet) space.",
 py='''def min_window(s, t):
    need = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1
    window = {}
    have, required = 0, len(need)
    best = (float("inf"), 0, 0)
    left = 0
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            have += 1
        while have == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right + 1)
            c = s[left]
            window[c] -= 1
            if c in need and window[c] < need[c]:
                have -= 1
            left += 1
    return s[best[1]:best[2]] if best[0] != float("inf") else ""''',
 js='''function minWindow(s, t) {
  const need = new Map();
  for (const c of t) need.set(c, (need.get(c) || 0) + 1);
  const win = new Map();
  let have = 0, left = 0, bestLen = Infinity, bestL = 0;
  for (let r = 0; r < s.length; r++) {
    const c = s[r];
    win.set(c, (win.get(c) || 0) + 1);
    if (need.has(c) && win.get(c) === need.get(c)) have++;
    while (have === need.size) {
      if (r - left + 1 < bestLen) { bestLen = r - left + 1; bestL = left; }
      const d = s[left];
      win.set(d, win.get(d) - 1);
      if (need.has(d) && win.get(d) < need.get(d)) have--;
      left++;
    }
  }
  return bestLen === Infinity ? "" : s.slice(bestL, bestL + bestLen);
}''')

add(id="sliding-window-max", title="Sliding Window Maximum", difficulty="Hard", cat="sliding-window", tags=["Array","Deque","Monotonic Queue"],
 desc=["A window of size `k` slides over `nums` from left to right, one step at a time. Return a list of the maximum value in each window position."],
 constraints=["1 <= nums.length <= 10^5","1 <= k <= nums.length"], params=["nums","k"], fn={"py":"max_sliding_window","js":"maxSlidingWindow"},
 examples=[[[1,3,-1,-3,5,3,6,7],3],[[1],1]], tests=[[[1,3,-1,-3,5,3,6,7],3],[[1],1],[[9,8,7,6],2],[[1,2,3,4],4],[[4,-2],2],[[7,2,4],2],[rints(3000,-1000,1000),50]],
 hints=["Keep a deque of indices whose values are decreasing.","Pop from the back anything smaller than the new value; pop from the front any index that has left the window."],
 editorial=["Maintain a deque of indices with strictly decreasing values. The front is always the current window's maximum. Each index is pushed and popped once, so the whole scan is O(n), compared with O(n·k) for recomputing every window."],
 complexity="O(n) time, O(k) space.",
 py='''from collections import deque

def max_sliding_window(nums, k):
    dq = deque()
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out''',
 js='''function maxSlidingWindow(nums, k) {
  const dq = [], out = [];
  let head = 0;
  for (let i = 0; i < nums.length; i++) {
    while (dq.length > head && nums[dq[dq.length - 1]] <= nums[i]) dq.pop();
    dq.push(i);
    if (dq[head] <= i - k) head++;
    if (i >= k - 1) out.push(nums[dq[head]]);
  }
  return out;
}''')

# ------------------------------------------------------------------ STACK
add(id="valid-parentheses", title="Valid Parentheses", difficulty="Easy", cat="stack", tags=["String","Stack"],
 desc=["`s` contains only the characters `()[]{}`. Return `true` if every bracket is closed by the same type, in the correct order."],
 constraints=["1 <= s.length <= 10^4"], params=["s"], fn={"py":"is_valid","js":"isValid"},
 examples=[["()[]{}"],["(]"],["([{}])"]], tests=[["()[]{}"],["(]"],["([{}])"],["("],[")"],["([)]"],["{[]}"],["(((((())))))"],["]["]],
 hints=["The most recent unclosed bracket must be closed first. Which data structure gives you 'most recent'?","At the end, the stack must be empty."],
 editorial=["Push opening brackets. On a closing bracket, the stack's top must be its partner; pop it, otherwise fail. Leftover openers mean failure."],
 complexity="O(n) time, O(n) space.",
 py='''def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack''',
 js='''function isValid(s) {
  const pairs = { ")": "(", "]": "[", "}": "{" };
  const stack = [];
  for (const ch of s) {
    if (ch in pairs) {
      if (stack.pop() !== pairs[ch]) return false;
    } else stack.push(ch);
  }
  return stack.length === 0;
}''')

add(id="eval-rpn", title="Evaluate Reverse Polish Notation", difficulty="Medium", cat="stack", tags=["Array","Stack","Math"],
 desc=["Evaluate an arithmetic expression written in Reverse Polish Notation, given as a list of tokens. Operators are `+`, `-`, `*` and `/`.","Division between integers truncates toward zero (so `-7 / 2` is `-3`). The expression is always valid."],
 constraints=["1 <= tokens.length <= 10^4","Intermediate results fit in 32-bit integers"], params=["tokens"], fn={"py":"eval_rpn","js":"evalRPN"},
 examples=[[["2","1","+","3","*"]],[["4","13","5","/","+"]]], tests=[[["2","1","+","3","*"]],[["4","13","5","/","+"]],[["10","6","9","3","+","-11","*","/","*","17","+","5","+"]],[["7"]],[["-7","2","/"]],[["3","4","-"]]],
 hints=["Numbers go on a stack. An operator pops two, computes, pushes the result.","Careful with the order: the first popped value is the right operand. In Python, `int(a / b)` truncates toward zero; `//` floors."],
 editorial=["Scan tokens; push numbers; for an operator pop `b` then `a` and push `a op b`. Division needs truncation toward zero, which differs from floor division for negatives."],
 complexity="O(n) time, O(n) space.",
 py='''def eval_rpn(tokens):
    stack = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(t))
    return stack[0]''',
 js='''function evalRPN(tokens) {
  const st = [];
  for (const t of tokens) {
    if ("+-*/".includes(t) && t.length === 1) {
      const b = st.pop(), a = st.pop();
      st.push(t === "+" ? a + b : t === "-" ? a - b : t === "*" ? a * b : Math.trunc(a / b));
    } else st.push(Number(t));
  }
  return st[0];
}''')

add(id="daily-temperatures", title="Daily Temperatures", difficulty="Medium", cat="stack", tags=["Array","Monotonic Stack"],
 desc=["Given daily `temperatures`, return a list where `answer[i]` is how many days you must wait after day `i` for a warmer temperature, or 0 if it never gets warmer."],
 constraints=["1 <= temperatures.length <= 10^5","30 <= temperatures[i] <= 100"], params=["temperatures"], fn={"py":"daily_temperatures","js":"dailyTemperatures"},
 examples=[[[73,74,75,71,69,72,76,73]],[[30,40,50,60]]], tests=[[[73,74,75,71,69,72,76,73]],[[30,40,50,60]],[[30,60,90]],[[90,80,70]],[[50]],[[55,38,53,81,61,93,97,32,43,78]],[rints(3000,30,100)]],
 hints=["Keep a stack of days still waiting for a warmer day.","When today is warmer than the day on top of the stack, you've found that day's answer."],
 editorial=["Monotonic stack of indices with decreasing temperatures. For each new day, pop every colder day from the top and set its wait to `today - that_day`. Each index is pushed and popped once."],
 complexity="O(n) time, O(n) space.",
 py='''def daily_temperatures(temperatures):
    ans = [0] * len(temperatures)
    stack = []
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans''',
 js='''function dailyTemperatures(t) {
  const ans = new Array(t.length).fill(0), st = [];
  for (let i = 0; i < t.length; i++) {
    while (st.length && t[st[st.length - 1]] < t[i]) {
      const j = st.pop();
      ans[j] = i - j;
    }
    st.push(i);
  }
  return ans;
}''')

add(id="min-stack", title="Min Stack", difficulty="Medium", cat="design", tags=["Stack","Design"],
 kind="design", cls={"py":"MinStack","js":"MinStack"}, jsmap={"get_min":"getMin"},
 desc=["Design a stack that supports `push(val)`, `pop()`, `top()` and `get_min()` (JavaScript: `getMin()`), each in O(1) time.","The tests call your methods in sequence. `pop`, `top` and `get_min` are only called on a non-empty stack."],
 constraints=["-2^31 <= val <= 2^31 - 1","At most 3 × 10^4 calls"], params=[],
 examples=[], design_examples=[[["MinStack","push","push","push","get_min","pop","top","get_min"],[[],[-2],[0],[-3],[],[],[],[]]]],
 tests_design=[
   [["MinStack","push","push","push","get_min","pop","top","get_min"],[[],[-2],[0],[-3],[],[],[],[]]],
   [["MinStack","push","get_min","push","get_min","push","get_min","pop","get_min"],[[],[5],[],[3],[],[7],[],[],[]]],
   [["MinStack","push","push","get_min","pop","get_min"],[[],[1],[1],[],[],[]]],
   [["MinStack","push","push","push","get_min","pop","get_min","pop","get_min"],[[],[2],[0],[3],[],[],[],[],[]]]],
 hints=["Store, alongside each value, the minimum of the stack at the moment it was pushed.","Or keep a second stack of minimums."],
 editorial=["Push pairs `(val, min_so_far)`, where `min_so_far = min(val, previous min)`. The top pair always knows the current minimum, so every operation is O(1)."],
 complexity="O(1) per operation, O(n) space.",
 py='''class MinStack:
    def __init__(self):
        self.items = []

    def push(self, val):
        low = min(val, self.items[-1][1]) if self.items else val
        self.items.append((val, low))

    def pop(self):
        self.items.pop()

    def top(self):
        return self.items[-1][0]

    def get_min(self):
        return self.items[-1][1]''',
 js='''class MinStack {
  constructor() { this.items = []; }
  push(val) {
    const low = this.items.length ? Math.min(val, this.items[this.items.length - 1][1]) : val;
    this.items.push([val, low]);
  }
  pop() { this.items.pop(); }
  top() { return this.items[this.items.length - 1][0]; }
  getMin() { return this.items[this.items.length - 1][1]; }
}''')

add(id="largest-rectangle", title="Largest Rectangle in Histogram", difficulty="Hard", cat="stack", tags=["Array","Monotonic Stack"],
 desc=["`heights[i]` is the height of a histogram bar of width 1. Return the area of the largest rectangle that fits entirely inside the histogram."],
 constraints=["1 <= heights.length <= 10^5","0 <= heights[i] <= 10^4"], params=["heights"], fn={"py":"largest_rectangle_area","js":"largestRectangleArea"},
 examples=[[[2,1,5,6,2,3]],[[2,4]]], tests=[[[2,1,5,6,2,3]],[[2,4]],[[1]],[[0]],[[2,2,2,2]],[[6,2,5,4,5,1,6]],[[1,2,3,4,5]],[[5,4,3,2,1]],[rints(3000,0,1000)]],
 hints=["For each bar, the widest rectangle of its height extends until a shorter bar on each side.","Keep a stack of increasing heights; popping a bar tells you its right limit (current index) and left limit (new stack top)."],
 editorial=["Scan with a stack of indices of increasing height, plus a sentinel 0 at the end. When a shorter bar arrives, pop taller bars: each popped bar's rectangle spans from just after the new top of the stack to just before the current index."],
 complexity="O(n) time, O(n) space.",
 py='''def largest_rectangle_area(heights):
    stack = []
    best = 0
    for i, h in enumerate(heights + [0]):
        while stack and heights[stack[-1]] >= h:
            top = stack.pop()
            left = stack[-1] + 1 if stack else 0
            best = max(best, heights[top] * (i - left))
        stack.append(i)
    return best''',
 js='''function largestRectangleArea(heights) {
  const st = [];
  let best = 0;
  for (let i = 0; i <= heights.length; i++) {
    const h = i === heights.length ? 0 : heights[i];
    while (st.length && heights[st[st.length - 1]] >= h) {
      const top = st.pop();
      const left = st.length ? st[st.length - 1] + 1 : 0;
      best = Math.max(best, heights[top] * (i - left));
    }
    st.push(i);
  }
  return best;
}''')

# ------------------------------------------------------------------ BINARY SEARCH
sorted_big = sorted(R.sample(range(-100000, 100000), 5000))
add(id="binary-search", title="Binary Search", difficulty="Easy", cat="binary-search", tags=["Array","Binary Search"],
 desc=["`nums` is sorted in ascending order with distinct values. Return the index of `target`, or `-1` if it isn't there.","Your algorithm must run in O(log n)."],
 constraints=["1 <= nums.length <= 10^4","All values are distinct"], params=["nums","target"], fn={"py":"search","js":"search"},
 examples=[[[-1,0,3,5,9,12],9],[[-1,0,3,5,9,12],2]], tests=[[[-1,0,3,5,9,12],9],[[-1,0,3,5,9,12],2],[[5],5],[[5],-5],[[1,3],3],[[1,3],1],[sorted_big, sorted_big[3777]],[sorted_big, 100001]],
 hints=["Look at the middle. If it's too small, the target can only be to the right.","Use `lo <= hi` and update `lo = mid + 1` or `hi = mid - 1`."],
 editorial=["Maintain the invariant 'if target exists, it's in `nums[lo..hi]`'. Each comparison with the middle halves the range, so at most about log₂(n) + 1 steps."],
 complexity="O(log n) time, O(1) space.",
 py='''def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1''',
 js='''function search(nums, target) {
  let lo = 0, hi = nums.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (nums[mid] === target) return mid;
    if (nums[mid] < target) lo = mid + 1; else hi = mid - 1;
  }
  return -1;
}''')

add(id="search-insert", title="Search Insert Position", difficulty="Easy", cat="binary-search", tags=["Array","Binary Search"],
 desc=["`nums` is sorted with distinct values. Return the index of `target` if present; otherwise return the index where it would be inserted to keep the list sorted."],
 constraints=["1 <= nums.length <= 10^4"], params=["nums","target"], fn={"py":"search_insert","js":"searchInsert"},
 examples=[[[1,3,5,6],5],[[1,3,5,6],2],[[1,3,5,6],7]], tests=[[[1,3,5,6],5],[[1,3,5,6],2],[[1,3,5,6],7],[[1,3,5,6],0],[[1],1],[[1],2],[[2,4,6,8,10],9]],
 hints=["You're looking for the first index whose value is ≥ target.","Search over [0, len] instead of [0, len − 1]."],
 editorial=["This is 'first index with nums[i] ≥ target', the classic lower bound. Binary search with `lo, hi = 0, len(nums)` and `while lo < hi`."],
 complexity="O(log n) time, O(1) space.",
 py='''def search_insert(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo''',
 js='''function searchInsert(nums, target) {
  let lo = 0, hi = nums.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (nums[mid] < target) lo = mid + 1; else hi = mid;
  }
  return lo;
}''')

add(id="find-min-rotated", title="Find Minimum in Rotated Sorted Array", difficulty="Medium", cat="binary-search", tags=["Array","Binary Search"],
 desc=["A sorted list of distinct numbers was rotated some number of times (for example `[0,1,2,4,5,6,7]` might become `[4,5,6,7,0,1,2]`). Return its minimum element in O(log n)."],
 constraints=["1 <= nums.length <= 5000","All values are distinct"], params=["nums"], fn={"py":"find_min","js":"findMin"},
 examples=[[[3,4,5,1,2]],[[4,5,6,7,0,1,2]],[[11,13,15,17]]], tests=[[[3,4,5,1,2]],[[4,5,6,7,0,1,2]],[[11,13,15,17]],[[1]],[[2,1]],[[5,1,2,3,4]],[[2,3,4,5,1]]],
 hints=["Compare the middle with the last element.","If `nums[mid] > nums[hi]`, the drop (and the minimum) is to the right of mid."],
 editorial=["If the middle is greater than the right end, the rotation point is in `(mid, hi]`; otherwise the minimum is in `[lo, mid]`. Shrink until `lo == hi`."],
 complexity="O(log n) time, O(1) space.",
 py='''def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]''',
 js='''function findMin(nums) {
  let lo = 0, hi = nums.length - 1;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (nums[mid] > nums[hi]) lo = mid + 1; else hi = mid;
  }
  return nums[lo];
}''')

add(id="search-rotated", title="Search in Rotated Sorted Array", difficulty="Medium", cat="binary-search", tags=["Array","Binary Search"],
 desc=["`nums` is a sorted list of distinct values that has been rotated at an unknown pivot. Return the index of `target`, or `-1`, in O(log n) time."],
 constraints=["1 <= nums.length <= 5000","All values are distinct"], params=["nums","target"], fn={"py":"search_rotated","js":"searchRotated"},
 examples=[[[4,5,6,7,0,1,2],0],[[4,5,6,7,0,1,2],3],[[1],0]], tests=[[[4,5,6,7,0,1,2],0],[[4,5,6,7,0,1,2],3],[[1],0],[[1],1],[[3,1],1],[[5,1,3],5],[[6,7,1,2,3,4,5],6],[[1,3,5],3]],
 hints=["After splitting at mid, one half is always properly sorted.","Check whether the target lies inside the sorted half's range; if so go there, else go to the other half."],
 editorial=["At each step decide which half is sorted by comparing `nums[lo]` with `nums[mid]`. If the target falls within that sorted half's bounds, search it; otherwise search the other half."],
 complexity="O(log n) time, O(1) space.",
 py='''def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1''',
 js='''function searchRotated(nums, target) {
  let lo = 0, hi = nums.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (nums[mid] === target) return mid;
    if (nums[lo] <= nums[mid]) {
      if (nums[lo] <= target && target < nums[mid]) hi = mid - 1; else lo = mid + 1;
    } else {
      if (nums[mid] < target && target <= nums[hi]) lo = mid + 1; else hi = mid - 1;
    }
  }
  return -1;
}''')

add(id="koko-bananas", title="Koko Eating Bananas", difficulty="Medium", cat="binary-search", tags=["Array","Binary Search on Answer"],
 desc=["There are `piles` of bananas and `h` hours. Each hour Koko picks one pile and eats up to `k` bananas from it (if the pile has fewer, she finishes it and waits for the hour to end).","Return the minimum integer speed `k` that lets her finish everything within `h` hours."],
 constraints=["1 <= piles.length <= 10^4","piles.length <= h <= 10^9","1 <= piles[i] <= 10^9"], params=["piles","h"], fn={"py":"min_eating_speed","js":"minEatingSpeed"},
 examples=[[[3,6,7,11],8],[[30,11,23,4,20],5],[[30,11,23,4,20],6]], tests=[[[3,6,7,11],8],[[30,11,23,4,20],5],[[30,11,23,4,20],6],[[1],1],[[1000000000],2],[[312884470],312884469],[[5,5,5],15]],
 hints=["If speed k works, every speed above k also works. That monotonic yes/no is binary-searchable.","Hours needed at speed k: sum of ceil(pile / k)."],
 editorial=["Binary search k on [1, max(piles)] for the first speed whose total hours `Σ ceil(p/k)` is ≤ h. Each check is O(n), and there are O(log max) checks."],
 complexity="O(n log M) time where M = max pile, O(1) space.",
 py='''def min_eating_speed(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        k = (lo + hi) // 2
        hours = sum((p + k - 1) // k for p in piles)
        if hours <= h:
            hi = k
        else:
            lo = k + 1
    return lo''',
 js='''function minEatingSpeed(piles, h) {
  let lo = 1, hi = Math.max(...piles);
  while (lo < hi) {
    const k = Math.floor((lo + hi) / 2);
    let hours = 0;
    for (const p of piles) hours += Math.ceil(p / k);
    if (hours <= h) hi = k; else lo = k + 1;
  }
  return lo;
}''')

# ------------------------------------------------------------------ LINKED LIST
add(id="reverse-linked-list", title="Reverse Linked List", difficulty="Easy", cat="linked-list", tags=["Linked List","Recursion"],
 desc=["Given the `head` of a singly linked list, reverse it and return the new head.","Each node has `val` and `next`. Tests show lists as arrays, e.g. `[1,2,3]` means 1 → 2 → 3."],
 constraints=["0 <= number of nodes <= 5000"], params=["head"], fn={"py":"reverse_list","js":"reverseList"}, types={"args":["list"],"ret":"list"},
 examples=[[[1,2,3,4,5]],[[1,2]],[[]]], tests=[[[1,2,3,4,5]],[[1,2]],[[]],[[7]],[list(range(3000))]],
 hints=["Keep three references: previous, current and next.","Save `nxt = cur.next` before you point `cur.next` backwards."],
 editorial=["Iterate once, flipping each `next` pointer to the previous node. When `cur` becomes `None`, `prev` is the new head."],
 complexity="O(n) time, O(1) space.",
 py='''def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev''',
 js='''function reverseList(head) {
  let prev = null, cur = head;
  while (cur) {
    const nxt = cur.next;
    cur.next = prev;
    prev = cur;
    cur = nxt;
  }
  return prev;
}''')

add(id="merge-two-lists", title="Merge Two Sorted Lists", difficulty="Easy", cat="linked-list", tags=["Linked List","Two Pointers"],
 desc=["Merge two sorted linked lists `list1` and `list2` into one sorted list made by splicing together their nodes. Return its head."],
 constraints=["0 <= nodes in each list <= 50","Both lists are sorted in non-decreasing order"], params=["list1","list2"], fn={"py":"merge_two_lists","js":"mergeTwoLists"}, types={"args":["list","list"],"ret":"list"},
 examples=[[[1,2,4],[1,3,4]],[[],[]],[[],[0]]], tests=[[[1,2,4],[1,3,4]],[[],[]],[[],[0]],[[5],[1,2,3]],[[1,1,1],[1,1]],[[-3,0,9],[-5,10]]],
 hints=["Use a dummy node so you never special-case the head.","Attach whichever current node is smaller, advance that list, repeat; then attach the leftover."],
 editorial=["Walk both lists with a `tail` pointer starting at a dummy node. Link the smaller head each time. When one list runs out, link the rest of the other one."],
 complexity="O(n + m) time, O(1) space.",
 py='''def merge_two_lists(list1, list2):
    dummy = tail = ListNode()
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 or list2
    return dummy.next''',
 js='''function mergeTwoLists(a, b) {
  const dummy = new ListNode();
  let tail = dummy;
  while (a && b) {
    if (a.val <= b.val) { tail.next = a; a = a.next; }
    else { tail.next = b; b = b.next; }
    tail = tail.next;
  }
  tail.next = a || b;
  return dummy.next;
}''')

add(id="middle-of-list", title="Middle of the Linked List", difficulty="Easy", cat="linked-list", tags=["Linked List","Fast & Slow Pointers"],
 desc=["Return the middle node of the list (as the list from that node to the end). With two middle nodes, return the second one."],
 constraints=["1 <= number of nodes <= 100"], params=["head"], fn={"py":"middle_node","js":"middleNode"}, types={"args":["list"],"ret":"list"},
 examples=[[[1,2,3,4,5]],[[1,2,3,4,5,6]]], tests=[[[1,2,3,4,5]],[[1,2,3,4,5,6]],[[1]],[[1,2]],[[1,2,3]]],
 hints=["Move one pointer by one step and another by two.","When the fast pointer falls off the end, the slow one is in the middle."],
 editorial=["Fast and slow pointers: `fast` moves two nodes per step, `slow` one. When `fast` (or `fast.next`) is null, `slow` is at the (second) middle."],
 complexity="O(n) time, O(1) space.",
 py='''def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow''',
 js='''function middleNode(head) {
  let slow = head, fast = head;
  while (fast && fast.next) { slow = slow.next; fast = fast.next.next; }
  return slow;
}''')

add(id="remove-nth-from-end", title="Remove Nth Node From End of List", difficulty="Medium", cat="linked-list", tags=["Linked List","Two Pointers"],
 desc=["Remove the `n`-th node from the end of the list and return the head.","Can you do it in one pass?"],
 constraints=["1 <= size <= 30","1 <= n <= size"], params=["head","n"], fn={"py":"remove_nth_from_end","js":"removeNthFromEnd"}, types={"args":["list",None],"ret":"list"},
 examples=[[[1,2,3,4,5],2],[[1],1],[[1,2],1]], tests=[[[1,2,3,4,5],2],[[1],1],[[1,2],1],[[1,2],2],[[1,2,3],3],[[10,20,30,40],1]],
 hints=["Start a second pointer n steps ahead of the first.","A dummy node before the head handles removing the head itself."],
 editorial=["Put `fast` n nodes ahead of `slow` (both starting at a dummy). Move both until `fast.next` is null; then `slow.next` is the node to remove."],
 complexity="O(size) time, O(1) space.",
 py='''def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next''',
 js='''function removeNthFromEnd(head, n) {
  const dummy = new ListNode(0, head);
  let fast = dummy, slow = dummy;
  for (let i = 0; i < n; i++) fast = fast.next;
  while (fast.next) { fast = fast.next; slow = slow.next; }
  slow.next = slow.next.next;
  return dummy.next;
}''')

add(id="add-two-numbers", title="Add Two Numbers", difficulty="Medium", cat="linked-list", tags=["Linked List","Math"],
 desc=["Two non-negative integers are stored as linked lists with their digits in **reverse** order (so `[2,4,3]` is 342). Return their sum as a list in the same format."],
 constraints=["1 <= nodes in each list <= 100","No leading zeros except the number 0 itself"], params=["l1","l2"], fn={"py":"add_two_numbers","js":"addTwoNumbers"}, types={"args":["list","list"],"ret":"list"},
 examples=[[[2,4,3],[5,6,4]],[[0],[0]],[[9,9,9,9,9,9,9],[9,9,9,9]]], tests=[[[2,4,3],[5,6,4]],[[0],[0]],[[9,9,9,9,9,9,9],[9,9,9,9]],[[1],[9,9]],[[5],[5]],[[1,8],[0]]],
 hints=["It's grade-school addition, starting from the ones digit, which is conveniently at the head.","Keep a carry; continue while either list or the carry remains."],
 editorial=["Walk both lists together, adding digits plus carry; append `total % 10` and carry `total // 10`. Don't forget a final carry of 1."],
 complexity="O(max(n, m)) time, O(1) extra space besides the output.",
 py='''def add_two_numbers(l1, l2):
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:
        total = carry + (l1.val if l1 else 0) + (l2.val if l2 else 0)
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next''',
 js='''function addTwoNumbers(l1, l2) {
  const dummy = new ListNode();
  let tail = dummy, carry = 0;
  while (l1 || l2 || carry) {
    const total = carry + (l1 ? l1.val : 0) + (l2 ? l2.val : 0);
    carry = Math.floor(total / 10);
    tail.next = new ListNode(total % 10);
    tail = tail.next;
    l1 = l1 ? l1.next : null;
    l2 = l2 ? l2.next : null;
  }
  return dummy.next;
}''')

add(id="palindrome-list", title="Palindrome Linked List", difficulty="Easy", cat="linked-list", tags=["Linked List","Two Pointers"],
 desc=["Return `true` if the values of the linked list read the same forwards and backwards."],
 constraints=["1 <= number of nodes <= 10^5","0 <= Node.val <= 9"], params=["head"], fn={"py":"is_palindrome_list","js":"isPalindromeList"}, types={"args":["list"]},
 examples=[[[1,2,2,1]],[[1,2]]], tests=[[[1,2,2,1]],[[1,2]],[[1]],[[1,2,1]],[[1,1,2,1]],[[9,9,9,9]]],
 hints=["Easiest: copy the values into an array and use two pointers.","O(1) space: find the middle, reverse the second half, compare."],
 editorial=["The simple version copies values into a list and checks it against its reverse (O(n) space). The space-optimal version uses fast/slow pointers to find the middle, reverses the second half in place and compares the halves."],
 complexity="O(n) time; O(1) space with the in-place reversal.",
 py='''def is_palindrome_list(head):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    return vals == vals[::-1]''',
 js='''function isPalindromeList(head) {
  let slow = head, fast = head, prev = null;
  while (fast && fast.next) { fast = fast.next.next; const nxt = slow.next; slow.next = prev; prev = slow; slow = nxt; }
  if (fast) slow = slow.next;
  while (prev && slow) { if (prev.val !== slow.val) return false; prev = prev.next; slow = slow.next; }
  return true;
}''')

# ------------------------------------------------------------------ TREES
add(id="max-depth-tree", title="Maximum Depth of Binary Tree", difficulty="Easy", cat="trees", tags=["Tree","DFS","BFS"],
 desc=["Return the maximum depth of a binary tree: the number of nodes on the longest path from the root down to a leaf.","Trees are shown in level order with `null` for missing children, e.g. `[3,9,20,null,null,15,7]`."],
 constraints=["0 <= number of nodes <= 10^4"], params=["root"], fn={"py":"max_depth","js":"maxDepth"}, types={"args":["tree"]},
 examples=[[[3,9,20,None,None,15,7]],[[1,None,2]]], tests=[[[3,9,20,None,None,15,7]],[[1,None,2]],[[]],[[0]],[[1,2,3,4,None,None,5,6]],[[1,2,None,3,None,4,None,5]]],
 hints=["The depth of a tree is 1 + the larger depth of its two subtrees.","An empty tree has depth 0."],
 editorial=["Recursive DFS: `max_depth(None) = 0`, otherwise `1 + max(max_depth(left), max_depth(right))`. Equivalent BFS: count levels."],
 complexity="O(n) time, O(h) space for the recursion (h = height).",
 py='''def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))''',
 js='''function maxDepth(root) {
  if (!root) return 0;
  return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}''')

add(id="invert-tree", title="Invert Binary Tree", difficulty="Easy", cat="trees", tags=["Tree","DFS"],
 desc=["Mirror a binary tree: swap every node's left and right children. Return the root."],
 constraints=["0 <= number of nodes <= 100"], params=["root"], fn={"py":"invert_tree","js":"invertTree"}, types={"args":["tree"],"ret":"tree"},
 examples=[[[4,2,7,1,3,6,9]],[[2,1,3]],[[]]], tests=[[[4,2,7,1,3,6,9]],[[2,1,3]],[[]],[[1]],[[1,2]],[[1,2,3,4,5,None,6]]],
 hints=["Swap the children of the root, then invert each subtree.","Base case: an empty tree is its own mirror."],
 editorial=["Recursively invert both subtrees and swap them. Every node is visited once."],
 complexity="O(n) time, O(h) space.",
 py='''def invert_tree(root):
    if root:
        root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root''',
 js='''function invertTree(root) {
  if (root) [root.left, root.right] = [invertTree(root.right), invertTree(root.left)];
  return root;
}''')

add(id="same-tree", title="Same Tree", difficulty="Easy", cat="trees", tags=["Tree","DFS"],
 desc=["Return `true` if the binary trees `p` and `q` have the same shape and the same values at every node."],
 constraints=["0 <= nodes in each tree <= 100"], params=["p","q"], fn={"py":"is_same_tree","js":"isSameTree"}, types={"args":["tree","tree"]},
 examples=[[[1,2,3],[1,2,3]],[[1,2],[1,None,2]]], tests=[[[1,2,3],[1,2,3]],[[1,2],[1,None,2]],[[1,2,1],[1,1,2]],[[],[]],[[1],[]],[[5,4,6,None,None,7],[5,4,6,None,None,7]]],
 hints=["Two empty trees are the same; one empty and one not are different.","Otherwise compare the roots, then recurse on left and right."],
 editorial=["Recursive comparison: both null → true; one null → false; values differ → false; else both subtrees must match."],
 complexity="O(n) time, O(h) space.",
 py='''def is_same_tree(p, q):
    if p is None or q is None:
        return p is q
    return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)''',
 js='''function isSameTree(p, q) {
  if (!p || !q) return p === q;
  return p.val === q.val && isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
}''')

add(id="level-order", title="Binary Tree Level Order Traversal", difficulty="Medium", cat="trees", tags=["Tree","BFS","Queue"],
 desc=["Return the values of the tree level by level, from left to right: a list of lists, one per level."],
 constraints=["0 <= number of nodes <= 2000"], params=["root"], fn={"py":"level_order","js":"levelOrder"}, types={"args":["tree"]},
 examples=[[[3,9,20,None,None,15,7]],[[1]],[[]]], tests=[[[3,9,20,None,None,15,7]],[[1]],[[]],[[1,2,3,4,5,6,7]],[[1,2,None,3,None,4]]],
 hints=["Breadth-first search with a queue.","Process the queue in rounds: the queue's length at the start of a round is the size of that level."],
 editorial=["BFS from the root. Each round, pop exactly as many nodes as the queue held when the round began, collecting their values and pushing their children."],
 complexity="O(n) time, O(n) space.",
 py='''from collections import deque

def level_order(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        out.append(level)
    return out''',
 js='''function levelOrder(root) {
  if (!root) return [];
  const out = [];
  let q = [root];
  while (q.length) {
    out.push(q.map(n => n.val));
    q = q.flatMap(n => [n.left, n.right].filter(Boolean));
  }
  return out;
}''')

add(id="validate-bst", title="Validate Binary Search Tree", difficulty="Medium", cat="trees", tags=["Tree","DFS","BST"],
 desc=["Return `true` if the tree is a valid binary search tree: every node's left subtree holds only smaller values, its right subtree only larger values, and both subtrees are BSTs too."],
 constraints=["1 <= number of nodes <= 10^4","-2^31 <= Node.val <= 2^31 - 1"], params=["root"], fn={"py":"is_valid_bst","js":"isValidBST"}, types={"args":["tree"]},
 examples=[[[2,1,3]],[[5,1,4,None,None,3,6]]], tests=[[[2,1,3]],[[5,1,4,None,None,3,6]],[[1]],[[2,2,2]],[[5,4,6,None,None,3,7]],[[10,5,15,None,None,6,20]],[[3,1,5,0,2,4,6]]],
 hints=["Checking only a node against its direct children isn't enough. Look at test `[5,4,6,null,null,3,7]`.","Pass down the allowed (low, high) range for each subtree."],
 editorial=["DFS with bounds: the root may be anything; going left tightens the upper bound to the parent's value, going right tightens the lower bound. Any value outside its bounds breaks the BST property."],
 complexity="O(n) time, O(h) space.",
 py='''def is_valid_bst(root):
    def ok(node, lo, hi):
        if node is None:
            return True
        if not (lo < node.val < hi):
            return False
        return ok(node.left, lo, node.val) and ok(node.right, node.val, hi)
    return ok(root, float("-inf"), float("inf"))''',
 js='''function isValidBST(root) {
  const ok = (n, lo, hi) => !n || (lo < n.val && n.val < hi && ok(n.left, lo, n.val) && ok(n.right, n.val, hi));
  return ok(root, -Infinity, Infinity);
}''')

add(id="kth-smallest-bst", title="Kth Smallest Element in a BST", difficulty="Medium", cat="trees", tags=["Tree","BST","In-order"],
 desc=["Return the `k`-th smallest value (1-indexed) in a binary search tree."],
 constraints=["1 <= k <= number of nodes <= 10^4"], params=["root","k"], fn={"py":"kth_smallest","js":"kthSmallest"}, types={"args":["tree",None]},
 examples=[[[3,1,4,None,2],1],[[5,3,6,2,4,None,None,1],3]], tests=[[[3,1,4,None,2],1],[[5,3,6,2,4,None,None,1],3],[[1],1],[[2,1,3],3],[[5,3,6,2,4,None,None,1],6]],
 hints=["An in-order traversal of a BST visits values in sorted order.","Stop as soon as you've visited k nodes."],
 editorial=["Iterative in-order traversal with an explicit stack: go left as far as possible, pop, count; when the count hits k, return that value."],
 complexity="O(h + k) time, O(h) space.",
 py='''def kth_smallest(root, k):
    stack, node = [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right''',
 js='''function kthSmallest(root, k) {
  const st = [];
  let n = root;
  while (st.length || n) {
    while (n) { st.push(n); n = n.left; }
    n = st.pop();
    if (--k === 0) return n.val;
    n = n.right;
  }
}''')

add(id="diameter-tree", title="Diameter of Binary Tree", difficulty="Easy", cat="trees", tags=["Tree","DFS"],
 desc=["The diameter of a binary tree is the number of **edges** on the longest path between any two nodes. The path may or may not pass through the root. Return the diameter."],
 constraints=["1 <= number of nodes <= 10^4"], params=["root"], fn={"py":"diameter","js":"diameter"}, types={"args":["tree"]},
 examples=[[[1,2,3,4,5]],[[1,2]]], tests=[[[1,2,3,4,5]],[[1,2]],[[1]],[[1,2,None,3,4,5,None,None,6]],[[4,-7,-3,None,None,-9,-3,9,-7,-4,None,6,None,-6,-6]]],
 hints=["For each node, the longest path through it = height(left) + height(right).","Compute heights bottom-up and update a global best on the way."],
 editorial=["A single DFS returns each subtree's height while tracking `best = max(best, left_height + right_height)`. This avoids recomputing heights, which would make it O(n²)."],
 complexity="O(n) time, O(h) space.",
 py='''def diameter(root):
    best = 0
    def height(node):
        nonlocal best
        if node is None:
            return 0
        l, r = height(node.left), height(node.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    height(root)
    return best''',
 js='''function diameter(root) {
  let best = 0;
  const h = n => { if (!n) return 0; const l = h(n.left), r = h(n.right); best = Math.max(best, l + r); return 1 + Math.max(l, r); };
  h(root);
  return best;
}''')

# ------------------------------------------------------------------ HEAP
add(id="kth-largest", title="Kth Largest Element in an Array", difficulty="Medium", cat="heap", tags=["Array","Heap","Quickselect"],
 desc=["Return the `k`-th largest element of `nums` (in sorted order, not the k-th distinct)."],
 constraints=["1 <= k <= nums.length <= 10^5"], params=["nums","k"], fn={"py":"find_kth_largest","js":"findKthLargest"},
 examples=[[[3,2,1,5,6,4],2],[[3,2,3,1,2,4,5,5,6],4]], tests=[[[3,2,1,5,6,4],2],[[3,2,3,1,2,4,5,5,6],4],[[1],1],[[2,1],2],[[7,7,7],2],[[-1,-1,-2],3],[rints(4000,-10**4,10**4),77]],
 hints=["Sorting works in O(n log n). Can you do O(n log k)?","Keep a min-heap of the k largest seen; its root is the answer."],
 editorial=["Push each number onto a min-heap and pop whenever it exceeds size k. The heap always holds the k largest so far, and its smallest element is the k-th largest. Quickselect gives O(n) average."],
 complexity="O(n log k) time, O(k) space.",
 py='''import heapq

def find_kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]''',
 js='''function findKthLargest(nums, k) {
  return [...nums].sort((a, b) => b - a)[k - 1];
}''')

add(id="last-stone-weight", title="Last Stone Weight", difficulty="Easy", cat="heap", tags=["Array","Heap","Simulation"],
 desc=["Each turn, smash the two heaviest stones `x <= y` together. If equal, both are destroyed; otherwise the lighter is destroyed and the heavier becomes `y - x`.","Return the weight of the last remaining stone, or 0 if none remain."],
 constraints=["1 <= stones.length <= 30","1 <= stones[i] <= 1000"], params=["stones"], fn={"py":"last_stone_weight","js":"lastStoneWeight"},
 examples=[[[2,7,4,1,8,1]],[[1]]], tests=[[[2,7,4,1,8,1]],[[1]],[[2,2]],[[10,4,2,10]],[[3,7,2]],[[9,3,2,10]]],
 hints=["You repeatedly need the two largest: a max-heap.","In Python, push negated weights into `heapq`."],
 editorial=["Simulate with a max-heap: pop two, push the difference if non-zero, repeat until at most one stone remains."],
 complexity="O(n log n) time, O(n) space.",
 py='''import heapq

def last_stone_weight(stones):
    heap = [-s for s in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        y = -heapq.heappop(heap)
        x = -heapq.heappop(heap)
        if y != x:
            heapq.heappush(heap, -(y - x))
    return -heap[0] if heap else 0''',
 js='''function lastStoneWeight(stones) {
  const s = [...stones];
  while (s.length > 1) {
    s.sort((a, b) => a - b);
    const y = s.pop(), x = s.pop();
    if (y !== x) s.push(y - x);
  }
  return s.length ? s[0] : 0;
}''')

add(id="k-closest-points", title="K Closest Points to Origin", difficulty="Medium", cat="heap", tags=["Array","Heap","Geometry"],
 desc=["Return the `k` points from `points` closest to the origin `(0, 0)` by Euclidean distance, in any order. The answer is guaranteed to be unique."],
 constraints=["1 <= k <= points.length <= 10^4"], params=["points","k"], fn={"py":"k_closest","js":"kClosest"}, cmp="unordered",
 examples=[[[[1,3],[-2,2]],1],[[[3,3],[5,-1],[-2,4]],2]], tests=[[[[1,3],[-2,2]],1],[[[3,3],[5,-1],[-2,4]],2],[[[0,1],[1,0]],2],[[[1,1],[2,2],[3,3],[-1,-1]],1],[[[6,10],[-3,3],[-2,5],[0,2]],3]],
 hints=["Compare squared distances; the square root doesn't change the order.","Sort by `x*x + y*y`, or keep a max-heap of size k."],
 editorial=["Sort by squared distance and take the first k (O(n log n)), or keep a max-heap of size k (O(n log k))."],
 complexity="O(n log k) time with a heap, O(k) space.",
 py='''import heapq

def k_closest(points, k):
    return heapq.nsmallest(k, points, key=lambda p: p[0] * p[0] + p[1] * p[1])''',
 js='''function kClosest(points, k) {
  return [...points].sort((a, b) => (a[0] ** 2 + a[1] ** 2) - (b[0] ** 2 + b[1] ** 2)).slice(0, k);
}''')

# ------------------------------------------------------------------ BACKTRACKING
add(id="subsets", title="Subsets", difficulty="Medium", cat="backtracking", tags=["Array","Backtracking","Bit Manipulation"],
 desc=["Given distinct integers `nums`, return every possible subset (the power set). The order of subsets and of numbers within a subset doesn't matter."],
 constraints=["1 <= nums.length <= 10","All values are distinct"], params=["nums"], fn={"py":"subsets","js":"subsets"}, cmp="deep",
 examples=[[[1,2,3]],[[0]]], tests=[[[1,2,3]],[[0]],[[5,-1]],[[1,2,3,4]]],
 hints=["Each element is either in or out: 2ⁿ subsets.","Backtrack: at index i, recurse once without nums[i] and once with it."],
 editorial=["Recursive include/exclude over the indices, or iteratively: start with `[[]]` and for each number add a copy of every existing subset with that number appended."],
 complexity="O(n · 2ⁿ) time and space.",
 py='''def subsets(nums):
    out = [[]]
    for x in nums:
        out += [s + [x] for s in out]
    return out''',
 js='''function subsets(nums) {
  const out = [], path = [];
  const go = i => {
    if (i === nums.length) { out.push([...path]); return; }
    go(i + 1);
    path.push(nums[i]); go(i + 1); path.pop();
  };
  go(0);
  return out;
}''')

add(id="permutations", title="Permutations", difficulty="Medium", cat="backtracking", tags=["Array","Backtracking"],
 desc=["Return all permutations of the distinct integers in `nums`, in any order."],
 constraints=["1 <= nums.length <= 6","All values are distinct"], params=["nums"], fn={"py":"permute","js":"permute"}, cmp="unordered",
 examples=[[[1,2,3]],[[0,1]]], tests=[[[1,2,3]],[[0,1]],[[1]],[[4,5,6,7]]],
 hints=["Choose an unused number for the next position, recurse, then un-choose it.","Track used numbers with a set or boolean array."],
 editorial=["Classic backtracking: the path grows one number at a time from the unused ones; when its length equals n, record a copy. There are n! permutations."],
 complexity="O(n · n!) time and space.",
 py='''def permute(nums):
    out, path, used = [], [], set()
    def go():
        if len(path) == len(nums):
            out.append(path[:])
            return
        for x in nums:
            if x not in used:
                used.add(x)
                path.append(x)
                go()
                path.pop()
                used.remove(x)
    go()
    return out''',
 js='''function permute(nums) {
  if (nums.length <= 1) return [nums.slice()];
  const out = [];
  nums.forEach((x, i) => {
    for (const p of permute([...nums.slice(0, i), ...nums.slice(i + 1)])) out.push([x, ...p]);
  });
  return out;
}''')

add(id="combination-sum", title="Combination Sum", difficulty="Medium", cat="backtracking", tags=["Array","Backtracking"],
 desc=["Given distinct positive `candidates` and a `target`, return all unique combinations whose numbers sum to `target`. Each candidate may be used any number of times.","Two combinations are the same if they use the same numbers the same number of times, regardless of order."],
 constraints=["1 <= candidates.length <= 30","2 <= candidates[i] <= 40","1 <= target <= 40"], params=["candidates","target"], fn={"py":"combination_sum","js":"combinationSum"}, cmp="deep",
 examples=[[[2,3,6,7],7],[[2,3,5],8],[[2],1]], tests=[[[2,3,6,7],7],[[2,3,5],8],[[2],1],[[1],2],[[7,3,2],18],[[8,7,4,3],11]],
 hints=["To avoid duplicates like [2,3,2] vs [2,2,3], only allow choosing candidates at index ≥ the last one you chose.","Stop exploring when the remaining target goes negative."],
 editorial=["Backtrack with a start index: at each step try `candidates[i]` for `i >= start`, staying at `i` (reuse allowed). Sorting first lets you break early once a candidate exceeds the remainder."],
 complexity="Exponential in target / min(candidates) in the worst case.",
 py='''def combination_sum(candidates, target):
    candidates = sorted(candidates)
    out, path = [], []
    def go(start, remain):
        if remain == 0:
            out.append(path[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remain:
                break
            path.append(c)
            go(i, remain - c)
            path.pop()
    go(0, target)
    return out''',
 js='''function combinationSum(candidates, target) {
  const c = [...candidates].sort((a, b) => a - b), out = [], path = [];
  const go = (start, rem) => {
    if (rem === 0) { out.push([...path]); return; }
    for (let i = start; i < c.length && c[i] <= rem; i++) { path.push(c[i]); go(i, rem - c[i]); path.pop(); }
  };
  go(0, target);
  return out;
}''')

add(id="generate-parentheses", title="Generate Parentheses", difficulty="Medium", cat="backtracking", tags=["String","Backtracking"],
 desc=["Return every string of `n` pairs of well-formed parentheses, in any order."],
 constraints=["1 <= n <= 8"], params=["n"], fn={"py":"generate_parenthesis","js":"generateParenthesis"}, cmp="unordered",
 examples=[[3],[1]], tests=[[1],[2],[3],[4],[5]],
 hints=["You can add '(' while you've used fewer than n.","You can add ')' only while there are more '(' than ')' so far."],
 editorial=["Backtrack on the string being built, tracking opens and closes. The two rules guarantee every completed string is valid, so no filtering is needed. The count is the n-th Catalan number."],
 complexity="O(Cₙ · n) where Cₙ is the n-th Catalan number.",
 py='''def generate_parenthesis(n):
    out = []
    def go(s, opened, closed):
        if len(s) == 2 * n:
            out.append(s)
            return
        if opened < n:
            go(s + "(", opened + 1, closed)
        if closed < opened:
            go(s + ")", opened, closed + 1)
    go("", 0, 0)
    return out''',
 js='''function generateParenthesis(n) {
  const out = [];
  const go = (s, o, c) => {
    if (s.length === 2 * n) { out.push(s); return; }
    if (o < n) go(s + "(", o + 1, c);
    if (c < o) go(s + ")", o, c + 1);
  };
  go("", 0, 0);
  return out;
}''')

add(id="n-queens-count", title="N-Queens: Count Solutions", difficulty="Hard", cat="backtracking", tags=["Backtracking","Bit Manipulation"],
 desc=["Place `n` chess queens on an `n × n` board so that no two attack each other (no shared row, column or diagonal). Return how many distinct arrangements exist."],
 constraints=["1 <= n <= 9"], params=["n"], fn={"py":"total_n_queens","js":"totalNQueens"},
 examples=[[4],[1]], tests=[[1],[2],[3],[4],[5],[6],[8],[9]],
 hints=["Place one queen per row; for each row try every column that's safe.","A cell (r, c) is on diagonal r − c and anti-diagonal r + c. Keep sets of used columns and diagonals."],
 editorial=["Backtrack row by row with three sets: used columns, used `r - c` diagonals and used `r + c` anti-diagonals. Each check is O(1), so pruning is cheap and the search finishes instantly for n ≤ 9."],
 complexity="Roughly O(n!) in the worst case, far less with pruning.",
 py='''def total_n_queens(n):
    cols, d1, d2 = set(), set(), set()
    def go(r):
        if r == n:
            return 1
        count = 0
        for c in range(n):
            if c in cols or r - c in d1 or r + c in d2:
                continue
            cols.add(c); d1.add(r - c); d2.add(r + c)
            count += go(r + 1)
            cols.remove(c); d1.remove(r - c); d2.remove(r + c)
        return count
    return go(0)''',
 js='''function totalNQueens(n) {
  const go = (r, cols, d1, d2) => {
    if (r === n) return 1;
    let count = 0;
    for (let c = 0; c < n; c++) {
      const a = 1 << c, b = 1 << (r - c + n), d = 1 << (r + c);
      if (cols & a || d1 & b || d2 & d) continue;
      count += go(r + 1, cols | a, d1 | b, d2 | d);
    }
    return count;
  };
  return go(0, 0, 0, 0);
}''')

# ------------------------------------------------------------------ GRAPHS
add(id="number-of-islands", title="Number of Islands", difficulty="Medium", cat="graphs", tags=["Matrix","DFS","BFS"],
 desc=["`grid` is a 2D map of `\"1\"` (land) and `\"0\"` (water). An island is land connected horizontally or vertically. Return the number of islands."],
 constraints=["1 <= rows, cols <= 300"], params=["grid"], fn={"py":"num_islands","js":"numIslands"},
 examples=[[[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]]],
 tests=[[[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]],[[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]],[[["0"]]],[[["1"]]],[[["1","0","1"],["0","1","0"],["1","0","1"]]],[[["1","1","1"],["0","1","0"],["1","1","1"]]]],
 hints=["Scan every cell. When you find unvisited land, that's a new island: count it, then sink all its connected land.","Use BFS with a queue to avoid deep recursion on big islands."],
 editorial=["For each land cell, increment the count and flood-fill (BFS/DFS) to mark its whole island as visited. Every cell is processed a constant number of times."],
 complexity="O(rows × cols) time and space.",
 py='''from collections import deque

def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen = set()
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                count += 1
                seen.add((r, c))
                q = deque([(r, c)])
                while q:
                    y, x = q.popleft()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == "1" and (ny, nx) not in seen:
                            seen.add((ny, nx))
                            q.append((ny, nx))
    return count''',
 js='''function numIslands(grid) {
  const R = grid.length, C = grid[0].length, seen = grid.map(r => r.map(() => false));
  let count = 0;
  for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) {
    if (grid[r][c] !== "1" || seen[r][c]) continue;
    count++;
    const st = [[r, c]]; seen[r][c] = true;
    while (st.length) {
      const [y, x] = st.pop();
      for (const [dy, dx] of [[1,0],[-1,0],[0,1],[0,-1]]) {
        const ny = y + dy, nx = x + dx;
        if (ny >= 0 && ny < R && nx >= 0 && nx < C && grid[ny][nx] === "1" && !seen[ny][nx]) { seen[ny][nx] = true; st.push([ny, nx]); }
      }
    }
  }
  return count;
}''')

add(id="flood-fill", title="Flood Fill", difficulty="Easy", cat="graphs", tags=["Matrix","DFS","BFS"],
 desc=["Starting from pixel `(sr, sc)` in `image`, recolour it and every pixel connected to it (up/down/left/right) that has the same original colour, using `color`. Return the image."],
 constraints=["1 <= rows, cols <= 50"], params=["image","sr","sc","color"], fn={"py":"flood_fill","js":"floodFill"},
 examples=[[[[1,1,1],[1,1,0],[1,0,1]],1,1,2],[[[0,0,0],[0,0,0]],0,0,0]], tests=[[[[1,1,1],[1,1,0],[1,0,1]],1,1,2],[[[0,0,0],[0,0,0]],0,0,0],[[[0,0,0],[0,1,1]],1,1,1],[[[1]],0,0,5],[[[2,2,3],[3,2,2],[2,3,2]],0,0,9]],
 hints=["If the start pixel already has the new colour, return immediately, or you'll loop forever.","DFS from the start; only spread into pixels of the original colour."],
 editorial=["Remember the original colour; if it equals the new one, nothing changes. Otherwise DFS/BFS recolouring every reachable pixel of the original colour."],
 complexity="O(rows × cols) time and space.",
 py='''def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image
    stack = [(sr, sc)]
    while stack:
        r, c = stack.pop()
        if 0 <= r < len(image) and 0 <= c < len(image[0]) and image[r][c] == old:
            image[r][c] = color
            stack += [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    return image''',
 js='''function floodFill(image, sr, sc, color) {
  const old = image[sr][sc];
  if (old === color) return image;
  const fill = (r, c) => {
    if (r < 0 || c < 0 || r >= image.length || c >= image[0].length || image[r][c] !== old) return;
    image[r][c] = color;
    fill(r + 1, c); fill(r - 1, c); fill(r, c + 1); fill(r, c - 1);
  };
  fill(sr, sc);
  return image;
}''')

add(id="course-schedule", title="Course Schedule", difficulty="Medium", cat="graphs", tags=["Graph","Topological Sort","BFS"],
 desc=["There are `num_courses` courses labelled `0` to `num_courses - 1`. Each pair `[a, b]` in `prerequisites` means you must take `b` before `a`.","Return `true` if you can finish every course (that is, the prerequisites contain no cycle)."],
 constraints=["1 <= num_courses <= 2000","0 <= prerequisites.length <= 5000"], params=["num_courses","prerequisites"], fn={"py":"can_finish","js":"canFinish"},
 examples=[[2,[[1,0]]],[2,[[1,0],[0,1]]]], tests=[[2,[[1,0]]],[2,[[1,0],[0,1]]],[1,[]],[3,[[1,0],[2,1]]],[3,[[0,1],[1,2],[2,0]]],[5,[[1,4],[2,4],[3,1],[3,2]]],[4,[[1,0],[2,0],[3,1],[3,2],[1,3]]]],
 hints=["Courses are nodes, prerequisites are directed edges. You need to detect a cycle.","Kahn's algorithm: repeatedly take a course with no remaining prerequisites."],
 editorial=["Compute in-degrees. Queue all courses with in-degree 0; pop one, 'take' it and decrement the in-degree of courses that depend on it. If you take every course, there's no cycle."],
 complexity="O(V + E) time and space.",
 py='''from collections import deque

def can_finish(num_courses, prerequisites):
    after = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        after[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    taken = 0
    while q:
        c = q.popleft()
        taken += 1
        for nxt in after[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return taken == num_courses''',
 js='''function canFinish(n, prereq) {
  const adj = Array.from({ length: n }, () => []), state = new Array(n).fill(0);
  for (const [a, b] of prereq) adj[b].push(a);
  const dfs = u => {
    if (state[u] === 1) return false;
    if (state[u] === 2) return true;
    state[u] = 1;
    for (const v of adj[u]) if (!dfs(v)) return false;
    state[u] = 2;
    return true;
  };
  for (let i = 0; i < n; i++) if (!dfs(i)) return false;
  return true;
}''')

add(id="rotting-oranges", title="Rotting Oranges", difficulty="Medium", cat="graphs", tags=["Matrix","BFS"],
 desc=["In `grid`, 0 is empty, 1 is a fresh orange and 2 is a rotten orange. Every minute, fresh oranges next to a rotten one (up/down/left/right) become rotten.","Return the minutes until no fresh orange remains, or `-1` if that's impossible."],
 constraints=["1 <= rows, cols <= 10"], params=["grid"], fn={"py":"oranges_rotting","js":"orangesRotting"},
 examples=[[[[2,1,1],[1,1,0],[0,1,1]]],[[[2,1,1],[0,1,1],[1,0,1]]],[[[0,2]]]], tests=[[[[2,1,1],[1,1,0],[0,1,1]]],[[[2,1,1],[0,1,1],[1,0,1]]],[[[0,2]]],[[[1]]],[[[0]]],[[[2,2],[1,1],[0,0],[2,0]]],[[[2,1,1],[1,1,1],[0,1,2]]]],
 hints=["Multi-source BFS: start the queue with every rotten orange at minute 0.","Count fresh oranges; if any remain after BFS, return -1."],
 editorial=["Seed a BFS queue with all rotten oranges. Process the queue level by level; each level is one minute. Track the fresh count; when it hits zero, the number of levels processed is the answer."],
 complexity="O(rows × cols) time and space.",
 py='''from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes''',
 js='''function orangesRotting(grid) {
  const R = grid.length, C = grid[0].length;
  let q = [], fresh = 0, minutes = 0;
  for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) {
    if (grid[r][c] === 2) q.push([r, c]); else if (grid[r][c] === 1) fresh++;
  }
  while (q.length && fresh) {
    const next = [];
    for (const [r, c] of q) for (const [y, x] of [[r+1,c],[r-1,c],[r,c+1],[r,c-1]]) {
      if (y >= 0 && y < R && x >= 0 && x < C && grid[y][x] === 1) { grid[y][x] = 2; fresh--; next.push([y, x]); }
    }
    q = next; minutes++;
  }
  return fresh ? -1 : minutes;
}''')

add(id="word-ladder", title="Word Ladder", difficulty="Hard", cat="graphs", tags=["String","BFS","Hash Set"],
 desc=["Transform `begin_word` into `end_word` by changing one letter at a time; every intermediate word must be in `word_list`.","Return the number of words in the shortest such sequence (including both ends), or 0 if no sequence exists."],
 constraints=["1 <= word length <= 10","1 <= word_list.length <= 5000","all words have the same length, lowercase letters"], params=["begin_word","end_word","word_list"], fn={"py":"ladder_length","js":"ladderLength"},
 examples=[["hit","cog",["hot","dot","dog","lot","log","cog"]],["hit","cog",["hot","dot","dog","lot","log"]]], tests=[["hit","cog",["hot","dot","dog","lot","log","cog"]],["hit","cog",["hot","dot","dog","lot","log"]],["a","c",["a","b","c"]],["hot","dog",["hot","dog"]],["hot","dog",["hot","dot","dog"]],["red","tax",["ted","tex","red","tax","tad","den","rex","pee"]]],
 hints=["Words are nodes; an edge joins words that differ in one letter. Shortest path in an unweighted graph → BFS.","Generate neighbours by replacing each position with a–z and checking a set: O(L × 26) per word."],
 editorial=["BFS from `begin_word`. For each word, try every one-letter change; if the result is in the remaining word set, enqueue it and remove it from the set so it's never revisited. The BFS level at which `end_word` appears is the answer."],
 complexity="O(N × L × 26) time, O(N × L) space.",
 py='''from collections import deque

def ladder_length(begin_word, end_word, word_list):
    words = set(word_list)
    if end_word not in words:
        return 0
    q = deque([(begin_word, 1)])
    letters = "abcdefghijklmnopqrstuvwxyz"
    while q:
        word, steps = q.popleft()
        if word == end_word:
            return steps
        for i in range(len(word)):
            for ch in letters:
                cand = word[:i] + ch + word[i + 1:]
                if cand in words:
                    words.remove(cand)
                    q.append((cand, steps + 1))
    return 0''',
 js='''function ladderLength(begin, end, list) {
  const words = new Set(list);
  if (!words.has(end)) return 0;
  let q = [begin], steps = 1;
  while (q.length) {
    const next = [];
    for (const w of q) {
      if (w === end) return steps;
      for (let i = 0; i < w.length; i++) for (let c = 97; c < 123; c++) {
        const cand = w.slice(0, i) + String.fromCharCode(c) + w.slice(i + 1);
        if (words.has(cand)) { words.delete(cand); next.push(cand); }
      }
    }
    q = next; steps++;
  }
  return 0;
}''')

# ------------------------------------------------------------------ DP
add(id="climbing-stairs", title="Climbing Stairs", difficulty="Easy", cat="dp", tags=["Dynamic Programming","Math"],
 desc=["You climb a staircase of `n` steps, taking 1 or 2 steps at a time. In how many distinct ways can you reach the top?"],
 constraints=["1 <= n <= 45"], params=["n"], fn={"py":"climb_stairs","js":"climbStairs"},
 examples=[[2],[3]], tests=[[1],[2],[3],[4],[5],[10],[30],[45]],
 hints=["To stand on step n you came from step n−1 or step n−2.","ways(n) = ways(n−1) + ways(n−2). Look familiar?"],
 editorial=["It's the Fibonacci recurrence. Keep only the last two values and iterate; plain recursion without memoisation would be exponential."],
 complexity="O(n) time, O(1) space.",
 py='''def climb_stairs(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a''',
 js='''function climbStairs(n) {
  let a = 1, b = 1;
  for (let i = 0; i < n; i++) [a, b] = [b, a + b];
  return a;
}''')

add(id="house-robber", title="House Robber", difficulty="Medium", cat="dp", tags=["Array","Dynamic Programming"],
 desc=["Houses along a street hold `nums[i]` money. You can't rob two adjacent houses (the alarm links them). Return the most money you can rob."],
 constraints=["1 <= nums.length <= 100","0 <= nums[i] <= 400"], params=["nums"], fn={"py":"rob","js":"rob"},
 examples=[[[1,2,3,1]],[[2,7,9,3,1]]], tests=[[[1,2,3,1]],[[2,7,9,3,1]],[[5]],[[2,1]],[[1,3,1]],[[2,1,1,2]],[[0,0,0]],[[183,219,57,193,94,233,202,154,65,240,97,234,100,249,186,66,90,238,168,128]]],
 hints=["At house i you either skip it (keep the best up to i−1) or rob it (its money + best up to i−2).","You only need the last two best values."],
 editorial=["`best[i] = max(best[i-1], best[i-2] + nums[i])`. Two rolling variables are enough."],
 complexity="O(n) time, O(1) space.",
 py='''def rob(nums):
    prev, cur = 0, 0
    for x in nums:
        prev, cur = cur, max(cur, prev + x)
    return cur''',
 js='''function rob(nums) {
  let prev = 0, cur = 0;
  for (const x of nums) [prev, cur] = [cur, Math.max(cur, prev + x)];
  return cur;
}''')

add(id="coin-change", title="Coin Change", difficulty="Medium", cat="dp", tags=["Array","Dynamic Programming","BFS"],
 desc=["Given coin denominations `coins` (unlimited supply of each) and an `amount`, return the fewest coins that make up exactly that amount, or `-1` if it can't be done."],
 constraints=["1 <= coins.length <= 12","1 <= coins[i] <= 2^31 - 1","0 <= amount <= 10^4"], params=["coins","amount"], fn={"py":"coin_change","js":"coinChange"},
 examples=[[[1,2,5],11],[[2],3],[[1],0]], tests=[[[1,2,5],11],[[2],3],[[1],0],[[1],1],[[186,419,83,408],6249],[[2,5,10,1],27],[[3,7],5],[[1,3,4],6]],
 hints=["Greedy (always take the biggest coin) fails: try coins [1,3,4] and amount 6.","dp[a] = fewest coins for amount a = 1 + min(dp[a − c]) over coins c."],
 editorial=["Bottom-up DP over amounts 0..amount. `dp[0] = 0`, everything else starts at infinity, and each amount tries every coin. If `dp[amount]` is still infinite, return −1."],
 complexity="O(amount × coins) time, O(amount) space.",
 py='''def coin_change(coins, amount):
    INF = amount + 1
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1''',
 js='''function coinChange(coins, amount) {
  const dp = new Array(amount + 1).fill(Infinity);
  dp[0] = 0;
  for (let a = 1; a <= amount; a++) for (const c of coins) if (c <= a) dp[a] = Math.min(dp[a], dp[a - c] + 1);
  return dp[amount] === Infinity ? -1 : dp[amount];
}''')

add(id="max-subarray", title="Maximum Subarray", difficulty="Medium", cat="dp", tags=["Array","Dynamic Programming","Kadane"],
 desc=["Return the largest sum of any non-empty contiguous subarray of `nums`."],
 constraints=["1 <= nums.length <= 10^5","-10^4 <= nums[i] <= 10^4"], params=["nums"], fn={"py":"max_sub_array","js":"maxSubArray"},
 examples=[[[-2,1,-3,4,-1,2,1,-5,4]],[[1]],[[5,4,-1,7,8]]], tests=[[[-2,1,-3,4,-1,2,1,-5,4]],[[1]],[[5,4,-1,7,8]],[[-3,-1,-2]],[[0]],[[-1,0,-2]],[rints(5000,-10**4,10**4)]],
 hints=["Should the best subarray ending at i extend the one ending at i−1, or start fresh at i?","Start fresh exactly when the running sum has gone negative."],
 editorial=["Kadane's algorithm: `cur = max(x, cur + x)` is the best sum ending here; the answer is the maximum `cur` seen. Initialise with the first element so all-negative arrays work."],
 complexity="O(n) time, O(1) space.",
 py='''def max_sub_array(nums):
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best''',
 js='''function maxSubArray(nums) {
  let cur = nums[0], best = nums[0];
  for (let i = 1; i < nums.length; i++) { cur = Math.max(nums[i], cur + nums[i]); best = Math.max(best, cur); }
  return best;
}''')

add(id="longest-increasing-subsequence", title="Longest Increasing Subsequence", difficulty="Medium", cat="dp", tags=["Array","Dynamic Programming","Binary Search"],
 desc=["Return the length of the longest strictly increasing subsequence of `nums` (elements in order, not necessarily adjacent)."],
 constraints=["1 <= nums.length <= 2500"], params=["nums"], fn={"py":"length_of_lis","js":"lengthOfLIS"},
 examples=[[[10,9,2,5,3,7,101,18]],[[0,1,0,3,2,3]],[[7,7,7,7]]], tests=[[[10,9,2,5,3,7,101,18]],[[0,1,0,3,2,3]],[[7,7,7,7]],[[1]],[[1,2,3,4,5]],[[5,4,3,2,1]],[[4,10,4,3,8,9]],[rints(2500,-10**4,10**4)]],
 hints=["O(n²): dp[i] = 1 + max(dp[j]) over j < i with nums[j] < nums[i].","O(n log n): keep `tails[k]` = smallest possible tail of an increasing subsequence of length k+1, and binary search where each number goes."],
 editorial=["Patience sorting: for each number, find the first tail ≥ it (lower bound) and replace it, or append if it's larger than every tail. The number of tails is the LIS length."],
 complexity="O(n log n) time, O(n) space.",
 py='''from bisect import bisect_left

def length_of_lis(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)''',
 js='''function lengthOfLIS(nums) {
  const dp = new Array(nums.length).fill(1);
  let best = 0;
  for (let i = 0; i < nums.length; i++) {
    for (let j = 0; j < i; j++) if (nums[j] < nums[i] && dp[j] + 1 > dp[i]) dp[i] = dp[j] + 1;
    best = Math.max(best, dp[i]);
  }
  return best;
}''')

add(id="unique-paths", title="Unique Paths", difficulty="Medium", cat="dp", tags=["Dynamic Programming","Combinatorics"],
 desc=["A robot starts at the top-left of an `m × n` grid and can only move right or down. How many distinct paths reach the bottom-right corner?"],
 constraints=["1 <= m, n <= 100","The answer is at most 2 × 10^9"], params=["m","n"], fn={"py":"unique_paths","js":"uniquePaths"},
 examples=[[3,7],[3,2]], tests=[[3,7],[3,2],[1,1],[1,10],[10,10],[23,12],[7,3]],
 hints=["Paths to a cell = paths to the cell above + paths to the cell to the left.","A single row of length n updated m times is enough memory."],
 editorial=["`dp[c] += dp[c-1]` row by row, starting from all ones. (Combinatorics also works: choose which m−1 of the m+n−2 moves go down.)"],
 complexity="O(m × n) time, O(n) space.",
 py='''def unique_paths(m, n):
    row = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]''',
 js='''function uniquePaths(m, n) {
  const row = new Array(n).fill(1);
  for (let r = 1; r < m; r++) for (let c = 1; c < n; c++) row[c] += row[c - 1];
  return row[n - 1];
}''')

add(id="longest-common-subsequence", title="Longest Common Subsequence", difficulty="Medium", cat="dp", tags=["String","Dynamic Programming"],
 desc=["Return the length of the longest subsequence common to `text1` and `text2`, or 0 if there is none."],
 constraints=["1 <= text1.length, text2.length <= 1000","lowercase letters"], params=["text1","text2"], fn={"py":"longest_common_subsequence","js":"longestCommonSubsequence"},
 examples=[["abcde","ace"],["abc","abc"],["abc","def"]], tests=[["abcde","ace"],["abc","abc"],["abc","def"],["a","a"],["bsbininm","jmjkbkjkv"],["oxcpqrsvwf","shmtulqrypy"],["ezupkr","ubmrapg"]],
 hints=["dp[i][j] = LCS of the first i characters of text1 and the first j of text2.","If the last characters match: 1 + dp[i−1][j−1]; otherwise max(dp[i−1][j], dp[i][j−1])."],
 editorial=["Fill an (n+1) × (m+1) table with the recurrence above. Only the previous row is needed, so memory can drop to O(m)."],
 complexity="O(n × m) time, O(m) space.",
 py='''def longest_common_subsequence(text1, text2):
    prev = [0] * (len(text2) + 1)
    for a in text1:
        cur = [0]
        for j, b in enumerate(text2):
            cur.append(prev[j] + 1 if a == b else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]''',
 js='''function longestCommonSubsequence(a, b) {
  let prev = new Array(b.length + 1).fill(0);
  for (let i = 0; i < a.length; i++) {
    const cur = [0];
    for (let j = 0; j < b.length; j++) cur.push(a[i] === b[j] ? prev[j] + 1 : Math.max(prev[j + 1], cur[j]));
    prev = cur;
  }
  return prev[b.length];
}''')

add(id="word-break", title="Word Break", difficulty="Medium", cat="dp", tags=["String","Dynamic Programming","Hash Set"],
 desc=["Return `true` if `s` can be split into a sequence of one or more words from `word_dict`. Words may be reused."],
 constraints=["1 <= s.length <= 300","1 <= word_dict.length <= 1000"], params=["s","word_dict"], fn={"py":"word_break","js":"wordBreak"},
 examples=[["leetcode",["leet","code"]],["applepenapple",["apple","pen"]],["catsandog",["cats","dog","sand","and","cat"]]], tests=[["leetcode",["leet","code"]],["applepenapple",["apple","pen"]],["catsandog",["cats","dog","sand","and","cat"]],["a",["a"]],["ab",["a"]],["aaaaaaab",["a","aa","aaa"]],["cars",["car","ca","rs"]]],
 hints=["ok[i] = can the first i characters be segmented?","ok[i] is true if some ok[j] is true and s[j:i] is a word."],
 editorial=["DP over prefix lengths with a set for O(1) word lookups. `ok[0] = True`. For each end `i`, try every start `j` (or only starts within the longest word's length)."],
 complexity="O(n² ) time (with slicing), O(n) space.",
 py='''def word_break(s, word_dict):
    words = set(word_dict)
    ok = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(i):
            if ok[j] and s[j:i] in words:
                ok[i] = True
                break
    return ok[-1]''',
 js='''function wordBreak(s, dict) {
  const words = new Set(dict), ok = new Array(s.length + 1).fill(false);
  ok[0] = true;
  for (let i = 1; i <= s.length; i++) for (let j = 0; j < i; j++) if (ok[j] && words.has(s.slice(j, i))) { ok[i] = true; break; }
  return ok[s.length];
}''')

add(id="edit-distance", title="Edit Distance", difficulty="Hard", cat="dp", tags=["String","Dynamic Programming"],
 desc=["Return the minimum number of single-character operations (insert, delete or replace) needed to turn `word1` into `word2`."],
 constraints=["0 <= word1.length, word2.length <= 500","lowercase letters"], params=["word1","word2"], fn={"py":"min_distance","js":"minDistance"},
 examples=[["horse","ros"],["intention","execution"]], tests=[["horse","ros"],["intention","execution"],["",""],["","abc"],["abc",""],["kitten","sitting"],["same","same"],["dinitrophenylhydrazine","benzalphenylhydrazone"]],
 hints=["dp[i][j] = edits to turn the first i chars of word1 into the first j of word2.","If the last characters match, no edit is needed for them; otherwise 1 + the min of insert, delete or replace."],
 editorial=["Levenshtein DP: base rows `dp[i][0] = i` and `dp[0][j] = j`. Transition: `dp[i][j] = dp[i-1][j-1]` if the characters match, else `1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`."],
 complexity="O(n × m) time, O(m) space with a rolling row.",
 py='''def min_distance(word1, word2):
    prev = list(range(len(word2) + 1))
    for i, a in enumerate(word1, 1):
        cur = [i]
        for j, b in enumerate(word2, 1):
            if a == b:
                cur.append(prev[j - 1])
            else:
                cur.append(1 + min(prev[j], cur[j - 1], prev[j - 1]))
        prev = cur
    return prev[-1]''',
 js='''function minDistance(a, b) {
  let prev = Array.from({ length: b.length + 1 }, (_, j) => j);
  for (let i = 1; i <= a.length; i++) {
    const cur = [i];
    for (let j = 1; j <= b.length; j++) cur.push(a[i - 1] === b[j - 1] ? prev[j - 1] : 1 + Math.min(prev[j], cur[j - 1], prev[j - 1]));
    prev = cur;
  }
  return prev[b.length];
}''')

add(id="partition-equal-subset", title="Partition Equal Subset Sum", difficulty="Medium", cat="dp", tags=["Array","Dynamic Programming","Knapsack"],
 desc=["Return `true` if `nums` can be split into two subsets with equal sums."],
 constraints=["1 <= nums.length <= 200","1 <= nums[i] <= 100"], params=["nums"], fn={"py":"can_partition","js":"canPartition"},
 examples=[[[1,5,11,5]],[[1,2,3,5]]], tests=[[[1,5,11,5]],[[1,2,3,5]],[[1]],[[2,2]],[[1,2,5]],[[3,3,3,4,5]],[[100]*20+[1,1]]],
 hints=["If the total is odd, it's impossible. Otherwise: can some subset sum to total / 2?","0/1 knapsack: a set (or boolean array) of reachable sums, updated per number."],
 editorial=["Track all reachable subset sums. For each number, add it to every previously reachable sum. Iterating sums from high to low with a boolean array keeps each number used at most once."],
 complexity="O(n × total) time, O(total) space.",
 py='''def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    half = total // 2
    reach = [True] + [False] * half
    for x in nums:
        for s in range(half, x - 1, -1):
            if reach[s - x]:
                reach[s] = True
    return reach[half]''',
 js='''function canPartition(nums) {
  const total = nums.reduce((a, b) => a + b, 0);
  if (total % 2) return false;
  let reach = new Set([0]);
  for (const x of nums) reach = new Set([...reach, ...[...reach].map(s => s + x)]);
  return reach.has(total / 2);
}''')

# ------------------------------------------------------------------ GREEDY & INTERVALS
add(id="merge-intervals", title="Merge Intervals", difficulty="Medium", cat="greedy", tags=["Array","Sorting","Intervals"],
 desc=["Merge all overlapping intervals in `intervals` (each `[start, end]`) and return the non-overlapping result, sorted by start. Touching intervals like `[1,4]` and `[4,5]` overlap."],
 constraints=["1 <= intervals.length <= 10^4"], params=["intervals"], fn={"py":"merge","js":"merge"},
 examples=[[[[1,3],[2,6],[8,10],[15,18]]],[[[1,4],[4,5]]]], tests=[[[[1,3],[2,6],[8,10],[15,18]]],[[[1,4],[4,5]]],[[[1,4]]],[[[1,4],[0,4]]],[[[1,4],[2,3]]],[[[5,6],[1,2],[3,4]]],[[[2,3],[4,5],[6,7],[8,9],[1,10]]]],
 hints=["Sort by start. Then an interval overlaps the previous merged one exactly when its start ≤ the previous end.","Extend the previous end with max(), don't overwrite it."],
 editorial=["Sort by start. Keep a result list; if the next interval starts at or before the last result's end, extend that end to the maximum; otherwise append it."],
 complexity="O(n log n) time, O(n) space.",
 py='''def merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out''',
 js='''function merge(intervals) {
  const out = [];
  for (const [s, e] of [...intervals].sort((a, b) => a[0] - b[0])) {
    if (out.length && s <= out[out.length - 1][1]) out[out.length - 1][1] = Math.max(out[out.length - 1][1], e);
    else out.push([s, e]);
  }
  return out;
}''')

add(id="insert-interval", title="Insert Interval", difficulty="Medium", cat="greedy", tags=["Array","Intervals"],
 desc=["`intervals` is sorted by start and non-overlapping. Insert `new_interval` and merge where necessary. Return the resulting sorted, non-overlapping list."],
 constraints=["0 <= intervals.length <= 10^4"], params=["intervals","new_interval"], fn={"py":"insert","js":"insert"},
 examples=[[[[1,3],[6,9]],[2,5]],[[[1,2],[3,5],[6,7],[8,10],[12,16]],[4,8]]], tests=[[[[1,3],[6,9]],[2,5]],[[[1,2],[3,5],[6,7],[8,10],[12,16]],[4,8]],[[],[5,7]],[[[1,5]],[2,3]],[[[1,5]],[6,8]],[[[3,5]],[1,2]],[[[1,5]],[0,6]]],
 hints=["Three phases: intervals entirely before, overlapping, entirely after.","While overlapping, grow the new interval to cover each one."],
 editorial=["Copy intervals ending before the new one starts; then merge every interval whose start ≤ the new end into it; then copy the rest. One linear pass."],
 complexity="O(n) time, O(n) space.",
 py='''def insert(intervals, new_interval):
    s, e = new_interval
    out, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < s:
        out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= e:
        s = min(s, intervals[i][0]); e = max(e, intervals[i][1]); i += 1
    out.append([s, e])
    out.extend(intervals[i:])
    return out''',
 js='''function insert(intervals, ni) {
  let [s, e] = ni;
  const before = intervals.filter(x => x[1] < s), after = intervals.filter(x => x[0] > e);
  for (const x of intervals) if (!(x[1] < ni[0]) && !(x[0] > ni[1])) { s = Math.min(s, x[0]); e = Math.max(e, x[1]); }
  return [...before, [s, e], ...after];
}''')

add(id="jump-game", title="Jump Game", difficulty="Medium", cat="greedy", tags=["Array","Greedy"],
 desc=["You start at index 0. `nums[i]` is the maximum jump length from index `i`. Return `true` if you can reach the last index."],
 constraints=["1 <= nums.length <= 10^4","0 <= nums[i] <= 10^5"], params=["nums"], fn={"py":"can_jump","js":"canJump"},
 examples=[[[2,3,1,1,4]],[[3,2,1,0,4]]], tests=[[[2,3,1,1,4]],[[3,2,1,0,4]],[[0]],[[1,0]],[[0,1]],[[2,0,0]],[[1,1,1,0]],[[5,0,0,0,0,0,1]]],
 hints=["Track the farthest index reachable so far.","If you ever stand at an index beyond the farthest reach, you're stuck."],
 editorial=["Scan left to right keeping `reach = max(reach, i + nums[i])`. If `i > reach` at any point, return false. Greedy works because reachability is just an interval [0, reach]."],
 complexity="O(n) time, O(1) space.",
 py='''def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True''',
 js='''function canJump(nums) {
  let reach = 0;
  for (let i = 0; i < nums.length; i++) {
    if (i > reach) return false;
    reach = Math.max(reach, i + nums[i]);
  }
  return true;
}''')

add(id="non-overlapping-intervals", title="Non-overlapping Intervals", difficulty="Medium", cat="greedy", tags=["Array","Greedy","Intervals"],
 desc=["Return the minimum number of intervals to remove so the rest don't overlap. Intervals that only touch (like `[1,2]` and `[2,3]`) do not overlap."],
 constraints=["1 <= intervals.length <= 10^5"], params=["intervals"], fn={"py":"erase_overlap_intervals","js":"eraseOverlapIntervals"},
 examples=[[[[1,2],[2,3],[3,4],[1,3]]],[[[1,2],[1,2],[1,2]]],[[[1,2],[2,3]]]], tests=[[[[1,2],[2,3],[3,4],[1,3]]],[[[1,2],[1,2],[1,2]]],[[[1,2],[2,3]]],[[[1,100],[11,22],[1,11],[2,12]]],[[[0,2],[1,3],[2,4],[3,5],[4,6]]],[[[5,6]]]],
 hints=["Keep as many as possible instead: the classic activity-selection problem.","Sort by end time; always keep the interval that finishes first."],
 editorial=["Sort by end. Keep an interval if it starts at or after the end of the last kept one; otherwise remove it. Choosing the earliest finish leaves the most room for the rest (exchange argument)."],
 complexity="O(n log n) time, O(1) extra space.",
 py='''def erase_overlap_intervals(intervals):
    removed = 0
    end = float("-inf")
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if s >= end:
            end = e
        else:
            removed += 1
    return removed''',
 js='''function eraseOverlapIntervals(intervals) {
  let removed = 0, end = -Infinity;
  for (const [s, e] of [...intervals].sort((a, b) => a[1] - b[1])) {
    if (s >= end) end = e; else removed++;
  }
  return removed;
}''')

add(id="gas-station", title="Gas Station", difficulty="Medium", cat="greedy", tags=["Array","Greedy"],
 desc=["Stations are arranged in a circle. Station `i` gives `gas[i]` fuel, and driving to station `i + 1` costs `cost[i]`. With an empty tank, from which station index can you drive all the way around once? Return it, or `-1`. The answer is unique if it exists."],
 constraints=["1 <= n <= 10^5"], params=["gas","cost"], fn={"py":"can_complete_circuit","js":"canCompleteCircuit"},
 examples=[[[1,2,3,4,5],[3,4,5,1,2]],[[2,3,4],[3,4,3]]], tests=[[[1,2,3,4,5],[3,4,5,1,2]],[[2,3,4],[3,4,3]],[[5],[4]],[[1],[2]],[[3,1,1],[1,2,2]],[[5,1,2,3,4],[4,4,1,5,1]]],
 hints=["If total gas < total cost, it's impossible.","If you run dry going from start to i, no station between start and i can be the answer either; restart at i + 1."],
 editorial=["One pass tracking the tank since the current candidate start. When the tank drops below zero at i, set start = i + 1 and reset the tank. If the overall sum of gas − cost is non-negative, the final start works."],
 complexity="O(n) time, O(1) space.",
 py='''def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start, tank = i + 1, 0
    return start''',
 js='''function canCompleteCircuit(gas, cost) {
  let total = 0, tank = 0, start = 0;
  for (let i = 0; i < gas.length; i++) {
    total += gas[i] - cost[i];
    tank += gas[i] - cost[i];
    if (tank < 0) { start = i + 1; tank = 0; }
  }
  return total < 0 ? -1 : start;
}''')

# ------------------------------------------------------------------ MATH & BITS
add(id="single-number", title="Single Number", difficulty="Easy", cat="bits", tags=["Array","Bit Manipulation"],
 desc=["Every element of `nums` appears twice except one. Return that one, using O(1) extra memory."],
 constraints=["1 <= nums.length <= 3 × 10^4","nums.length is odd"], params=["nums"], fn={"py":"single_number","js":"singleNumber"},
 examples=[[[2,2,1]],[[4,1,2,1,2]]], tests=[[[2,2,1]],[[4,1,2,1,2]],[[1]],[[-1,-1,-2]],[[0,7,7]],[[3,5,6,5,3]]],
 hints=["What is x XOR x? What is x XOR 0?","XOR is commutative, so order doesn't matter."],
 editorial=["XOR all numbers together. Pairs cancel to 0 and the lone number remains."],
 complexity="O(n) time, O(1) space.",
 py='''def single_number(nums):
    x = 0
    for n in nums:
        x ^= n
    return x''',
 js='''function singleNumber(nums) {
  return nums.reduce((a, b) => a ^ b, 0);
}''')

add(id="missing-number", title="Missing Number", difficulty="Easy", cat="bits", tags=["Array","Math","Bit Manipulation"],
 desc=["`nums` contains `n` distinct numbers from the range `[0, n]`. Return the one number in that range that is missing."],
 constraints=["1 <= n <= 10^4"], params=["nums"], fn={"py":"missing_number","js":"missingNumber"},
 examples=[[[3,0,1]],[[0,1]],[[9,6,4,2,3,5,7,0,1]]], tests=[[[3,0,1]],[[0,1]],[[9,6,4,2,3,5,7,0,1]],[[0]],[[1]],[[1,2,3]],[[0,1,2]]],
 hints=["The sum 0 + 1 + … + n is n(n+1)/2.","Subtract the actual sum."],
 editorial=["Expected sum minus actual sum. (XOR-ing every index and value also works and never overflows in fixed-width languages.)"],
 complexity="O(n) time, O(1) space.",
 py='''def missing_number(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)''',
 js='''function missingNumber(nums) {
  let x = nums.length;
  nums.forEach((v, i) => { x ^= i ^ v; });
  return x;
}''')

add(id="counting-bits", title="Counting Bits", difficulty="Easy", cat="bits", tags=["Dynamic Programming","Bit Manipulation"],
 desc=["For every `i` from 0 to `n`, count the 1-bits in its binary form. Return the list of counts.","Try for O(n) without counting each number from scratch."],
 constraints=["0 <= n <= 10^5"], params=["n"], fn={"py":"count_bits","js":"countBits"},
 examples=[[2],[5]], tests=[[0],[1],[2],[5],[8],[16],[31]],
 hints=["`i >> 1` is i with its last bit removed, and you already know its count.","bits[i] = bits[i >> 1] + (i & 1)."],
 editorial=["DP on the binary representation: shifting right drops the lowest bit, so `bits[i] = bits[i >> 1] + (i & 1)`."],
 complexity="O(n) time, O(n) space for the output.",
 py='''def count_bits(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits''',
 js='''function countBits(n) {
  const b = new Array(n + 1).fill(0);
  for (let i = 1; i <= n; i++) b[i] = b[i >> 1] + (i & 1);
  return b;
}''')

add(id="power-of-two", title="Power of Two", difficulty="Easy", cat="bits", tags=["Math","Bit Manipulation"],
 desc=["Return `true` if `n` is a power of two (1, 2, 4, 8, …)."],
 constraints=["-2^31 <= n <= 2^31 - 1"], params=["n"], fn={"py":"is_power_of_two","js":"isPowerOfTwo"},
 examples=[[1],[16],[3]], tests=[[1],[16],[3],[0],[-16],[1024],[1023],[1073741824]],
 hints=["A power of two has exactly one 1-bit.","`n & (n - 1)` clears the lowest 1-bit."],
 editorial=["Positive and `n & (n - 1) == 0`. Zero and negatives are never powers of two."],
 complexity="O(1).",
 py='''def is_power_of_two(n):
    return n > 0 and n & (n - 1) == 0''',
 js='''function isPowerOfTwo(n) {
  return n > 0 && (n & (n - 1)) === 0;
}''')

add(id="valid-sudoku", title="Valid Sudoku", difficulty="Medium", cat="arrays", tags=["Matrix","Hash Set"],
 desc=["Determine whether a partly filled 9 × 9 Sudoku `board` is valid: each row, each column and each of the nine 3 × 3 boxes must contain the digits 1–9 at most once. Empty cells are `\".\"`. The board doesn't need to be solvable."],
 constraints=["board is 9 × 9","cells are digits 1-9 or '.'"], params=["board"], fn={"py":"is_valid_sudoku","js":"isValidSudoku"},
 examples=[[[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]]],
 tests=[[[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]],
        [[["8","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]],
        [[[".",".",".",".",".",".",".",".","."] for _ in range(9)]],
        [[["1","1",".",".",".",".",".",".","."]]+[[".",".",".",".",".",".",".",".","."] for _ in range(8)]],
        [[["1",".",".",".",".",".",".",".","."],[".","1",".",".",".",".",".",".","."]]+[[".",".",".",".",".",".",".",".","."] for _ in range(7)]]],
 hints=["Keep a set for every row, every column and every box.","Box index for cell (r, c): (r // 3) * 3 + c // 3."],
 editorial=["One pass over the 81 cells. For each digit, check and record it in its row set, column set and box set. A repeat anywhere means invalid."],
 complexity="O(81) = O(1) time and space.",
 py='''def is_valid_sudoku(board):
    seen = set()
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == ".":
                continue
            keys = (("r", r, v), ("c", c, v), ("b", r // 3, c // 3, v))
            if any(k in seen for k in keys):
                return False
            seen.update(keys)
    return True''',
 js='''function isValidSudoku(board) {
  const seen = new Set();
  for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) {
    const v = board[r][c];
    if (v === ".") continue;
    const keys = [`r${r}${v}`, `c${c}${v}`, `b${Math.floor(r / 3)}${Math.floor(c / 3)}${v}`];
    if (keys.some(k => seen.has(k))) return false;
    keys.forEach(k => seen.add(k));
  }
  return true;
}''')

add(id="lru-cache", title="LRU Cache", difficulty="Medium", cat="design", tags=["Hash Table","Linked List","Design"],
 kind="design", cls={"py":"LRUCache","js":"LRUCache"},
 desc=["Design a Least Recently Used cache with a fixed `capacity`.","`get(key)` returns the value, or `-1` if absent. `put(key, value)` inserts or updates; if that exceeds the capacity, evict the least recently used key. Both must run in O(1) average time. Reading or writing a key makes it the most recently used."],
 constraints=["1 <= capacity <= 3000","At most 2 × 10^5 calls"], params=[],
 design_examples=[[["LRUCache","put","put","get","put","get","put","get","get","get"],[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]]],
 tests_design=[
   [["LRUCache","put","put","get","put","get","put","get","get","get"],[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]],
   [["LRUCache","put","get"],[[1],[2,1],[2]]],
   [["LRUCache","put","put","put","get","get"],[[1],[1,1],[1,5],[2,2],[1],[2]]],
   [["LRUCache","get","put","get","put","put","get","get"],[[2],[2],[2,6],[1],[1,5],[1,2],[1],[2]]],
   [["LRUCache","put","put","get","put","put","get"],[[2],[2,1],[2,2],[2],[1,1],[4,1],[2]]]],
 hints=["A dict gives O(1) lookup; you also need O(1) 'move to most recent' and 'drop least recent'.","Python's `OrderedDict` has `move_to_end` and `popitem(last=False)`. A JavaScript `Map` remembers insertion order, so delete and re-insert to refresh."],
 editorial=["Pair a hash map with an ordering structure. With an ordered map: on get, move the key to the end; on put, update/insert at the end and pop from the front when over capacity. The classic hand-built version uses a doubly linked list plus a dict of nodes."],
 complexity="O(1) average per operation, O(capacity) space.",
 py='''from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.data = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key, value):
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.cap:
            self.data.popitem(last=False)''',
 js='''class LRUCache {
  constructor(capacity) { this.cap = capacity; this.map = new Map(); }
  get(key) {
    if (!this.map.has(key)) return -1;
    const v = this.map.get(key);
    this.map.delete(key); this.map.set(key, v);
    return v;
  }
  put(key, value) {
    this.map.delete(key); this.map.set(key, value);
    if (this.map.size > this.cap) this.map.delete(this.map.keys().next().value);
  }
}''')
