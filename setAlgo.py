ranking_women = {
    'angelica': {
        'alejandro': 2,
        'bernardo': 1,
        'camilo': 3,
        'diego': 4
    },
    'blanca': {
        'alejandro': 2,
        'bernardo': 3,
        'camilo': 4,
        'diego': 1
    },
    'clara': {
        'alejandro': 1,
        'bernardo': 2,
        'camilo': 3,
        'diego': 4
    },
    'diana': {
        'alejandro': 2,
        'bernardo': 1,
        'camilo': 4,
        'diego': 3
    }
}

ranking_men = {
    'alejandro': {
        'angelica' : 1,
        'blanca' : 2,
        'clara' : 3,
        'diana' : 4
    },
    'bernardo' : {
        'angelica' : 1,
        'blanca' : 2,
        'clara' : 4,
        'diana' : 4
    },
    'camilo' : {
        'angelica' : 3,
        'blanca' : 4,
        'clara' : 2,
        'diana' : 2
    },
    'diego' : {
        'angelica' : 2,
        'blanca' : 1,
        'clara' : 3,
        'diana' : 4
    }
}





tentative_engagements = []

free_men = []

def all_men():
    for man in ranking_men:
        free_men.append(man)

def another_iteration_step():
    while(len(free_men) > 0):
        for man in free_men:
            begin_matching(man)

def begin_matching(man):
    print('dealing with %s'%(man))
    n = 1
    for name, value in ranking_men[man].items():
        if(value == n ):
            already_match = [ couple for couple in tentative_engagements if name in couple]
            if(len(already_match) == 0 ):
                tentative_engagements.append([man, name])
                free_men.remove(man)
                break
            else:
                current_match = ranking_women[women][already_match[0][0]]
                this_match = ranking_women[women][men]

                if(current_match < this_match):
                    print('she is satisifed with %s..'%(taken_match[0][0]))
                    n += 1
                else:
                    print('she prefers the man that we are evaluationg')
                    free_men.remove(man)
                    free_men.append(already_match[0][0])
                    already_match[0][0] = man
                    break

def main():
    all_men()
    another_iteration_step()
    print (tentative_engagements)

main()
