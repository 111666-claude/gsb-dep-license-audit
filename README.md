# dep-license-audit

对依赖闭包做许可证审计：允许清单、禁止清单、按包的例外覆盖层，以及去重后的传递闭包。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m licenseaudit --sample=deny
python3 -m licenseaudit --sample=exception
python3 -m licenseaudit --sample=dupe
python3 -m licenseaudit --sample=trim
python3 -m licenseaudit --sample=work
```

## 口径

- **闭包**：从根包出发，沿依赖关系传递地取所有可达包，每个包只出现一次。
- **合规**：许可证在允许清单里**且**不在禁止清单里才算通过；两边都去掉两端空白再比较。
- **例外**：包在例外集合里时不受允许/禁止清单约束，直接放行。
- **输出**：返回不合规的包，按第一次访问顺序。
- **查找**：邻接关系只读一次建索引，不在遍历里反复扫全表。

## 不变量

- 每个可达包在结果里最多出现一次。
- 例外包不出现在不合规列表里。
- `scanned` 不随包数平方级放大：八百个包的 `scanned` 不超过 6000。

## 输出契约

`audit(...)` 返回不合规包名列表。场景打印一行 JSON。
`--sample=work` 打印 `{"packages": N, "scanned": N}`。
