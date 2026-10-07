"""传递闭包与许可证合规检查。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def audit(graph, roots, licenses, allow, deny, exceptions, counter):
    allow = {name.strip() for name in allow}
    deny = {name.strip() for name in deny}
    seen = []
    visited = set()
    queue = list(roots)
    while queue:
        pkg = queue.pop(0)
        if pkg in visited:
            continue
        visited.add(pkg)
        seen.append(pkg)
        counter.scanned += 1
        for dep in graph.get(pkg, ()):  # 邻接关系按 key 直接索引，不扫全表
            if dep not in visited:
                queue.append(dep)
    violations = []
    for pkg in seen:
        if pkg in exceptions:
            continue
        license_name = licenses.get(pkg, "").strip()
        if license_name in deny:
            violations.append(pkg)
            continue
        if license_name in allow:
            continue
        violations.append(pkg)
    return violations
