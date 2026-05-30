---
# Fieldwork home strip — renders cards from content/en/fieldwork/*/index.md.
# To add a story: drop a featured.jpg into a new folder under content/en/fieldwork/
# and create an index.md with title / summary / date / location frontmatter.
widget: blank
headless: true
active: false

weight: 85

title: Fieldwork
subtitle: Modelling is only half the work.

design:
  columns: '1'
---

{{< fieldwork-gallery sort="date" order="desc" resize="900x900" >}}
