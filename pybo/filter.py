# datetime 객체를 보기 편한 문자열로 만들 수 있는 템플릿 필터를 적용
# format_datetime 함수는 1번째 매개변수 value로 전달받은 datetime 객체를 2번째 매개변수의 날짜 형식으로 변환하는 함수이다.
# 현재 매개변수 fmt에는 기본값으로 '%Y년 %m월 %d일 %H:%M'을 지정해서 fmt에 아무 값도 넘어오지 않을 경우에는
# 기본 처리를 할 수 있도록 만들었다
def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)