# GridFlare v0.1

A simple, homelab video streaming service with current integration for youtube. Just a fun little project I threw together, becuase I wanted to learn how to intergrate FTP's, .m4s, and a video player on the web. It uses [Plyr.js](https://github.com/sampotts/plyr) for the video player, and there’s not much else to it.

![demo](image.png)

---

### Installation

> [!IMPORTANT]
> Windows support is untested at best.

Pre-requisties: `Python 3.9+`, `yt-dlp`, `ffmpeg`

1. Clone this repo:
```bash
git clone https://github.com/solarbyte-dev/gridflare
```
2. Get the videos:
```bash
python lazydown.py [YOUTUBE_LINK] [NAME_OF_VIDEO]
```
3. Run the server:
```bash
python main.py
```
> [!NOTE]
> If you plan to use any other downloading service/want to sync already downloaded videos, then go over to video.json and fill the details correctly for each video, a future update will address this

---

### Features

* Grid layout for displaying video thumbnails.
* Clicking a thumbnail opens a video player in fullscreen.
* Video player is fully customizable (play, pause, volume, fullscreen, etc.).
* Responsive; it’ll scale to any screen size (more or less).
* Simple, almost *too* minimalistic interface.

---

### How It Works

It’s really simple. I used the [Plyr.js](https://github.com/sampotts/plyr) library for the video player. `script.js` reads video.json and fetches the correct image and thumbnail, which is then showed on the website. It's REALLY barebones (for now)

---

### TODOs (Maybe Later)

* More options (like sorting stuff, tags etc)
* An  updating script; auto-generating thumbnails
* Add keyboard shortcuts for video controls (because I like mpv too much)

---

### License
Licensed under the MIT license
