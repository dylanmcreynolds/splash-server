# import vakt
# from vakt import Policy, ALLOW_ACCESS

# from vakt.rules import (
#     CIDR,
#     Any,
#     Eq,
#     NotEq,
#     In,
#     StartsWith,
#     And,
#     Greater,
#     Less,
#     SubjectMatch
# )
# # policy = vakt.Policy(
# #     123456,
# #     actions=[Eq('fork'), Eq('clone')],
# #     resources=[StartsWith('repos/Google', ci=True)],
# #     subjects=[{'name': Any(), 'stars': And(Greater(50), Less(999))}],
# #     effect=vakt.ALLOW_ACCESS,
# #     context={'referer': Eq('https://github.com')},
# #     description="""
# #     Allow to fork or clone any Google repository for
# #     users that have > 50 and < 999 stars and came from Github
# #     """
# # )


# def test_vakt():
#     policy_view_teams_runs = vakt.Policy(
#         1,
#         description="""
#             Users can view runs if they are a member of a team with
#             team field in resource equal to team name. Team will be
#         """,
#         actions=[Eq('view')],
#         resources=[{'team': SubjectMatch()}],
#         effect=vakt.ALLOW_ACCESS,   
#     )

#     storage = vakt.MemoryStorage()
#     storage.add(policy)
#     guard = vakt.Guard(storage, vakt.RulesChecker())

#     inq = vakt.Inquiry(action='fork',
#                     resources={"team_id": ['lotto']},
#                     subject={'name': 'larry', 'teams': ['lotto', 'quick_step']}

#     assert guard.is_allowed(inq)
