# LangOps Documentation Docker Setup

This directory contains Docker configuration files for running the LangOps documentation website.

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Start the documentation server
docker-compose -f docker-compose.docs.yml up --build

# Or use the Makefile
make docs-docker-compose
```

### Option 2: Using Docker directly

```bash
# Build the documentation image
docker build -f Dockerfile.langops.docs -t langops-docs .

# Run the documentation server
docker run --rm -p 8000:8000 langops-docs

# Or use the Makefile
make docs-docker
```

### Option 3: Local Development

```bash
# Install dependencies
pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python

# Serve locally
mkdocs serve

# Or use the Makefile
make docs-serve
```

## Access the Documentation

Once running, the documentation will be available at:

- **Local**: <http://localhost:8000/langops/>
- **Docker**: <http://localhost:8000/langops/>

## Files

- `Dockerfile.langops.docs` - Docker configuration for the documentation server
- `docker-compose.docs.yml` - Docker Compose configuration
- `mkdocs.yml` - MkDocs configuration
- `docs/` - Documentation source files

## Features

- **Live Reload**: Changes to documentation files are automatically reflected
- **Beautiful Design**: Material Design theme with custom styling
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Search**: Full-text search across all documentation
- **Dark/Light Mode**: Automatic theme switching
- **Code Highlighting**: Syntax highlighting for code blocks
- **Copy Code**: One-click code copying
- **Navigation**: Tabbed navigation with breadcrumbs

## Development

For development, mount the source directories to enable live reload:

```bash
# Using Docker Compose (volumes are already configured)
docker-compose -f docker-compose.docs.yml up --build

# Using Docker directly with volumes
docker run --rm -p 8000:8000 \
  -v $(pwd)/docs:/app/docs:ro \
  -v $(pwd)/mkdocs.yml:/app/mkdocs.yml:ro \
  langops-docs
```

## Production Deployment

For production deployment, you can:

1. **Build static files**:

   ```bash
   mkdocs build
   # Static files will be in site/ directory
   ```

2. **Deploy to GitHub Pages**:

   ```bash
   mkdocs gh-deploy
   ```

3. **Use with a reverse proxy**:
   - Uncomment the nginx service in `docker-compose.docs.yml`
   - Configure nginx.conf for your domain
   - Use SSL certificates for HTTPS

## Troubleshooting

### Port already in use

If port 8000 is already in use, change the port mapping:

```bash
# Docker
docker run --rm -p 8080:8000 langops-docs

# Docker Compose
# Edit docker-compose.docs.yml and change "8000:8000" to "8080:8000"
```

### Permission issues

If you encounter permission issues, ensure the docs user has proper permissions:

```bash
# Fix permissions
sudo chown -R $(id -u):$(id -g) docs/
```

### Missing dependencies

If you see import errors, ensure all required packages are installed:

```bash
# Rebuild the Docker image
docker-compose -f docker-compose.docs.yml build --no-cache
```

## Health Check

The Docker container includes a health check that verifies the documentation server is running:

```bash
# Check container health
docker ps

# View health check logs
docker logs langops-docs
```

## Contributing

To contribute to the documentation:

1. Edit files in the `docs/` directory
2. Test locally with `make docs-serve`
3. Verify the build works with `make docs-build`
4. Submit a pull request

## Support

For issues with the documentation setup:

- Check the [main README](README.md) for general information
- Review the [MkDocs documentation](https://www.mkdocs.org/)
- Check the [Material for MkDocs documentation](https://squidfunk.github.io/mkdocs-material/)
- Open an issue on the [GitHub repository](https://github.com/adirothbuilds/langops/issues)
