# CLI Commands

## Context7

Whenever in doubt about how to use a command, use Context7 to look up its documentation.

## Python Packages

- `uv pip install` - install packages
- `uv add` - add dependencies
- `uv add --dev` - add development dependencies

## Profiling and Benchmarking

- `py-spy record -f speedscope -o profile.json -- python script.py` - CPU profiling with results in profile.json
- `memray run -o output.bin script.py && memray stats output.bin` - Memory profiling with results in STDOUT

## Code Formatting and Linting

- `ruff format script.py` - Format file
- `ruff check --select E,F,B,I script.py` - Check for linting violations
- `ruff check --fix --select E,F,B,I script.py` - Fix linting violations

## Type Checking

- `uvx ty check script.py` - Type checking

## Documentation

- `sphinx-apidoc -f -o docs/source .` - Build API documentation

## Shell Utilities

### Code Analysis

- `tokei` - Count lines of code in current directory
- `tokei src/ -t Python` - Count lines for specific language
- `tokei --exclude target/ --exclude node_modules/` - Exclude directories from count
- `tokei -o json > stats.json` - Output statistics as JSON
- `tokei --sort lines` - Sort results by lines of code

### File Search

- `fd -e py` - Find all Python files
- `fd '^test_.*\.rs$' src/` - Find files matching regex pattern
- `fd -e jpg -x convert {} {.}.png` - Execute command on found files
- `fd -H '^\..*config$'` - Find hidden files matching pattern
- `fd --changed-within 1d` - Find files modified in last day

### Text Processing

- `sd 'old_pattern' 'new_pattern' file.txt` - Find and replace text
- `sd '(\w+)_(\w+)' '$2_$1' file.txt` - Replace using regex groups
- `sd -p 'pattern' 'replacement' file.txt` - Preview changes without modifying
- `choose 0 1 10` - Select specific fields from STDIN (like cut)
- `choose -f ':' 0 6` - Select fields with custom delimiter

### Command Output Parsing

- `ps aux | jc --ps | jq '.[0]'` - Convert ps output to JSON
- `df -h | jc --df | jq '.[] | select(.use_percent > 80)'` - Parse df output as JSON
- `git log --oneline | jc --git-log | jq '.[0:5]'` - Convert git log to JSON
- `jc /etc/passwd | jq '.[] | select(.username == "root")'` - Parse system files as JSON

### Code Search (AST-based)

- `sg -p 'function $NAME($_) { $$$ }' -l js` - Find all function definitions
- `sg -p 'console.log($$$)' src/` - Find specific code patterns
- `sg -p 'useState($VAL)' -r 'useState(() => $VAL)' -l tsx` - Find and replace structurally
- `sg -p '@$DECORATOR\ndef $FUNC($_):\n    $$$' -l python` - Find Python decorators

### Benchmarking

- `hyperfine 'fd -e py'` - Benchmark single command
- `hyperfine 'find . -name "*.py"' 'fd -e py'` - Compare command performance
- `hyperfine --warmup 3 'cargo build --release'` - Benchmark with warmup runs
- `hyperfine --export-json results.json 'pytest' 'python -m unittest'` - Export benchmark results
- `hyperfine -P threads 1 8 'make -j {threads}'` - Parametrized benchmarks

### HTTP Requests

- `curlie httpbin.org/get` - GET request with formatted output
- `curlie POST httpbin.org/post name=test value=123` - POST JSON data
- `curlie -H "Authorization: Bearer token" api.example.com` - Request with custom headers
- `http GET httpbin.org/get` - GET request (httpie)
- `http POST api.example.com/users name='Jane' role='admin'` - POST JSON (httpie)
- `http --download example.com/file.pdf` - Download file (httpie)

### Selection

- `echo "option1\noption2" | sk --query "opt" --select-1` - Auto-select if single match
- `fd -e py | sk --filter "test"` - Filter results non-interactively
- `ps aux | sk --query "python" --no-interactive` - Search without interaction
