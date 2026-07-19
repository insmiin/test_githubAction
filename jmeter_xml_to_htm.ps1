param(
    [string]$XmlFile,
    [string]$OutputFile
)

[xml]$xml = Get-Content $XmlFile

$rows = foreach ($sample in $xml.testResults.httpSample) {

    $rc = $sample.rc
    $rm = $sample.rm
    $success = $sample.s -eq "true"

    if ($success) {
        $result = "Passed"
    }
    elseif ($rc -ne "200") {
        $result = "Undefined result"
    }
    else {
        $result = "Failed"
    }

    $rowClass = if ($success) { "pass" } else { "fail" }

    # URL
    $url = $sample.'java.net.URL'
    $uri = [System.Uri]$url
    $api = "$($uri.Host)$($uri.AbsolutePath)"

    # Test case
    $testcase = $sample.lb

    # HTTP status
    $httpStatus = "$rc - $rm"

    if ($rc -ne "200") {
        $apiResponse = ""
        $expectedReturn = ""
    }
    else {
        $apiResponse = $sample.responseData

        $expectedReturn = ""
        if ($sample.assertionResult) {
            $expectedReturn =
                $sample.assertionResult.failureMessage
        }
    }

    $enc = [System.Net.WebUtility]

@"
<tr class="$rowClass">
    <td>$($enc::HtmlEncode($api))</td>
    <td>$($enc::HtmlEncode($testcase))</td>
    <td>$($enc::HtmlEncode($httpStatus))</td>
    <td>$($enc::HtmlEncode($apiResponse))</td>
    <td>$($enc::HtmlEncode($expectedReturn))</td>
    <td class="status">$result</td>
</tr>
"@
}

$html = @"
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>API Test Result</title>
<style>
body {
    font-family: Segoe UI, Arial, sans-serif;
    margin: 24px;
    background: #f6f7f9;
}
table {
    border-collapse: collapse;
    width: 100%;
    background: white;
}
th,td {
    border:1px solid #dadce0;
    padding:8px;
}
tr.pass td { background:#f0fbf4; }
tr.fail td { background:#fff4f4; }
.pass td.status { color:#137333; font-weight:bold; }
.fail td.status { color:#b3261e; font-weight:bold; }
</style>
</head>
<body>

<h1>API Test Result</h1>

<table>
<thead>
<tr>
    <th>API Name</th>
    <th>Test Case</th>
    <th>Http status code</th>
    <th>API Response</th>
    <th>Expected Return</th>
    <th>Result</th>
</tr>
</thead>
<tbody>
$($rows -join "`n")
</tbody>
</table>

</body>
</html>
"@

$html | Set-Content $OutputFile -Encoding UTF8

Write-Host "HTML report generated: $OutputFile"