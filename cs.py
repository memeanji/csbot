import streamlit as st
import re

# 초기 세션 상태 설정
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'context' not in st.session_state:
    st.session_state['context'] = '메뉴선택'

# 비용이 많이 드는 작업을 캐시하기 위한 함수 (예시)
@st.cache_data
def expensive_computation():
    # 실제 계산 코드 또는 외부 데이터 불러오기
    result = "비싼 작업 결과 예시"
    return result

# CSS 스타일 추가
col1, col2 = st.columns([4, 1])

# 제목 스타일 CSS 삽입 (h1 태그 색 검정으로 강제)
st.markdown("""
<style>
h1 {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

with col1:
    st.markdown("<h1>📦 고객센터 챗봇</h1>", unsafe_allow_html=True)
st.markdown(
    """
<style>
    .chat-container {
        max-width: 700px;
        margin: auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .chat-message {
        padding: 12px;
        margin: 8px 0;
        border-radius: 20px;
        max-width: 70%;
        word-wrap: break-word;
        font-size: 16px;
        line-height: 1.4;
        display: inline-block;
    }
    .user-message {
        background-color: #F0F8FF;
        border-radius: 20px 20px 0px 20px;
        text-align: right;
        float: right;
        clear: both;
        padding: 10px;
        color: #000000;
    }
    .bot-message {
        background-color: #EAEAEA;
        border-radius: 20px 20px 20px 0px;
        text-align: left;
        float: left;
        clear: both;
        padding: 10px;
        color: black;
    }
    .chat-wrapper {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    details {
        background-color: #f8f9fa;
        padding: 10px;
        margin: 8px 0;
        border-radius: 8px;
        border: 1px solid #ddd;
        cursor: pointer;
    }
    summary {
        list-style: none;
        display: flex;
        align-items: center;
    }
    summary::-webkit-details-marker {
        display: none;
    }
    summary::before {
        content: "▶";
        color: red;
        margin-right: 10px;
        font-size: 16px;
        transition: transform 0.2s ease-in-out;
    }
    details[open] summary::before {
        content: "▼";
    }
    div.details {
        margin-top: -20px;
        margin-bottom: -20px;
        position: relative;
        top: -20px;
    }
    .container {
        margin-top: -20px;
    }
</style>

<div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px; text-align: center;margin-bottom: 20px;"> 
    📚 <b> Cs 상담 운영 안내</b><br>
    🕒 운영시간: 24시간 상담 가능 <br>
    📖 문의: 02-1234-1234
</div>

<details open style="margin-bottom: 20px;">  <!-- 여기 margin-bottom 추가 -->
    <summary><b>instacart 상담사 인사 및 메뉴</b></summary>
    <p>안녕하세요! 저는 instacart 상담사에요 🛒</p>
    <p>무엇을 도와드릴까요?</p>
    <ol>
        <li>주문 상태 확인</li>
        <li>배송 문의</li>
        <li>상품 정보</li>
        <li>교환/환불</li>
        <li>기타 문의</li>
    </ol>
</details>
    """,
    unsafe_allow_html=True
)

# 시나리오별 처리 함수들

def handle_order_status(user_input):
    if re.match(r'^\d{5,10}$', user_input):
        return f"주문 번호 {user_input}의 상태는 '배송 중'입니다. 추가로 도와드릴까요?\n(계속하려면 '메뉴' 또는 '종료'를 입력하세요.)", '주문상태완료'
    else:
        return "유효한 주문 번호를 입력해 주세요. (숫자 5~10자리)", '주문번호입력'

def handle_delivery_inquiry(user_input):
    options = {'1': '배송 지연 문의', 
               '2': '배송지 변경 요청',
             '3': '기타 배송 문의'}
     # 숫자만 추출 (ex. "1번", "2 번", "1. 배송" 등에서 숫자만 인식)
    cleaned_input = re.sub(r'\D', '', user_input.strip())

     # 숫자 우선 추출
    digits = re.sub(r'\D', '', cleaned_input)

    # 키워드 기반 간단 매칭
    if digits in options:
        keyword = options[digits]
        return f"{keyword}에 대해 도움을 드리겠습니다. 구체적으로 문의사항을 입력해 주세요.", '배송상세문의'
    elif '배송지' in cleaned_input or '변경' in cleaned_input:
        return "배송지 변경 요청에 대해 도움을 드리겠습니다. 구체적으로 문의사항을 입력해 주세요.", '배송상세문의'
    elif '지연' in cleaned_input:
        return "배송 지연 문의에 대해 도움을 드리겠습니다. 구체적으로 문의사항을 입력해 주세요.", '배송상세문의'
    elif '기타' in cleaned_input:
        return "기타 배송 문의에 대해 도움을 드리겠습니다. 구체적으로 문의사항을 입력해 주세요.", '배송상세문의'
    else:
        return "배송 문의 번호 또는 키워드를 다시 입력해 주세요:\n1. 배송 지연 문의\n2. 배송지 변경 요청\n3. 기타 배송 문의", '배송문의'




    if cleaned_input in options:
        keyword = options[cleaned_input]
        return f"{keyword}에 대해 도움을 드리겠습니다. 구체적으로 문의사항을 입력해 주세요.", '배송상세문의'
    
    return "배송 문의 번호 또는 키워드를 다시 입력해 주세요:\n1. 배송 지연 문의\n2. 배송지 변경 요청\n3. 기타 배송 문의", '배송문의'

def clean_user_input(user_input):
    return user_input.strip().replace('.', '').lower()

def chatbot_response(user_input):
    context = st.session_state.get('context', '메뉴선택')
    cleaned = clean_user_input(user_input)

    if context == '메뉴선택':
        if '상담원' in cleaned:
            return (
                "💬 상담원 연결을 요청하였습니다. 현재 상담원이 모두 통화 중입니다. "
                "잠시만 기다려 주세요. 또는 02-1234-5678로 직접 문의해 주세요. (메뉴/종료 입력 가능)"
            )
        elif '1' in cleaned or '주문' in cleaned:
            st.session_state['context'] = '주문번호입력'
            return "주문 번호를 입력해 주세요."
        elif '2' in cleaned or '배송' in cleaned:
            st.session_state['context'] = '배송문의'
            return "배송 관련 문의입니다.\n1. 배송 지연 문의\n2. 배송지 변경 요청\n3. 기타 배송 문의\n번호를 입력하세요."
        elif '3' in cleaned or '상품' in cleaned:
            return "상품 정보는 현재 준비 중입니다. 다른 메뉴를 선택해 주세요."
        elif '4' in cleaned or '환불' in cleaned or '교환' in cleaned:
            return "교환/환불 관련 문의는 고객센터로 연락해 주세요. 02-1234-5678"
        elif '5' in cleaned or '기타' in cleaned or 'faq' in cleaned:
            return "FAQ를 확인하시려면 'FAQ'를 입력하세요. 상담원 연결을 원하면 '상담원'을 입력하세요."
        else:
            return "메뉴 번호 또는 키워드를 입력해 주세요.\n1. 주문 상태 확인\n2. 배송 문의\n3. 상품 정보\n4. 교환/환불\n5. 기타 문의"


    elif context == '주문번호입력':
        if cleaned.isdigit() and 5 <= len(cleaned) <= 10:
            st.session_state['context'] = '주문상태완료'
            return f"주문 번호 {cleaned}의 상태는 '배송 중'입니다. 추가로 도와드릴까요?\n(계속하려면 '메뉴' 또는 '종료'를 입력하세요.)"
        else:
            return "유효한 주문 번호를 입력해 주세요. (숫자 5~10자리)"

    elif context == '주문상태완료':     
        if cleaned == '메뉴':
            st.session_state['context'] = '메뉴선택'
            return "메뉴로 돌아왔습니다.\n1. 주문 상태 확인\n2. 배송 문의\n3. 상품 정보\n4. 교환/환불\n5. 기타 문의"
        elif cleaned in ['아니요', '없음', '아니', '아니에요', '그만']:
            return "도움이 더 필요하시면 언제든 말씀해 주세요. '메뉴' 또는 '종료'를 입력해 주세요."
        else:
            return "계속 도와드릴까요? '메뉴' 또는 '종료'를 입력해 주세요."
        
    elif context == '배송문의':
        reply, next_context = handle_delivery_inquiry(user_input)
        st.session_state['context'] = next_context
        return reply

    elif context == '배송상세문의':
        if cleaned in ['메뉴', '종료']:
            if cleaned == '메뉴':
                st.session_state['context'] = '메뉴선택'
                return "메뉴로 돌아왔습니다.\n1. 주문 상태 확인\n2. 배송 문의\n3. 상품 정보\n4. 교환/환불\n5. 기타 문의"
            else:
                return "상담을 종료합니다. 감사합니다!"
        else:
            # 사용자 입력 강조 + 자연스러운 안내
            return f"📦 배송지 변경 요청 내용:\n ➡️ {user_input.strip()}\n요청이 정상적으로 접수되었습니다. 담당자가 확인 후 순차적으로 처리해 드릴 예정입니다.\n(메뉴/종료 입력 가능)"

# 이전 대화 출력
for msg in st.session_state['messages']:
    role_class = "user-message" if msg["role"] == "user" else "bot-message"
    st.markdown(f'<div class="chat-message {role_class}">{msg["text"]}</div>', unsafe_allow_html=True)

# 사용자 입력 폼
if user_input := st.chat_input("메시지를 입력하세요..."):
    st.session_state['messages'].append({"role": "user", "text": user_input})
    response = chatbot_response(user_input)
    st.session_state['messages'].append({"role": "bot", "text": response})
    st.rerun()
