# ANSWERS

## 1. Order of the Dockerfile instructions

Each instruction in a Dockerfile creates a layer, and when one layer changes, Docker rebuilds that layer and every layer after it. Because of this, I put the things that rarely change at the top and the things that change often at the bottom. First I copy only requirements.txt and run pip install, and I copy app.py at the end because it changes most often. If I swapped them and copied app.py before pip install, every small code change would break the cache and pip install would run again on every build. This would make builds slower for no reason, because the dependencies did not actually change.

## 2. Data inside a container

When a container is removed, the data written inside it is lost, because it lives in the container's writable layer, which is deleted together with the container. I tested this with my /visits endpoint: without a volume, the counter went back to 1 after I removed and restarted the container. When I ran it with `-v hw1-data:/data`, the counter continued from where it stopped, because the data was stored in the volume, outside the container. This way the container itself stays stateless and can be removed or replaced at any time without losing data. Important state should be kept outside the container, for example in a volume, a database or object storage.

## 3. The `latest` tag

The `latest` tag does not point to one fixed version; it points to whatever version was pushed most recently. So the same Dockerfile can pull a different image today and in a few months, and the build is no longer reproducible. A new version can also conflict with the versions my code and dependencies expect, and the app may break without any change in my code. Instead, I pinned the base image to an exact version, `python:3.12.7-slim-bookworm`, and I also pinned my dependencies in requirements.txt (`flask==3.1.3`, `gunicorn==23.0.0`).
