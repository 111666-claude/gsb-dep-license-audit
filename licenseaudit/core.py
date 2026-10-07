"""传递闭包与许可证合规检查。"""

from collections import deque


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def audit(graph, roots, licenses, allow, deny, exceptions, counter):
    index = {}
    for key, deps in graph.items():
        counter.scanned += 1
        index[key] = deps

    seen = set()
    order = []
    queue = deque(roots)
    while queue:
        pkg = queue.popleft()
        if pkg in seen:
            continue
        seen.add(pkg)
        order.append(pkg)
        counter.scanned += 1
        for dep in index.get(pkg, ()):
            if dep not in seen:
                queue.append(dep)

    allowed = {name.strip() for name in allow}
    denied = {name.strip() for name in deny}
    exempt = set(exceptions)

    violations = []
    for pkg in order:
        if pkg in exempt:
            continue
        license_name = licenses.get(pkg, "").strip()
        if license_name in allowed and license_name not in denied:
            continue
        violations.append(pkg)
    return violations
