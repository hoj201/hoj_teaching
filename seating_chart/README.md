# Description
Code for generating welcome slides

```shell
poetry run python make_slides.py
```

You can customize the slides by editing
 - `agenda.json`
 - `announcements.json`
 - `do_nows.json`

# Todo
 - use a seed to randomly generate seats
 - allow use of url-links in agenda
 - post slides to s3-bucket so they can be viewed as a web-page
 - make streamlet interface so you can run code from anywhere