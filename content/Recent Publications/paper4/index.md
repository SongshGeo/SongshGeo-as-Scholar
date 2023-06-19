---
title: 'Decreased Virtual Water Outflows from the Yellow River Basin Are Increasingly Critical to China'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - admin
  - Shuai Wang
  - Xutong Wu
  - Yongyuan Huang
  - Bojie Fu

# Author notes (optional)
author_notes:
  - []
  - 'Correspoonding Author'
  - []
  - []
  - []

date: '*2022-03-29T00:00:00Z'
doi: '10.1016/j.jaridenv.2020.104314'

# Schedule page publish date (NOT publication's date).
publishDate: '2022-04-26T00:00:00Z'

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ['2']

# Publication name and optional abbreviated publication name.
publication: In *Hydrology and Earth System Sciences*
publication_short: In *Hydrology and Earth System Sciences*

abstract: Water scarcity is an emerging threat to food security and socio-economic prosperity, and it is crucial to assess crop production response to water scarcity in large river basins. The water footprint, which considers water use in supply chains, provides a powerful tool for assessing the contributions of water resources within a certain region by tracking the volume and structure of virtual water flows. In this study of the structure of the water footprint network from a complexity perspective, we reassessed the significance of water resources for crop services in a large river basin with a severe water shortage – the Yellow River basin (YRB) of China. The temporal increase of the complexity index indicated that the virtual water outflows (VWFs) from the YRB were becoming increasingly critical to China; i.e. the ability of YRB to produce crops boosted the difficulty of its water being replaced by water exporting from other basins. Decomposition of complexity suggested that during the 1980s to 2000s, the temporally increased complexity was due mainly to the lack of competitors and the increasing uniqueness of crops supporting VWFs. This complexity deeply embedded the YRB into the footprints of a water network that facilitated further development with constrained water resources. Still, it also reinforced reliance from other regions on YRB’s scarce water. Based on this analysis, we suggest that resource regulation should be carried out appropriately to ensure ecological sustainability and high-quality development of river basins.

# Summary. An optional shortened abstract.
summary: The temporal increase of the complexity index indicated that the virtual water outflows (VWFs) from the YRB were becoming increasingly critical to China; i.e. the ability of YRB to produce crops boosted the difficulty of its water being replaced by water exporting from other basins. 

tags:
  - social-hydrology
  - water resources management
  - human-water relationship
  - system evolution
  - network analysis
  - Python
  - LaTeX
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
  - project2

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
# slides: example
---

## Brief Introduction

The water footprint and virtual water ([Conference on Priorities for Water Resources Allocation and Management](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx6), [1993](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx6)), a geographically explicit indicator that involves water use in supply chains, has provided a powerful tool for assessing the contribution of water resources to a basin and tracking the transfer of water resources across regions ([Jaramillo and Destouni](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx18), [2015](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx18); [Oki and Kanae](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx29), [2004](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx29)). Virtual water can be associated with specific products that transfer through complex trade relationships between geographic units ([Hoekstra](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx17), [2014](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx17)). Virtual water trade networks consist of virtual water outflows (VWFs) that are embedded in production and consumption trajectories of crops ([Oki and Kanae](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx29), [2004](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx29); [Chini et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx5), [2018](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx5); [Bae and Dall'erba](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx2), [2018](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx2)). For example, the VWF from China's water-rich south to its water-scarce north has been quantified, and the network represented by crop trade between provinces has been mapped ([Zhai et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx42), [2019](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx42); [Zhuo et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx44), [2016](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx44)[a](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx44)). However, because these volume-based studies have ignored the complexity of crop supply and demands (linked with trade) and the uniqueness of each basin (determined by regional characteristics), they have failed to consider the structure of water footprint networks. The structure of a water footprint network reflects the inherent heterogeneity of the distribution of the resources and the pattern of production and consumption. This heterogeneity is consistent with the fact that a water resource cannot be simply replaced by the same volume of water in another basin ([Yu and Ding](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx41), [2021](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx41); [Zhuo et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx44), [2016](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx44)[a](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx44); [Li et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx19), [2020](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx19)). This replacement problem reflects that water is not the only resource needed for widely circulated agricultural products. Because of path dependence, others resources, such as the unique hydrothermal conditions and the status of infrastructure within a basin, all determine the position of the basin (or a region) in a water footprint network ([Best](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx4), [2019](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx4)). Complexity, a rapidly developing concept in fields of study such as complexity science, network science, and development economics, represents the “capacity” that is embedded in a certain region, based on measurement of its position in structural terms ([Hidalgo](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx14), [2021](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx14); [Arthur](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx1), [2021](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx1); [Meng et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx28), [2020](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx28); [Hidalgo et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx16), [2007](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx16)). For water resources that are unevenly distributed geographically, complexity can characterize a basin's overall capacity to provide water services required for national crop production. Because complexity-based metrics have been extensively studied in the empirical assessment of economic vitality through a bipartite-networks approach, the concept of complexity should be taken into consideration in the context of water footprint networks to upgrade the toolbox used for integrated water resources management ([Hidalgo](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx14), [2021](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx14); [Hidalgo and Hausmann](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx15), [2009](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx15); [Liu et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx21), [2017](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx21)). With such a toolbox, the regional significance of the water supply services provided by the basin through agricultural production can be comprehensively reassessed in a way that takes into account structural factors (Fig. [1](https://hess.copernicus.org/articles/26/2035/2022/#Ch1.F1)).


![Methodology abstract](https://hess.copernicus.org/articles/26/2035/2022/hess-26-2035-2022-f01-web.png)
Figure 1 Virtual water transfers between regions through multiple dominant crops. When the proportion of VWF from a region is large enough when considering a specific crop, we establish a connection between the region and the crop. In that way, we abstract region-crop bipartite networks for analysis. Here, we give a more straightforward illustration of our method: (1) illustrating a nation comprised of three regions (A, B, and C) where three types of crops (a, b, and c) can be the productions for supporting virtual water flows (VWFs). Region B does not produce crop a, and region C produces a negligible crop a and 0. (2) When considering VWF volume, it is hard to compare regions A and B, as they support 40 % national total VWF. (3) However, when the structure is involved, their position in region-crop bipartite networks are different, typically in their differences of diversification (N=1), uniqueness (N=2), and competitiveness (N=3) (the parameter N refers to levels of decomposition, detailed interpretation in Sect. 2.4). (4) Therefore, considering both volume (by ignoring eligible VWF crops) and structure, the GENEPY index is a method for distilling information (see Sect. 2.3). Our main results derive from comparisons between indexes of YRB, China, and random networks (as a benchmark). We generated three different null models by shuffling links in different ways, and Table 2 gives them mathematical descriptions.

## Main Results

The total volume of virtual water outflows from the provinces in the YRB decreased continuously during the study period (Fig. [2](https://hess.copernicus.org/articles/26/2035/2022/#Ch1.F2)a), and its proportion of the national total decreased by an even more significant percentage (Fig. [2](https://hess.copernicus.org/articles/26/2035/2022/#Ch1.F2)b). In 1978, there were five provinces in the YRB whose virtual water outflows (VWF) exceeded the national average, but there were only three of them in 2008, and their overall ranking had decreased significantly. Though the total volume, share, and ranking of VWF across provinces of the YRB were all decreasing, the average complexity index of the YRB was holistically higher than that of China (Fig. [3](https://hess.copernicus.org/articles/26/2035/2022/#Ch1.F3)a). The gap between the two increased rapidly after 1985. It reached its widest point in 1993 when the average complexity index of the YRB was about 1.4 times the national average (Fig. [3](https://hess.copernicus.org/articles/26/2035/2022/#Ch1.F3)b). After then, the difference between the two decreased with some fluctuations, but the complexity of the YRB remained about 1.2 times the national average (Fig. [3](https://hess.copernicus.org/articles/26/2035/2022/#Ch1.F3)b).

![Figure 2](https://hess.copernicus.org/articles/26/2035/2022/hess-26-2035-2022-f02-web.png)
**Figure 2**Virtual water outflows (VWFs) of the Yellow River basin (YRB) changes from 1978 to 2008. **(a)** Total VWF in the YRB and China. **(b)** Proportion of total VWF in the YRB to the national volume. **(c)** Ranking of VWF in Chinese provinces in 1978. Blue bars are provinces in the YRB. **(d)** Ranking of VWF in Chinese provinces in 2008. Blue bars are provinces in the YRB.


![Main result](https://hess.copernicus.org/articles/26/2035/2022/hess-26-2035-2022-f03-web.png)
Figure 3 (a) Average complexity index of YRB and of China from 1978 to 2008. (b) Ratios of average complexity index of YRB to
that of China from 1978 to 2008. The solid line was fitted with generalized additive models (GAMs). The grey shaded area
indicates a 90 % confidence interval. The red dashed line indicates the baseline where the average complexity index of the
is YRB is equal to that of China.

## Discussion: reasons of changing complexity

The use of regional VWF, especially within a water footprint network, has been a common approach to assess the importance of water resources, but complex structures have not been comprehensively evaluated in these assessments ([Mekonnen and Hoekstra](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx27), [2020](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx27), [2011](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx25); [Fang et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx10), [2014](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx10)). The Yellow River, an agriculture-oriented basin with substantial heterogeneity in the upper, middle, and lower reaches, has scarce water resources that are the cornerstone of its crop production ([Wang et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx35), [2019](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx35)). With “The Reform and Opening” of China since 1978, domestic crop trades have gradually increased both in diversity and the volume, and that increase may have caused the total VWF volume to keep increasing. At the same time, however, the YRB was the first basin to apply a water allocation scheme because extreme water shortages caused the river to frequently dry after the 1970s ([Wang et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx35), [2019](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx35)). Therefore, during the time that the national VWF was transferred mainly from the north (where the YRB is located) to the south ([Zhuo et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx45), [2016](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx45)[b](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx45)), the contribution of the YRB, which is deficient in water resources, decreased in volume (Fig. [2](https://hess.copernicus.org/articles/26/2035/2022/#Ch1.F2)). 

However, considering the structure of the crop–water footprint bipartite network, that did not indicate the YRB had been decreasing in importance to China. On the contrary, our complexity-based analysis revealed the differences in complexity between the YRB and China since 1978. As a result, the YRB's water footprints have been complex for other basins to replace crop production. Our decomposition results suggested that this difficulty was due mainly to a low number of competitors and the increasing uniqueness of crops supporting VWF from the YRB. The Yellow River is a large river that crosses an arid, semi-arid, and monsoon climate zone. The small number of competitors and the relatively high uniqueness of the YRB depend partially on the unique geographical conditions in the YRB ([Fu et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx11), [2017](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx11)). For example, high-quality apples produced in the fertile but arid Loess Plateau in the middle reaches of the YRB and the wet areas in the lower reaches together account for more than 90 % of the total apple production in China regions, which can compete with the YRB. The increasing uniqueness of the YRB means that its ability to improve the quality of its agricultural products and push competitors out of the crop supply network is growing. Those regions that can compete with a particular crop from the YRB (such as Xinjiang, which also exports many high-quality apples) are limited by an extreme shortage of water resources and cannot increase diversification, hence lacking overall competitiveness. 

## Discussion: future applications of Virtual water complexity

Assessing the value of natural resources has been a constant problem because of the trade-off between economic efficiency, social equity, and resource availability ([Dalin et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx7), [2015](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx7); [Grafton et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx13), [2018](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx13); [Yoon et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx40), [2021](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx40)). The “Porter hypothesis” of the environment has proposed that environmental regulation can stimulate technological innovation. Similarly, the stimulus of resource scarcity can improve optimization of a market allocation for efficient use of resources ([Wagner](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx33), [2004](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx33); [Luptáčik](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx24), [2010](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx24)). The complexity of the YRB had risen above the national average since about 1987, when the river basin was regulated. Because of water scarcity, the Chinese government required provinces to adhere to strict resource quotas ([Wang et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx34), [2018](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx34)). During this period, although the total VWF of the YRB and its proportion decreased, the increasing complexity indicated that the resource-constrained YRB was gaining market advantages. In different ways, this advantage has manifested itself as an increase of the position of the YRB in the virtual water network and by an increase of both competitiveness and uniqueness (Fig. [4](https://hess.copernicus.org/articles/26/2035/2022/#Ch1.F4)) ([Fang and Chen](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx9), [2015](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx9); [Fang et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx10), [2014](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx10); [Yang et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx39), [2012](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx39)). After the 1990s, the complexity index of China evidenced a similar trend of improvement, which was concomitant with the period when the strict control of water resources and a transformation to water conservation were implemented throughout the whole country ([Zhou et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx43), [2020](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx43); [Liu and Yang](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx20), [2012](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx20)). 

According to the literature ([Zhou et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx43), [2020](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx43)), the slowdown of the growth of China's water consumption can be divided into two stages by the 1990s. While growth during the earlier period occurred mainly in arid and semi-arid areas (e.g. the YRB), growth during the latter period affected the whole country. Therefore, the increase of the national average level of complexity lagged behind that of the YRB. This lag was probably the result of the rest of China pursuing structural advantages later than the YRB. Traditional development economic theory points out that the use of resources with comparative advantage is a prerequisite for producing an economically efficient division of labour and a marketing network ([Hidalgo and Hausmann](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx15), [2009](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx15)). In this case, however, before water resources are severely restricted, it may not be more cost-effective to intensify a comparative advantage than to expand resource investment. This conclusion is consistent with the theories related to the “peak water use” and the “efficiency paradox” ([Gleick and Palaniappan](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx12), [2010](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx12); [Grafton et al.](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx13), [2018](https://hess.copernicus.org/articles/26/2035/2022/#bib1.bibx13)). Thus, the complexity index may depict the process by which the YRB and then China pursued this structural advantage within the water footprint network as constrained by resources.

## Conclusion
This paper took the structure of the water footprint network from a complexity perspective. It assessed the significance of water resources for crop services in a large river basin with a severe water shortage – the Yellow River basin (YRB). From 1978 to 2008, the number of virtual water flows (VWFs) from the YRB and its percentage of the total VWF from the national total decreased significantly. The fact that the YRB has lagged behind the national VWF trend is probably related to restricted water use policies. However, our results showed that the complexity of the YRB increased and was significantly higher than the national average during the period from the 1980s to the 2000s. Decomposition of complexity suggested that this pattern was due mainly to few competitors and the increasing uniqueness of supporting VWF crops for the YRB. Based on an assessment of water conservation policies in China, we suggested that the initial promulgation of resource regulations was the key to a competitiveness-oriented transformation for crop production in the YRB. Subsequently, the increased complexity enabled the YRB to develop with limited water resources. However, it also more deeply embedded the YRB into water footprint networks where scarce water cannot be easily replaced. From the complexity analysis, we point out that resource regulation should be carried out at an appropriate stage to ensure ecological sustainability and high-quality development of river basins.

## Related
[Post: Plain introduction: Complexity, another dimension of virtual water]()
<!-- 
{{% callout note %}}
Click the _Cite_ button above to demo the feature to enable visitors to import publication metadata into their reference management software.
{{% /callout %}}

{{% callout note %}}
Create your slides in Markdown - click the _Slides_ button to check out the example.
{{% /callout %}}

Supplementary notes can be added here, including [code, math, and images](https://wowchemy.com/docs/writing-markdown-latex/). -->
