from tkinter import *
import math, random
from collections import defaultdict, Counter
import numpy as np

'''
데이터를 입력하고 추천받기 버튼을 누르면 추천해주는 프로그램 제작
데이터 : 저장 방식은 현재 변수에만 저장, 추후에나 db나 외부파일에 저장하는 방식으로 변경
'''


# 윈도우 창 만들기
root = Tk()

root.title("추천 시스템 시뮬레이터")
root.configure(width = "100m", height = "120m")

# global 선언받을 전역변수들 만들기
user_interests = {}
unique_interests = []

# 변수에 명목상 아무 값이나 넣음.
select1 = ""
select2 = ""
select3 = ""
regionresult = ""


# 더미 데이터

def set_dummy():
	global user_interests, unique_interests
	user_interests = {
		"김철수" : ['서울', '뉴욕', '파리', '쿤밍', '로스앤젤레스', '방콕', '호치민'],
		"신세계" : ['니스', '베를린', '호치민', '파리', '런던'],
		"박지구" : ['암스테르담', '프라하', '아다스아바바', '상파울루', '리마', '토론토'],
		"홍미국" : ['카이로', '암스테르담', '케이프타운', '로마', '상트페테르부르크'],
		"최유럽" : ['부산', '로마', '상하이', '두바이'],
		"곽아프리카" : ['암스테르담', '제주도', '쿤밍', '이스탄', '남극', '시드니'],
		"최독일" : ['케이프타운', '상트페테르부르크', '퍼스', '베이징'],
		"나북한" : ['부산', '프라하', '전주', '치앙마이'],
		"김남한" : ['치앙마이', '다낭', '뉴욕', '시애틀'],
		"이프라하" : ['서울', '쿤밍', '바르샤바', '뉴욕'],
		"박영희" : ['케이프타운', '카이로', '리마'],
		"소가나" : ['이스탄불', '다낭', '시애틀', '상트페테르부르크'],
		"한민족" : ['토론토', '카이로', '암스테르담'],
		"기차표" : ['헬싱키', '파리', '런던', '칸쿤', '베를린'],
		"표창장" : ['두바이', '로마', '제주도'],
		"test123" : ['서울', '쿤밍', '바르샤바'],
		"이기상" : ['뉴욕', '치앙마이', '시애틀']
	}
	set_unique_interests()

	L1.delete(0, END)
	L2.delete(0, END)
	L3.delete(0, END)

	idx = 0
	for user in user_interests:
		L1.insert(idx, user)
		idx += 1

	idx = 0
	for region in unique_interests:
		L2.insert(idx, region)

# 더미 데이터 사용하고 싶을 때 누르는 버튼
Bt0 = Button(root, text = "더미 데이터 사용", command = set_dummy)
Bt0.place(x = 130, y = 10, width = 100, height = 30)

# 사용자가 선택한 요소 전체 목록 출력
# sorted는 중복요소느 몇 개던 하나로 치환해 계산

def set_unique_interests():
	global unique_interests
	unique_interests = sorted(list({interest
	                                for user_interests in user_interests.values()
	                                for interest in user_interests}))

# listbox를 클릭했을 때 클릭된 요소를 감지해 변수에 저장
def onselect1(evt):
	global select1
	w = evt.widget
	index = w.curselection()
	value = w.get(index)
	select1 = value
	select_noselect()
	print(select1)

def onselect2(evt):
	global select2
	w = evt.widget
	index = w.curselection()
	value = w.get(index)
	select2 = value
	print(select2)

def onselect3(evt):
	global select3
	w = evt.widget
	index = w.curselection()
	value = w.get(index)
	select3 = value
	print(select3)

# 코사인 유사도 구하는 함수
def cosine_similarity(v, w):
	return np.dot(v, w) / math.sqrt(np.dot(v, v) * np.dot(w, w))


# 1. 유저 베이스 추천 : 유저별 선택/미선택 지역 분류 리스트 만들기
# 관심이 있다고 한 경우 1, 아닌 경우 0

def make_user_interest_vector(user_interests):
	return [1 if interest in user_interests else 0
	        for interest in unique_interests]

# unique_interest[키값}에 해당하는 요소가 관심사에 있으면 1, 없으면 0으로 자료 생성
def get_user_interest_matrix():
	user_interests_matrix = list(map(make_user_interest_vector, user_interests.values()))
	return user_interests_matrix


# 최종적으로 이 함수만 호출해도 위 2개가 자동 호출됨!
# 코사인 유사도를 통해서 한 아이템이 선택되었을 때 다른 아이템이 같이 선택되는 빈도를 통해 연관도 집계

def get_user_similarities():
	user_similarities = [[cosine_similarity(interest_vector_i, interest_vector_j)
	                      for interest_vector_j in get_user_interest_matrix()]
	                     for interest_vector_i in get_user_interest_matrix()]
	return user_similarities

def most_similar_users_to(user_id):
	pairs = [(other_user_id, similarity)
	         for other_user_id, similarity in enumerate(get_user_similarities()[user_id])
	         if user_id != other_user_id and similarity > 0]
	return sorted(pairs,
	              key = lambda pair : pair[1],
	              reverse = True)

# 모든 유사도를 더했을 때 가장 높은 유사도 총합을 갖는 유저의 자료를 추천해주는 함수
def user_based_suggestion(include_current_interest = False):
	global regionresult
	suggestions = defaultdict(float)
	user_idx = list(user_interests).index(select1)
	for other_user_id, similarity in most_similar_users_to(user_idx):
		for interest in user_interests[list(user_interests)[other_user_id]]:
			suggestions[interest] += similarity

	suggestions = sorted(suggestions.items(),
	                     key = lambda pair: pair[1],
	                     reverse = True)

	if include_current_interest:
		regionresult = suggestions
		print(regionresult)
	else:
		regionresult = [(suggestion, weight)
		                for suggestion, weight in suggestions
		                if suggestion not in user_interests[select1]]

	idx = 0
	L4.delete(0, END)
	for suggested_region in regionresult[:5]:
		print(suggested_region)
		L4.insert(0, suggested_region[0])
		idx += 1

# 2. 아이템 기반 추천

# 하나의 아이템에 관심을 표한 사용자는 1, 아니면 0
def get_interest_user_matrix():
	intererst_user_matrix = [[user_interest_vector[j]
	                          for user_interest_vector in get_user_interest_matrix()]
	                         for j, _ in enumerate(unique_interests)]
	return intererst_user_matrix

# 아이템 간 코사인 유사도 적용. 이 아이템에 관심있는 사용자가 나머지 아이템에도 관심이 있는가 없는가.
def get_interest_similarities():
	interest_similarities = [[cosine_similarity(user_vector_i, user_vector_j)
	                          for user_vector_j in get_interest_user_matrix()]
	                         for user_vector_i in get_interest_user_matrix()]
	return interest_similarities

# 특정 아이템을 선택하면 그 아이템과 함께 가장 많이 선택된 다음 아이템 선택
def most_similar_interests_to(interest_id):
	similarities = get_interest_similarities()[interest_id]

	pairs = [(unique_interests[other_user_id], similarity)
	         for other_user_id, similarity in enumerate(similarities)
	         if interest_id != other_user_id and similarity > 0]

	return sorted(pairs,
	              key = lambda pair : pair[1],
	              reverse = True)

def item_based_suggestion(include_current_interest = False):
	suggestions = defaultdict(float)
	user_idx = list(user_interests).index(select1)
	user_interest_vector = get_user_interest_matrix()[user_idx]

	for interest_id, is_interested in enumerate(user_interest_vector):
		if is_interested == 1:
			similar_interests = most_similar_interests_to(interest_id)

			for interest, similarity in similar_interests:
				suggestions[interest] += similarity

	suggestions = sorted(suggestions.items(),
	                     key = lambda pair : pair[1],
	                     reverse = True)

	if include_current_interest:
		regionresult = suggestions
		print(regionresult)
	else:
		regionresult = [(suggestion, weight)
		                for suggestion, weight in suggestions
		                if suggestion not in user_interests[select1]]
		print(regionresult)

	idx = 0
	L4.delete(0, END)
	for suggested_region in regionresult[:5]:
		L4.insert(idx, suggested_region[0])
		idx += 1



# 특정 유저 클릭 시 그 유저가 선택한 목록은 L3로, 선택하지 않은 것만 L2에 남겨두는 함수
def select_noselect():
	l2idx = 0
	l3idx = 0
	L2.delete(0, END)
	L3.delete(0, END)

	for region in unique_interests:
		if region in user_interests[select1]:
			L3.insert(l3idx, region)
			l3idx += 1
		else:
			L2.insert(l2idx, region)
			l2idx += 1


def insert_user():
	username = E1.get()
	user_interests[username] = []
	L1.delete(0, END)
	idx = 0
	for user in user_interests:
		L1.insert(idx, user)
		idx += 1

# 버튼 1 -> 유저 베이스 결과 얻기
Bt1 = Button(root, text = "사용자기반 추천받기", command = user_based_suggestion)
Bt1.place(x = 50, y = 250, width = 120, height = 30)

# 버튼 2 -> 아이템 베이스 결과 얻기
Bt2 = Button(root, text = "장소 기반 추천받기", command = item_based_suggestion)
Bt2.place(x = 200, y = 250, width = 120, height = 30)

# 버튼 3 -> 유저 정보 추가 버튼
Bt3 = Button(root, text = "사용자 추가하기", command = insert_user)
Bt3.place(x = 200, y = 300, width = 120, height = 30)

Bt4 = Button(root, text = "추가")
Bt4.place(x = 240, y = 130, width = 30, height = 40)

Bt5 = Button(root, text = "삭제")
Bt5.place(x = 240, y = 190, width =30, height = 40)

# 리스트 박스
L1 = Listbox(root)
L1.bind("<<ListboxSelect>>", onselect1)
L1.place(x = 10, y = 100, width = 100, height = 150)

L2 = Listbox(root)
L2.bind("<<ListboxSelect>>", onselect2)
L2.place(x = 140, y = 100, width = 100, height = 150)

L3 = Listbox(root)
L3.place(x = 270, y = 100, width = 100, height = 150)
L3.bind("<<ListboxSelect>>", onselect3)

L4 = Listbox(root)
L4.place(x = 35, y = 360, width = 300, height = 80)

#엔트리
E1 = Entry(root)
E1.place(x = 50, y = 300, width = 120, height = 30)

#레이블
Lb1 = Label(root, text = "등록 유저 목록")
Lb1.place(x = 10, y = 70, width = 100, height = 30)

Lb2 = Label(root, text = "등록 여행지 목록")
Lb2.place(x = 140, y = 70, width = 100, height = 30)

Lb3= Label(root, text = "선택 여행지 목록")
Lb3.place(x = 270, y = 70, width = 100, height = 30)

Lb4 = Label(root, text = "추천 여행지 목록")
Lb4.place(x = 120, y = 340, width = 120, height = 20)


root.mainloop()
