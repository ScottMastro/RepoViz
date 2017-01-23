alg_list = ["lc", "mc", "hc", "i", "d"]

def alg(maxi, i, choice):
    if choice == 'lc':
        return 10
    if choice == 'mc':
        return 50
    if choice == 'hc':
        return 90
    if choice == 'i':
        return (int)(100*(i/float(maxi)))
    if choice == 'd':
        return (int)(100 - 100*(i/float(maxi)))
    assert(false)

def main():
    words = raw_input("Enter top words, separated by commas: ")
    word_list = words.replace(" ","").split(",")
    num_words = len(word_list)
    word_history = []
    print "Your choices for commit history algorithm: low constant [lc], medium constant [mc], high constant [hc], increasing [i], and decreasing [d]"
    for i in range(0, num_words):
        algorithm = None
        while algorithm is None:
            algorithm = raw_input("Algorithm for word {0}: ".format(word_list[i]))
            if (algorithm not in alg_list):
                print("Invalid algorithm. Try again.")
                algorithm = None
        word_history.append(algorithm)
        
    num_days = int(raw_input("Enter number of days: "))
    file_name = raw_input("Enter name of file to write: ")
    f = open(file_name, 'w')
    f.write("gitstats\n")
    for day in range(0, num_days):
        f.write("%	2007-07-{0}\n".format(day))
        for word in range(0, num_words):
            num_commits = alg(num_days, day, word_history[word])
            f.write("{0} {1}\n".format(word_list[word], num_commits))
    f.close()
    print "wrote fake gitstats to {0}".format(file_name)
            

if __name__ == "__main__":
    main()
