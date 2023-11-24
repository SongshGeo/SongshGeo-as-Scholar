---
title: 'Decoupling of SDGs followed by re-coupling as sustainable development progresses'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - Xutong Wu
  - Bojie Fu
  - Shuai Wang
  - admin
  - Yingjie Li
  - Zhenci Xu
  - Yongping Wei
  - Jianguo Liu

# Author notes (optional)
author_notes:
  - []
  - 'Correspoonding Author'
  - []
  - []
  - []
  - []
  - []
  - []

date: '2022-02-22T00:00:00Z'
doi: '10.1016/j.jaridenv.2020.104314'

# Schedule page publish date (NOT publication's date).
publishDate: '2022-03-24T00:00:00Z'

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ['2']

# Publication name and optional abbreviated publication name.
publication: In *Nature Sustainability*
publication_short: In *Nature Sustainability*

abstract: In the context of global change, the community, as the basic unit of a social-ecological system, is facing both potential or existing shocks and trends in the structure and function of the system. Community-based adaptation (CBA) provides an effective way for communities to mitigate change and even seize the opportunity for transformation. In order to understand the mechanisms of current CBA adaptation pathways, a review of research on CBA over the past 20 years is presented. In the CBA process, funding agencies, rights agencies, research institutions and implementers are the agents engaged in action. The objects to which the adaptation agents adapt have shocking first-order impacts as well as concomitant second-order impacts. The adaptation pathway has a hierarchy, which corresponds to the eight steps of clarifying adaptation objects, liquidating adaptation assets, assessing adaptation capabilities, clarifying adaptation needs, setting adaptation purposes, dividing adaptation stages, designing adaptation measures, and implementing adaptation measures. The negative effects of physical, resource and social barriers can induce maladaptation. Thus, we propose a prospective direction for optimizing community-based adaptation, including improving monitoring and evaluation systems to build an indicator framework for long-term community adaptation, using social-ecological networks as a tool to strengthen multiple-agent decision making, and promoting nature-based solutions to enhance social-ecological system adaptation.

# Summary. An optional shortened abstract.
summary: SDG interactions showed nonlinear changes as the SDG Index increased:SDGs were both more positively and more negatively connected at low and high sustainable development levels, but they were clustered into more isolated positive connection groups at middle levels. 


tags: 
  - system evolution
  - sustainability
  - GIS
  - R
  - Data analysis

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

## Brief introduction

为了应对人类面临的贫困、不平等、气候变化、环境退化等全球挑战，联合国于2015年通过了17项可持续发展目标（SDGs），涵盖经济、社会、环境3个维度，是实现所有人更美好和更可持续未来的蓝图。SDGs间存在广泛的相互关联，一项目标的实现可能对其他目标产生正面促进（协同关系）或负面影响（权衡关系）。因此，理解SDGs间复杂的相互作用关系是全面实现SDGs的关键。当前研究主要关注不同SDGs之间的权衡协同关系、不同SDGs的相对重要程度以及不同类型国家SDGs相互作用的差异。关于SDGs相互作用的动态变化，特别是其如何随可持续发展进程变化的研究仍非常有限。

针对这一研究局限，傅伯杰院士团队应用网络分析方法，基于《可持续发展报告2020》发布的166个国家的SDGs数据，沿SDG指数梯度建立SDGs相互作用网络，进而分析相关网络指标、网络关键节点以及协同网络中SDGs聚类随可持续发展进程的变化，试图回答以下问题：（1）随着可持续发展水平的提高，SDGs相互作用是否变化以及如何变化？（2）哪些SDGs与其他SDGs更相关，其联系如何随可持续发展水平变化？（3）哪些SDGs倾向于共同实现，这些聚类如何随可持续发展水平变化？

In order to address the global challenges facing humanity, such as poverty, inequality, climate change and environmental degradation, the United Nations adopted 17 Sustainable Development Goals (SDGs) in 2015, covering three dimensions - economic, social and environmental - as a blueprint for a better and more sustainable future for all. (synergies) or negatively (trade-offs). Understanding the complex interactions between the SDGs is therefore key to the full realisation of the SDGs. Current research has focused on the trade-off synergies between different SDGs, the relative importance of different SDGs and the differences in SDG interactions between different types of countries. Research on the dynamics of SDG interactions, especially how they change with the sustainable development process, is still very limited.

To address this research limitation, Academician Fu Bojie's team applied network analysis methods to build SDGs interaction networks along the SDG index gradient based on the SDGs data of 166 countries published in the Sustainable Development Report 2020, and then analysed the changes of relevant network indicators, network key nodes and SDGs clustering in the synergistic network with the sustainable development process, in an attempt to answer the following questions: ( (1) Do SDG interactions change as the level of sustainable development increases and how do they change? (2) Which SDGs are more relevant to other SDGs, and how do their linkages change with the level of sustainable development? (3) Which SDGs tend to be jointly achieved and how do these clusters change with the level of sustainable development?

## Main results

研究表明，随着可持续发展整体水平的提高，SDGs相互作用发生非线性变化，不同目标先解耦又重新耦合：在较低和较高的可持续发展水平上，SDGs之间的正负相关关系均较紧密，但在中等可持续发展水平上，相关关系较少，SDGs聚集成更孤立的正相关模块（图1）。

The study shows that as the overall level of sustainable development increases, the SDGs interact in a non-linear way, with the different goals first decoupling and then recoupling: at both lower and higher levels of sustainable development, the positive and negative correlations between the SDGs are stronger, but at medium levels of sustainable development, there are fewer correlations and the SDGs cluster into more isolated modules of positive correlation (Figure 1).

![Figure 1](https://mmbiz.qpic.cn/sz_mmbiz_jpg/VibcXcibPAUA5EGkF76GklMib3z9nBLEROzAGLRyVPaphl4MfccuOPOVddrtjuKTqAa8HV13UoMAM3wgzyE2Blqsw/640?wx_fmt=jpeg&wxfrom=5&wx_lazy=1&wx_co=1)
图1 网络指标及其随可持续发展水平的变化
Figure 1. Network indicators and their change with sustainable development level

  在SDGs相互作用非线性变化过程中，各SDGs在相互作用网络中的重要程度发生变化（图2）。在协同网络中，SDG 3“良好健康与福祉”、SDG 9“产业、创新和基础设施”、SDG 16“和平、正义与强大机构”和SDG 6“清洁饮水和卫生设施”一直起相对主导作用；SDG 4“优质教育”、SDG 1“无贫穷”和SDG 7“经济适用的清洁能源”在低可持续发展水平上较为重要；而SDG 8“体面工作和经济增长”和SDG 5“性别平等”在高可持续发展水平上较为重要。在权衡网络中，SDG 12“负责任消费和生产”和SDG 13“气候行动”通常与其他SDGs存在权衡，特别是在高可持续发展水平上；而SDG 15“陆地生物”以及SDG 14“水下生物”在低可持续发展水平上与其他SDGs负向联系较多。

  The importance of each SDG in the network of interactions changes during the process of non-linear changes in SDG interactions (Figure 2). Within the synergistic network, SDG 3 'good health and well-being', SDG 9 'industry, innovation and infrastructure', SDG 16 'peace, justice and strong institutions' and SDG 6 'Clean Water and Sanitation' has been relatively dominant; SDG 4 'Quality Education', SDG 1 'Poverty Free' and SDG 7 'Affordable and Clean Energy' have been relatively dominant. "SDG 4 'quality education', SDG 1 'no poverty' and SDG 7 'affordable and clean energy' are more important at lower levels of sustainable development; while SDG 8 'decent work and economic growth' and SDG 5 'gender equality' are more important at higher levels of sustainable development. Development" are more important at high levels of sustainability. In the trade-off network, SDG 12 'responsible consumption and production' and SDG 13 'climate action' generally have trade-offs with other SDGs, especially at high sustainable development levels, while SDG 15 'terrestrial biology' and SDG 13 'climate action' are more important at high sustainable development levels. terrestrial organisms' and SDG 14 'underwater organisms' are more negatively associated with other SDGs at lower levels of sustainability.

  
![Figure 2](https://mmbiz.qpic.cn/sz_mmbiz_jpg/VibcXcibPAUA5EGkF76GklMib3z9nBLEROzTQ9oWJ4T6edqAibPm7KYGAialNy5COgfIhRc40argDapn540StGjZzqA/640?wx_fmt=jpeg&wxfrom=5&wx_lazy=1&wx_co=1)

图2 各SDGs连通性随可持续发展水平的变化
Figure 2 Changes in connectivity across SDGs with level of sustainability

协同网络中SDGs聚类随可持续发展水平的变化也反映了SDGs先解耦又重新耦合的过程（图3）。根据目标之间的正向联系，17项SDGs在低可持续发展水平上可以分为3个聚类模块，分别体现了社会经济SDGs、环境SDGs和SDG 17“促进目标实现的伙伴关系”。随着可持续发展水平的提高，这些模块分裂成更多更小的模块，网络的模块度增加。而在高可持续发展水平上，13个SDGs重新聚合成更大的模块，只剩下SDG 14、SDG 17、SDGs 12和13与之分离。  

The change in the clustering of SDGs in the synergistic network with the level of sustainable development also reflects the process of first decoupling and then recoupling of SDGs (Figure 3). Based on the positive linkages between the goals, the 17 SDGs can be grouped into three clusters at low sustainable development levels, reflecting the socio-economic SDGs, environmental SDGs and SDG 17 'partnerships for goal achievement' respectively. As the level of sustainability increases, these modules split into more and smaller modules and the modularity of the network increases. At higher levels of sustainability, the 13 SDGs regroup into larger modules, leaving only SDG 14, SDG 17, SDGs 12 and 13 separate from them.  

![Figure 3](https://mmbiz.qpic.cn/sz_mmbiz_jpg/VibcXcibPAUA5EGkF76GklMib3z9nBLEROzfFxpM9WhVcHiaibNxOdicGGCNpBbIkEdibeWlX0K1tat6LFJY0y794In8w/640?wx_fmt=jpeg&wxfrom=5&wx_lazy=1&wx_co=1)

  

图3 协同网络中SDGs聚类随可持续发展水平的变化
Figure 3 Changes in clustering of SDGs in the synergistic network with the level of sustainable development

## Discussion
研究通过揭示SDGs相互作用随可持续发展进程的非线性变化，可以确定可持续发展的关键转型阶段，明确不同可持续发展水平的国家所面临的机遇和挑战，在深入理解可持续发展进程的基础上，为不同发展阶段的国家指明具体的行动方向，以在2030年前实现尽可能多的SDGs。研究强调分析SDGs相互作用动态变化的必要性，也为在不同尺度下开展相关研究奠定了基础。

By revealing the non-linear changes in SDGs interactions with the sustainable development process, the study can identify key transitional stages of sustainable development, clarify the opportunities and challenges faced by countries at different levels of sustainable development, and point to specific directions of action for countries at different stages of development to achieve as many SDGs as possible by 2030, based on a deeper understanding of the sustainable development process. The study emphasises the need to analyse the dynamics of SDGs interactions and also provides the basis for relevant research at different scales.

## Related

<!-- {{% callout note %}}
Click the _Cite_ button above to demo the feature to enable visitors to import publication metadata into their reference management software.
{{% /callout %}}

{{% callout note %}}
Create your slides in Markdown - click the _Slides_ button to check out the example.
{{% /callout %}}

Supplementary notes can be added here, including [code, math, and images](https://wowchemy.com/docs/writing-markdown-latex/). -->
