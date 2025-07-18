from langops.parser.pipeline_parser import PipelineParser

logs = """
##[section]Starting: Install dependencies
2025-07-08T09:00:01.001Z - ##[command]npm install
added 152 packages in 2.1s
found 3 vulnerabilities (1 low, 2 moderate)

Run `npm audit fix` to address issues.

##[section]Finishing: Install dependencies

##[section]Starting: Run unit tests
> my-app@1.0.0 test
> jest

 PASS  src/components/button.test.ts
 FAIL  src/services/user.test.ts
  ✕ should fetch user data (25ms)

  ● should fetch user data

    TypeError: Cannot read properties of undefined (reading 'id')

      22 |   it('should fetch user data', () => {
    > 23 |     const user = getUser(undefined);
         |                             ^

Test Suites: 1 failed, 1 passed
Tests:       3 passed, 1 failed
##[error]Unit tests failed.

##[section]Finishing: Run unit tests

##[section]Starting: Lint code
> eslint src/

✖ 3 problems (2 errors, 1 warning)
  Line 45:  Unexpected console statement
  Line 87:  'any' type is discouraged
  Line 90:  Use of deprecated function

##[section]Finishing: Lint code

##[section]Starting: Build package
> tsc

src/main.ts:18:13 - error TS2339: Property 'foo' does not exist on type 'Bar'.

18 |   const x = obj.foo;
               ~~~~~~~

Found 1 error.

##[error]Build failed due to TypeScript error.

##[section]Finishing: Build package

##[section]Starting: Publish artifact
##[warning]Skipping publish due to build failure

##[section]Finishing: Publish artifact
"""

parser = PipelineParser(source="azure_devops", kwargs={"window_size": 30})
parsed_bundle = parser.parse(logs)
parsed_json = parser.to_json(parsed_bundle)
print("Parsed Pipeline Bundle as JSON:")
print("=" * 30)
print(parsed_json)
print("=" * 30)