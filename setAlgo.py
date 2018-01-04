# women_ranking = {
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
# men_ranking = {
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

women_ranking = {
    'angelica': {
        'alejandro': 3,
        'bernardo': 2,
        'camilo': 4,
        'diego': 1
    },
    'blanca': {
        'alejandro': 3,
        'bernardo': 4,
        'camilo': 1,
        'diego': 2
    },
    'clara': {
        'alejandro': 4,
        'bernardo': 2,
        'camilo': 1,
        'diego': 3
    },
    'diana': {
        'alejandro': 1,
        'bernardo': 2,
        'camilo': 3,
        'diego': 4
    }
}

men_ranking = {
    'alejandro': {
        'angelica' : 3,
        'blanca' : 2,
        'clara' : 4,
        'diana' : 1
    },
    'bernardo' : {
        'angelica' : 4,
        'blanca' : 2,
        'clara' : 1,
        'diana' : 3
    },
    'camilo' : {
        'angelica' : 4,
        'blanca' : 2,
        'clara' : 3,
        'diana' : 1
    },
    'diego' : {
        'angelica' : 4,
        'blanca' : 3,
        'clara' : 2,
        'diana' : 1
    }
}



tentative_engagements = []

free_proposer = []
proposer_ranking = {}
recipient_ranking = {}
proposer = 'women'
def set_proposer_recipient(proposer):
    global proposer_ranking
    global recipient_ranking
    # set who is the proposer and who is the recipient
    if (proposer == 'men'):
        proposer_ranking = men_ranking
        recipient_ranking = women_ranking
    elif(proposer == 'women'):
        proposer_ranking = women_ranking
        recipient_ranking = men_ranking
    return proposer_ranking, recipient_ranking


def all_proposer():
    # get the list of proposer's names
    print('inside all proposer')
    print('proposer_ranking %s'%(proposer_ranking))
    for person in proposer_ranking:
        free_proposer.append(person)


def another_iteration_step():
    print('indide another_iteration_step')
    #run the algorithm until there is no single proposer.
    while(len(free_proposer) > 0):
        for person in free_proposer:
            begin_matching(person)

def begin_matching(actual_proposer):
    print('dealing with %s'%(actual_proposer))

    option = 1
    single = True

    # quiero regresar a la for loop si la persona no se le ha propuesto a nadie
    while single:
        # continue iteraiting until the person is match
        for recipient, rank in proposer_ranking[actual_proposer].items():
            print('we are looking for the option %s'%(option))
            if(rank == option ):
                # n = n + 1
                already_match = [ couple for couple in tentative_engagements if recipient in couple]
                print('this is already_match %s'%(already_match))
                if(len(already_match) == 0 ):
                    print('the option num %s'%(option-1))
                    print('is avaliable for %s'%(actual_proposer))
                    tentative_engagements.append([actual_proposer, recipient])
                    free_proposer.remove(actual_proposer)
                    # I want to break the full for loop.
                    single = False
                    print (tentative_engagements)
                    break
                elif(len(already_match) > 0):
                        current_match = recipient_ranking[recipient][already_match[0][0]]
                        this_match = recipient_ranking[recipient][actual_proposer]
                        if(current_match < this_match):
                            print('she is satisifed with %s..'%(already_match[0][0]))
                            option = option + 1
                            print (tentative_engagements)
                            break
                        else:
                            print('she prefers the man that we are evaluationg')
                            free_proposer.remove(actual_proposer)
                            free_proposer.append(already_match[0][0])
                            print('here we change the tentative match')
                            print('tentative_engagements before %s'%(tentative_engagements))
                            already_match[0][0] = actual_proposer
                            print('tentative_engagements after the change %s'%(tentative_engagements))
                            single = False
                            print (tentative_engagements)
                            break




def main():
    # proposer = 'men '
    set_proposer_recipient(proposer)
    all_proposer()
    another_iteration_step()
    print (tentative_engagements)


main()
