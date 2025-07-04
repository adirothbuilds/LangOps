#!/usr/bin/env python3
"""
This script demonstrates the enhanced JenkinsParser functionality.
It tests the parser with various log formats, severity levels,
and provides a summary of parsed stages.
"""

from langops.parser.jenkins_parser import JenkinsParser
from langops.core.types import SeverityLevel

# Sample Jenkins log data with different stage formats
SAMPLE_JENKINS_LOG = """
[Pipeline] { (Build)
Started by user admin
2023-10-01T10:00:00 INFO Starting build process
2023-10-01T10:01:00 ERROR Failed to compile: java.lang.NullPointerException
2023-10-01T10:02:00 WARNING Memory usage is high

[Pipeline] { (Test)
2023-10-01T10:05:00 INFO Running unit tests
2023-10-01T10:06:00 ERROR Test failed: AssertionError
2023-10-01T10:07:00 CRITICAL System.OutOfMemoryError occurred

Stage "Deploy"
2023-10-01T10:10:00 INFO Deploying to staging
2023-10-01T10:11:00 ERROR Docker build failed
2023-10-01T10:12:00 INFO Deployment complete

Running in Cleanup
2023-10-01T10:15:00 INFO Cleaning up workspace
2023-10-01T10:16:00 WARNING Temporary files remain
"""


def test_enhanced_parser():
    """
    Test the enhanced Jenkins parser.
    This function demonstrates how to use the JenkinsParser
    to parse Jenkins logs with different severity levels and formats.
    It also provides a summary of the parsed stages.
    
    Returns:
        None
    """
    parser = JenkinsParser()
    
    print("Testing enhanced JenkinsParser...")
    
    # Test with WARNING minimum severity
    result = parser.parse(SAMPLE_JENKINS_LOG, min_severity=SeverityLevel.WARNING)
    
    print(f"\nFound {len(result.stages)} stages:")
    for stage in result.stages:
        print(f"  - {stage.name}: {len(stage.logs)} log entries")
        for log in stage.logs:
            print(f"    [{log.severity.value}] {log.message[:60]}...")
    
    # Test summary functionality
    summary = parser.get_stages_summary(result)
    print("\nStage Summary:")
    for stage_name, severity_counts in summary.items():
        print(f"  {stage_name}: {severity_counts}")
    
    # Test with different severity levels
    print("\nTesting different severity levels:")
    for severity in [SeverityLevel.INFO, SeverityLevel.WARNING, SeverityLevel.ERROR, SeverityLevel.CRITICAL]:
        result = parser.parse(SAMPLE_JENKINS_LOG, min_severity=severity)
        total_logs = sum(len(stage.logs) for stage in result.stages)
        print(f"  {severity.value}: {total_logs} total log entries")
    
    print("\nTest completed successfully!")


if __name__ == "__main__":
    test_enhanced_parser()
