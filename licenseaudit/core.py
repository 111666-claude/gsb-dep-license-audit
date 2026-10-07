"""传递闭包与许可证合规检查。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def audit(graph, roots, licenses, allow, deny, exceptions, counter):
    seen = []
    stack = list(roots)
    while stack:
        pkg = stack.pop(0)
        seen.append(pkg)
        for key in graph:
            counter.scanned += 1
            if key == pkg:
                stack.extend(graph[key])
    violations = []
    for pkg in seen:
        license_name = licenses.get(pkg, "")
        if license_name in allow:
            continue
        violations.append(pkg)
    return violations
