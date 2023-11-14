# Libs & Funcs -------------------------------------------------------------------------------------------------------------------------- #
#
import streamlit as st
import openai
from openai import OpenAI
import os
import ast
import time

st.set_page_config( layout = 'wide' )

openai.api_key = os.getenv('api_key')
secret_key = os.getenv('secret_key')

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = os.getenv('api_key')
)


summary_prompt = \
"""// ROLE
As an experienced bilingual journalist fluent in both English and Korean, you are tasked with composing a news briefing that authentically captures the essence of Korean journalistic style.

// WRITING STYLE
- Modify sentence endings such as (~함, ~임, ~음, ~힘) in line with the examples provided.
- The final output should look like a Korean news briefing, giving the impression that it was originally composed in Korean rather than translated from English.
- Implement the use of formal language, specifically mirroring the expressions and words observed in reputable Korean newspapers.
- Enhance readability by concatenating two sentences if necessary.
- Favor the construction of longer, more comprehensive sentences to enhance readability, as is typical in Korean reporting.
- Craft the subtitles based on the principle of informative progression, capturing the main event, detailed insights, and broader context. Each subtitle should be highly relevant and succinct, summarizing the forthcoming section efficiently. Always select the most significant and newsworthy aspects to shape these key statements, ensuring the briefing remains focused and impactful.

// TASK
Generate a structured news briefing in Korean on the given news article.
The briefing should be composed of a headline that captures the essence of the news, followed by exact three key insights or developments, as the STRUCTURE describes below.
Each insight should be supported by two bullet points that provide factual details, statistics, or quotes from officials or experts. Maintain a formal and informative tone throughout the briefing, ensuring clarity and neutrality in the presentation of information.

// Step-by-Step guide
Please generate a news briefing following the specified structure and style guidelines:

1 - Begin by identifying 3 subtitles. The subtitles for each paragraph are carefully selected to guide the reader through varying facets of the news topic. They provide structure to the information, allowing readers to quickly understand key aspects without needing to read in full detail

2 - Title: Craft a concise and impactful title that summarizes the most significant aspect of the news story. It should capture the essence of the content and include key details such as statistics, events, or notable figures.

3 - Subtitle of First Paragraph: Introduce the main focus or announcement related to the topic. This should be the leading piece of information that sets the stage for the rest of the briefing.

4 - Content of First Paragraph: Provide bullet points with additional details, supporting statistics, or contextual information that expand upon the subtitle. Each bullet point should offer a piece of evidence or a specific fact that reinforces the main point.

5 - Subtitle of Second Paragraph: Present a related consequence, subsequent development, anticipatory projection, or a secondary angle of the main subject. This should build upon the information provided in the first paragraph.

6 - Content of Second Paragraph: Elaborate on the subtitle with bullet points that give evidence, specific examples, or further implications. These should deepen the reader's understanding of the secondary aspect of the topic.

7 - Subtitle of Third Paragraph: Offer a further dimension, a humanizing angle, potential outcomes, or additional perspectives on the issue. This should provide a comprehensive view of the subject matter.

8 - Content of Third Paragraph: Delve into the elements or opinions introduced in the subtitle with bullet points. Include forecasts, expert opinions, potential solutions, or social implications to conclude the briefing with a broadened perspective.

9 - Ensure that each section is clearly marked with the appropriate subtitle and that the bullet points under each subtitle are informative and relevant to the overarching topic.
```

// INSTRUCTIONS
The language should be Korean, and the content should reflect the style and structure of the given examples, capturing the general meaning of titles, subtitles, and bullet points.

Do not add anything from your own knowledge. Stick to the facts of the given news article.

Answer in a consistent style.
"""



def summary_gpt(user_input):
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
          "content": "이스라엘 대법원, 네타냐후의 총리직 자격심사 보류\n\n☐ 1월 2일 이스라엘 대법원은 베냐민 네타냐후(Benjamin Netanyahu) 총리가 차기 정부를 구성할 자격이 있는지 판단하는 것이 현재로서는 ‘시기상조(premature)’라며 차기 총리직 자격 여부에 대한 심리를 보류한다고 판결함. \n- 대법원 측은 결정문을 통해 선거 기간은 ‘불확실성의 영역'이며, 판결의 필요성도 총선 결과에서 어떤 후보가 1위를 차지하느냐에 따라 크게 좌우될 것이라고 밝혔음. \n- 2019년 11월 이스라엘 검찰은 네타냐후 총리를 뇌물, 사기, 배임 등의 혐의로 기소하였음. \n\n☐ 이번 판결에 따라, 네타냐후 총리의 범죄 혐의를 둘러싼 재판은 적어도 조기 총선이 시행되는 2020년 3월 이후로 미뤄질 전망임. \n- 네타냐후 총리가 이끄는 리쿠르당은 \"민주주의에서는 국민들이 지도자를 결정하는 것이 옳다\"며 판결을 지지하였으며, 경쟁자인 청백당도 \"네타냐후 총리는 법원 판결이 아닌 선거를 통해 축출되어야 한다\"고 밝힘.\n- 일각에서는 이스라엘 대법원이 이번 결정을 통해 이스라엘 정부와 사법부 사이의 잠재적 대립을 피했다고 지적함. \n\n☐ 한편, 네타냐후 총리는 1월 1일 의회에 면책특권을 요청했음. \n- 네타냐후 총리는 TV 연설에서 \"면책특권 요청은 법에 따른 것이며, 여러분과 이스라엘의 미래를 받들려는 목적을 지닌다”고 설명하였음. \n- 이스라엘 법률에 따르면, 이스라엘 의원은 자동으로 면책특권을 받지 않지만, 연관성이 있을 경우 면책특권을 요청할 수 있음."
        },
        {
          "role": "user",
          "content": "IMF predicts Lithuania’s economy contracting 1.4% this year\nThe International Monetary Fund (IMF) forecasts that Lithuania’s economy will contract 1.4 percent this year before growing 2.9 percent in 2024, the Bank of Lithuania said on Tuesday. \n\nAccording to IMF forecasts, the country’s GDP should grow by 2.7 percent in 2025, 2.5 percent in 2026, 2.2 percent in 2027, and 2.1 percent in 2028.\n\nBorja Gracia, the IMF mission chief for Lithuania, predicted in June that the country’s economy would contract by 1.4 percent on average this year, while next year, GDP growth should reach the pace of between 2.5 and 3 percent.\n\nThe IMF now expects Lithuania’s annual inflation to decelerate to 4.1 percent by the end of this year, from 6.4 percent in August, and ease further to 3 percent in late 2024. The Fund sees the annual inflation rate reaching 2.9 percent in late 2025 and averaging 2.5 percent in 2026-2028.\n\nAs estimated by the IMF, the unemployment rate in Lithuania should reach 7.8 percent this year before going down to 6.7 percent in 2024, easing further to 6.2 percent in 2025, and reaching 6 percent in 2026–2028.\n\nAccording to Gediminas Šimkus, board chairman of the Bank of Lithuania, the country’s economic resilience is underpinned by a robust labour market, relatively low private sector indebtedness and recovering real income of households, as well as significant corporate and bank reserves.\n\n“However, we do not have the luxury of time: all institutions need to focus on measures ensuring that Lithuania’s economic growth is sustained. We see risks to economic growth and financial stability in the context of persistent uncertainty, which is mostly linked to Russia’s war against Ukraine,” he is quoted in a press release from the central bank.\n\nAccording to the IMF, the biggest risk to Lithuania’s economy is the scenario where inflation in the country remains significantly higher than the euro area average (at 5.3 percent in August) over a longer period of time, as this would reduce both domestic and foreign demand due to negative effects on competitiveness.\n\nMeanwhile, the Bank of Lithuania noted that “the IMF forecast was prepared before the very positive GDP and labour market data for the second quarter of 2023 were published”.\n\nAs pointed out by the IMF, Lithuania’s banking sector is particularly resilient due to high liquidity and capital buffers.\n\nThe Fund noted, however, that growing loan interest rates as a result of rising key interest rates pose significant risks to the financial sector. It also mentioned that the windfall profit tax – the so-called bank “solidarity contribution” – must be a temporary measure."
        },
        {
          "role": "assistant",
          "content": "IMF, 2023년 리투아니아 경제 1.4% 위축 전망\n\n☐ 국제통화기금(IMF)은 2023년 리투아니아의 경제가 위축될 것으로 전망함\n- 리투아니아 중앙은행은 IMF가 리투아니아 경제를 2023년 1.4% 위축, 2024년 2.9% 성장할 것으로 전망했다고 밝힘\n- IMF는 리투아니아의 GDP가 2025년 2.7%, 2026년 2.5%, 2027년 2.2%, 2028년 2.1% 성장할 것으로 전망함\n- 또한, IMF는 리투아니아 경제의 가장 큰 위험 요인으로 유로존 평균보다 높은 인플레이션의 장기화와 이로 인한 국내외 수요 감소를 꼽음\n\n☐ IMF는 리투아니아의 연간 인플레이션도 하락할 것으로 전망함\n- IMF는 2023년 말까지 리투아니아의 연간 인플레이션이 4.1% 수준으로 하락하고, 2024년에는 3%까지 하락할 것으로 전망함\n- 실업률은 2023년 7.8%에 도달한 후 2024년에는 6.7%, 2025년 6.2%, 2026~2028년에는 6%를 기록할 것이라 밝힘\n\n☐ 리투아니아 중앙은행 총재는 경제 성장이 지속될 수 있도록 보완 조치가 필요하다고 밝힘\n- 게디미나스 심쿠스(Gediminas Šimkus) 리투아니아 중앙은행 총재는 리투아니아의 경제 회복력은 강한 노동시장, 상대적으로 낮은 민간 부문 부채, 가계 실질 소득 회복, 기업과 은행 준비금으로 뒷받침된다고 발언함\n- 그러나 우크라이나 전쟁으로 인한 불확실성은 경제 성장과 금융 안정성을 위협하고 있으며, 경제 성장이 지속될 수 있도록 추가적인 조치가 필요하다고 덧붙임"
        },
        {
          "role": "user",
          "content": "Salcon clinches Sungai Selangor Dam hydro power plant project for RM65 mil\nKUALA LUMPUR (April 17): Salcon Bhd’s unit has secured a contract to build a small hydro power plant of 10.44MW at the Sungai Selangor Dam worth RM65 million.\n\nIn a filing to the stock exchange on Monday (April 17), the company said its wholly-owned subsidiary Salcon Engineering Bhd has accepted the letter of award from AIS Small Hydro Sdn Bhd for the engineering, procurement, construction and commissioning (EPCC) of the power plant.\n\nAIS Small Hydro is a special purpose vehicle (SPV) company formed by Air Selangor Holdings Bhd and Worldwide Holdings Bhd.\n\n“The scope of the project comprises the design, manufacture, factory testing, delivery to the site, erection, testing and commissioning, maintenance and training of AIS Small Hydro personnel,” the company stated.\n\nThe contract is scheduled for completion by May 3, 2025.\n\n“The award of the project reflects the strong confidence that AIS Small Hydro has in Salcon and we look forward to further expanding our portfolio of renewable energy projects in the near future,” said Salcon executive director Datuk Eddy Leong in a separate statement.\n\nHe added the project is expected to contribute positively towards the earnings and net assets of Salcon for the financial years ending Dec 31, 2023 to 2025.\n\nSalcon shares gained 2.33% or half a sen to 22 sen, valuing the company at RM217.67 million."
        },
        {
          "role": "assistant",
          "content": "말레이시아 인프라 개발 기업 살콘, 소형 수력발전소 사업 수주\n\n☐ 말레이시아 인프라 개발 기업 살콘(Salcon Bhd)이 총 사업비 6,500만 링깃(한화 약 192억 9,733만 원) 규모 수력발전소 사업을 수주함.\n- 4월 17일 살콘은 자회사 살콘 엔지니어링(Salcon Engineering Bhd)이 숭아이 슬랑고르 댐(Sungai Selangor Dam)에 총 발전용량 10.44메가와트(MW)급 소형 수력발전소를 건설하는 사업의 낙찰통지서(letter of award)를 받았다고 밝힘.\n\n☐ 살콘은 수력발전소 설계, 제작, 테스트, 인도, 유지 및 보수, 인력 훈련 등이 수주한 사업 내용에 포함된다고 밝힘.\n- 숭아이 슬랑고르 댐은 아이르 슬랑고르(Air Selangor Holdings Bhd)와 월드와이드 홀딩스(Worldwide Holdings Bhd)가 설립한 특별목적회사(SPV, special purpose vehicle)인 AIS 스몰 하이드로(AIS Small Hydro)가 운영하는 인프라임.\n- 낙찰통지서에 따르면 살콘은 2025년 5월 3일까지 소형 수력발전소를 완공해야 함.\n\n☐ 에디 레옹(Eddy Leong) 살콘 최고경영자(CEO)는 이번 사업 낙찰을 통하여 살콘과 AIS 스몰 하이드로와의 끈끈한 신뢰 관계를 확인할 수 있었다고 발언함. \n- 에디 레옹 살콘 CEO는 이번 사업을 계기로 재생에너지 프로젝트의 포트폴리오를 넓혀나가겠다고 덧붙임."
        },
        {
          "role": "user",
          "content": "Chile announces first 5G tech business development center\n\nChile's Catholic University (PUC) is to implement the first 5G technology business development and pilot center in the country. The facility will develop prototypes and scaling of digital solutions for different industries, the Chilean government's Production Development Corporation (Corfo) announced Monday in Santiago.\n\n“Through the 5G Center we seek to add value, enhance, pilot, and develop new technological solutions that come from SMEs, enterprises, or startups, to contribute to the productive transformation of the sectors in the territories,” said Corfo Executive Vice President José Miguel Benavente.\n\nCorfo released Monday the details of the Scaling and New Business Center (5TEC), a public-private initiative, awarded to the PUC and strategic partners, in charge of promoting and facilitating the creation and development of new businesses based on 5G technology applications in Chile.\n\nAccording to the parties, the aim is to work with priority productive sectors of the South American country, such as health, mining, forestry, logistics, mobility, and smart cities, through an investment of over US$ 11.2 million over six years.\n\nPUC's Research Deputy Rector Pedro Bouchon said that this center “constitutes a great opportunity to make Chile a reference point for the application of this technology and its evolutions in the innovation and entrepreneurship ecosystem, both public and private, at an international level.”\n\nBouchon highlighted the importance of this type of initiative to transform the economy and contribute to local society, as well as its potential to impact national and international industries.\n\nIn 2021, Chile was the first country in Latin America to tender the spectrum with national coverage for the 5G network, which then meant an improvement in terms of higher speed, data traffic, and digitization of various processes.\n\nThe launch of 5G was framed within a series of measures adopted by the Chilean government in connectivity, among which the National Fiber Optic, Southern Fiber Optic (south), Tarapacá Fiber Optic (north), and Connectivity for Education 2030 projects stand out."
        },
        {
          "role": "assistant",
          "content": "칠레, 5G 기술 개발 센터 건립...5G 주파수 사용 신규 허가도\n\n☐ 칠레 정부가 5G 기술 비즈니스 센터를 세우고 5G를 칠레 각 산업에 활용할 방법을 모색함. \n- 최근 칠레 재무부(Ministerio de Hacienda) 산하의 칠레생산개발공사(CORFO, Corporación de Fomento de la Producción de Chile)가 5G 기술 비즈니스 센터를 건립한다고 발표했음.\n- 해당 센터는 칠레 가톨릭대학(PUC, Pontificia Universidad Católica de Chile) 내에 설치되며, 5G 응용 기술을 비롯하여 5G 기술을 칠레 각 산업에서 조화롭게 사용할 방법을 강구함.\n- 호세 베나벤테(José Miguel Benavente) 칠레생산개발공사 부사장은 센터 건립을 계기로 5G 기술을 중소기업과 스타트업 기업에도 보급할 수 있는 길이 열리기를 희망한다고 말했음.\n\n☐ 칠레 정부는 5G 기술 개발을 위해 향후 6년 동안 1,100만 달러 이상을 투자할 방침임.\n- 칠레생산개발공사는 5G 기술이 헬스케어, 광업, 물류, 운송, 스마트시티 등 다양한 분야에 활용될 수 있는 잠재력을 지녔다고 언급했음.\n- 센터 건립 후 칠레 정부는 기술 개발에만 앞으로 6년간 1,100만 달러(한화 약 145억 원) 이상을 투입할 예정임.\n- 센터가 설립될 칠레 가톨릭대학도 5G가 혁신의 중심이 될 것이라고 하면서, 기술 개발에 대한 기대를 감추지 않았음.\n\n☐ 칠레 정부가 5G 사업자를 추가해 시장 경쟁을 강화하는 등 5G 시장 육성에 적극적으로 나서고 있음.\n- 칠레는 지난 2021년 중남미 국가로는 처음으로 5G 서비스를 정식으로 시작하는 등 5G 부문에서 주변국보다 한발 앞서가고 있음.\n- 최근 칠레 정부는 로컬 통신사 클라로(Claro)에 임시 5G 주파수를 할당하여 서비스를 시작할 수 있도록 했음.\n- 칠레 정부는 기존 세 곳이었던 5G 서비스 업체를 네 곳으로 늘리면 보다 공정한 시장 경쟁 구도가 조성되고, 이를 통해 건전한 성장이 가능할 것이라는 시장 감독 기구의 권고를 수용한 결정이라고 주파수 추가 할당 취지를 설명했음."
        },
        {
          "role": "user",
          "content": user_input
        }
      ],
      temperature=0.3,
      max_tokens=1200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].message.content
    

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
                        st.subheader(':black_nib: GPT 요약본')
                        st.markdown(past_results['result_1'])

    
    #
    # result
    #
    if submit:
        placeholder.empty()
        st.session_state['display'] = []
        if secret_key_user == secret_key:
                if all(len(input_value.strip()) > 0 for input_value in input_values):
                    with st.spinner('열심히 요약하고 있어요...'):
                        # Clear the previous results from the display before storing new ones
                        # Reset the display state
                        
                        # Store user inputs into session_state['user_input']
                        st.session_state['user_input'] = input_values
                        
                        temp_list = []
                        # Process each text using func_1, func_2, and func_3
                        for i, text in enumerate(st.session_state['user_input']):
                            gpt_summarized_text_en = summary_gpt(text)
                            with st.expander('{}번 기사 처리 결과'.format(str(i+1))):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.header(':newspaper: 입력글')
                                    st.divider()
                                    st.markdown(text)
                                
                                with col2:
                                    st.header(':printer: 결과')
                                    st.divider()
                                    st.subheader(':black_nib: GPT 요약본')
                                    st.markdown(gpt_summarized_text_en)
                                    

                            # Append results to display
                            st.session_state['display'].append({'user_input' : text,
                                                                'result_1' : gpt_summarized_text_en
                                                                })

                            # append to temp_list
                            temp_list.append([text,
                                            gpt_summarized_text_en
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
                    st.subheader(':black_nib: GPT 요약본')
                    st.markdown(result[1])
    else:
        st.write("No history yet.")


#
# hist_tab2 ------------------------------------------------------------------------------------------------------------------------------ #
