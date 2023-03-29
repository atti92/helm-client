# helm-client

This project aims to provide an easy interface over helm-cli.

Basic syntax is very similar to helm cli.

`helm.repo.list()` is the same as `helm repo list`

## Example Usage

```python
import helm
from helm.models import HelmRepo

repositories: List[HelmRepo] = helm.repo.list()
for repo in repositories:
    print(repo.name)
```

## Models

We aim to provide pydantic models for all reasonable use-cases.

## Arguments

The default implementation of the commands can handle keyword arguments, like `namespace=something` and transforms them to correct cli arguments.

- `--arg-name value` is the same as `arg_name=value`
- `--boolarg` is the same as `boolarg=True`

## Work in progress

Expect breaking changes
