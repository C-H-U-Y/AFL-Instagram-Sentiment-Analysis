comments = open("../comment harvesting/comments.csv", "r", encoding="utf-8").read()

games = comments.split("\n")[:-1]

# 1. total number of comments
num_comments = 0

# 2. number of comments about umps
ump_comments = 0

# 3. number of games with ump comments
total_games = 0
games_commented_on = 0

num_games_majority_umps_comments = 0

for game in games:
    # game has umpire comment
    game_has_umpire_comment = False

    # majority comments
    majority_ump_comments = False

    # increment games
    total_games += 1

    # extract data
    image = game.split(".png,")[0]
    comment_data = game.split(".png,")[1]
    game_comments = comment_data.split(";")
    
    # add to total comments
    num_comments += len(game_comments)
    
    number_of_games_comments = 0
    number_of_games_umpire_comments = 0
    
    # detect umpire comments
    for comment in game_comments:
        number_of_games_comments += 1

        comment = comment.lower()
        if(
            ("umpir" in comment) or 
            ("umps" in comment) or 
            ("yellow" in comment) or 
            (("green" in comment) and not (("greene" in comment) or ("tom" in comment)))
        ):
            ump_comments += 1
            game_has_umpire_comment = True
            number_of_games_umpire_comments += 1

            print(comment)
    
    if((number_of_games_umpire_comments/number_of_games_comments) >= 0.25):
        num_games_majority_umps_comments += 1
    
    if(game_has_umpire_comment):
        games_commented_on += 1


print("\n\n==================================================================")
print("Regarding AFL 'match results' instagram posts from round 2 onwards")
print("==================================================================")
print("{} percent of 'top comments' speculated about umpires".format(round(((ump_comments/num_comments)*100), 2)))
print("{} percent of games had an umpire related 'top comment'".format(round(((games_commented_on/total_games)*100), 2)))
print("[1 in 4] comments where umpire related in {} games".format(num_games_majority_umps_comments))


print(total_games)