import pandas as pd
from urllib.parse import urlparse

df = pd.read_csv("C:/Users/lim.miin/Downloads/results.jtl")

html = """
<html>
<head>
<title>JMeter Result</title>
<style>
body{
    font-family:Segoe UI;
    background:#f6f7f9;
}
table{
    border-collapse:collapse;
    width:100%;
}
th{
    background:#e9ecef;
    text-align:left;
    padding:10px;
}
td{
    padding:10px;
    border:1px solid #ddd;
}
.pass{
    background:#edf7ed;
}
.fail{
    background:#fdecea;
}
</style>
</head>
<body>

<h1>JMeter Result</h1>

<table>
<tr>
<th>API Name</th>
<th>Test Case</th>
<th>Status Code & Description</th>
<th>Response</th>
<th>Result</th>
</tr>
"""

for _, row in df.iterrows():

    p = urlparse(row["URL"])
    api = p.netloc + p.path

    if p.query:
        api += "?" + p.query

    result = "Passed" if row["success"] else "Failed"

    css = "pass" if row["success"] else "fail"

    html += f"""
    <tr class="{css}">
        <td>{api}</td>
        <td>{row['label']}</td>
        <td>{row['responseCode']} -- {row['responseMessage']}</td>
        <td>{row['responseMessage']}</td>
        <td>{result}</td>
    </tr>
    """

html += """
</table>
</body>
</html>
"""

with open("C:/Users/lim.miin/Downloads/JMeterResult.html","w",encoding="utf-8") as f:
    f.write(html)