def read_entrants(file_name):
    students = []
    with open(file_name, 'r') as file:
        for line in file:
            s = line.strip('\n').split()
            students.append({'name': s[0],
                             'last name': s[1],
                             'best mark': None,
                             'exams': {'physics': float(s[2]), 'chemistry': float(s[3]), 'math': float(s[4]),
                                       'computer science': float(s[5]), 'admission exam': float(s[6])},
                             'departments': s[7:]})
    return students


def get_departments():
    return {'Biotech': {'applicants': [], 'exams': ['chemistry', 'physics']},
            'Chemistry': {'applicants': [], 'exams': ['chemistry']},
            'Engineering': {'applicants': [], 'exams': ['computer science', 'math']},
            'Mathematics': {'applicants': [], 'exams': ['math']},
            'Physics': {'applicants': [], 'exams': ['physics', 'math']}}


def calculate_best_mark(exams, marks):
    exams_mark = sum([v for k, v in marks.items() if k in exams]) / len(exams)
    return max(marks['admission exam'], exams_mark)


def choose_applicants(applicant_quota, applicants):
    university = get_departments()

    for i in range(3):
        departments_candidates = get_departments()
        # sort applicants by preferred department
        for applicant in applicants:
            applicant_dep = applicant['departments'][i]
            chooses_dep = departments_candidates[applicant_dep]
            applicant_exams = applicant['exams']
            department_exams = chooses_dep['exams']
            applicant['best mark'] = calculate_best_mark(department_exams, applicant_exams)
            chooses_dep['applicants'].append(applicant)
        # Allocate applicants to departments
        for department_name, attributes in departments_candidates.items():
            department = university[department_name]['applicants']
            candidates = attributes['applicants']
            selection_bias = lambda s: (-s['best mark'], s['name'], s['last name'])

            candidates.sort(key=selection_bias)
            if len(department) < applicant_quota:
                if len(candidates) > applicant_quota - len(department):
                    department.extend(candidates[: applicant_quota - len(department)])
                else:
                    department.extend(candidates)

            department.sort(key=selection_bias)
        # remove entered applicants
        for department in university.values():
            for applicant in department['applicants']:
                if applicant in applicants:
                    applicants.remove(applicant)

        departments_candidates.clear()
    return university


def print_applicants(applicants):
    for department_name, department in applicants.items():
        print(department_name)
        entered = department['applicants']
        for person in entered:
            print(f"{person['name']} {person['last name']} {person['best mark']}")
        print()


def write_files(applicants):
    for department_name, department in applicants.items():
        with open(f'{department_name.lower()}.txt', 'w', encoding='utf-8') as file:
            entered = department['applicants']
            for person in entered:
                file.write(f"{person['name']} {person['last name']} {person['best mark']}\n")


def go():
    applicant_quota = int(input())
    applicants = read_entrants('./applicant_list_7.txt')
    entered_applicants = choose_applicants(applicant_quota, applicants)
    print_applicants(entered_applicants)
    write_files(entered_applicants)


go()
