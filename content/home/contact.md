---
# An instance of the Contact widget.
widget: contact

# This file represents a page section.
headless: true

# Order that this section appears on the page.
weight: 110

title: Contact
subtitle:

content:
  # Automatically link email and phone or display as text?
  autolink: true

  # Email form provider
  form:
    provider: netlify
    formspree:
      id:
    netlify:
      # Enable CAPTCHA challenge to reduce spam?
      captcha: false

  # Contact details (edit or remove options as required)
  email:  songshgeo@bnu.edu.cn
  address:
    street: Xinjiekouwai
    city: Beijing
    region: Haidian District
    postcode: '100875'
    country: China
    country_code: China
  coordinates:
    latitude: '37.4275'
    longitude: '-122.1697'
  # directions: Enter Building 1 and take the stairs to Office 200 on Floor 2
  # office_hours:
  #   - 'Monday 10:00 to 13:00'
  #   - 'Wednesday 09:00 to 10:00'
  appointment_url: 'https://calendly.com/songshgeo'
  contact_links:
    # - icon: twitter
    #   icon_pack: fab
    #   name: DM Me
    #   link: 'https://twitter.com/Twitter'
    # - icon: video
    #   icon_pack: fas
    #   name: Book an academic meeting with me.
    #   link: 'https://calendly.com/songshgeo'

design:
  columns: '2'
---
