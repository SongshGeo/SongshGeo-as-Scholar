---
title: Mksci
summary: A python-based command-line tool for managing a scientific project, saving you from aggravating version iteration of documents before getting published.
tags:
date: '2021-10-10T00:00:00Z'

# Optional external URL for project (replaces project detail page).
external_link: ''

image:
  caption: 'Image credit: [**Unsplash**](https://unsplash.com/photos/m_HRfLhgABo)'
  focal_point: Smart


links:
  - icon: twitter
    icon_pack: fab
    name: Follow
    url: https://twitter.com/ShuangSong11
url_code: ''
url_pdf: ''
url_slides: ''
url_video: ''

# Slides (optional).
#   Associate this project with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
# slides: example
---

## Introduction
There are many trivial routines in researchers' daily life: data management, file organization, and polishing manuscripts or re-submit them again and again... To boost productivity, we designed this toolbox package to help researchers maintain their study items/projects better. This package aims at reminding you to store helpful information when necessary, and then reuse them to generate documents in the future automatically. It helps researchers quickly re-access to their projects no matter how many versions or years have passed. 

## Quick start

Install through `pip`:
```shell
pip install mksci
```

Setup a new project in a new folder:
```shell
mksci project new <folder-name>
```
or init the current path folder as a new project:
```bash
mksci project init .
```

Then, you will find that setting files are created automatically: `config.yaml`, `author.yaml`, and `docs.yaml`. Make some personal settings for them, for example: 
```yaml
project:
	name: "Demo"
	status: "Ongoing"
	start: 2022-08-09
	end: None
	introduction: "This is a demo mksci project."

repo:
	name: "Mksci_demo"
	owner: "songshgeo"
	background: "img@background" # assets: img: background
	license: "MIT"
```

If you have not decided when to Don't worry, you can update your settings whenever you work on this project. 

Then, to use your settings in generating documents, you can refresh your project: 

```shell
mksci project refresh
```

You will find that all doc files defined in `docs.yaml` are automatically generated with the information you filled: 
In other words, `mksci` provides you with a way to define project-level variables which can automatically update in all your documents: data description, code documents, paper manuscript, data description...
![CleanShot2022-08-16at08.53.04](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/CleanShot%202022-08-16%20at%2008.53.04.png)

More information is [accessible in the document](#).

## Contribution
- [Shuang Song](https://cv.songshgeo.com/), a ph.d student at Beijing Normal University designed and developed this tool package.
- Miemie: also contributed to developing this project.
