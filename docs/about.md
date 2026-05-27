# About

Serica is a lightweight self-hosted gallery server built on Flask and Waitress. It serves directories of images and short videos as styled, grid-based gallery pages — no database, no authentication layer, no admin panel.

The use case is intentionally narrow: you mount a directory of media files into the container, optionally drop in a `cover.jpg` per subdirectory, and Serica renders one page per subdirectory plus an index of all available galleries.

Each page lays media out in a repeating `2 / 2 / 1` grid pattern (two split rows followed by a fullscreen one) and exposes a sticky navigation bar that links to all sibling galleries.

It was built to host wedding and trip photo collections behind a reverse proxy on a personal server, where the deployer controls who can reach the URL. There is no built-in authentication: if you expose Serica directly to the public internet, every gallery is world-readable.

Run it behind nginx (or any reverse proxy) with HTTP basic auth, OAuth2-proxy, or IP allowlisting if that's not what you want.
