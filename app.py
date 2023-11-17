# Libs & Funcs -------------------------------------------------------------------------------------------------------------------------- #
#
import streamlit as st
st.set_page_config( layout = 'wide' )

import openai
from openai import OpenAI
import os
import re
import ast
import json
import pandas as pd

secret_key = os.getenv('secret_key')

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = os.getenv('api_key')
)

# from kotan import KoTAN

# Check if 'translator' is not already set in session state
# if 'translator' not in st.session_state:
#     # If not, show a spinner and load the translator
#     with st.spinner('_작업에 필요한 구성요소들을 불러오고 있는 중입니다..._'):
#         st.session_state.translator = KoTAN(task="mt",
#                                             tgt="ko",
#                                             level="fine",
#                                             style="formal")

secret_key = "movefast"

# --- #

def summary_gpt(user_input):
    summary_prompt = \
    """// ROLE AND TASK
    As an experienced journalist fluent in English, you are tasked with composing a news briefing that authentically captures the essence of journalistic style.

    // WRITING STYLE
    - Implement the use of formal language, specifically mirroring the expressions and words observed in reputable newspapers.

    // Step-by-Step Guide
    1 - Identify the main issue: Craft a concise and impactful title that summarizes the most significant aspect of the news story. It should capture the essence of the content and include key details such as statistics, events, or notable figures.

    2 - Identify the 3 key points and generate corresponding subtitles: The 3 subtitles must be carefully selected to guide the reader through varying facets of the news topic. They provide structure to the information, allowing readers to quickly understand key aspects without needing to read in full detail. These 3 subtitles must be based on the principle of informative progression, capturing the main event, detailed insights, and broader context. Each subtitle should be highly relevant and succinct, summarizing the forthcoming section efficiently. Always select the most significant and newsworthy aspects to shape these key statements, ensuring the briefing remains focused and impactful.

    3 - Write The first Subtitle: Introduce the main focus or announcement related to the topic. This should be the leading piece of information that sets the stage for the rest of the briefing.

    4 - Write the Content of the first Subtitle: Provide bullet points with additional details, supporting statistics, or contextual information that expand upon the subtitle. Each bullet point should offer a piece of evidence or a specific fact that reinforces the main point.

    5 - Write The second Subtitle: Present a related consequence, subsequent development, anticipatory projection, or a secondary angle of the main subject. This should build upon the information provided in the first paragraph.

    6 - Write Content of the second Subtitle: Elaborate on the subtitle with bullet points that give evidence, specific examples, or further implications. These should deepen the reader's understanding of the secondary aspect of the topic.

    7 - Write The Third Subtitle: Offer a further dimension, a humanizing angle, potential outcomes, or additional perspectives on the issue. This should provide a comprehensive view of the subject matter.

    8 - Write Content of Third Subtitle: Delve into the elements or opinions introduced in the subtitle with bullet points. Include forecasts, expert opinions, potential solutions, or social implications to conclude the briefing with a broadened perspective.

    9 - Ensure that each section is clearly marked with the appropriate subtitle and that the bullet points under each subtitle are informative and relevant to the overarching topic.
    ```

    // STRUCTURE
    Your summary must be structured as follows:
    ```
    <Title reflecting the main news topic>

    ☐ <Subtitle summarizing the first key aspect of the news>
    - <A fact or statement providing detail on the first aspect>
    - <Another fact or statement providing additional detail on the first aspect>
    - <A third fact or statement providing further detail on the first aspect>

    ☐ <Subtitle summarizing the second key aspect of the news>
    - <A fact or statement providing detail on the second aspect>
    - <Another fact or statement providing additional detail on the second aspect>
    - <A third fact or statement providing further detail on the second aspect>

    ☐ <Subtitle summarizing the third key aspect of the news>
    - <A fact or statement providing detail on the third aspect>
    - <Another fact or statement providing additional detail on the third aspect>
    - <A third fact or statement providing further detail on the third aspect>
    ```

    // CAUTION
    Do not add anything from your own knowledge.
    Stick to the facts of the given news article.

    It is very important that you identify the 3 main subjects from the text, which will be marked with "☐ " as subtitles. Break down the given article into digestible parts, guiding the reader through the logical progression of why an event is significant (first subtitle), what are its broader implications or subsequent developments (second subtitle), and broader perspectives or additional details that round out the narrative (third subtitle).

    Answer in a consistent style.
    """

    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {
          "role": "system",
          "content": summary_prompt
        },
        {
          "role": "user",
          "content": "High Court rejects last legal challenge to Netanyahu staying PM\nAll three justices hinted that making a ruling now is premature, and will only become relevant once Netanyahu's candidacy to form a government is presented to President Reuven Rivlin.\nThe High Court of Justice rejected the last remaining legal challenge to Benjamin Netanyahu remaining prime minister, following his indictment for bribery on November 21.\nAs a result, Netanyahu will remain prime minister at least until March 2 and could potentially continue afterward, even at such point as his trial for bribery begins.\nThe Likud responded that the court was right to reject the petition, because “in a democracy, only the people decide who will lead them.”\nBlue and White leader Benny Gantz also praised the verdict, saying it was the correct decision and “Netanyahu must be defeated in the court of public opinion in the ballot box.”\nTechnically, the court only ordered the petition withdrawn and did not reject it fully, leaving the door open to disqualifying Netanyahu post-election.\nBut in practical terms, and from the tone of the ruling, the court has made it clear it wants no part in forcing Netanyahu out of office any earlier than at a point where the law demands this unambiguously, leaving the question of who leads the country to the voters.\nBefore and after Attorney-General Avichai Mandelblit’s November 21 decision to issue an indictment against Netanyahu, there was high speculation that the High Court might fire the prime minister, on the basis of its two-decade precedent in which all indicted ministers have been obligated to resign.\nOn the basis of those two decades of judicial rulings, around 70 hi-tech officials petitioned the High Court to fire Netanyahu before the election, or at least determine his status, so voters would know whether he could form the next government after the March 2 election.\nThe petitioners said that the question was about the right of the voters to know whether one of the two candidates for prime minister was eligible or not. However, the court was persuaded by Mandelblit’s office that elections themselves are extremely uncertain, and that the process of political parties recommending a candidate for prime minister was also uncertain.\nIn light of these uncertainties, and due to the strong possibility that Netanyahu may never be able to get 61 MKs to support him, the court said it should not step in prematurely to strike down his candidacy, needlessly angering significant portions of the country who support him. “The election period is a politically sensitive time, so it is fitting to act with heavy restraint…this is in light of the most complex and sensitive period without historical precedent within which the State Israel currently finds itself,” wrote the court.\nAt the same time, the court rejected technical arguments by Netanyahu’s lawyers and by the Likud party, saying that it did not even have the theoretical jurisdiction to decide Netanyahu’s status. Rather, the court said that it was empowered to decide Netanyahu’s status, and was merely declining to do so at this time.\nThe court had heard oral arguments on the issue on Tuesday.\nAlthough the High Court announced that it would decide on the matter at a later point, the overall feel of the justices’ questions to the lawyers was that they would very much prefer to stay out of the issue. Chief Justice Esther Hayut, her deputy Justice Hanan Melcer and Justice Uzi Vogelman conducted the hearing.\nAround 70 hi-tech officials had requested the court rule on Netanyahu’s eligibility to form a government before the upcoming March 2 election, mainly due to the charge of bribery which he faces in Case 4000 – also known as the “Bezeq-Walla Affair.”\nDuring the hearing, lawyers for the petitioners said the High Court had set a clear precedent when it forced Arye Deri to resign as minister upon indictment for bribery 20 years ago and the precedent demands that the court do the same in Netanyahu’s case.\nAll three justices hinted that making a ruling now is premature and will only become relevant once Netanyahu’s candidacy to form a government is presented to President Reuven Rivlin following the upcoming election in March.\nThey hammered the petitioners’ lawyer, Daphna Holech-Lechner, to give them an example where the courts had been asked to make a preelection declaratory statement about the status of a candidate before there was an explicit legal obligation to do so."
        },
        {
          "role": "assistant",
          "content": "Israeli Supreme Court puts Netanyahu's eligibility to serve as prime minister on hold\n\n☐ On January 2, Israel's Supreme Court ruled that it is \"premature\" to determine whether Prime Minister Benjamin Netanyahu is eligible to form the next government at this time, putting on hold a hearing on his eligibility to serve as prime minister. \n- In its decision, the Supreme Court noted that the election period is a \"zone of uncertainty\" and that the need for a ruling will depend largely on which candidate comes out on top in the general election. \n- In November 2019, Israeli prosecutors indicted Mr. Netanyahu on charges of bribery, fraud, and embezzlement. \n\nAs a result of the ruling, Netanyahu's trial for his alleged crimes will be delayed until at least March 2020, when early elections will be held. \n- Netanyahu's Likud party supported the ruling, stating that \"in a democracy, the people decide who their leaders are,\" while his rival Blue and White party said that \"Netanyahu should be ousted through an election, not a court ruling.\"\n- Some observers noted that the Israeli Supreme Court avoided a potential confrontation between the Israeli government and the judiciary with this decision. \n\nOn January 1, Netanyahu asked the Knesset for immunity. \n- In a televised address, Netanyahu explained that \"my request for immunity is in accordance with the law and serves the purpose of protecting you and the future of Israel.\" \n- Under Israeli law, Israeli lawmakers are not automatically granted immunity, but can request it if they are implicated."
        },
        {
          "role": "user",
          "content": "IMF predicts Lithuania’s economy contracting 1.4% this year\nThe International Monetary Fund (IMF) forecasts that Lithuania’s economy will contract 1.4 percent this year before growing 2.9 percent in 2024, the Bank of Lithuania said on Tuesday. \n\nAccording to IMF forecasts, the country’s GDP should grow by 2.7 percent in 2025, 2.5 percent in 2026, 2.2 percent in 2027, and 2.1 percent in 2028.\n\nBorja Gracia, the IMF mission chief for Lithuania, predicted in June that the country’s economy would contract by 1.4 percent on average this year, while next year, GDP growth should reach the pace of between 2.5 and 3 percent.\n\nThe IMF now expects Lithuania’s annual inflation to decelerate to 4.1 percent by the end of this year, from 6.4 percent in August, and ease further to 3 percent in late 2024. The Fund sees the annual inflation rate reaching 2.9 percent in late 2025 and averaging 2.5 percent in 2026-2028.\n\nAs estimated by the IMF, the unemployment rate in Lithuania should reach 7.8 percent this year before going down to 6.7 percent in 2024, easing further to 6.2 percent in 2025, and reaching 6 percent in 2026–2028.\n\nAccording to Gediminas Šimkus, board chairman of the Bank of Lithuania, the country’s economic resilience is underpinned by a robust labour market, relatively low private sector indebtedness and recovering real income of households, as well as significant corporate and bank reserves.\n\n“However, we do not have the luxury of time: all institutions need to focus on measures ensuring that Lithuania’s economic growth is sustained. We see risks to economic growth and financial stability in the context of persistent uncertainty, which is mostly linked to Russia’s war against Ukraine,” he is quoted in a press release from the central bank.\n\nAccording to the IMF, the biggest risk to Lithuania’s economy is the scenario where inflation in the country remains significantly higher than the euro area average (at 5.3 percent in August) over a longer period of time, as this would reduce both domestic and foreign demand due to negative effects on competitiveness.\n\nMeanwhile, the Bank of Lithuania noted that “the IMF forecast was prepared before the very positive GDP and labour market data for the second quarter of 2023 were published”.\n\nAs pointed out by the IMF, Lithuania’s banking sector is particularly resilient due to high liquidity and capital buffers.\n\nThe Fund noted, however, that growing loan interest rates as a result of rising key interest rates pose significant risks to the financial sector. It also mentioned that the windfall profit tax – the so-called bank “solidarity contribution” – must be a temporary measure."
        },
        {
          "role": "assistant",
          "content": "IMF forecasts Lithuania's economy to contract by 1.4% in 2023\n\n☐ The International Monetary Fund (IMF) expects Lithuania's economy to contract in 2023.\n- Lithuania's central bank says IMF projects Lithuania's economy to contract by 1.4% in 2023 and grow by 2.9% in 2024.\n- The IMF expects Lithuania's GDP to grow by 2.7% in 2025, 2.5% in 2026, 2.2% in 2027, and 2.1% in 2028.\n- The IMF also cites prolonged inflation, which is higher than the eurozone average, and the resulting decline in domestic and foreign demand as the biggest risk to Lithuania's economy.\n\n☐ The IMF also expects Lithuania's annual inflation to decline.\n- The IMF expects Lithuania's annual inflation to decline to 4.1% by the end of 2023, and to fall to 3% in 2024.\n- The unemployment rate is expected to reach 7.8% in 2023, followed by 6.7% in 2024, 6.2% in 2025, and 6% in 2026-2028.\n\n☐ The Governor of the Central Bank of Lithuania stated that complementary measures are needed to ensure that economic growth is sustained.\n- Central Bank of Lithuania Governor Gediminas Šimkus stated that Lithuania's economic resilience is underpinned by a strong labor market, relatively low private sector debt, a recovery in household real incomes, and strong corporate and bank reserves.\n- However, he added that uncertainty stemming from the war in Ukraine threatens economic growth and financial stability, and that additional measures are needed to ensure that economic growth is sustainable"
        },
        {
          "role": "user",
          "content": "Salcon clinches Sungai Selangor Dam hydro power plant project for RM65 mil\nKUALA LUMPUR (April 17): Salcon Bhd’s unit has secured a contract to build a small hydro power plant of 10.44MW at the Sungai Selangor Dam worth RM65 million.\n\nIn a filing to the stock exchange on Monday (April 17), the company said its wholly-owned subsidiary Salcon Engineering Bhd has accepted the letter of award from AIS Small Hydro Sdn Bhd for the engineering, procurement, construction and commissioning (EPCC) of the power plant.\n\nAIS Small Hydro is a special purpose vehicle (SPV) company formed by Air Selangor Holdings Bhd and Worldwide Holdings Bhd.\n\n“The scope of the project comprises the design, manufacture, factory testing, delivery to the site, erection, testing and commissioning, maintenance and training of AIS Small Hydro personnel,” the company stated.\n\nThe contract is scheduled for completion by May 3, 2025.\n\n“The award of the project reflects the strong confidence that AIS Small Hydro has in Salcon and we look forward to further expanding our portfolio of renewable energy projects in the near future,” said Salcon executive director Datuk Eddy Leong in a separate statement.\n\nHe added the project is expected to contribute positively towards the earnings and net assets of Salcon for the financial years ending Dec 31, 2023 to 2025.\n\nSalcon shares gained 2.33% or half a sen to 22 sen, valuing the company at RM217.67 million."
        },
        {
          "role": "assistant",
          "content": "Malaysian Infrastructure Development Company Salcon Wins Small Hydropower Plant Project\n\n☐ Malaysian infrastructure developer Salcon Bhd has been awarded a hydroelectric power plant project with a total project cost of RM65 million (US$19,973.3 million).\n- On April 17, Salcon announced that its subsidiary, Salcon Engineering Bhd, received a letter of award for the construction of a small hydropower plant with a total capacity of 10.44 megawatts (MW) at the Sungai Selangor Dam.\n\n☐ Salkon disclosed that the award includes the design, fabrication, testing, delivery, maintenance and repair of the hydropower plant and training of personnel.\n- The Sungai Slangor Dam is an infrastructure project operated by AIS Small Hydro, a special purpose vehicle (SPV) formed by Air Selangor Holdings Bhd and Worldwide Holdings Bhd.\n- According to the award notice, Salkon is required to complete the small hydropower plant by May 3, 2025.\n\nMr. Eddy Leong, Chief Executive Officer of Salkon, said that winning the project confirms the strong relationship of trust between Salkon and AIS Small Hydro. \n- Mr. Eddy Leong added that Salkon will use this opportunity to expand its portfolio of renewable energy projects."
        },
        {
          "role": "user",
          "content": "Chile announces first 5G tech business development center\n\nChile's Catholic University (PUC) is to implement the first 5G technology business development and pilot center in the country. The facility will develop prototypes and scaling of digital solutions for different industries, the Chilean government's Production Development Corporation (Corfo) announced Monday in Santiago.\n\n“Through the 5G Center we seek to add value, enhance, pilot, and develop new technological solutions that come from SMEs, enterprises, or startups, to contribute to the productive transformation of the sectors in the territories,” said Corfo Executive Vice President José Miguel Benavente.\n\nCorfo released Monday the details of the Scaling and New Business Center (5TEC), a public-private initiative, awarded to the PUC and strategic partners, in charge of promoting and facilitating the creation and development of new businesses based on 5G technology applications in Chile.\n\nAccording to the parties, the aim is to work with priority productive sectors of the South American country, such as health, mining, forestry, logistics, mobility, and smart cities, through an investment of over US$ 11.2 million over six years.\n\nPUC's Research Deputy Rector Pedro Bouchon said that this center “constitutes a great opportunity to make Chile a reference point for the application of this technology and its evolutions in the innovation and entrepreneurship ecosystem, both public and private, at an international level.”\n\nBouchon highlighted the importance of this type of initiative to transform the economy and contribute to local society, as well as its potential to impact national and international industries.\n\nIn 2021, Chile was the first country in Latin America to tender the spectrum with national coverage for the 5G network, which then meant an improvement in terms of higher speed, data traffic, and digitization of various processes.\n\nThe launch of 5G was framed within a series of measures adopted by the Chilean government in connectivity, among which the National Fiber Optic, Southern Fiber Optic (south), Tarapacá Fiber Optic (north), and Connectivity for Education 2030 projects stand out."
        },
        {
          "role": "assistant",
          "content": "Chile establishes 5G technology development center, grants new licenses for 5G spectrum use\n\n☐ The Chilean government has established a 5G technology business center to explore ways to leverage 5G for different industries in the country. \n- Recently, the Corporación de Fomento de la Producción de Chile (CORFO), part of the Ministry of Finance (Ministerio de Hacienda), announced the creation of a 5G Technology Business Center.\n- The center will be housed at the Pontificia Universidad Católica de Chile (PUC) and will explore the harmonized use of 5G technology in Chilean industries, including 5G applications.\n- José Miguel Benavente, vice president of the Chilean Production Development Corporation, said he hopes the center will pave the way for 5G technology to reach SMEs and startups.\n\nThe Chilean government plans to invest more than $11 million over the next six years to develop 5G technology.\n- The Chilean Production Development Corporation noted that 5G technology has the potential to be used in a variety of sectors, including healthcare, mining, logistics, transportation, and smart cities.\n- After the center is established, the Chilean government will invest more than $11 million (KRW 14.5 billion) over the next six years to develop the technology.\n- The Catholic University of Chile, where the center will be located, is also excited about the technology, saying that 5G will be a center of innovation.\n\n☐ The Chilean government is actively promoting the 5G market by adding more 5G operators to increase market competition.\n- Chile is ahead of its neighbors in the 5G space, becoming the first Latin American country to officially launch 5G services in 2021.\n- Recently, the Chilean government allocated temporary 5G spectrum to local carrier Claro, allowing it to launch services.\n- The government explained that the decision to allocate additional spectrum was in response to recommendations from market watchdogs that increasing the number of 5G service providers from three to four would create a more level playing field and allow for healthy growth."
        },
        {
          "role": "user",
          "content": user_input
        }
      ],
      temperature=0.1,
      max_tokens=600,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].message.content

# --- #

# streamlit cloud 환경에서만 gpt로 대체
def translate_nllb(gpt_summarized_text_en):
    translate_prompt = \
    """I am working on a document that is intended for publication in a South Korean newspaper. As a professional English to Korean translator, your expertise is critical to ensuring that the translation not only accurately conveys the original text's meaning but also reads as if it were authored in Korean, with the natural flow and word choice reminiscent of a native Korean journalist. 

To achieve this, please follow these instructions:

1. Translate the English text into Korean, maintaining a natural and fluent tone throughout.
2. Use vocabulary and expressions commonly found in Korean news articles to ensure the translation resonates with readers accustomed to that style.
3. Focus on readability, ensuring that the Korean version is clear and easily understandable.
4. Maintain a consistent writing style throughout the translation, mirroring the tone and level of formality used in reputable Korean newspapers.

Could you please provide a translation that meets these criteria?"""
    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {
          "role": "system",
          "content": translate_prompt
        },
        {
          "role": "user",
          "content": "Indonesia records 5.01% economic growth in Q1 2022\n\n☐ On May 9, Statistics Indonesia announced that the economy grew 5.01% in the first quarter of 2022.\n- Statistics Indonesia attributed the growth to a significant increase in international prices of key commodity exports, which helped offset the negative impact of the omicron variant outbreak in the community.\n- In February 2022, when the number of new COVID-19 cases in Indonesia peaked, the Indonesian government imposed movement restrictions, which led to a contraction in economic activity.\n\n☐ Looking at quarterly gross domestic product (GDP) growth, Indonesia's GDP grew by 1.06% quarter-on-quarter in Q3 2021, but reversed to 0.96% in Q4.\n- In the first quarter of 2022, private consumption growth was up 4.34% year-on-year.\n- The share of private consumption in Indonesia's economy is more than half of GDP.\n\n☐ Bank Indonesia slightly revised its 2022 growth forecast to 4.5-5.3% from 4.7-5.5%, as spillover effects from the war in Ukraine slow the global economic recovery.\n- The exchange rate of the rupiah to the U.S. dollar stabilized in Q1 2022, fluctuating between IDR 14,200 and IDR 14,400 (USD 1,240 and USD 1,260).\n- Indonesia's trade balance recorded a surplus of USD 9.3 billion (Rp 11,852.9 billion) in Q1 2022, up 20% year-on-year.\n- Andry Asmoro, chief economist at local commercial bank Bank Mandiri, predicts that Indonesia's GDP growth could reach 5.17% in 2022."
        },
        {
          "role": "assistant",
          "content": "인도네시아, 2022년 1/4분기 경제성장률 5.01% 기록\n\n☐ 5월 9일 인도네시아 통계청은 2022년 1/4분기 경제성장률이 5.01%를 기록했다고 발표함.\n- 인도네시아 통계청은 주요 원자재 수출 품목의 국제 시세가 크게 상승한 덕분에 지역사회에서의 오미크론(omicron) 변이 유행으로 인한 부정적 여파가 상쇄될 수 있었다고 설명함.\n- 2022년 2월 인도네시아 국내 코로나19 신규 확진자 수가 정점에 달하자 인도네시아 정부가 이동 제한 조치를 내린 탓에 경제 활동이 위축된 바 있음.\n\n☐ 분기별 국내총생산(GDP) 성장률을 살펴보면, 2021년 3/4분기 인도네시아의 GDP는 전 분기 대비 1.06% 성장했지만, 4/4분기에는 0.96% 역(-)성장을 기록함.\n- 2022년 1/4분기 민간소비 성장률은 전년 동기 대비 4.34% 증가한 것으로 나타남.\n- 인도네시아 경제에서 민간 소비가 차지하는 비중은 GDP 대비 절반 이상임.\n\n☐ 우크라이나 전쟁으로 인한 파급효과가 세계 경제 회복 속도를 둔화시키는 가운데, 인도네시아 중앙은행은 2022년 성장률 전망치를 4.7~5.5%에서 4.5~5.3%로 소폭 하향 조정함.\n- 2022년 1/4분기 달러당 루피화 환율은 1만 4,200~1만 4,400루피아(한화 약 1,240~1,260원) 사이에서 변동하는 등 안정세임.\n- 2022년 1/4분기 인도네시아 무역수지는 93억 달러(한화 약 11조 8,529억 원) 흑자를 기록했으며, 흑자 규모는 전년 동기 대비 20% 증가함.\n- 현지 시중은행 만디리 은행(Bank Mandiri)의 수석 이코노미스트인 안드리 아스모로(Andry Asmoro)는 2022년 인도네시아 GDP 성장률이 5.17%에 달할 수 있다고 전망함."
        },
        {
          "role": "user",
          "content": "Israeli Supreme Court puts Netanyahu's eligibility to serve as prime minister on hold\n\n☐ On January 2, Israel's Supreme Court ruled that it is \"premature\" to determine whether Prime Minister Benjamin Netanyahu is eligible to form the next government at this time, putting on hold a hearing on his eligibility to serve as prime minister\n- In its decision, the Supreme Court noted that the election period is a \"zone of uncertainty\" and that the need for a ruling will depend largely on which candidate comes out on top in the general election\n- In November 2019, Israeli prosecutors indicted Mr. Netanyahu on charges of bribery, fraud, and embezzlement\n\n☐ As a result of the ruling, Netanyahu's trial for his alleged crimes will be delayed until at least March 2020, when early elections will be held\n- Netanyahu's Likud party supported the ruling, stating that \"in a democracy, the people decide who their leaders are,\" while his rival Blue and White party said that \"Netanyahu should be ousted through an election, not a court ruling.\"\n- Some observers noted that the Israeli Supreme Court avoided a potential confrontation between the Israeli government and the judiciary with this decision\n\n☐ On January 1, Netanyahu asked the Knesset for immunity\n- In a televised address, Netanyahu explained that \"my request for immunity is in accordance with the law and serves the purpose of protecting you and the future of Israel.\"\n- Under Israeli law, Israeli lawmakers are not automatically granted immunity, but can request it if they are implicated"
        },
        {
          "role": "assistant",
          "content": "이스라엘 대법원, 네타냐후의 총리직 자격심사 보류\n\n☐ 1월 2일 이스라엘 대법원은 베냐민 네타냐후(Benjamin Netanyahu) 총리가 차기 정부를 구성할 자격이 있는지 판단하는 것이 현재로서는 ‘시기상조(premature)’라며 차기 총리직 자격 여부에 대한 심리를 보류한다고 판결함. \n- 대법원 측은 결정문을 통해 선거 기간은 ‘불확실성의 영역'이며, 판결의 필요성도 총선 결과에서 어떤 후보가 1위를 차지하느냐에 따라 크게 좌우될 것이라고 밝혔음. \n- 2019년 11월 이스라엘 검찰은 네타냐후 총리를 뇌물, 사기, 배임 등의 혐의로 기소하였음. \n\n☐ 이번 판결에 따라, 네타냐후 총리의 범죄 혐의를 둘러싼 재판은 적어도 조기 총선이 시행되는 2020년 3월 이후로 미뤄질 전망임. \n- 네타냐후 총리가 이끄는 리쿠르당은 \"민주주의에서는 국민들이 지도자를 결정하는 것이 옳다\"며 판결을 지지하였으며, 경쟁자인 청백당도 \"네타냐후 총리는 법원 판결이 아닌 선거를 통해 축출되어야 한다\"고 밝힘.\n- 일각에서는 이스라엘 대법원이 이번 결정을 통해 이스라엘 정부와 사법부 사이의 잠재적 대립을 피했다고 지적함. \n\n☐ 한편, 네타냐후 총리는 1월 1일 의회에 면책특권을 요청했음. \n- 네타냐후 총리는 TV 연설에서 \"면책특권 요청은 법에 따른 것이며, 여러분과 이스라엘의 미래를 받들려는 목적을 지닌다”고 설명하였음. \n- 이스라엘 법률에 따르면, 이스라엘 의원은 자동으로 면책특권을 받지 않지만, 연관성이 있을 경우 면책특권을 요청할 수 있음."
        },
        {
          "role": "user",
          "content" : gpt_summarized_text_en
        }
      ],
      temperature=0.5,
      max_tokens=1200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    
    return response.choices[0].message.content
    # fin_text = []
    # for txt in gpt_summarized_text_en.split('\n'):
    #     fin_text.append(st.session_state.translator.predict(txt.strip()))
        
    # flattened_strings = [item for sublist in fin_text for item in (sublist if sublist else [""])]
    # resulting_string = '\n'.join(flattened_strings)
    # return resulting_string


    
# --- #

def edit_gpt(gpt_summarized_text_en, nllb_translated_text_ko):
    edit_prompt = \
    """// ROLE
    You are a professional proofreader and editor proficient in both English and Korean languages.

    // TASK
    And your task revolves around two texts: the "GPT generated summary" in English and its corresponding "translated text" in Korean. Your responsibilities are twofold:
    1. Enhance the readability of the "translated text" by editing it.
    2. Modify the text according to the provided instructions and writing guidelines.

    // INSTRUCTIONS
    - Modify sentence endings such as (~함, ~임, ~음, ~했음) in line with the examples provided.
    - The final output should resemble a Korean news briefing, giving the impression that it was originally composed in Korean rather than translated from English.
    - Implement the use of formal language, specifically mirroring the style observed in reputable Korean newspapers.
    - Enhance readability by concatenating two sentences if necessary.
    - Ensure your responses maintain a consistent style.

    // WRITING GUIDELINES
    1 - When referencing an individual, follow their surname with their English name in parentheses, as well as their professional affiliation or job title. Subsequently, only the affiliation or position following a person's surname should be used.
    Example: 호세 베나벤테(José Miguel Benavente) 칠레생산개발공사 부사장은 센터 건립을 계기로 5G 기술을 중소기업과 스타트업 기업에도 보급할 수 있는 길이 열리기를 희망한다고 말했음. 부사장은 저렇게 했음.

    2 - For proper nouns such as names of people, organizations, locations, and companies, use both the Korean and English names when first mentioned.
    Example: 로컬 통신사 클라로(Claro)

    3 - Express currency values alongside their equivalent in Korean Won.
    Example: 1,100만 달러(한화 약 145억 원)

    4 -For numerical representation, use commas for thousands separators. Use Korean words for trillion/billion/million, and numbers for values less than a thousand.
    Example: 100달러, 100만 달러

    5 - For numerical representation, use commas for thousands separators. Use Korean words for trillion/billion/million, and numbers for values less than a thousand.
    Example: 7억 3,450만 4,000달러

    6 - Use comparative phrases for months and years such as "전년 동기 대비", "전년 동월 대비", "전년 대비"

    7 - Indicate the date in the first paragraph using the month and day.
    Example: 5월 9일 인도네시아 통계청은

    8 - Use numerical fractions for quarterly representations.
    Example: 2022년 1/4분기 경제성장률이

    9- When a proper noun is an acronym, write the acronym along with the full name in parentheses. 
    Example: 칠레 가톨릭대학(PUC, Pontificia Universidad Católica de Chile)

    10 - Never use pronouns (for instance, '그는', '그녀는', '이 회사는', '그들은' etc.). Always replace them with the specific names they refer to.
    Example:  5G 기술 비즈니스 센터를 건립한다고 발표했음. - 해당 센터는 ~.
    """

    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {
          "role": "system",
          "content": edit_prompt
        },
        {
          "role": "user",
          "content": "```GPT generated summary in English:\nIndonesia records 5.01% economic growth in Q1 2022\n\n☐ On May 9, Statistics Indonesia announced that the economy grew 5.01% in the first quarter of 2022.\n- Statistics Indonesia attributed the growth to a significant increase in international prices of key commodity exports, which helped offset the negative impact of the omicron variant outbreak in the community.\n- In February 2022, when the number of new COVID-19 cases in Indonesia peaked, the Indonesian government imposed movement restrictions, which led to a contraction in economic activity.\n\n☐ Looking at quarterly GDP growth, Indonesia's GDP grew by 1.06% quarter-on-quarter in Q3 2021, but reversed to 0.96% in Q4.\n- In the first quarter of 2022, private consumption growth was up 4.34% year-on-year.\n- The share of private consumption in Indonesia's economy is more than half of GDP.\n\n☐ Bank Indonesia slightly revised its 2022 growth forecast to 4.5-5.3% from 4.7-5.5%, as spillover effects from the war in Ukraine slow the global economic recovery.\n- The exchange rate of the rupiah to the U.S. dollar stabilized in Q1 2022, fluctuating between IDR 14,200 and IDR 14,400.\n- Indonesia's trade balance recorded a surplus of USD 9.3 billion in Q1 2022, up 20% year-on-year.\n- Andry Asmoro, chief economist at local commercial bank Bank Mandiri, predicts that Indonesia's GDP growth could reach 5.17% in 2022.\n```\n\n```translated text:\n인도네시아가 2022년 1분기 5.01%의 경제성장률을 기록하고 있다.\n\n☐ 5월 9일 통계청 인도네시아는 2022년 1분기 경제 성장률이 5.01%라고 발표했다.\n- 통계 인도네시아는 성장이 주요 상품 수출의 국제 가격의 상당한 증가에 기인했으며, 이는 지역사회에서 오미크론 변이체 발병의 부정적인 영향을 상쇄하는 데 도움이 되었다.\n- 인도네시아의 코로나19 신규 확진자가 정점을 찍은 2022년 2월 인도네시아 정부가 이동제한령을 내렸으며, 이로 인해 경제활동이 위축됐다.\n\n☐ 분기별 GDP 성장률을 살펴보면, 인도네시아 GDP는 2021년 3분기에는 전분기 대비 1.06% 성장하였으나, 4분기에는 0.96%로 반전되었다.\n- 2022년 1분기 민간소비 증가율은 전년 동기 대비 4.34% 증가하였다.\n- 인도네시아 경제에서 민간 소비가 차지하는 비중은 GDP의 절반 이상이다.\n\n☐ 인도네시아은행은 우크라이나 전쟁으로 인한 파급효과가 세계 경제 회복을 늦추면서 2022년 성장률 전망치를 4.7-5.5%에서 4.5-5.3%로 소폭 수정했다.\n- 2022년 1분기에는 루피아 대 미국 달러화 환율이 안정화되어 IDR 14,200과 IDR 14,400 사이에서 변동하였다.\n- 인도네시아 무역수지는 2022년 1분기 전년 대비 20% 증가한 93억 달러의 흑자를 기록했다.\n- 현지 시중은행인 만디리은행의 안드리 아스모로 수석 이코노미스트는 인도네시아의 GDP 성장률이 2022년 5.17%에 이를 수 있다고 전망했다.\n```"
        },
        {
          "role": "assistant",
          "content": "인도네시아, 2022년 1/4분기 경제성장률 5.01% 기록\n\n☐ 5월 9일 인도네시아 통계청은 2022년 1/4분기 경제성장률이 5.01%를 기록했다고 발표함.\n- 인도네시아 통계청은 주요 원자재 수출 품목의 국제 시세가 크게 상승한 덕분에 지역사회에서의 오미크론(omicron) 변이 유행으로 인한 부정적 여파가 상쇄될 수 있었다고 설명함.\n- 2022년 2월 인도네시아 국내 코로나19 신규 확진자 수가 정점에 달하자 인도네시아 정부가 이동 제한 조치를 내린 탓에 경제 활동이 위축된 바 있음.\n\n☐ 분기별 국내총생산(GDP) 성장률을 살펴보면, 2021년 3/4분기 인도네시아의 GDP는 전 분기 대비 1.06% 성장했지만, 4/4분기에는 0.96% 역(-)성장을 기록함.\n- 2022년 1/4분기 민간소비 성장률은 전년 동기 대비 4.34% 증가한 것으로 나타남.\n- 인도네시아 경제에서 민간 소비가 차지하는 비중은 GDP 대비 절반 이상임.\n\n☐ 우크라이나 전쟁으로 인한 파급효과가 세계 경제 회복 속도를 둔화시키는 가운데, 인도네시아 중앙은행은 2022년 성장률 전망치를 4.7~5.5%에서 4.5~5.3%로 소폭 하향 조정함.\n- 2022년 1/4분기 달러당 루피화 환율은 1만 4,200~1만 4,400루피아(한화 약 1,240~1,260원) 사이에서 변동하는 등 안정세임.\n- 2022년 1/4분기 인도네시아 무역수지는 93억 달러(한화 약 11조 8,529억 원) 흑자를 기록했으며, 흑자 규모는 전년 동기 대비 20% 증가함.\n- 현지 시중은행 만디리 은행(Bank Mandiri)의 수석 이코노미스트인 안드리 아스모로(Andry Asmoro)는 2022년 인도네시아 GDP 성장률이 5.17%에 달할 수 있다고 전망함."
        },
        {
          "role": "user",
          "content": "```GPT generated summary in English:\nChile establishes 5G technology development center, grants new licenses for 5G spectrum use\n\n☐ The Chilean government has established a 5G technology business center to explore ways to leverage 5G for different industries in the country. \n- Recently, the Corporación de Fomento de la Producción de Chile (CORFO), part of the Ministry of Finance (Ministerio de Hacienda), announced the creation of a 5G Technology Business Center.\n- The center will be housed at the Pontificia Universidad Católica de Chile (PUC) and will explore the harmonized use of 5G technology in Chilean industries, including 5G applications.\n- José Miguel Benavente, vice president of the Chilean Production Development Corporation, said he hopes the center will pave the way for 5G technology to reach SMEs and startups.\n\nThe Chilean government plans to invest more than $11 million over the next six years to develop 5G technology.\n- The Chilean Production Development Corporation noted that 5G technology has the potential to be used in a variety of sectors, including healthcare, mining, logistics, transportation, and smart cities.\n- After the center is established, the Chilean government will invest more than $11 million (KRW 14.5 billion) over the next six years to develop the technology.\n- The Catholic University of Chile, where the center will be located, is also excited about the technology, saying that 5G will be a center of innovation.\n\n☐ The Chilean government is actively promoting the 5G market by adding more 5G operators to increase market competition.\n- Chile is ahead of its neighbors in the 5G space, becoming the first Latin American country to officially launch 5G services in 2021.\n- Recently, the Chilean government allocated temporary 5G spectrum to local carrier Claro, allowing it to launch services.\n- The government explained that the decision to allocate additional spectrum was in response to recommendations from market watchdogs that increasing the number of 5G service providers from three to four would create a more level playing field and allow for healthy growth.\n```\n\n```translated text:\n칠레가 5G 기술개발센터를 설립하고 5G 스펙트럼 사용에 대한 새로운 라이선스를 부여한다.\n\n☐ 칠레 정부는 5G 기술 사업 센터를 설립해 자국 내 다양한 산업을 위한 5G 활용 방안을 모색했다.\n- 최근 재무부(Ministerio de Hacienda) 산하 칠레산업진흥공단(CORFO)은 5G 기술사업센터 조성을 발표했다.\n- 센터는 칠레 교황청 가톨릭대학(PUC)에 들어설 예정이며, 5G 애플리케이션을 포함한 칠레 산업에서 5G 기술의 조화로운 활용을 모색할 예정이다.\n- 칠레 생산개발공사 호세 미구엘 베나벤테 부사장은 센터가 중소기업과 스타트업에 5G 기술이 도달할 수 있는 길을 열기를 희망한다고 말했다.\n\n칠레 정부는 5G 기술 개발을 위해 향후 6년간 1천100만 달러 이상을 투자할 계획이다.\n- 칠레 생산개발공사는 5G 기술이 헬스케어, 광업, 물류, 교통, 스마트시티 등 다양한 분야에서 활용될 가능성이 있다고 지적했다.\n- 센터가 설립된 후 칠레 정부는 향후 6년간 1천100만 달러(145억 원) 이상을 투자해 기술 개발에 나선다.\n- 센터가 들어설 칠레 가톨릭대학도 5G가 혁신의 중심이 될 것이라며 기술에 기대를 모으고 있다.\n\n☐ 칠레 정부는 시장 경쟁력을 높이기 위해 5G 사업자를 더 추가하는 등 5G 시장을 적극적으로 추진하고 있다.\n- 칠레가 5G 공간에서 이웃나라보다 앞서 2021년 중남미 국가 중 처음으로 5G 서비스를 공식 출시했다.\n- 최근 칠레 정부는 현지 통신사 클라도에 임시 5G 스펙트럼을 할당해 서비스를 시작할 수 있게 했다.\n- 추가 스펙트럼 배분 결정은 5G 서비스 사업자를 기존 3개에서 4개로 늘리면 보다 공평한 경쟁이 조성되고 건전한 성장이 가능하다는 시장 감시당국의 권고에 따른 것이라고 정부는 설명했다.\n```"
        },
        {
          "role": "assistant",
          "content": "칠레, 5G 기술 개발 센터 건립...5G 주파수 사용 신규 허가도\n\n☐ 칠레 정부가 5G 기술 비즈니스 센터를 세우고 5G를 칠레 각 산업에 활용할 방법을 모색함. \n- 최근 칠레 재무부(Ministerio de Hacienda) 산하의 칠레생산개발공사(CORFO, Corporación de Fomento de la Producción de Chile)가 5G 기술 비즈니스 센터를 건립한다고 발표했음.\n- 해당 센터는 칠레 가톨릭대학(PUC, Pontificia Universidad Católica de Chile) 내에 설치되며, 5G 응용 기술을 비롯하여 5G 기술을 칠레 각 산업에서 조화롭게 사용할 방법을 강구함.\n- 호세 베나벤테(José Miguel Benavente) 칠레생산개발공사 부사장은 센터 건립을 계기로 5G 기술을 중소기업과 스타트업 기업에도 보급할 수 있는 길이 열리기를 희망한다고 말했음.\n\n☐ 칠레 정부는 5G 기술 개발을 위해 향후 6년 동안 1,100만 달러 이상을 투자할 방침임.\n- 칠레생산개발공사는 5G 기술이 헬스케어, 광업, 물류, 운송, 스마트시티 등 다양한 분야에 활용될 수 있는 잠재력을 지녔다고 언급했음.\n- 센터 건립 후 칠레 정부는 기술 개발에만 앞으로 6년간 1,100만 달러(한화 약 145억 원) 이상을 투입할 예정임.\n- 센터가 설립될 칠레 가톨릭대학도 5G가 혁신의 중심이 될 것이라고 하면서, 기술 개발에 대한 기대를 감추지 않았음.\n\n☐ 칠레 정부가 5G 사업자를 추가해 시장 경쟁을 강화하는 등 5G 시장 육성에 적극적으로 나서고 있음.\n- 칠레는 지난 2021년 중남미 국가로는 처음으로 5G 서비스를 정식으로 시작하는 등 5G 부문에서 주변국보다 한발 앞서가고 있음.\n- 최근 칠레 정부는 로컬 통신사 클라로(Claro)에 임시 5G 주파수를 할당하여 서비스를 시작할 수 있도록 했음.\n- 칠레 정부는 기존 세 곳이었던 5G 서비스 업체를 네 곳으로 늘리면 보다 공정한 시장 경쟁 구도가 조성되고, 이를 통해 건전한 성장이 가능할 것이라는 시장 감독 기구의 권고를 수용한 결정이라고 주파수 추가 할당 취지를 설명했음."
        },
        {
          "role": "user",
          "content": "```GPT generated summary in English:\n{}\n```\n\n```translated text:\n{}\n```".format(gpt_summarized_text_en, nllb_translated_text_ko)
        }
      ],
      temperature=0.1,
      max_tokens=1200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].message.content

# --- #

def pronouns_gpt(gpt_proofread_text_ko):
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {
        "role": "system",
        "content": "You are going to write a JSON. 제공된 텍스트에서 괄호 안 영어와 함께 표기된 모든 고유명사(기관명, 인물명, 지역명, 정책명, 정당명 등등)를 추출해서 다음과 같은 jason object를 만들어 주세요:\n\n```json\n[\n    {\n        \"순번\": 1,\n        \"한글표기\": \"<한글표기1>\",\n        \"영어표기\": \"<영어표기1>\",\n        \"해당국가\": \"<해당국가1>\",\n        \"이머릭스\": \"https://www.google.com/search?q=<영어표기1>+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=<해당국가1>+<영어표기1>&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=<해당국가1>+<영어표기1>&tbm=nws\"\n    },\n    {\n        \"순번\": 2>,\n        \"한글표기\": \"<한글표기1>\",\n        \"영어표기\": \"<영어표기1>\",\n        \"해당국가\": \"<해당국가1>\",\n        \"이머릭스\": \"https://www.google.com/search?q=<영어표기1>+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=<해당국가1>+<영어표기1>&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=<해당국가1>+<영어표기1>&tbm=nws\"\n    }\n]\n```  Provide your answer in JSON form. Reply with only the answer in JSON form and include no other commentary. "
        },
        {
        "role": "user",
        "content": "턔국 상원의원, 전진당에 왕실모독죄 개정 공약을 포기하라고 촉구\n☐ 태국 상원의원이 전진당(Move Forward Party)에 왕실모독죄 개정 공악을 표기하라고 축구함\n- 7월 31일 완차이 손시리(Wanchai Sonsiri) 상원의원은 전진당이 왕실모독죄 개정 공약을 포기한다면, 연정 파트너인 푸어타이(Pheu Thai)당 후보가 신임 총리가 되는데 필요한 상하원 과반수를 확보할 수 있다고 주장함\n- 완차이 손시리 의원은 7월 13일 1차 투표 때 피타 림짜른랏(Pita Limjaroenrat) 전진당 대표에 투표한 상원의원 13명 중 한 사람임\n\n☐ 피타 림짜른랏 전진당 대표가 2차 투표에 참여하지 못하게 되자, 전진당은 차기 정부 구성을 연정 파트너인 푸어타이당에 넘긴 상태임\n- 이에 푸어타이당은 8월 4일로 예정된 2차 투표에서 탁신 전 총리와 가까운 부동산 재벌 스레타 타위신(Srettha Thavisin)을 총리 후보로 지명할 계획임\n- 완차이 손시리 의원은 “푸어타이당이 스레타 타위신을 지명한다면 그에게 표를 던질 것”이라고 덧붙임\n\n☐ 완차이 손시리 의원은 푸어타이당이 다양한 정당 및 상원의원들과 협력할 수 있기 때문에 연립정부를 이끌 가능성이 더 높다고 평가함\n- 완차이 손시리 의원은 “만약 푸어타이당과 전진당이 연립정부 구성에 서로 관심이 없을 경우 전진당이 왕실모독죄 개정 공약을 포기해야만 상원의원들의 지지를 얻을 수 있을 것”이라고 주장함\n- 태국 군부 및 보수파 의원들은 국왕과 왕실을 모독하는 자를 처벌하는 내용을 담은 왕실모독죄 조항을 개정하자는 전진당의 형사법 개혁에 반대하고 있음"
        },
        {
        "role": "assistant",
        "content": "[\n    {\n        \"순번\": 1,\n        \"한글표기\": \"완차이 손시리\",\n        \"영어표기\": \"Wanchai Sonsiri\",\n        \"해당국가\": \"태국\",\n        \"이머릭스\": \"https://www.google.com/search?q=Wanchai+Sonsiri+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=태국+Wanchai+Sonsiri&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=태국+Wanchai+Sonsiri&tbm=nws\"\n    },\n    {\n        \"순번\": 2,\n        \"한글표기\": \"전진당\",\n        \"영어표기\": \"Move Forward Party\",\n        \"해당국가\": \"태국\",\n        \"이머릭스\": \"https://www.google.com/search?q=Move+Forward+Party+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=태국+Move+Forward+Party&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=태국+Move+Forward+Party&tbm=nws\"\n    },\n    {\n        \"순번\": 3,\n        \"한글표기\": \"푸어타이당\",\n        \"영어표기\": \"Pheu Thai Party\",\n        \"해당국가\": \"태국\",\n        \"이머릭스\": \"https://www.google.com/search?q=Pheu+Thai+Party+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=태국+Pheu+Thai+Party&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=태국+Pheu+Thai+Party&tbm=nws\"\n    },\n    {\n        \"순번\": 4,\n        \"한글표기\": \"피타 림짜른랏\",\n        \"영어표기\": \"Pita Limjaroenrat\",\n        \"해당국가\": \"태국\",\n        \"이머릭스\": \"https://www.google.com/search?q=Pita+Limjaroenrat+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=태국+Pita+Limjaroenrat&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=태국+Pita+Limjaroenrat&tbm=nws\"\n    },\n    {\n        \"순번\": 5,\n        \"한글표기\": \"스레타 타위신\",\n        \"영어표기\": \"Srettha Thavisin\",\n        \"해당국가\": \"태국\",\n        \"이머릭스\": \"https://www.google.com/search?q=Srettha+Thavisin+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=태국+Srettha+Thavisin&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=태국+Srettha+Thavisin&tbm=nws\"\"\n    }\n\n]"
        },
        {
        "role" : "user",
        'content' : gpt_proofread_text_ko
            
        }
    ],
    temperature=0,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    )
    return response.choices[0].message.content

# --- #

    # session states
        # 사이드바에서 입력하는 기사 개수 저장
if 'number_of_articles' not in st.session_state:
    st.session_state['number_of_articles'] = 1
        # 유저인풋
if "user_input" not in st.session_state:
    st.session_state["user_input"] = []
        # 추출되는 결과물 저장
if "history" not in st.session_state:
    st.session_state["history"] = []

if "display" not in st.session_state:
    st.session_state["display"] = []


#
# Libs & Funcs -------------------------------------------------------------------------------------------------------------------------- #

# Page Structure -------------------------------------------------------------------------------------------------------------------------- #
#

# 기사입력 -> 요약 -> 번역 -> 윤문
# 1. 기사입력
    # 기사 입력창 개수를 사용자가 조정
    # 세션에 저장
    # for - loop를 통해 fucntion 실행
    # 결과물을 모두 session state에 저장 후 expander를 통해 보여주기
    
tab1, tab2 = st.tabs(["**MAIN**", "**HISTORY**"])

#
# Page Structure -------------------------------------------------------------------------------------------------------------------------- #


# SIDE BAR -------------------------------------------------------------------------------------------------------------------------- #
#
# Use the sidebar for configuration
with st.sidebar:
    st.title("🎈 설정")
    st.caption("💡`Secret Key`와 요약과 번역이 필요한 기사를 미리 입력하세요")

    # Secret key input
    secret_key_user = st.text_input(':secret: **Secret Key**', placeholder='chan@ec21rnc.com에 문의해주세요', type="password")
    #
    st.divider()

    # Let the user decide the number of article inputs
    number_inputs = st.number_input('**총 몇개의 기사를 요약할건가요?** _(최대 10개 까지만 한번에 처리 가능합니다)_',
                                    step=1,
                                    min_value=1,
                                    max_value=10,
                                    key='number_inputs')
    
    st.session_state['number_of_articles'] = number_inputs
    
    # Article input form
    with st.form(key='article_form'):
        with st.expander("⌨️ **필요한 기사를 복사/붙여넣기 해주세요**", expanded=True):
            # Create text areas for each article based on the session state value
            input_values = [st.text_area(f'_{i+1}번 기사_', key=f"text_input_{i+1}", placeholder=f"[{i+1}번 기사 제목]\n[{i+1}번 기사 내용]")
                            for i in range(st.session_state['number_of_articles'])]

        # Submit button for the form
        submit = st.form_submit_button('**:fast_forward: GPT로 보내기**',
                                       use_container_width = True)

#
# SIDE BAR -------------------------------------------------------------------------------------------------------------------------- #


# MAIN_tab1 ------------------------------------------------------------------------------------------------------------------------------ #
#
    # displays the result

with tab1:
    #
    # Title
    #
    st.title(":blue[EC21R&C] 요약봇 :robot_face:")
    st.divider()
    
    
    # Display the results from the current session state
    # 왼쪽에 원문, 오른쪽에 나머지 결과 띄우면 좋을 듯
    placeholder = st.empty()
    
    with placeholder.container():
        if st.session_state["display"]:
            for i, past_results in enumerate(st.session_state["display"]):
                with st.expander('{}번 기사 처리 결과'.format(str(i+1))):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.header(':newspaper: 입력글')
                        st.divider()
                        st.markdown(past_results['user_input'])
                    
                    with col2:
                        st.header(':printer: 결과')
                        st.divider()
                        st.subheader(':black_nib: GPT 작성본')
                        st.markdown(past_results['gpt_proofread_text_ko'])
                        st.divider()
                        st.subheader(':mag_right: 고유명사 검색 결과')
                        st.dataframe(past_results['gpt_pronouns'],
                                     column_config={'이머릭스' : st.column_config.LinkColumn('이머릭스 링크'),
                                     '네이버' : st.column_config.LinkColumn('네이버 링크'),
                                     '구글' : st.column_config.LinkColumn('구글 링크')
                                     }
                                     )
                        st.divider()
                        st.subheader(':abc: GPT 영어 요약본')
                        st.markdown(past_results['gpt_summarized_text_en'])


    
    #
    # result
    #
    if submit:
        placeholder.empty()
        st.session_state['display'] = []
        if secret_key_user == secret_key:
                if all(len(input_value.strip()) > 0 for input_value in input_values):
                    with st.spinner('_열심히 요약하고 있어요... 서버 상황에 따라 1~2분정도 소요됩니다_'):
                        # Clear the previous results from the display before storing new ones
                        # Reset the display state
                        
                        # Store user inputs into session_state['user_input']
                        st.session_state['user_input'] = input_values
                        
                        temp_list = []
                        # Process each text using func_1, func_2, and func_3
                        for i, text in enumerate(st.session_state['user_input']):
                            gpt_summarized_text_en = summary_gpt(text)
                            nllb_translate_text_ko = translate_nllb(gpt_summarized_text_en)
                            gpt_proofread_text_ko = edit_gpt(gpt_summarized_text_en, nllb_translate_text_ko)
                            gpt_pronouns = pronouns_gpt(gpt_proofread_text_ko)
                            gpt_pronouns = pd.DataFrame(json.loads(gpt_pronouns))
                            with st.expander('{}번 기사 처리 결과'.format(str(i+1))):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.header(':newspaper: 입력글')
                                    st.divider()
                                    st.markdown(text)
                                
                                with col2:
                                    st.header(':printer: 결과')
                                    st.divider()
                                    st.subheader(':black_nib: GPT 작성본')
                                    st.markdown(gpt_proofread_text_ko)
                                    st.divider()
                                    st.subheader(':mag_right: 고유명사 검색 결과')
                                    st.dataframe(gpt_pronouns,
                                                 column_config={'이머릭스' : st.column_config.LinkColumn('이머릭스 링크'),
                                                 '네이버' : st.column_config.LinkColumn('네이버 링크'),
                                                 '구글' : st.column_config.LinkColumn('구글 링크')
                                                 }
                                                 )
                                    st.divider()
                                    st.subheader(':abc: GPT 영어 요약본')
                                    st.markdown(gpt_summarized_text_en)
                                    

                                    


                            # Append results to display
                            st.session_state['display'].append({'user_input' : text,
                                                                'gpt_summarized_text_en' : gpt_summarized_text_en,
                                                                'gpt_proofread_text_ko' : gpt_proofread_text_ko,
                                                                'gpt_pronouns' : gpt_pronouns
                                                                })

                            # append to temp_list
                            temp_list.append([text,
                                            gpt_summarized_text_en,
                                            gpt_proofread_text_ko,
                                            gpt_pronouns
                                            ])
                    
                        # Append results to history
                    st.session_state['history'].append(temp_list)
                else:
                    st.error('기사를 입력하세요', icon="🚨")
        else:
            st.error('올바른 `Secret Key`를 입력하세요', icon="🚨")





#
# MAIN_tab1 ------------------------------------------------------------------------------------------------------------------------------ #


# hist_tab2 ------------------------------------------------------------------------------------------------------------------------------ #
#
    # stores the results as history

with tab2:  
    st.markdown('# :speech_balloon: History')
    st.caption(':warning: 페이지를 새로고침하면 히스토리가 사라집니다')
    st.divider()
    # If there is any history, let the user select which submission to view
    if st.session_state['history']:
        submission_options = [f"{i+1}번째 실행 결과" for i in range(len(st.session_state['history']))]
        selected_submission = st.selectbox("**이전 결과물을 선택하세요:**", options=submission_options, index=len(submission_options)-1)

        # Get the index of the selected submission
        selected_index = submission_options.index(selected_submission)

        # Display the results of the selected submission
        submission = st.session_state['history'][selected_index]
        for result in submission:
            with st.expander(result[0].split('\n')[0].strip()):
                col1, col2 = st.columns(2)
                with col1:
                    st.header(':newspaper: 입력글')
                    st.divider()
                    st.markdown(result[0])
                
                with col2:
                    st.header(':printer: 결과')
                    st.divider()
                    st.subheader(':black_nib: GPT 작성본')
                    st.markdown(result[2])
                    st.divider()
                    st.subheader(':mag_right: 고유명사 검색 결과')
                    st.dataframe(result[3],
                                 column_config={'이머릭스' : st.column_config.LinkColumn('이머릭스 링크'),
                                                '네이버' : st.column_config.LinkColumn('네이버 링크'),
                                                '구글' : st.column_config.LinkColumn('구글 링크')
                                                }
                                                )
                    st.divider()
                    st.subheader(':abc: GPT 영어 요약본')
                    st.markdown(result[1])
                    

                    

    else:
        st.write("No history yet.")


#
# hist_tab2 ------------------------------------------------------------------------------------------------------------------------------ #
