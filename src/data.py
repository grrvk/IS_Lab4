import random
from src.scheme import *


GROUPS = [Group('МІ-41', 20),
          Group('МІ-42', 22),
          Group('ТК-41', 18),
          Group('ТТП-41', 30),
          Group('ТТП-42', 28)]

AUDITORIUMS = [Auditorium('43', 60),
               Auditorium('235', 30),
               Auditorium('705', 25),
               Auditorium('704', 20),
               Auditorium('233', 30),
               Auditorium('221', 35),
               Auditorium('306', 27),
               Auditorium('204', 30),
               Auditorium('303', 35),
               Auditorium('308', 40),
               Auditorium('309', 25),
               Auditorium('3', 22)]

TEACHERS = [Teacher('Пашко', ['Статистичне моделювання в задачах штучного інтелекту'],
                    ['Лекція'], 20),
            Teacher('Вергунова', ['Складність алгоритмів'],
                    ['Лекція'], 20),
            Teacher('Бобиль', ['Нейронні мережі'],
                    ['Лекція', 'Практика'], 20),
            Teacher('Закала', ['Нейронні мережі'],
                    ['Практика'], 20),
            Teacher('Мащенко', ['Теорія прийняття рішень'],
                    ['Лекція'], 20),
            Teacher('Зінько', ['Теорія прийняття рішень'],
                    ['Практика'], 20),
            Teacher('Тарануха', ['Інтелектуальні системи', 'Основи комп. лінгвістики'],
                    ['Лекція'], 20),
            Teacher('Федорус', ['Інтелектуальні системи'],
                    ['Практика'], 20),
            Teacher('Мисечко', ['Інтелектуальні системи'],
                    ['Практика'], 20),
            Teacher('Ткаченко', ['Інформаційні технології'],
                    ['Лекція'], 20),
            Teacher('Терещенко', ['Інформаційні технології'],
                    ['Практика'], 20),
            Teacher('Свистунов', ['Інформаційні технології'],
                    ['Практика'], 20)
            ]

subject_and_type = {}

for teacher in TEACHERS:
    for subject in teacher.subject_taught:
        if not subject in subject_and_type.keys():
            subject_and_type[subject] = [teacher.subject_type[0]]
        else:
            subject_and_type[subject].append(teacher.subject_type[0])
            subject_and_type[subject] = list(set(subject_and_type[subject]))

subject_and_type_list = []
for key, value in subject_and_type.items():
    subject_and_type_list.append((key,value))
SUBJECTS = []

for group in GROUPS:
    subjects_and_types = random.sample(subject_and_type_list, int(len(subject_and_type_list)*0.6))
    for sat in subjects_and_types:
        if len(sat[1]) == 1:
            SUBJECTS.append(Subject(sat[0], group, 2, 0))
        else:
            SUBJECTS.append(Subject(sat[0], group, 2, 2))

TIMESLOTS = ['08:40', '10:35', '12:20']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
