# andrewarrow.dev

## Lessons

Lesson content lives in `lesson-NNNNN/content.html`. Shared document markup is
in `templates/lessons/header.html` and `templates/lessons/footer.html`.
Edit these source files rather than the generated `index.html` files.

Build the checked-in static lesson pages with:

```sh
python3 scripts/build-lessons.py
```

Commit the source changes and regenerated `lesson-NNNNN/index.html` files
together. Hosting continues to serve the generated HTML directly.

Check whether generated pages are current without changing files:

```sh
python3 scripts/build-lessons.py --check
```

To add a lesson, create the next `lesson-NNNNN` folder, copy the previous
lesson's `content.html`, update its lesson label and back link, and update the
new and previous lessons' next links. Keep lesson images beside the corresponding
`content.html`, then run the build command.
