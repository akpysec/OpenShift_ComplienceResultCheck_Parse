# Red Hat Open Shift Operator output Parser
Open Shift operator exports output as XML when running compliance check.
The XML file is usually very large (around ~30 thousand lines for CIS compliance check) and it's very difficult to go around the exported check configuration / findings.
This script will parse through all the lines, will drop duplicate check and output all to a nice Excell spread sheet.

### How to run:
- You can specify a path to ComplianceCheckResult-cis.YAML file and specify the output path ComplianceCheckResult-cis.xlsx
- Run - `python OpenShift_RewriteResultYAML.py`


### Enjoy :)
