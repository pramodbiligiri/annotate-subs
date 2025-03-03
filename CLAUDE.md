# CLAUDE.md - Guidelines for Repository

## Build & Run Commands
```bash
# Install dependencies
npm install

# Run script to annotate subtitles
node index.js <input-srt-file> [options]
```

## Code Style Guidelines
- **Language**: JavaScript/Node.js
- **Formatting**: Use 2-space indentation
- **Naming**: 
  - Use camelCase for variables and functions
  - Use PascalCase for classes
- **Imports**: Group imports by type (built-in > external > local)
- **Error Handling**: Use try/catch blocks for async operations
- **Documentation**: Add JSDoc comments for functions

## Linting
```bash
# Run linter
npm run lint
```

## Testing
```bash
# Run all tests
npm test

# Run a specific test
npm test -- -t "test-name"
```

This repository contains tools for working with subtitle (.srt) files, likely for annotation or processing purposes.