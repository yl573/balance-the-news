#!/usr/bin/env bash
python3 siteRoots.py left & python3 siteRoots.py right & python3 siteRoots.py center
python3 siteRoots.py leftcenter & python3 siteRoots.py right-center

python3 siteURLs.py left & python3 siteURLs.py right & python3 siteURLs.py center
python3 siteURLs.py leftcenter & python3 siteURLs.py right-center
