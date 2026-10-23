"""More problems for data/problems.json (linked lists through design). See problems_src.py for the format."""
from problems_src import add, rints, R

# ------------------------------------------------------------------ LINKED LIST
add(id="remove-duplicates-list", title="Remove Duplicates from Sorted List", difficulty="Easy", cat="linked-list", tags=["Linked List"],
 desc=["Given the `head` of a sorted linked list, delete every duplicate so each value appears only once. Return the list, still sorted."],
 constraints=["0 <= number of nodes <= 300","The list is sorted in non-decreasing order"], params=["head"], fn={"py":"delete_duplicates","js":"deleteDuplicates"}, types={"args":["list"],"ret":"list"},
 examples=[[[1,1,2]],[[1,1,2,3,3]]], tests=[[[1,1,2]],[[1,1,2,3,3]],[[]],[[5]],[[2,2,2,2]],[[-3,-3,0,1,1,1,4]]],
 hints=["Because the list is sorted, duplicates sit next to each other.","When `cur.next` has the same value as `cur`, skip it by pointing `cur.next` one node further. Only move `cur` when the values differ."],
 editorial=["Walk the list with one pointer. If the next node repeats the current value, unlink it; otherwise advance. Every node is looked at once."],
 complexity="O(n) time, O(1) space.",
 py='''def delete_duplicates(head):
    cur = head
    while cur and cur.next:
        if cur.next.val == cur.val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head''',
 js='''function deleteDuplicates(head) {
  let cur = head;
  while (cur && cur.next) {
    if (cur.next.val === cur.val) cur.next = cur.next.next;
    else cur = cur.next;
  }
  return head;
}''')

add(id="swap-pairs", title="Swap Nodes in Pairs", difficulty="Medium", cat="linked-list", tags=["Linked List","Recursion"],
 desc=["Swap every two adjacent nodes of a linked list and return its head. Change the links, not the values."],
 constraints=["0 <= number of nodes <= 100"], params=["head"], fn={"py":"swap_pairs","js":"swapPairs"}, types={"args":["list"],"ret":"list"},
 examples=[[[1,2,3,4]],[[1,2,3]],[[]]], tests=[[[1,2,3,4]],[[1,2,3]],[[]],[[1]],[[1,2]],[list(range(1,12))]],
 hints=["A dummy node in front of the head means the first swap isn't a special case.","For each pair (a, b) after `prev`: point `prev.next` to b, `a.next` to whatever followed b, and `b.next` to a. Then `prev = a`."],
 editorial=["Keep `prev`, the node before the pair. Rewire three pointers per pair and move `prev` two nodes on. The dummy node's `next` is the new head."],
 complexity="O(n) time, O(1) space.",
 py='''def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        a = prev.next
        b = a.next
        prev.next = b
        a.next = b.next
        b.next = a
        prev = a
    return dummy.next''',
 js='''function swapPairs(head) {
  const dummy = new ListNode(0, head);
  let prev = dummy;
  while (prev.next && prev.next.next) {
    const a = prev.next, b = a.next;
    prev.next = b;
    a.next = b.next;
    b.next = a;
    prev = a;
  }
  return dummy.next;
}''')

add(id="rotate-list", title="Rotate List", difficulty="Medium", cat="linked-list", tags=["Linked List","Two Pointers"],
 desc=["Rotate the list to the right by `k` places: the last `k` nodes move to the front, in order."],
 constraints=["0 <= number of nodes <= 500","0 <= k <= 2 × 10^9"], params=["head","k"], fn={"py":"rotate_right","js":"rotateRight"}, types={"args":["list",None],"ret":"list"},
 examples=[[[1,2,3,4,5],2],[[0,1,2],4]], tests=[[[1,2,3,4,5],2],[[0,1,2],4],[[],3],[[1],99],[[1,2],2],[[1,2,3,4,5],0],[[1,2,3,4,5],2000000001]],
 hints=["Rotating by the list's length changes nothing, so use `k % length`.","Join the tail to the head to make a ring, walk `length - k` steps, and cut the ring there."],
 editorial=["Count the length and find the tail in one pass. Reduce k modulo the length. Link the tail to the head, step forward `length - k` nodes from the tail to reach the new tail, then break the link after it."],
 complexity="O(n) time, O(1) space.",
 py='''def rotate_right(head, k):
    if not head:
        return head
    n, tail = 1, head
    while tail.next:
        tail = tail.next
        n += 1
    k %= n
    if k == 0:
        return head
    tail.next = head
    for _ in range(n - k):
        tail = tail.next
    new_head = tail.next
    tail.next = None
    return new_head''',
 js='''function rotateRight(head, k) {
  if (!head) return head;
  let n = 1, tail = head;
  while (tail.next) { tail = tail.next; n++; }
  k %= n;
  if (k === 0) return head;
  tail.next = head;
  for (let i = 0; i < n - k; i++) tail = tail.next;
  const newHead = tail.next;
  tail.next = null;
  return newHead;
}''')

add(id="reorder-list", title="Reorder List", difficulty="Medium", cat="linked-list", tags=["Linked List","Two Pointers"],
 desc=["Reorder the list L0 → L1 → … → Ln-1 → Ln into L0 → Ln → L1 → Ln-1 → L2 → …, changing the links in place.","Return nothing. The judge reads your rearranged list from `head`."],
 constraints=["1 <= number of nodes <= 5 × 10^4"], params=["head"], fn={"py":"reorder_list","js":"reorderList"}, types={"args":["list"],"ret":"list"}, inplace=0,
 examples=[[[1,2,3,4]],[[1,2,3,4,5]]], tests=[[[1,2,3,4]],[[1,2,3,4,5]],[[1]],[[1,2]],[[1,2,3]],[list(range(1,21))]],
 hints=["Three steps you already know: find the middle, reverse the second half, merge the two halves alternately.","Fast/slow pointers find the middle. Cut the list there so the first half ends with `None`."],
 editorial=["Split at the middle with fast and slow pointers, reverse the second half, then weave: take one node from the front half, one from the reversed back half, and repeat. Each step is O(n) and needs no extra list."],
 complexity="O(n) time, O(1) space.",
 py='''def reorder_list(head):
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev, second = second, nxt
    first, second = head, prev
    while second:
        a, b = first.next, second.next
        first.next = second
        second.next = a
        first, second = a, b''',
 js='''function reorderList(head) {
  let slow = head, fast = head;
  while (fast.next && fast.next.next) { slow = slow.next; fast = fast.next.next; }
  let second = slow.next;
  slow.next = null;
  let prev = null;
  while (second) { const nxt = second.next; second.next = prev; prev = second; second = nxt; }
  let first = head;
  second = prev;
  while (second) {
    const a = first.next, b = second.next;
    first.next = second;
    second.next = a;
    first = a;
    second = b;
  }
}''')

# ------------------------------------------------------------------ TREES
add(id="symmetric-tree", title="Symmetric Tree", difficulty="Easy", cat="trees", tags=["Tree","DFS"],
 desc=["Return `true` if the tree is a mirror of itself around its centre."],
 constraints=["1 <= number of nodes <= 1000"], params=["root"], fn={"py":"is_symmetric","js":"isSymmetric"}, types={"args":["tree"]},
 examples=[[[1,2,2,3,4,4,3]],[[1,2,2,None,3,None,3]]], tests=[[[1,2,2,3,4,4,3]],[[1,2,2,None,3,None,3]],[[1]],[[1,2,3]],[[1,2,2,2,None,2]],[[5,4,4,None,1,1,None]]],
 hints=["Compare two subtrees at once: are `a` and `b` mirrors?","Mirrors have equal roots, and `a.left` mirrors `b.right` while `a.right` mirrors `b.left`."],
 editorial=["Write `mirror(a, b)`: both empty is true, one empty is false, otherwise the values match and the outer pair and the inner pair are mirrors. Call it on the root's two children."],
 complexity="O(n) time, O(h) space.",
 py='''def is_symmetric(root):
    def mirror(a, b):
        if not a or not b:
            return a is b
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
    return mirror(root.left, root.right)''',
 js='''function isSymmetric(root) {
  const mirror = (a, b) => {
    if (!a || !b) return a === b;
    return a.val === b.val && mirror(a.left, b.right) && mirror(a.right, b.left);
  };
  return mirror(root.left, root.right);
}''')

add(id="path-sum", title="Path Sum", difficulty="Easy", cat="trees", tags=["Tree","DFS"],
 desc=["Return `true` if the tree has a root-to-leaf path whose values add up to `target_sum`. A leaf is a node with no children."],
 constraints=["0 <= number of nodes <= 5000","-1000 <= Node.val, target_sum <= 1000"], params=["root","target_sum"], fn={"py":"has_path_sum","js":"hasPathSum"}, types={"args":["tree",None]},
 examples=[[[5,4,8,11,None,13,4,7,2,None,None,None,1],22],[[1,2,3],5]], tests=[[[5,4,8,11,None,13,4,7,2,None,None,None,1],22],[[1,2,3],5],[[],0],[[1,2],1],[[1,2],3],[[-2,None,-3],-5],[[1],1]],
 hints=["Subtract each node's value from the target on the way down.","Only check `remaining == 0` at a leaf. An empty tree has no paths at all."],
 editorial=["Recurse with the remaining sum. At a leaf, the answer is whether the remainder equals the leaf's value. Otherwise either child may complete the path."],
 complexity="O(n) time, O(h) space.",
 py='''def has_path_sum(root, target_sum):
    if root is None:
        return False
    rest = target_sum - root.val
    if not root.left and not root.right:
        return rest == 0
    return has_path_sum(root.left, rest) or has_path_sum(root.right, rest)''',
 js='''function hasPathSum(root, targetSum) {
  if (!root) return false;
  const rest = targetSum - root.val;
  if (!root.left && !root.right) return rest === 0;
  return hasPathSum(root.left, rest) || hasPathSum(root.right, rest);
}''')

add(id="right-side-view", title="Binary Tree Right Side View", difficulty="Medium", cat="trees", tags=["Tree","BFS"],
 desc=["Imagine standing to the right of the tree. Return the values you can see, from top to bottom."],
 constraints=["0 <= number of nodes <= 100"], params=["root"], fn={"py":"right_side_view","js":"rightSideView"}, types={"args":["tree"]},
 examples=[[[1,2,3,None,5,None,4]],[[1,None,3]],[[]]], tests=[[[1,2,3,None,5,None,4]],[[1,None,3]],[[]],[[1,2,3,4]],[[1,2,3,4,5,6,7,8]],[[1,2]]],
 hints=["Go level by level.","The last node of each level is the one you can see."],
 editorial=["Breadth-first search one level at a time and keep the last value of every level. A DFS that visits right before left and records the first node seen at each new depth also works."],
 complexity="O(n) time, O(width) space.",
 py='''def right_side_view(root):
    out = []
    level = [root] if root else []
    while level:
        out.append(level[-1].val)
        level = [c for n in level for c in (n.left, n.right) if c]
    return out''',
 js='''function rightSideView(root) {
  const out = [];
  let level = root ? [root] : [];
  while (level.length) {
    out.push(level[level.length - 1].val);
    const next = [];
    for (const n of level) {
      if (n.left) next.push(n.left);
      if (n.right) next.push(n.right);
    }
    level = next;
  }
  return out;
}''')

add(id="lca-bst", title="Lowest Common Ancestor of a BST", difficulty="Medium", cat="trees", tags=["Tree","BST"],
 desc=["Given a binary search tree and two values `p` and `q` that are both in it, return the value of their lowest common ancestor: the deepest node that has both as descendants (a node counts as its own descendant)."],
 constraints=["2 <= number of nodes <= 10^5","All values are unique","p != q"], params=["root","p","q"], fn={"py":"lowest_common_ancestor","js":"lowestCommonAncestor"}, types={"args":["tree",None,None]},
 examples=[[[6,2,8,0,4,7,9,None,None,3,5],2,8],[[6,2,8,0,4,7,9,None,None,3,5],2,4]], tests=[[[6,2,8,0,4,7,9,None,None,3,5],2,8],[[6,2,8,0,4,7,9,None,None,3,5],2,4],[[2,1],2,1],[[6,2,8,0,4,7,9,None,None,3,5],3,5],[[6,2,8,0,4,7,9,None,None,3,5],7,9],[[6,2,8,0,4,7,9,None,None,3,5],0,5]],
 hints=["In a BST, if both values are smaller than the node, the answer is on the left.","The first node where p and q fall on different sides (or one equals the node) is the answer."],
 editorial=["Start at the root. If both values are below the node, go left; if both are above, go right; otherwise this node splits them and is the lowest common ancestor."],
 complexity="O(h) time, O(1) space.",
 py='''def lowest_common_ancestor(root, p, q):
    node = root
    while node:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:
            return node.val''',
 js='''function lowestCommonAncestor(root, p, q) {
  let node = root;
  while (node) {
    if (p < node.val && q < node.val) node = node.left;
    else if (p > node.val && q > node.val) node = node.right;
    else return node.val;
  }
}''')

add(id="build-tree", title="Build Tree from Preorder and Inorder", difficulty="Medium", cat="trees", tags=["Tree","Divide and Conquer","Hash Table"],
 desc=["Given the `preorder` and `inorder` traversals of a binary tree with unique values, rebuild the tree and return its root."],
 constraints=["1 <= preorder.length <= 3000","inorder has the same values","All values are unique"], params=["preorder","inorder"], fn={"py":"build_tree","js":"buildTree"}, types={"args":[None,None],"ret":"tree"},
 examples=[[[3,9,20,15,7],[9,3,15,20,7]],[[-1],[-1]]], tests=[[[3,9,20,15,7],[9,3,15,20,7]],[[-1],[-1]],[[1,2],[2,1]],[[1,2],[1,2]],[[1,2,4,5,3,6,7],[4,2,5,1,6,3,7]],[[1,2,3,4],[4,3,2,1]]],
 hints=["The first value in preorder is the root.","Find the root in inorder: everything to its left is the left subtree. A dict from value to inorder index makes that lookup O(1)."],
 editorial=["Consume preorder from the front. For each root, its position in inorder splits the remaining values into the left and right subtrees; build the left subtree first because preorder lists it first."],
 complexity="O(n) time, O(n) space.",
 py='''def build_tree(preorder, inorder):
    where = {v: i for i, v in enumerate(inorder)}
    nxt = [0]
    def build(lo, hi):
        if lo > hi:
            return None
        val = preorder[nxt[0]]
        nxt[0] += 1
        node = TreeNode(val)
        mid = where[val]
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node
    return build(0, len(inorder) - 1)''',
 js='''function buildTree(preorder, inorder) {
  const where = new Map(inorder.map((v, i) => [v, i]));
  let next = 0;
  const build = (lo, hi) => {
    if (lo > hi) return null;
    const val = preorder[next++];
    const node = new TreeNode(val);
    const mid = where.get(val);
    node.left = build(lo, mid - 1);
    node.right = build(mid + 1, hi);
    return node;
  };
  return build(0, inorder.length - 1);
}''')

add(id="max-path-sum", title="Binary Tree Maximum Path Sum", difficulty="Hard", cat="trees", tags=["Tree","DFS","Dynamic Programming"],
 desc=["A path is any sequence of connected nodes, each used at most once; it does not have to pass through the root. Return the largest sum of values on any non-empty path."],
 constraints=["1 <= number of nodes <= 3 × 10^4","-1000 <= Node.val <= 1000"], params=["root"], fn={"py":"max_path_sum","js":"maxPathSum"}, types={"args":["tree"]},
 examples=[[[1,2,3]],[[-10,9,20,None,None,15,7]]], tests=[[[1,2,3]],[[-10,9,20,None,None,15,7]],[[-3]],[[2,-1]],[[-1,-2,-3]],[[5,4,8,11,None,13,4,7,2,None,None,None,1]],[[1,-2,3,4,None,None,-6]]],
 hints=["For each node, compute the best path that starts at it and goes down one side: its 'gain'.","The best path that bends at a node is `val + max(0, left gain) + max(0, right gain)`. Track the best of those globally; return only the one-sided gain to the parent."],
 editorial=["A post-order DFS returns, for each node, the best downward path starting there. Negative gains are dropped (take 0). At every node, update the global answer with the path through both children. The answer may be a single negative node, so start the best at minus infinity."],
 complexity="O(n) time, O(h) space.",
 py='''def max_path_sum(root):
    best = [float("-inf")]
    def gain(node):
        if node is None:
            return 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best[0] = max(best[0], node.val + left + right)
        return node.val + max(left, right)
    gain(root)
    return best[0]''',
 js='''function maxPathSum(root) {
  let best = -Infinity;
  const gain = node => {
    if (!node) return 0;
    const left = Math.max(gain(node.left), 0);
    const right = Math.max(gain(node.right), 0);
    best = Math.max(best, node.val + left + right);
    return node.val + Math.max(left, right);
  };
  gain(root);
  return best;
}''')

# ------------------------------------------------------------------ HEAPS
add(id="kth-largest-stream", title="Kth Largest Element in a Stream", difficulty="Easy", cat="heap", tags=["Heap","Design"],
 kind="design", cls={"py":"KthLargest","js":"KthLargest"},
 desc=["Design a class that tracks the `k`-th largest score in a stream.","`KthLargest(k, nums)` starts with the scores in `nums`. `add(val)` adds a score and returns the current `k`-th largest. There will always be at least `k` scores when you are asked."],
 constraints=["1 <= k <= 10^4","0 <= nums.length <= 10^4","At most 10^4 calls to add"], params=[],
 design_examples=[[["KthLargest","add","add","add","add","add"],[[3,[4,5,8,2]],[3],[5],[10],[9],[4]]]],
 tests_design=[
   [["KthLargest","add","add","add","add","add"],[[3,[4,5,8,2]],[3],[5],[10],[9],[4]]],
   [["KthLargest","add","add","add"],[[1,[]],[-3],[-2],[-4]]],
   [["KthLargest","add","add","add","add"],[[2,[0]],[-1],[1],[-2],[3]]],
   [["KthLargest","add","add","add"],[[4,[7,7,7,7,8,3]],[2],[10],[9]]]],
 hints=["Keep only the k largest scores you've seen; the smallest of them is the answer.","A min-heap of size k does exactly that: push, and pop if it grows past k."],
 editorial=["Hold a min-heap of at most k values. Every add pushes, then pops the minimum if the heap is larger than k. The heap's root is the k-th largest so far."],
 complexity="O(log k) per add, O(k) space.",
 py='''import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = []
        for x in nums:
            self.add(x)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]''',
 js='''class KthLargest {
  constructor(k, nums) {
    this.k = k;
    this.top = [];              // the k largest, sorted ascending
    for (const x of nums) this.add(x);
  }

  add(val) {
    let i = this.top.length;
    this.top.push(val);
    while (i > 0 && this.top[i - 1] > val) { this.top[i] = this.top[i - 1]; i--; }
    this.top[i] = val;
    if (this.top.length > this.k) this.top.shift();
    return this.top[0];
  }
}''')

add(id="task-scheduler", title="Task Scheduler", difficulty="Medium", cat="heap", tags=["Greedy","Heap","Counting"],
 desc=["A CPU runs `tasks` (letters), one per time unit. Two runs of the same letter must be at least `n` units apart, so the CPU may need to sit idle. Return the fewest time units needed to finish every task."],
 constraints=["1 <= tasks.length <= 10^4","0 <= n <= 100"], params=["tasks","n"], fn={"py":"least_interval","js":"leastInterval"},
 examples=[[["A","A","A","B","B","B"],2],[["A","C","A","B","D","B"],1]], tests=[[["A","A","A","B","B","B"],2],[["A","C","A","B","D","B"],1],[["A","A","A","B","B","B"],0],[["A"],5],[["A","A","A","A","A","A","B","C","D","E","F","G"],2],[[c for c in "AAABBBCCCDDE"],2]],
 hints=["The most frequent task decides the shape: it needs `max_count - 1` gaps of `n` slots after its runs.","Count how many tasks tie for the maximum: they all fit in the final row. If there are more tasks than slots, there's no idling at all."],
 editorial=["Let m be the highest count and t the number of letters with that count. Lay out m rows of width n + 1; the last row only holds the t most frequent letters, giving `(m - 1) × (n + 1) + t`. Other letters fill the idle slots, and if they overflow, the answer is simply the number of tasks. A max-heap simulation gives the same result more slowly."],
 complexity="O(n) time, O(1) space (26 letters).",
 py='''from collections import Counter

def least_interval(tasks, n):
    counts = Counter(tasks).values()
    top = max(counts)
    ties = sum(1 for c in counts if c == top)
    return max(len(tasks), (top - 1) * (n + 1) + ties)''',
 js='''function leastInterval(tasks, n) {
  const counts = {};
  for (const t of tasks) counts[t] = (counts[t] || 0) + 1;
  const vals = Object.values(counts);
  const top = Math.max(...vals);
  const ties = vals.filter(c => c === top).length;
  return Math.max(tasks.length, (top - 1) * (n + 1) + ties);
}''')

add(id="merge-k-sorted", title="Merge K Sorted Lists", difficulty="Hard", cat="heap", tags=["Heap","Divide and Conquer"],
 desc=["You get `lists`, an array of `k` arrays each sorted in ascending order. Merge them into one sorted array.","The heap version is the point: always take the smallest current front among the k lists."],
 constraints=["0 <= k <= 10^4","0 <= lists[i].length <= 500","Total length <= 10^4"], params=["lists"], fn={"py":"merge_k_lists","js":"mergeKLists"},
 examples=[[[[1,4,5],[1,3,4],[2,6]]],[[]],[[[]]]], tests=[[[[1,4,5],[1,3,4],[2,6]]],[[]],[[[]]],[[[5],[1],[3]]],[[[1,2,3],[],[0,10]]],[[sorted(rints(40,-50,50)) for _ in range(6)]]],
 hints=["Put the first item of every list in a min-heap, tagged with which list and index it came from.","Pop the smallest, append it, and push the next item from the same list."],
 editorial=["A heap of k fronts gives the next smallest in O(log k), so N total items take O(N log k). Merging the lists pairwise, like merge sort, has the same cost."],
 complexity="O(N log k) time, O(k) extra space.",
 py='''import heapq

def merge_k_lists(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    out = []
    while heap:
        val, i, j = heapq.heappop(heap)
        out.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out''',
 js='''function mergeKLists(lists) {
  // Merge pairs of lists until one is left: the same O(N log k) as a heap.
  const merge2 = (a, b) => {
    const out = [];
    let i = 0, j = 0;
    while (i < a.length && j < b.length) out.push(a[i] <= b[j] ? a[i++] : b[j++]);
    while (i < a.length) out.push(a[i++]);
    while (j < b.length) out.push(b[j++]);
    return out;
  };
  if (!lists.length) return [];
  let round = lists;
  while (round.length > 1) {
    const next = [];
    for (let i = 0; i < round.length; i += 2) next.push(i + 1 < round.length ? merge2(round[i], round[i + 1]) : round[i]);
    round = next;
  }
  return round[0];
}''')

# ------------------------------------------------------------------ BACKTRACKING
add(id="letter-combinations", title="Letter Combinations of a Phone Number", difficulty="Medium", cat="backtracking", tags=["Backtracking","Strings"],
 desc=["Each digit 2-9 on a phone keypad maps to letters (2 → abc, 3 → def, 4 → ghi, 5 → jkl, 6 → mno, 7 → pqrs, 8 → tuv, 9 → wxyz). Return every string the `digits` could spell, in any order. An empty input gives an empty list."],
 constraints=["0 <= digits.length <= 4","digits[i] is in '2'..'9'"], params=["digits"], fn={"py":"letter_combinations","js":"letterCombinations"}, cmp="unordered",
 examples=[["23"],[""],["2"]], tests=[["23"],[""],["2"],["79"],["234"],["9999"]],
 hints=["Build the string one digit at a time; each digit offers 3 or 4 choices.","Recurse with the current prefix and the index of the next digit. When the prefix is as long as `digits`, record it."],
 editorial=["Classic backtracking over a fixed number of positions. Alternatively, start from `[\"\"]` and for each digit replace the list with every string extended by every letter for that digit."],
 complexity="O(4^n × n) time for n digits.",
 py='''def letter_combinations(digits):
    if not digits:
        return []
    keys = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    out = [""]
    for d in digits:
        out = [s + c for s in out for c in keys[d]]
    return out''',
 js='''function letterCombinations(digits) {
  if (!digits) return [];
  const keys = { 2: "abc", 3: "def", 4: "ghi", 5: "jkl", 6: "mno", 7: "pqrs", 8: "tuv", 9: "wxyz" };
  let out = [""];
  for (const d of digits) {
    const next = [];
    for (const s of out) for (const c of keys[d]) next.push(s + c);
    out = next;
  }
  return out;
}''')

add(id="palindrome-partitioning", title="Palindrome Partitioning", difficulty="Medium", cat="backtracking", tags=["Backtracking","Strings"],
 desc=["Split `s` into pieces so that every piece is a palindrome. Return every possible split, in any order. Each split lists its pieces left to right."],
 constraints=["1 <= s.length <= 12","lowercase English letters"], params=["s"], fn={"py":"partition","js":"partition"}, cmp="unordered",
 examples=[["aab"],["a"]], tests=[["aab"],["a"],["aba"],["abc"],["aaaa"],["racecar"],["abbab"]],
 hints=["Choose the first piece: try every prefix that is a palindrome, then split the rest the same way.","When the start index reaches the end of the string, the current list of pieces is one answer."],
 editorial=["Backtrack over the start position. For each end position where `s[start:end]` reads the same backwards, add it to the path, recurse from `end`, then remove it."],
 complexity="O(n × 2^n) time in the worst case (all letters equal).",
 py='''def partition(s):
    out, path = [], []
    def go(start):
        if start == len(s):
            out.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece == piece[::-1]:
                path.append(piece)
                go(end)
                path.pop()
    go(0)
    return out''',
 js='''function partition(s) {
  const out = [], path = [];
  const isPal = t => t === [...t].reverse().join("");
  const go = start => {
    if (start === s.length) { out.push([...path]); return; }
    for (let end = start + 1; end <= s.length; end++) {
      const piece = s.slice(start, end);
      if (isPal(piece)) { path.push(piece); go(end); path.pop(); }
    }
  };
  go(0);
  return out;
}''')

WS = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
add(id="word-search", title="Word Search", difficulty="Medium", cat="backtracking", tags=["Backtracking","Matrix","DFS"],
 desc=["Given a grid of letters `board` and a `word`, return `true` if the word can be traced through the grid.","Each next letter must be in a cell next to the previous one (up, down, left or right), and a cell can't be used twice in one word."],
 constraints=["1 <= rows, cols <= 6","1 <= word.length <= 15"], params=["board","word"], fn={"py":"exist","js":"exist"},
 examples=[[WS,"ABCCED"],[WS,"SEE"],[WS,"ABCB"]], tests=[[WS,"ABCCED"],[WS,"SEE"],[WS,"ABCB"],[[["A"]],"A"],[[["A","B"],["C","D"]],"ABDC"],[[["A","B"],["C","D"]],"ABCD"],[[["A","A","A"],["A","A","A"]],"AAAAAAA"]],
 hints=["Start a search from every cell that matches the first letter.","Mark a cell as used before recursing into its neighbours, and unmark it afterwards so other paths can use it."],
 editorial=["DFS from each cell with the index of the next letter to match. Temporarily overwrite the cell with a marker while it's on the path, then restore it. Return as soon as the whole word is matched."],
 complexity="O(rows × cols × 3^L) time for a word of length L.",
 py='''def exist(board, word):
    rows, cols = len(board), len(board[0])
    def dfs(r, c, i):
        if i == len(word):
            return True
        if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[i]:
            return False
        board[r][c] = "#"
        found = dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1)
        board[r][c] = word[i]
        return found
    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))''',
 js='''function exist(board, word) {
  const rows = board.length, cols = board[0].length;
  const dfs = (r, c, i) => {
    if (i === word.length) return true;
    if (r < 0 || c < 0 || r >= rows || c >= cols || board[r][c] !== word[i]) return false;
    board[r][c] = "#";
    const found = dfs(r + 1, c, i + 1) || dfs(r - 1, c, i + 1) || dfs(r, c + 1, i + 1) || dfs(r, c - 1, i + 1);
    board[r][c] = word[i];
    return found;
  };
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) if (dfs(r, c, 0)) return true;
  return false;
}''')

# ------------------------------------------------------------------ GRAPHS
def rgrid(r, c, p):
    return [[1 if R.random() < p else 0 for _ in range(c)] for _ in range(r)]

add(id="max-area-island", title="Max Area of Island", difficulty="Medium", cat="graphs", tags=["Graph","DFS","Matrix"],
 desc=["`grid` holds 1 for land and 0 for water. An island is land cells joined up, down, left or right. Return the area (number of cells) of the largest island, or 0 if there is none."],
 constraints=["1 <= rows, cols <= 50"], params=["grid"], fn={"py":"max_area_of_island","js":"maxAreaOfIsland"},
 examples=[[[[0,0,1,0,0],[1,1,1,0,0],[0,0,0,1,1],[0,0,0,1,0]]],[[[0,0,0]]]], tests=[[[[0,0,1,0,0],[1,1,1,0,0],[0,0,0,1,1],[0,0,0,1,0]]],[[[0,0,0]]],[[[1]]],[[[1,1],[1,1]]],[rgrid(12,15,0.45)],[rgrid(20,20,0.55)]],
 hints=["Same as counting islands, but each flood fill returns the size of what it filled.","Sink each visited cell (set it to 0) so it's never counted twice."],
 editorial=["Scan every cell. At unvisited land, run a DFS or BFS that marks cells as it goes and counts them. Keep the largest count."],
 complexity="O(rows × cols) time and space.",
 py='''def max_area_of_island(grid):
    rows, cols = len(grid), len(grid[0])
    def fill(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != 1:
            return 0
        grid[r][c] = 0
        return 1 + fill(r + 1, c) + fill(r - 1, c) + fill(r, c + 1) + fill(r, c - 1)
    return max(fill(r, c) for r in range(rows) for c in range(cols))''',
 js='''function maxAreaOfIsland(grid) {
  const rows = grid.length, cols = grid[0].length;
  const fill = (r, c) => {
    if (r < 0 || c < 0 || r >= rows || c >= cols || grid[r][c] !== 1) return 0;
    grid[r][c] = 0;
    return 1 + fill(r + 1, c) + fill(r - 1, c) + fill(r, c + 1) + fill(r, c - 1);
  };
  let best = 0;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) best = Math.max(best, fill(r, c));
  return best;
}''')

def rconn(n, p):
    m = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if R.random() < p: m[i][j] = m[j][i] = 1
    return m

add(id="number-of-provinces", title="Number of Provinces", difficulty="Medium", cat="graphs", tags=["Graph","Union Find","DFS"],
 desc=["There are `n` cities. `is_connected[i][j]` is 1 if city i and city j are directly linked. A province is a group of cities linked directly or through other cities. Return the number of provinces."],
 constraints=["1 <= n <= 200","is_connected[i][i] == 1","is_connected is symmetric"], params=["is_connected"], fn={"py":"find_circle_num","js":"findCircleNum"},
 examples=[[[[1,1,0],[1,1,0],[0,0,1]]],[[[1,0,0],[0,1,0],[0,0,1]]]], tests=[[[[1,1,0],[1,1,0],[0,0,1]]],[[[1,0,0],[0,1,0],[0,0,1]]],[[[1]]],[[[1,0,0,1],[0,1,1,0],[0,1,1,1],[1,0,1,1]]],[rconn(15,0.08)],[rconn(30,0.04)]],
 hints=["It's the number of connected components in a graph given as an adjacency matrix.","Union-find: union every linked pair, then count distinct roots. Or DFS from every unvisited city."],
 editorial=["Union-find with path compression joins each pair (i, j) with a 1. Every successful union reduces the component count by one, starting from n."],
 complexity="O(n² α(n)) time, O(n) space.",
 py='''def find_circle_num(is_connected):
    n = len(is_connected)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    count = n
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
                    count -= 1
    return count''',
 js='''function findCircleNum(isConnected) {
  const n = isConnected.length;
  const parent = [...Array(n).keys()];
  const find = x => {
    while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
  };
  let count = n;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    if (isConnected[i][j]) {
      const a = find(i), b = find(j);
      if (a !== b) { parent[a] = b; count--; }
    }
  }
  return count;
}''')

add(id="shortest-path-binary-matrix", title="Shortest Path in Binary Matrix", difficulty="Medium", cat="graphs", tags=["Graph","BFS","Matrix"],
 desc=["In an n × n `grid` of 0s (open) and 1s (blocked), find the shortest clear path from the top-left to the bottom-right cell. You may move in all 8 directions. Return the number of cells on the path, or -1 if there is no path."],
 constraints=["1 <= n <= 100"], params=["grid"], fn={"py":"shortest_path_binary_matrix","js":"shortestPathBinaryMatrix"},
 examples=[[[[0,1],[1,0]]],[[[0,0,0],[1,1,0],[1,1,0]]],[[[1,0,0],[1,1,0],[1,1,0]]]], tests=[[[[0,1],[1,0]]],[[[0,0,0],[1,1,0],[1,1,0]]],[[[1,0,0],[1,1,0],[1,1,0]]],[[[0]]],[[[0,0],[0,1]]],[rgrid(10,10,0.25)],[rgrid(15,15,0.3)]],
 hints=["Fewest steps in an unweighted grid means BFS.","Check both corners first. Each cell has up to 8 neighbours; mark a cell as visited when you add it to the queue."],
 editorial=["BFS from (0, 0) with distance 1, exploring all 8 neighbours. The first time the bottom-right cell is dequeued, its distance is the answer. If the queue empties first, return -1."],
 complexity="O(n²) time and space.",
 py='''from collections import deque

def shortest_path_binary_matrix(grid):
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    seen = {(0, 0)}
    q = deque([(0, 0, 1)])
    while q:
        r, c, d = q.popleft()
        if r == n - 1 and c == n - 1:
            return d
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc] and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc, d + 1))
    return -1''',
 js='''function shortestPathBinaryMatrix(grid) {
  const n = grid.length;
  if (grid[0][0] || grid[n - 1][n - 1]) return -1;
  const seen = grid.map(row => row.map(() => false));
  seen[0][0] = true;
  let q = [[0, 0]], d = 1;
  while (q.length) {
    const next = [];
    for (const [r, c] of q) {
      if (r === n - 1 && c === n - 1) return d;
      for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
        const nr = r + dr, nc = c + dc;
        if (nr >= 0 && nc >= 0 && nr < n && nc < n && !grid[nr][nc] && !seen[nr][nc]) {
          seen[nr][nc] = true;
          next.push([nr, nc]);
        }
      }
    }
    q = next;
    d++;
  }
  return -1;
}''')

def rtimes(n, m):
    out = set()
    while len(out) < m:
        u, v = R.randint(1, n), R.randint(1, n)
        if u != v: out.add((u, v))
    return [[u, v, R.randint(1, 20)] for u, v in sorted(out)]

add(id="network-delay-time", title="Network Delay Time", difficulty="Medium", cat="graphs", tags=["Graph","Dijkstra","Heap"],
 desc=["A network has `n` nodes labelled 1 to n. `times[i] = [u, v, w]` means a signal takes `w` time to travel from u to v (one way). A signal is sent from node `k`. Return how long it takes for every node to receive it, or -1 if some node never does."],
 constraints=["1 <= k <= n <= 100","1 <= times.length <= 6000","0 <= w <= 100"], params=["times","n","k"], fn={"py":"network_delay_time","js":"networkDelayTime"},
 examples=[[[[2,1,1],[2,3,1],[3,4,1]],4,2],[[[1,2,1]],2,1],[[[1,2,1]],2,2]], tests=[[[[2,1,1],[2,3,1],[3,4,1]],4,2],[[[1,2,1]],2,1],[[[1,2,1]],2,2],[[[1,2,1],[2,3,2],[1,3,4]],3,1],[[[1,2,1],[2,1,3]],2,2],[rtimes(12,40),12,1],[rtimes(30,200),30,5]],
 hints=["It's the longest of the shortest paths from k. Weighted shortest paths call for Dijkstra's algorithm.","Use a min-heap of (time, node). The first time you pop a node, that's its final time."],
 editorial=["Dijkstra from k: pop the closest unsettled node, settle it, and relax its outgoing edges. When the heap is empty, if all n nodes were settled the answer is the largest settled time, otherwise -1."],
 complexity="O(E log V) time, O(V + E) space.",
 py='''import heapq

def network_delay_time(times, n, k):
    graph = {}
    for u, v, w in times:
        graph.setdefault(u, []).append((v, w))
    dist = {}
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in dist:
            continue
        dist[u] = d
        for v, w in graph.get(u, []):
            if v not in dist:
                heapq.heappush(heap, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1''',
 js='''function networkDelayTime(times, n, k) {
  // Dijkstra with a simple O(V^2) scan instead of a heap, which is fine for n <= 100.
  const graph = Array.from({ length: n + 1 }, () => []);
  for (const [u, v, w] of times) graph[u].push([v, w]);
  const dist = Array(n + 1).fill(Infinity);
  const done = Array(n + 1).fill(false);
  dist[k] = 0;
  for (let round = 0; round < n; round++) {
    let u = -1;
    for (let i = 1; i <= n; i++) if (!done[i] && (u === -1 || dist[i] < dist[u])) u = i;
    if (dist[u] === Infinity) return -1;
    done[u] = true;
    for (const [v, w] of graph[u]) dist[v] = Math.min(dist[v], dist[u] + w);
  }
  return Math.max(...dist.slice(1));
}''')

add(id="is-bipartite", title="Is Graph Bipartite?", difficulty="Medium", cat="graphs", tags=["Graph","BFS","Coloring"],
 desc=["`graph[i]` lists the neighbours of node i in an undirected graph (which may be disconnected). Return `true` if the nodes can be split into two groups so that every edge joins nodes from different groups."],
 constraints=["1 <= n <= 100","graph[u] does not contain u","If v is in graph[u], u is in graph[v]"], params=["graph"], fn={"py":"is_bipartite","js":"isBipartite"},
 examples=[[[[1,2,3],[0,2],[0,1,3],[0,2]]],[[[1,3],[0,2],[1,3],[0,2]]]], tests=[[[[1,2,3],[0,2],[0,1,3],[0,2]]],[[[1,3],[0,2],[1,3],[0,2]]],[[[]]],[[[1],[0],[3],[2]]],[[[1],[0,2],[1,3],[2,4],[3,0]]],[[[1],[0,2],[1,3],[2,0],[]]]],
 hints=["Try to colour the graph with two colours so neighbours always differ.","BFS from every uncoloured node. If you ever find a neighbour with your own colour, it's not bipartite."],
 editorial=["Two-colouring by BFS or DFS. Start each component with colour 0; give each neighbour the opposite colour. A conflict means an odd cycle, which can't be split into two groups."],
 complexity="O(V + E) time, O(V) space.",
 py='''def is_bipartite(graph):
    color = {}
    for start in range(len(graph)):
        if start in color:
            continue
        color[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    stack.append(v)
                elif color[v] == color[u]:
                    return False
    return True''',
 js='''function isBipartite(graph) {
  const color = Array(graph.length).fill(-1);
  for (let start = 0; start < graph.length; start++) {
    if (color[start] !== -1) continue;
    color[start] = 0;
    const stack = [start];
    while (stack.length) {
      const u = stack.pop();
      for (const v of graph[u]) {
        if (color[v] === -1) { color[v] = 1 - color[u]; stack.push(v); }
        else if (color[v] === color[u]) return false;
      }
    }
  }
  return true;
}''')

# ------------------------------------------------------------------ DYNAMIC PROGRAMMING
add(id="min-cost-climbing-stairs", title="Min Cost Climbing Stairs", difficulty="Easy", cat="dp", tags=["Dynamic Programming"],
 desc=["`cost[i]` is the price of standing on step i. After paying, you can climb one or two steps. You may start on step 0 or step 1. Return the cheapest way to reach the top (just past the last step)."],
 constraints=["2 <= cost.length <= 1000","0 <= cost[i] <= 999"], params=["cost"], fn={"py":"min_cost_climbing_stairs","js":"minCostClimbingStairs"},
 examples=[[[10,15,20]],[[1,100,1,1,1,100,1,1,100,1]]], tests=[[[10,15,20]],[[1,100,1,1,1,100,1,1,100,1]],[[0,0]],[[5,1]],[rints(50,0,99)],[rints(500,0,999)]],
 hints=["The cheapest way to reach step i comes from step i-1 or step i-2.","You only need the last two answers, not a whole table."],
 editorial=["Let `dp[i]` be the cheapest way to arrive at step i without paying for it yet. You arrive from step i-1 (paying `cost[i-1]`) or from step i-2 (paying `cost[i-2]`), so `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`, with `dp[0] = dp[1] = 0`. The top is step n. Two variables replace the table."],
 complexity="O(n) time, O(1) space.",
 py='''def min_cost_climbing_stairs(cost):
    a, b = 0, 0   # cheapest cost to reach steps i-2 and i-1
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return b''',
 js='''function minCostClimbingStairs(cost) {
  let a = 0, b = 0;
  for (let i = 2; i <= cost.length; i++) [a, b] = [b, Math.min(b + cost[i - 1], a + cost[i - 2])];
  return b;
}''')

add(id="decode-ways", title="Decode Ways", difficulty="Medium", cat="dp", tags=["Dynamic Programming","Strings"],
 desc=["Letters were encoded as numbers: A → 1, B → 2, …, Z → 26. Given a string of digits `s`, return how many ways it could be decoded. A piece with a leading zero, like \"06\", is not valid."],
 constraints=["1 <= s.length <= 100","s contains only digits"], params=["s"], fn={"py":"num_decodings","js":"numDecodings"},
 examples=[["12"],["226"],["06"]], tests=[["12"],["226"],["06"],["0"],["10"],["27"],["100"],["11106"],["1111111111"],["2611055971756562"]],
 hints=["Like climbing stairs: the last piece uses one digit or two.","One digit is valid if it isn't '0'. Two digits are valid if they form 10 to 26."],
 editorial=["`dp[i]` is the number of ways to decode the first i characters. Add `dp[i-1]` when `s[i-1]` is 1-9, and `dp[i-2]` when `s[i-2:i]` is 10-26. Start with `dp[0] = 1`."],
 complexity="O(n) time, O(1) space with two variables.",
 py='''def num_decodings(s):
    prev2, prev1 = 1, 1 if s[0] != "0" else 0
    for i in range(2, len(s) + 1):
        cur = 0
        if s[i - 1] != "0":
            cur += prev1
        if 10 <= int(s[i - 2:i]) <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1''',
 js='''function numDecodings(s) {
  let prev2 = 1, prev1 = s[0] !== "0" ? 1 : 0;
  for (let i = 2; i <= s.length; i++) {
    let cur = 0;
    if (s[i - 1] !== "0") cur += prev1;
    const two = Number(s.slice(i - 2, i));
    if (two >= 10 && two <= 26) cur += prev2;
    prev2 = prev1;
    prev1 = cur;
  }
  return prev1;
}''')

add(id="palindromic-substrings", title="Palindromic Substrings", difficulty="Medium", cat="dp", tags=["Strings","Two Pointers","Dynamic Programming"],
 desc=["Return how many substrings of `s` are palindromes. Substrings at different positions count separately, even if they contain the same letters."],
 constraints=["1 <= s.length <= 1000"], params=["s"], fn={"py":"count_substrings","js":"countSubstrings"},
 examples=[["abc"],["aaa"]], tests=[["abc"],["aaa"],["a"],["abba"],["racecar"],["".join(R.choice("ab") for _ in range(200))]],
 hints=["Every palindrome has a centre: a single letter or the gap between two letters.","Expand outwards from each of the 2n - 1 centres while the ends match, counting as you go."],
 editorial=["Expand around each centre. For an odd palindrome, start with `lo = hi = i`; for an even one, `lo = i, hi = i + 1`. Each successful expansion is one more palindrome."],
 complexity="O(n²) time, O(1) space.",
 py='''def count_substrings(s):
    count = 0
    for centre in range(2 * len(s) - 1):
        lo, hi = centre // 2, centre // 2 + centre % 2
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
            count += 1
            lo -= 1
            hi += 1
    return count''',
 js='''function countSubstrings(s) {
  let count = 0;
  for (let centre = 0; centre < 2 * s.length - 1; centre++) {
    let lo = Math.floor(centre / 2), hi = lo + (centre % 2);
    while (lo >= 0 && hi < s.length && s[lo] === s[hi]) { count++; lo--; hi++; }
  }
  return count;
}''')

add(id="max-product-subarray", title="Maximum Product Subarray", difficulty="Medium", cat="dp", tags=["Dynamic Programming","Arrays"],
 desc=["Return the largest product of any non-empty contiguous subarray of `nums`."],
 constraints=["1 <= nums.length <= 2 × 10^4","-10 <= nums[i] <= 10","The answer fits in a 32-bit integer"], params=["nums"], fn={"py":"max_product","js":"maxProduct"},
 examples=[[[2,3,-2,4]],[[-2,0,-1]]], tests=[[[2,3,-2,4]],[[-2,0,-1]],[[-2]],[[-2,3,-4]],[[0,2]],[[-1,-1,-1]],[[2,-5,-2,-4,3]],[rints(30,-3,3)]],
 hints=["A negative number turns the smallest product into the largest.","Track both the largest and the smallest product ending at each position."],
 editorial=["Like Kadane's algorithm, but keep `hi` and `lo`, the max and min products of subarrays ending here. For each x, the candidates are x, hi × x and lo × x; take the max and min of those."],
 complexity="O(n) time, O(1) space.",
 py='''def max_product(nums):
    best = hi = lo = nums[0]
    for x in nums[1:]:
        cands = (x, hi * x, lo * x)
        hi, lo = max(cands), min(cands)
        best = max(best, hi)
    return best''',
 js='''function maxProduct(nums) {
  let best = nums[0], hi = nums[0], lo = nums[0];
  for (let i = 1; i < nums.length; i++) {
    const x = nums[i];
    const a = hi * x, b = lo * x;
    hi = Math.max(x, a, b);
    lo = Math.min(x, a, b);
    best = Math.max(best, hi);
  }
  return best;
}''')

add(id="house-robber-ii", title="House Robber II", difficulty="Medium", cat="dp", tags=["Dynamic Programming"],
 desc=["Same as House Robber, except the houses stand in a circle, so the first and last houses are neighbours. Return the most money you can take without taking from two neighbouring houses."],
 constraints=["1 <= nums.length <= 100","0 <= nums[i] <= 1000"], params=["nums"], fn={"py":"rob_circle","js":"robCircle"},
 examples=[[[2,3,2]],[[1,2,3,1]],[[1,2,3]]], tests=[[[2,3,2]],[[1,2,3,1]],[[1,2,3]],[[5]],[[1,5]],[[200,3,140,20,10]],[rints(40,0,100)]],
 hints=["You can't take both the first and the last house. So solve two straight-line problems.","Answer = max(rob(nums without the last), rob(nums without the first)). Handle a single house separately."],
 editorial=["Reuse the linear House Robber DP on `nums[:-1]` and `nums[1:]` and return the larger result. With one house, just take it."],
 complexity="O(n) time, O(1) space.",
 py='''def rob_circle(nums):
    def rob(houses):
        take, skip = 0, 0
        for x in houses:
            take, skip = skip + x, max(take, skip)
        return max(take, skip)
    if len(nums) == 1:
        return nums[0]
    return max(rob(nums[:-1]), rob(nums[1:]))''',
 js='''function robCircle(nums) {
  const rob = houses => {
    let take = 0, skip = 0;
    for (const x of houses) [take, skip] = [skip + x, Math.max(take, skip)];
    return Math.max(take, skip);
  };
  if (nums.length === 1) return nums[0];
  return Math.max(rob(nums.slice(0, -1)), rob(nums.slice(1)));
}''')

add(id="target-sum", title="Target Sum", difficulty="Medium", cat="dp", tags=["Dynamic Programming","Backtracking"],
 desc=["Put a `+` or `-` in front of every number in `nums`, then add them all up. Return how many different sign choices give exactly `target`."],
 constraints=["1 <= nums.length <= 20","0 <= nums[i] <= 1000","-1000 <= target <= 1000"], params=["nums","target"], fn={"py":"find_target_sum_ways","js":"findTargetSumWays"},
 examples=[[[1,1,1,1,1],3],[[1],1]], tests=[[[1,1,1,1,1],3],[[1],1],[[1],2],[[0,0,0],0],[[1,2,3,4,5],3],[rints(20,0,20),10],[[7,9,3,8,0,2,4,8,3,9],0]],
 hints=["Brute force is 2^n. Notice that many sign choices reach the same running total.","Keep a dict from running total to the number of ways to reach it, and update it for each number."],
 editorial=["Process numbers one at a time with `ways[total]`. Each number turns every total t into t + x and t - x, adding up the counts. At the end, return `ways[target]`. (A subset-sum transformation, `(sum + target) / 2`, works too.)"],
 complexity="O(n × S) time, where S is the range of possible sums.",
 py='''def find_target_sum_ways(nums, target):
    ways = {0: 1}
    for x in nums:
        nxt = {}
        for t, c in ways.items():
            nxt[t + x] = nxt.get(t + x, 0) + c
            nxt[t - x] = nxt.get(t - x, 0) + c
        ways = nxt
    return ways.get(target, 0)''',
 js='''function findTargetSumWays(nums, target) {
  let ways = new Map([[0, 1]]);
  for (const x of nums) {
    const next = new Map();
    for (const [t, c] of ways) {
      next.set(t + x, (next.get(t + x) || 0) + c);
      next.set(t - x, (next.get(t - x) || 0) + c);
    }
    ways = next;
  }
  return ways.get(target) || 0;
}''')

add(id="longest-valid-parentheses", title="Longest Valid Parentheses", difficulty="Hard", cat="dp", tags=["Stack","Dynamic Programming","Strings"],
 desc=["Given a string of `(` and `)`, return the length of the longest substring that is a well-formed (balanced) set of parentheses."],
 constraints=["0 <= s.length <= 3 × 10^4"], params=["s"], fn={"py":"longest_valid_parentheses","js":"longestValidParentheses"},
 examples=[["(()"],[")()())"],[""]], tests=[["(()"],[")()())"],[""],["()(()"],["()(())"],["))))(((("],["(()())())(("],["".join(R.choice("()") for _ in range(300))]],
 hints=["Keep a stack of indexes. Put -1 on it first as a 'last unmatched position' marker.","On `(` push its index. On `)` pop; if the stack is now empty push this index as the new marker, otherwise the valid run is `i - stack[-1]` long."],
 editorial=["The bottom of the stack is always the index just before the current valid run. Every time a `)` matches, the run ends at i and starts after the index now on top. A DP over 'longest valid ending at i' also works in O(n)."],
 complexity="O(n) time, O(n) space.",
 py='''def longest_valid_parentheses(s):
    stack, best = [-1], 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best''',
 js='''function longestValidParentheses(s) {
  const stack = [-1];
  let best = 0;
  for (let i = 0; i < s.length; i++) {
    if (s[i] === "(") stack.push(i);
    else {
      stack.pop();
      if (!stack.length) stack.push(i);
      else best = Math.max(best, i - stack[stack.length - 1]);
    }
  }
  return best;
}''')

# ------------------------------------------------------------------ GREEDY & INTERVALS
def rints2(n):
    out = []
    for _ in range(n):
        s = R.randint(0, 100)
        out.append([s, s + R.randint(1, 30)])
    return out

add(id="meeting-rooms-ii", title="Meeting Rooms II", difficulty="Medium", cat="greedy", tags=["Intervals","Sorting","Heap"],
 desc=["`intervals[i] = [start, end]` is a meeting from `start` up to (not including) `end`. Return the fewest rooms needed so no two meetings in the same room overlap. A meeting ending at 10 frees its room for one starting at 10."],
 constraints=["1 <= intervals.length <= 10^4","0 <= start < end <= 10^6"], params=["intervals"], fn={"py":"min_meeting_rooms","js":"minMeetingRooms"},
 examples=[[[[0,30],[5,10],[15,20]]],[[[7,10],[2,4]]]], tests=[[[[0,30],[5,10],[15,20]]],[[[7,10],[2,4]]],[[[1,5]]],[[[1,10],[10,20],[20,30]]],[[[1,5],[1,5],[1,5]]],[rints2(30)],[rints2(200)]],
 hints=["The answer is the most meetings happening at the same moment.","Sort the start times and the end times separately. Sweep through starts; each start that comes before the earliest unused end needs a new room."],
 editorial=["Sort starts and ends. Walk the starts with pointer i and the ends with pointer j. If `starts[i] < ends[j]`, a new room is needed; otherwise a meeting ended, so reuse its room and advance j. A min-heap of end times gives the same answer."],
 complexity="O(n log n) time, O(n) space.",
 py='''def min_meeting_rooms(intervals):
    starts = sorted(s for s, e in intervals)
    ends = sorted(e for s, e in intervals)
    rooms = j = 0
    for s in starts:
        if s < ends[j]:
            rooms += 1
        else:
            j += 1
    return rooms''',
 js='''function minMeetingRooms(intervals) {
  const starts = intervals.map(x => x[0]).sort((a, b) => a - b);
  const ends = intervals.map(x => x[1]).sort((a, b) => a - b);
  let rooms = 0, j = 0;
  for (const s of starts) {
    if (s < ends[j]) rooms++;
    else j++;
  }
  return rooms;
}''')

add(id="jump-game-ii", title="Jump Game II", difficulty="Medium", cat="greedy", tags=["Greedy","Arrays","BFS"],
 desc=["You start at index 0. `nums[i]` is the farthest you can jump forward from index i. Return the fewest jumps needed to reach the last index. You can always reach it."],
 constraints=["1 <= nums.length <= 10^4","0 <= nums[i] <= 1000"], params=["nums"], fn={"py":"jump","js":"jump"},
 examples=[[[2,3,1,1,4]],[[2,3,0,1,4]]], tests=[[[2,3,1,1,4]],[[2,3,0,1,4]],[[0]],[[1,1,1,1]],[[5,1,1,1,1]],[[1,2,3]],[[R.randint(1,5) for _ in range(200)]]],
 hints=["Think in layers, like BFS: every index reachable with j jumps forms a range.","Track the end of the current layer and the farthest point the next layer reaches. When you pass the end, take a jump."],
 editorial=["Scan left to right keeping `end` (the edge of what's reachable with the current number of jumps) and `far` (the edge for one more jump). When i reaches `end`, add a jump and set `end = far`. Stop before the last index."],
 complexity="O(n) time, O(1) space.",
 py='''def jump(nums):
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return jumps''',
 js='''function jump(nums) {
  let jumps = 0, end = 0, far = 0;
  for (let i = 0; i < nums.length - 1; i++) {
    far = Math.max(far, i + nums[i]);
    if (i === end) { jumps++; end = far; }
  }
  return jumps;
}''')

add(id="partition-labels", title="Partition Labels", difficulty="Medium", cat="greedy", tags=["Greedy","Hash Table","Strings"],
 desc=["Split `s` into as many pieces as possible so that each letter appears in at most one piece. Return the sizes of the pieces, left to right."],
 constraints=["1 <= s.length <= 500","lowercase English letters"], params=["s"], fn={"py":"partition_labels","js":"partitionLabels"},
 examples=[["ababcbacadefegdehijhklij"],["eccbbbbdec"]], tests=[["ababcbacadefegdehijhklij"],["eccbbbbdec"],["a"],["abc"],["abca"],["".join(R.choice("abcdefghij") for _ in range(60))]],
 hints=["Record the last position of every letter.","Grow the current piece until its end reaches the last position of every letter inside it; then cut."],
 editorial=["First pass: `last[c]` for each letter. Second pass: extend `end = max(end, last[s[i]])`; when `i == end`, the piece from `start` to `end` is complete."],
 complexity="O(n) time, O(1) space (26 letters).",
 py='''def partition_labels(s):
    last = {c: i for i, c in enumerate(s)}
    out, start, end = [], 0, 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            out.append(end - start + 1)
            start = i + 1
    return out''',
 js='''function partitionLabels(s) {
  const last = {};
  for (let i = 0; i < s.length; i++) last[s[i]] = i;
  const out = [];
  let start = 0, end = 0;
  for (let i = 0; i < s.length; i++) {
    end = Math.max(end, last[s[i]]);
    if (i === end) { out.push(end - start + 1); start = i + 1; }
  }
  return out;
}''')

# ------------------------------------------------------------------ MATH & BITS
add(id="hamming-distance", title="Hamming Distance", difficulty="Easy", cat="bits", tags=["Bit Manipulation"],
 desc=["The Hamming distance between two numbers is how many bit positions differ. Return it for `x` and `y`."],
 constraints=["0 <= x, y <= 2^31 - 1"], params=["x","y"], fn={"py":"hamming_distance","js":"hammingDistance"},
 examples=[[1,4],[3,1]], tests=[[1,4],[3,1],[0,0],[0,2147483647],[93,73],[123456,654321]],
 hints=["`x ^ y` has a 1 exactly where the bits differ.","Count the 1 bits: `n & (n - 1)` removes the lowest one."],
 editorial=["XOR the numbers, then count set bits. Each `n &= n - 1` clears one, so the loop runs once per differing bit."],
 complexity="O(number of differing bits).",
 py='''def hamming_distance(x, y):
    n, count = x ^ y, 0
    while n:
        n &= n - 1
        count += 1
    return count''',
 js='''function hammingDistance(x, y) {
  let n = x ^ y, count = 0;
  while (n) { n &= n - 1; count++; }
  return count;
}''')

add(id="reverse-bits", title="Reverse Bits", difficulty="Easy", cat="bits", tags=["Bit Manipulation"],
 desc=["Treat `n` as a 32-bit unsigned integer. Reverse the order of its 32 bits and return the result as an unsigned integer."],
 constraints=["0 <= n <= 2^32 - 1"], params=["n"], fn={"py":"reverse_bits","js":"reverseBits"},
 examples=[[43261596],[4294967293]], tests=[[43261596],[4294967293],[0],[1],[2147483648],[4294967295],[12345]],
 hints=["Take bits off the bottom of n one at a time and push them onto the bottom of the result.","Do it exactly 32 times, so leading zeros become trailing zeros. In JavaScript, `>>> 0` (or multiplying by 2 instead of `<<`) keeps results unsigned."],
 editorial=["Loop 32 times: `result = result * 2 + (n & 1)`, then shift n right by one. Using multiplication instead of `<<` avoids JavaScript's signed 32-bit overflow."],
 complexity="O(1): always 32 steps.",
 py='''def reverse_bits(n):
    result = 0
    for _ in range(32):
        result = result * 2 + (n & 1)
        n >>= 1
    return result''',
 js='''function reverseBits(n) {
  let result = 0;
  for (let i = 0; i < 32; i++) {
    result = result * 2 + (n & 1);
    n >>>= 1;
  }
  return result;
}''')

# ------------------------------------------------------------------ DESIGN
add(id="time-map", title="Time Based Key-Value Store", difficulty="Medium", cat="design", tags=["Hash Table","Binary Search","Design"],
 kind="design", cls={"py":"TimeMap","js":"TimeMap"},
 desc=["Store several values for the same key at different timestamps.","`set(key, value, timestamp)` stores a value. `get(key, timestamp)` returns the value set with the largest timestamp `<=` the given one, or `\"\"` if there is none. Timestamps for `set` arrive in strictly increasing order."],
 constraints=["1 <= key.length, value.length <= 100","1 <= timestamp <= 10^7","At most 2 × 10^5 calls"], params=[],
 design_examples=[[["TimeMap","set","get","get","set","get","get"],[[],["foo","bar",1],["foo",1],["foo",3],["foo","bar2",4],["foo",4],["foo",5]]]],
 tests_design=[
   [["TimeMap","set","get","get","set","get","get"],[[],["foo","bar",1],["foo",1],["foo",3],["foo","bar2",4],["foo",4],["foo",5]]],
   [["TimeMap","get","set","get","get"],[[],["a",1],["a","x",5],["a",4],["b",5]]],
   [["TimeMap","set","set","set","get","get","get","get"],[[],["love","high",10],["love","low",20],["love","mid",30],["love",5],["love",10],["love",25],["love",99]]],
   [["TimeMap","set","set","get","get"],[[],["k","one",1],["j","two",2],["k",2],["j",1]]]],
 hints=["A dict from key to a list of (timestamp, value) pairs. Because timestamps only grow, each list stays sorted.","`get` is a binary search for the last timestamp that is `<=` the one asked for."],
 editorial=["Append on `set`. On `get`, binary search the key's list for the rightmost timestamp not after the query. Python's `bisect_right` does this in one call."],
 complexity="O(1) set, O(log n) get.",
 py='''import bisect

class TimeMap:
    def __init__(self):
        self.times = {}
        self.values = {}

    def set(self, key, value, timestamp):
        self.times.setdefault(key, []).append(timestamp)
        self.values.setdefault(key, []).append(value)

    def get(self, key, timestamp):
        i = bisect.bisect_right(self.times.get(key, []), timestamp)
        return self.values[key][i - 1] if i else ""''',
 js='''class TimeMap {
  constructor() {
    this.data = new Map();      // key -> [[timestamp, value], ...]
  }

  set(key, value, timestamp) {
    if (!this.data.has(key)) this.data.set(key, []);
    this.data.get(key).push([timestamp, value]);
  }

  get(key, timestamp) {
    const list = this.data.get(key) || [];
    let lo = 0, hi = list.length;  // first index with time > timestamp
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (list[mid][0] <= timestamp) lo = mid + 1;
      else hi = mid;
    }
    return lo ? list[lo - 1][1] : "";
  }
}''')

add(id="implement-trie", title="Implement Trie (Prefix Tree)", difficulty="Medium", cat="design", tags=["Trie","Design","Strings"],
 kind="design", cls={"py":"Trie","js":"Trie"}, jsmap={"starts_with":"startsWith"},
 desc=["A trie stores words letter by letter in a tree, so words that share a prefix share a path.","`insert(word)` adds a word. `search(word)` returns `true` if that exact word was inserted. `starts_with(prefix)` (`startsWith` in JavaScript) returns `true` if any inserted word begins with `prefix`."],
 constraints=["1 <= word.length, prefix.length <= 2000","lowercase English letters","At most 3 × 10^4 calls"], params=[],
 design_examples=[[["Trie","insert","search","search","starts_with","insert","search"],[[],["apple"],["apple"],["app"],["app"],["app"],["app"]]]],
 tests_design=[
   [["Trie","insert","search","search","starts_with","insert","search"],[[],["apple"],["apple"],["app"],["app"],["app"],["app"]]],
   [["Trie","search","starts_with","insert","starts_with","search"],[[],["a"],["a"],["a"],["a"],["a"]]],
   [["Trie","insert","insert","search","search","starts_with","starts_with"],[[],["car"],["card"],["ca"],["card"],["cart"],["car"]]],
   [["Trie","insert","insert","insert","search","starts_with","search"],[[],["dog"],["do"],["dot"],["dott"],["dox"],["do"]]]],
 hints=["Each node is a dict from letter to child node, plus a flag saying whether a word ends here.","`search` and `starts_with` both walk the path; they only differ in whether the final node must be marked as a word end."],
 editorial=["Write one helper that follows a string from the root and returns the last node (or nothing if the path breaks). `search` checks that node's end flag; `starts_with` only checks that it exists. `insert` walks the same way, creating nodes as needed."],
 complexity="O(L) per operation for a word of length L.",
 py='''class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and "$" in node

    def starts_with(self, prefix):
        return self._walk(prefix) is not None''',
 js='''class Trie {
  constructor() {
    this.root = {};
  }

  insert(word) {
    let node = this.root;
    for (const ch of word) node = node[ch] ??= {};
    node.$ = true;
  }

  walk(s) {
    let node = this.root;
    for (const ch of s) {
      if (!(ch in node)) return null;
      node = node[ch];
    }
    return node;
  }

  search(word) {
    const node = this.walk(word);
    return node !== null && node.$ === true;
  }

  startsWith(prefix) {
    return this.walk(prefix) !== null;
  }
}''')
