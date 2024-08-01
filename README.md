# Sequilt: Abstract Overview of Large-scale Sequence Dataset
Get the bird's eye view on a single page. 

## Installation
Install via PyPI

```shell
pip install sequilt
```

## Development

Install [pnpm](https://pnpm.io/installation) and [Hatch](https://hatch.pypa.io/latest/install/) to set up the development environment.

You can manage both TypeScript and Python environments with **pnpm**. Check the [`package.json`](https://github.com/jiwnchoi/Sequilt/blob/main/package.json).

Linter and formatter are configured with [Biome](https://biomejs.dev) and [Ruff](https://docs.astral.sh/ruff/). Highly recommend installing editor plugins. 

```shell
# For development
git clone https://github.com/jiwnchoi/sequilt.git
cd sequilt
pnpm install
pnpm dev # Excutes vite dev server and jupyter lab. 

# Build
pnpm build

# Deploy
pnpm deploy

# Lint and Format
pnpm check # Lint and Format both .py and .ts files

# Test
pnpm test # Test TypeScript with Vitest and Python with pytest
```

