# ranking_women = {
#     'angelica': {
#         'alejandro': 1,
#         'bernardo': 2,
#         'camilo': 3,
#         'diego': 4
#     },
#     'blanca': {
#         'alejandro': 3,
#         'bernardo': 1,
#         'camilo': 2,
#         'diego': 4
#     },
#     'clara': {
#         'alejandro': 1,
#         'bernardo': 2,
#         'camilo': 3,
#         'diego': 4
#     },
#     'diana': {
#         'alejandro': 2,
#         'bernardo': 1,
#         'camilo': 4,
#         'diego': 3
#     }
# }
#
# ranking_men = {
#     'alejandro': {
#         'angelica' : 1,
#         'blanca' : 2,
#         'clara' : 3,
#         'diana' : 4
#     },
#     'bernardo' : {
#         'angelica' : 1,
#         'blanca' : 2,
#         'clara' : 4,
#         'diana' : 3
#     },
#     'camilo' : {
#         'angelica' : 2,
#         'blanca' : 4,
#         'clara' : 1,
#         'diana' : 3
#     },
#     'diego' : {
#         'angelica' : 2,
#         'blanca' : 1,
#         'clara' : 3,
#         'diana' : 4
#     }
# }

ranking_women = {
    'angelica': {
        'alejandro': 1,
        'bernardo': 2,
        'camilo': 3,
        'diego': 4
    },
    'blanca': {
        'alejandro': 3,
        'bernardo': 1,
        'camilo': 2,
        'diego': 4
    },
    'clara': {
        'alejandro': 4,
        'bernardo': 2,
        'camilo': 3,
        'diego': 1
    },
    'diana': {
        'alejandro': 3,
        'bernardo': 4,
        'camilo': 1,
        'diego': 2
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
        'diana' : 3
    },
    'camilo' : {
        'angelica' : 1,
        'blanca' : 2,
        'clara' : 4,
        'diana' : 3
    },
    'diego' : {
        'angelica' : 4,
        'blanca' : 1,
        'clara' : 2,
        'diana' : 3
    }
}




tentative_engagements = []

free_men = []

def all_men():
    for man in ranking_men:
        free_men.append(man)

def another_iteration_step():
    m = 0
    while(len(free_men) > 0 and m < 15):
        for man in free_men:
            m+=1
            begin_matching(man)

def begin_matching(man):
    print('this are the free men')
    print(free_men)
    print('dealing with %s'%(man))

    n = 1
    single = True

    # quiero regresar a la for loop si la persona no se le ha propuesto a nadie
    while single:
        for name, value in ranking_men[man].items():
            print('we are looking for the option %s'%(n))
            if(value == n ):
                # n = n + 1
                already_match = [ couple for couple in tentative_engagements if name in couple]
                print('this is already_match %s'%(already_match))
                if(len(already_match) == 0 ):
                    print('the option num %s'%(n-1))
                    print('is avaliable for %s'%(man))
                    tentative_engagements.append([man, name])
                    free_men.remove(man)
                    print(tentative_engagements)
                    # I want to break the full for loop.
                    single = False
                    break
                elif(len(already_match) > 0):
                        current_match = ranking_women[name][already_match[0][0]]
                        this_match = ranking_women[name][man]
                        if(current_match < this_match):
                            print('she is satisifed with %s..'%(already_match[0][0]))
                            n = n + 1
                            break
                        else:
                            print('she prefers the man that we are evaluationg')
                            free_men.remove(man)
                            free_men.append(already_match[0][0])
                            print('here we change the tentative match')
                            print('tentative_engagements before %s'%(tentative_engagements))
                            already_match[0][0] = man
                            print('tentative_engagements after the change %s'%(tentative_engagements))
                            single = False
                            break




def main():
    all_men()
    another_iteration_step()
    print (tentative_engagements)

main()
