# YSYX Project Website

Welcome to the YSYX Project Website repository! This project serves as the new main page for the YSYX project study material, available at [YSYX Project](https://ysyx.oscc.cc/docs/). The website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Table of Contents

- [Local Development](#local-development)
  - [Recommended Workflow](#recommended-workflow)
  - [Build Docker Dev Container](#build-docker-dev-container)
  - [Start Docker Dev Container](#start-docker-dev-container)
  - [Start Dev Server](#start-dev-server)
- [Content Synchronization](#content-synchronization)
  - [Pull Content](#pull-content)
  - [Usage](#usage)
  - [Examples](#examples)
- [Directory Structure](#directory-structure)
  - [docs Directory](#docs-directory)
  - [i18n Directory](#i18n-directory)
- [Build](#build)
- [Deployment](#deployment)

## Local Development

### Recommended Workflow

To ensure a consistent development environment, we use a Docker development container. This approach provides several benefits:

- **Consistency**: All developers work in the same environment, eliminating "it works on my machine" issues.
- **Isolation**: Keeps the development environment isolated from the host system, preventing conflicts with other projects or dependencies.
- **Ease of Setup**: Simplifies the setup process by providing a pre-configured environment with all necessary dependencies.
- **Portability**: Allows the development environment to be easily shared and replicated across different machines.

Here’s how to get started:

1. **Update `TAG` in the Makefile**: Set the desired release tag (default is the latest release).
2. **Start the container and development server**:

    ```sh
    docker compose run -P docusaurus
    make pull
    npm run start -- --host 0.0.0.0
    ```

3. **Access the website**: Open your host browser and navigate to the local development server.

### Build Docker Dev Container

To build the Docker development container, run:

```sh
docker compose build
```

### Start Docker Dev Container

To start the Docker development container, run:

```sh
docker compose run -P docusaurus
```

The `-P` flag exposes the port for the web server, allowing you to connect to the website hosted inside the container from your host browser.

### Start Dev Server

If using Docker, start the development server with:

```sh
npm run start -- --host 0.0.0.0
```

This command starts a local development server and opens a browser window. Most changes are reflected live without having to restart the server.

## Content Synchronization

### Pull Content

`pull_content` is a Python script used to sync content from a GitHub release of the documentation content. It can be run directly or via `make`. Usually, developers should run:

```sh
make pull
```

This invokes the following command:

```sh
pull_content --repo oscc-web/ysyx-docs-content --tag latest --map zh:docs --map en:i18n/en/docusaurus-plugin-content-docs/current
```

### Usage

The script can be used from the command line with the following syntax:

```sh
pull_content.py [--map <source:destination>]...
```

- `--repo`: The GitHub repository in the format `owner/repo`.
- `--tag`: The release tag to download.
- `--map` or `-m`: Mapping in the format `source:destination`. This argument can be provided multiple times.

### Examples

**Example 1: Basic Download and Extraction**

Download and extract a release from the repository `oscc-web/ysyx-docs-content` with the tag `latest`.

```sh
pull_content.py oscc-web/ysyx-docs-content latest
```

**Example 2: Mapping Folders**

Download the release and map the `zh` and `en` folders to specific destinations.

```sh
pull_content.py oscc-web/ysyx-docs-content latest --map zh:./zh --map en:./en
```

### Content Sync Process

The content synchronization process involves pulling the latest documentation from the GitHub repository and mapping it to the appropriate directories in the project. Here is a visual representation of the process:

## Directory Structure

### docs Directory

The `docs` directory contains the documentation files organized in a hierarchical format. Each Markdown file represents a documentation page, and these files can be grouped into subdirectories to create a structured documentation hierarchy. The `docs` directory is essential for organizing and managing the content of your documentation site.

### i18n Directory

The `i18n` directory is used for internationalization (i18n) support. It contains translation files for different locales, allowing the website to be translated into multiple languages. Each locale has its own subdirectory within the `i18n` directory, and each subdirectory contains the necessary translation files for that locale. This structure enables the website to support multiple languages and provides a flexible translation workflow.

## Build

To generate static content into the `build` directory, run:

```sh
npm run build
```

This content can be served using any static content hosting service.

## Deployment

*To be determined (TBD)*
