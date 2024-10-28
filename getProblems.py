import requests
from random import shuffle

PROBLEMS_LINK = "https://codeforces.com/api/problemset.problems"
USER_SOLVED_PROBLEMS_LINK = "https://codeforces.com/api/user.status?handle="

def get_problems_by_rating(desired_rating):

    url = PROBLEMS_LINK
    response = requests.get(url)
    problems = response.json()

    if problems['status'] != 'OK':
        raise Exception("Failed to fetch problems from Codeforces API")

    filtered_problems = [
        problem for problem in problems['result']['problems']
        if 'rating' in problem and problem['rating'] == desired_rating
    ]
    
    return filtered_problems

def get_solved_problems(user_handle):

    url = USER_SOLVED_PROBLEMS_LINK + user_handle
    response = requests.get(url)
    submissions = response.json()

    if submissions['status'] != 'OK':
        raise Exception("Failed to fetch submissions from Codeforces API")

    solved_problems = set()
    for submission in submissions['result']:
        if submission['verdict'] == 'OK':
            problem = submission['problem']
            problem_id = (problem['contestId'], problem['index'])
            solved_problems.add(problem_id)
    
    return solved_problems


def get_problems(codeforcesUsers, rating, problemsNumber):

    problems_by_ratng = get_problems_by_rating(rating)
    shuffle(problems_by_ratng)

    solved_map = {}

    for user in codeforcesUsers:

        user_problems = get_solved_problems(user)
        user_map = {}
        
        for solved_problem in user_problems:
            user_map[str(solved_problem[0]) + solved_problem[1]] = 1
        
        solved_map[user] = user_map
    
    final_problemset = []
    
    for problem in problems_by_ratng:
        
        if (len(final_problemset) == problemsNumber):
            break

        problem_contest_id = str(problem["contestId"])
        problem_index = problem["index"]
        problem_id = problem_contest_id + problem_index

        for user in solved_map:
            if problem_id in user:
                break
        else:
            final_problemset.append(f"https://codeforces.com/contest/{problem_contest_id}/problem/{problem_index}")

    return final_problemset
