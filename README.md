# randimg

A web service that displays a random image.

## Pulling the image
Docker hub: https://hub.docker.com/r/daskaesebrot/randimg
```bash
docker pull daskaesebrot/randimg
```

## Configuration

You may configure the bot via multiple sources.
Environment variables take precedence over the config file.

### Environment variables
| Variable name | Description | Default value | Required? |
| - | - | - | - |
| `RANDIMG_IMAGE_DIR` | Where to load the images to display from. Supperted file types: `jpg` and `png` | `assets/images` | No |
| `RANDIMG_CACHE_DIR` | Where to save the cached images (converted/resized) | `cache` | No |
| `RANDIMG_SITE_TITLE` | The site title to use | `Random image` | No |
| `FORWARDED_ALLOW_IPS` | Reverse proxies to trust | `127.0.0.1` | No |
