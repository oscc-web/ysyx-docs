# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

### Local Development

#### Build docker dev container
```
docker compose build
```

#### Start docker dev container
```
docker compose run -P docusaurus
```

#### Start dev server
If using docker
```
npm run start -- --host 0.0.0.0
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

TBD
