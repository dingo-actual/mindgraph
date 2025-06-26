# conftest.py
import pytest
from failextract import extract_on_failure, FailureExtractor
import os
from datetime import datetime

def pytest_configure(config):
    """Set up FailExtract configuration."""
    # Configure the failure extractor with memory limits
    extractor = FailureExtractor()
    extractor.set_memory_limits(max_failures=500, max_passed=100)

def pytest_sessionstart(session):
    """Clean up old failure reports before starting new session."""
    output_dir = "tests/test_failures"
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                
        print(f"🧹 Cleaned up old failure reports in '{output_dir}/' directory")
    else:
        print(f"🧹 No old failure reports found in '{output_dir}/' directory")
    
    # Create fresh directory
    os.makedirs(output_dir, exist_ok=True)

def pytest_collection_modifyitems(items):
    """Automatically apply @extract_on_failure to all test functions."""
    for item in items:
        # Only apply to test functions, not fixtures
        if item.obj and callable(item.obj):
            # Check if already decorated
            if not hasattr(item.obj, '_failextract_wrapped'):
                # Apply the decorator with maximum information capture
                decorated = extract_on_failure(
                    include_locals=True,
                    include_fixtures=True,
                    max_depth=10,
                    code_context_lines=20,
                    max_code_lines=500
                )(item.obj)
                decorated._failextract_wrapped = True
                item.obj = decorated

def pytest_sessionfinish(session, exitstatus):
    """Generate individual markdown reports after all tests complete."""
    # Only generate reports if there were test failures
    if exitstatus != 0:
        save_individual_failure_reports()

def save_individual_failure_reports(output_dir="tests/test_failures"):
    """Save each test failure to its own markdown file with maximum information."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    extractor = FailureExtractor()
    
    if not extractor.failures:
        print("\n✓ No failures to report")
        return []
    
    print(f"\n📝 Generating individual failure reports...")
    generated_files = []
    
    for i, failure in enumerate(extractor.failures):
        # Create filename based on test name
        test_name = failure.get('test_name', f'unknown_test_{i}')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Clean test name for safe filename
        safe_name = test_name.replace('/', '_').replace('\\', '_').replace('::', '_')
        filename = f"{output_dir}/{safe_name}_{timestamp}.md"
        
        # Create detailed markdown content for this specific failure
        markdown_content = generate_detailed_markdown(failure)
        
        # Save to file
        with open(filename, 'w') as f:
            f.write(markdown_content)
        
        generated_files.append(filename)
        print(f"   ✓ Generated {filename}")
    
    print(f"\n📊 Summary: Generated {len(generated_files)} failure reports in '{output_dir}/' directory")
    return generated_files

def generate_detailed_markdown(failure):
    """Generate comprehensive markdown content for a single failure."""
    
    test_name = failure.get('test_name', 'Unknown Test')
    module = failure.get('test_module', 'Unknown Module')
    file_path = failure.get('test_file', 'Unknown File')
    line_number = failure.get('line_number', 'Unknown')
    exception_type = failure.get('exception_type', 'Unknown Error')
    exception_msg = failure.get('exception_message', 'No error message')
    traceback = failure.get('exception_traceback', 'No traceback available')
    timestamp = datetime.now().isoformat()
    # Start building the markdown
    content = [
        f"# Test Failure Report: `{test_name}`",
        f"",
        f"**Generated on:** {timestamp}",
        f"",
        f"## Test Information",
        f"",
        f"- **Test Name:** `{test_name}`",
        f"- **Module:** `{module}`",
        f"- **File:** `{file_path}`",
        f"- **Line Number:** {line_number}",
        f"",
        f"## Failure Details",
        f"",
        f"### Exception Type",
        f"`{exception_type}`",
        f"",
        f"### Error Message",
        f"```",
        f"{exception_msg}",
        f"```",
        f"",
        f"### Full Traceback",
        f"```python",
        f"{traceback}",
        f"```",
        f""
    ]
    
    # Add local variables if available
    if 'local_variables' in failure and failure['local_variables']:
        content.extend([
            f"## Local Variables at Failure",
            f"",
            f"```python"
        ])
        
        for var_name, var_value in failure['local_variables'].items():
            # Format variable output (limit length for readability)
            value_str = repr(var_value)
            if len(value_str) > 200:
                value_str = value_str[:200] + "..."
            content.append(f"{var_name} = {value_str}")
        
        content.extend(["```", ""])
    
    # Add test source code if available
    if 'test_source' in failure:
        content.extend([
            f"## Test Source Code",
            f"",
            f"```python",
            failure['test_source'],
            f"```",
            f""
        ])
    
    # Add fixture data if available
    if 'fixtures' in failure and failure['fixtures']:
        content.extend([
            f"## Fixture Information",
            f"",
            f"```python"
        ])
        
        for fixture in failure['fixtures']:
            fixture_name = fixture.get('name', 'unknown_fixture')
            fixture_type = fixture.get('type', 'unknown')
            
            if fixture_type == 'builtin':
                description = fixture.get('description', 'No description')
                content.append(f"# {fixture_name} (built-in): {description}")
            else:
                scope = fixture.get('scope', 'function')
                content.append(f"# {fixture_name} (scope: {scope})")
                
                if 'source' in fixture:
                    source = fixture['source']
                    if len(source) > 300:
                        source = source[:300] + "..."
                    content.append(f"{source}")
                    content.append("")
        
        content.extend(["```", ""])
    elif 'fixtures' in failure and not failure['fixtures']:
        content.extend([
            f"## Fixture Information",
            f"",
            f"No fixtures detected for this test.",
            f""
        ])
    
    # Add any additional metadata
    if 'markers' in failure and failure['markers']:
        content.extend([
            f"## Test Markers",
            f"",
            f"- " + "\n- ".join(failure['markers']),
            f""
        ])
    
    # Add duration if available
    if 'duration' in failure:
        content.extend([
            f"## Performance",
            f"",
            f"- **Test Duration:** {failure['duration']:.3f} seconds",
            f""
        ])
    
    return "\n".join(content)
