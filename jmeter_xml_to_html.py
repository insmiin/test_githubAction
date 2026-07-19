import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from html import escape
import sys

def xml_to_html(xml_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    rows = []

    for sample in root.findall("httpSample"):     #return ALL 1st level elements (called 'httpSample') , together with their own attributes & child elements under it
        # HTTP status
        rc = sample.attrib.get("rc", "")  #response code of http (not the response body)
        rm = sample.attrib.get("rm", "")  # response msg of http

        # sampler failed or success (success if httpcode is not errorcode  and assertion passed)
        success = sample.attrib.get("s", "false") == "true"

        # testcase Pass/Fail
        if success:
            result = "Passed"
        elif rc != "200":
            result = "Undefined result"
        else:
            result = "Failed"
        row_class = "pass" if success else "fail"


        # URL / API
        url = sample.findtext("java.net.URL", "")   #return txt of element
        parsed = urlparse(url)
        api = parsed.netloc + parsed.path

        # if parsed.query:
        #     api += f"?{parsed.query}"
        # if parsed.fragment:
        #     api += f"#{parsed.fragment}"

        # Thread/Test name
        testcase = sample.attrib.get("lb", "") #samplerName

        # Http statuscode
        http_status = f"{rc} - {rm}"

        if rc != "200":
            API_response  = ''
            failureMessage = 'http request failed'
        else:
            # Response JSON
            API_response = sample.findtext("responseData", "")

            # Assertion message
            assertion = sample.find("assertionResult")  # return 1st matching element called 'assertionResult' and its own attributes & child elements
            failureMessage = ''  # if there is more than 1 then need to use findall and loop thru it again.
            if assertion is not None:
                msg = assertion.findtext("failureMessage")
                print('msg==', msg)
                if msg:
                    failureMessage = msg

        rows.append(f"""
            <tr class="{row_class}">
                <td>{escape(api)}</td>
                <td>{escape(testcase)}</td>
                <td>{http_status}</td>
                <td>{escape(API_response)}</td>
                <td class="status">{result}</td>
                <td>{escape(failureMessage)}</td>
            </tr>
            """)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>API Test Result</title>
    <style>
    body {{
        font-family: Segoe UI, Arial, sans-serif;
        margin: 24px;
        background: #f6f7f9;
        color: #202124;
    }}
    h1 {{
        margin-bottom: 10px;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        background: white;
        border: 1px solid #dadce0;
    }}
    th, td {{
        border: 1px solid #dadce0;
        padding: 8px 10px;
        text-align: left;
        vertical-align: top;
        font-size: 13px;
    }}
    th {{
        background: #eef2f7;
    }}
    tr.pass td {{
        background: #f0fbf4;
    }}
    tr.fail td {{
        background: #fff4f4;
    }}
    td.status {{
        font-weight: bold;
    }}
    .pass td.status {{
        color: #137333;
    }}
    .fail td.status {{
        color: #b3261e;
    }}
    pre {{
        margin: 0;
        white-space: pre-wrap;
    }}
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
        <th>Result</th>
        <th>Failure Message</th>
    </tr>
    </thead>
    <tbody>
    {''.join(rows)}
    </tbody>
    </table>

    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML report generated: {output_file}")

# sys.argv[0] is 'jmeter_xml_to_html.py'
input_xml = sys.argv[1]   # Catches "results.xml"
output_html = sys.argv[2] # Catches "results_html.html"

# Usage
xml_to_html(input_xml, output_html)
# xml_to_html("C:/Users/lim.miin/Downloads/results.xml", "C:/Users/lim.miin/Downloads/JMeterResult.html")
