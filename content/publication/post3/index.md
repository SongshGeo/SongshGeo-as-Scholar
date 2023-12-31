---
title: 'Post: SES structures and outcomes'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - admin
  # - Shuai Wang
  # - Bojie Fu
  # - Yuxiang Dong
  # - Yanxu Liu
  # - Haibin Chen
  # - Yaping Wang

# Author notes (optional)
author_notes:
  - []
  # - 'Correspoonding Author'
  # - []
  # - []
  # - []
  # - []
  # - []

date: '2020-12-13T00:00:00Z'
# doi: '10.1111/jfr3.12679'

# Schedule page publish date (NOT publication's date).
# publishDate: '2020-12-13T00:00:00Z'

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
# publication_types: ['2']

# Publication name and optional abbreviated publication name.
# publication: In *Journal of Flood Risk Management*
# publication_short: In *Journal of Flood Risk Management*

abstract: 'Ostrom, (née Awan; August 7, 1933 – June 12, 2012) an American political economist, proposed perhaps the most popular framework for understanding coupled human and natural systems:Social-ecological System (SES). However, decades ago, a lot of works still should be addresssed in building causal association between its strucutures and outcomes.'

# Summary. An optional shortened abstract.
summary: Ostrom, (née Awan; August 7, 1933 – June 12, 2012) an American political economist, proposed perhaps the most popular framework for understanding coupled human and natural systems:Social-ecological System (SES). However, decades ago, a lot of works still should be addresssed in building causal association between its strucutures and outcomes.

tags: 


# Display this page in the Featured widget?
featured: true

# Custom links (uncomment lines below)
# links:
# - name: Custom Link
#   url: http://example.org

url_pdf: ''
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
image:
  caption: ''
  focal_point: ''
  preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects:
  - []

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
# slides: example
---
<!-- 
{{% callout note %}}
Click the _Cite_ button above to demo the feature to enable visitors to import publication metadata into their reference management software.
{{% /callout %}}

{{% callout note %}}
Create your slides in Markdown - click the _Slides_ button to check out the example.
{{% /callout %}} -->

## Linking social-ecological systems' structure and outcome
According to Ostrom's interpretation, interactions between Governance, Actors, Resources Systems and Resource Units consists a coherent structure of SESs, where human activities -especially governance practices, changes the system's outcomes a lot (@ostrom2008). From this point, a batch of researches had demonstrated that some "matched" structures can lead to more sustainable outcomes (such as resources consuming habits), while others usually lead to depletion. 

Since actors and resources units are portrayed as nodes, linkages as edges, network analysis is a widespread methodology to depict the difference. A series of research led by [Bodin at Stockholm Resilience Centre (SRC)](https://www.stockholmresilience.org/meet-our-team/staff/2008-01-11-bodin.html) tried to dive into this of general analysis. However, there are only still correlation-based links between structures and outocomes of SES, but few "dynamic process" of network involved. Here, I proposed a further quantitative analysis to fill this knowledge gap by introducing a causal inference method called "Differenced Synthetic Control" into such network analysis.

We focus on a type of "common-pool resources" (difficult to exclude other users from using resource, but prone to influence other when using it by self -in term: LOW Excludability but HIGH externality): WATER. 

![CleanShot2022-08-14at06.23.14](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/CleanShot%202022-08-14%20at%2006.23.14.png)
Figure 1. Framework for understanding linkages between SES structures and outcomes. a. In the general framework for analyzing social- ecological systems (SESs), (Adapted from Ostrom, 2008). Institutional shifts can change interactions within the SES and reframe the structures. b. We aim to investigate causal links between matched/mismatched SES structures and their corresponding outcomes.


## Governing water: how could institution change SES structure then lead to diff outcomes?
Widespread freshwater scarcity and overuse challenge the sustainability of large river basins, resulting in systematic risks to economies, societies, and ecosystems globally. In the context of future climate change, the gap between supply and demand for water resources in large river basins is expected to become increasingly more prominent. Those river basin systems successfully supporting sustainable water resource use are structurally well-aligned with water provisioning and social-ecological demands, without inefficient competition or overuses. 

For governing river basin systems, their SES structures can by be reshaped by institutions, such as policies, laws, and norms. Representing all relative governance practices, institutions include interplays between social or actors, ecological units, or between social and ecological system elements. Understanding how these complex interplays are crucial for developing strategies to effectively manage natural resources and enhance the resilience of social-ecological systems. Effective ("matched" or "fit") institutions operate at appropriate spatial, temporal, and functional scales to manage and balance different relationships and interactions between human and water systems, supporting (but not guaranteeing) the sustainability of SES (Figure 1 a). 

Some institutional advances have had desirable water governance outcomes e.g., the Ecological Water Diversion Project in Heihe River Basin, China, and collaborative water governance systems in Europe). However, imposing institutional changes on : large, complex river basin mav create or destroy hundreds of connections between social agents and ecological units. where matched social-ecological structures not ubiquitous. Two particular weaknesses in existing knowledge of institutional matches include understanding (Figure 1 b): (i) the causal links between SES structures and outcomes; (ii) details of the underlying processes, and especially the coordination of the incentives of different participants, that result from an institutional lack of matches. These weaknesses limit understanding of institutional design and hinder approaches toward institutional matches for improving the sustainability of river basin systems.

## My Informative Case-study: Institutional shifts in the Yellow River Basin

To fill the above knowledge gap, we select the Yellow River Basin (YRB) in China as a typical case study to quantitatively measure the effects of SES structures changing because it is one of the most anthropogenically altered large river basins. Under different water allocation institutions, its streamflow was first overdrawn, then dried up, and finally has been successfully restored. We focused on two institutional shifts, the Water Allocation Scheme that began in 1987 (87-WAS) and the Unified Basinal Regulation that took over in 1998 (98-UBR), which re-framed different SES structures. 

We conduct counterfactual identification on the effect of these institutional shifts, our results suggested that during the decade following the introduction of the 87-WAS, observed water use of the YRB increased by 8.57% more than expected, while 98-UBR ultimately decreased total water use. Furthermore, these heterogeneous effects of water use responses to SES structures aligned with our further theoretical marginal benefits analysis, supporting the hypothesis that SES structural changes played a vital role in sustainable water use. This quasi- natural experiment on the YRB offers profound insights into the links between SESs structures and outcomes, suggesting that fragmented ecological units linked to separated social actors should be avoided for sustainability.

![CleanShot2022-08-14at07.08.51](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/CleanShot%202022-08-14%20at%2007.08.51.png)

Full article accessible: 

