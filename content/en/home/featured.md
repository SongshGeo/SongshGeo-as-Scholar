---
# Publications — portfolio widget with filter buttons
# Tags `first-author` / `co-author` / `corresponding-author` / `recent`
# are populated by `scripts/auto_tag_publications.py`.
widget: portfolio
headless: true
active: true

# Order that this section appears on the page.
weight: 70

title: Publications
subtitle: ''

content:
  page_type: publication
  filter_default: 0

  filter_button:
    - name: All
      tag: '*'
    - name: Leading
      tag: role-leading
    - name: Featured
      tag: role-featured
    - name: Co-authored
      tag: role-co-authored

design:
  columns: '2'
  # 4 = Citation (publication only) — APA-style bibliographic list, tidiest for an academic CV
  view: 4
  flip_alt_rows: false
---
