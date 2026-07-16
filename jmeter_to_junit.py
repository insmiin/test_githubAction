import sys
import xml.etree.ElementTree as ET

input_file =  sys.argv[1]   #"D:/SVN qat/gt_test/test_githubAction/results_test.xml"
output_file = sys.argv[2]   #"D:/SVN qat/gt_test/test_githubAction/junit_test.xml"

jmeter_tree = ET.parse(input_file)
jmeter_root = jmeter_tree.getroot()

testsuite = ET.Element("testsuite")
tests = 0
failures = 0

for sample in jmeter_root.iter():
    if sample.tag not in ("sample", "httpSample"):
        continue

    tests += 1

    label = sample.attrib.get("lb", "Unnamed")
    success = sample.attrib.get("s", "true").lower() == "true"
    response_message = sample.attrib.get("rm", "")

    testcase = ET.SubElement(
        testsuite,
        "testcase",
        name=label,
        classname="JMeter"
    )

    if not success:
        failures += 1
        failure = ET.SubElement(
            testcase,
            "failure",
            message=response_message
        )
        failure.text = response_message

testsuite.set("tests", str(tests))
testsuite.set("failures", str(failures))

testsuites = ET.Element("testsuites")
testsuites.append(testsuite)

ET.ElementTree(testsuites).write(
    output_file,
    encoding="utf-8",
    xml_declaration=True
)