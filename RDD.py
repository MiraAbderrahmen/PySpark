import xml.etree.ElementTree as ET

r = ET.parse("coverage.cobertura.xml").getroot()

for pkg in r.iter("package"):
    if pkg.get("name") != "DwhIngestion.Service":
        continue

    total = uncovered = 0

    for c in pkg.findall("classes/class"):
        for m in c.findall("methods/method"):
            total += 1

            line_rate = float(m.get("line-rate", 0))

            if line_rate == 0:
                uncovered += 1
                print(
                    "UNCOVERED  %s :: %s%s"
                    % (
                        c.get("name"),
                        m.get("name"),
                        m.get("signature", "")
                    )
                )

    covered = total - uncovered
    method_rate = covered / total if total else 0

    print()
    print(f"Total methods = {total}")
    print(f"Covered methods = {covered}")
    print(f"Uncovered methods = {uncovered}")
    print(f"Method coverage = {method_rate:.2%}")