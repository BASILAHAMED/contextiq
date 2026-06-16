# Publishing ContextIQ

This project is prepared for PyPI publishing.

## Before publishing

1. Make sure the package name `contextiq` is available on PyPI.
2. Update the version in [pyproject.toml](./pyproject.toml).
3. Verify the README and metadata look right.
4. Run a build locally on a machine without the temp-directory permission issue seen in this workspace:

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

## Recommended path

Use GitHub Actions with API tokens.

Workflow:

- `workflow_dispatch` publishes to TestPyPI
- GitHub Release `published` publishes to PyPI

See:

- [`.github/workflows/publish-pypi.yml`](./.github/workflows/publish-pypi.yml)

## GitHub secrets

Add these repository secrets in GitHub:

1. `PYPI_API_TOKEN`
2. `TEST_PYPI_API_TOKEN`

The workflow uses:

- `PYPI_API_TOKEN` for real PyPI releases
- `TEST_PYPI_API_TOKEN` for manual TestPyPI publishing

## Manual publish fallback

If you prefer API-token uploads:

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine upload dist/*
```

## Notes

- This workspace had Windows temp-permission issues during `python -m build`, so the repo was prepared for CI-based publishing even though local artifact generation could not be completed here.
- The import package is `contextiq`.
- The CLI command is `contextiq`.
