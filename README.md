# randimg

A web service that displays a random image, made primarily to show random pictures of [Blåhaj](https://en.wikipedia.org/wiki/Bl%C3%A5haj) on my website [kaesebrot.eu/blahaj](https://kaesebrot.eu/blahaj) :)

<p align="center" width="100%">
    <img width="65%" src="docs/screenshot.png" title="Screenshot of randimg instance running at https://kaesebrot.eu/blahaj"></img>
</p>
```bash
docker pull daskaesebrot/randimg
```

## Configuration

You may configure the bot via multiple sources.
Environment variables take precedence over the config file.

### Environment variables
| Variable name | Description | Default value | Required? |
| - | - | - | - |
| `RANDIMG_IMAGE_DIR` | Where to load the images to display from. Supperted file types: `jpg` and `png` | `assets/images` (in Docker: `/var/assets`) | No |
| `RANDIMG_CACHE_DIR` | Where to save the cached images (converted/resized) | `cache` | No |
| `RANDIMG_SITE_TITLE` | The site title to use | `Random image` | No |
| `RANDIMG_SITE_EMOJI` | The site emoji (used for the favicon and title) | `🦈` | No |
| `FORWARDED_ALLOW_IPS` | Reverse proxies to trust | `127.0.0.1` | No |
