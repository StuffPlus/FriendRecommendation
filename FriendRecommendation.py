# class for the person inside the network
class Person:
    def __init__(self, name):
        self._name = name
        self._friends = []

    def __str__(self):
        return f"{self._name} -> {self._friends}"

    def get_name(self):
        return self._name  # return the name of the person

    def get_friends(self):
        return self._friends  # return friends of a person

    def get_friends_count(self):
        return len(self._friends)  # return the number of friends a person has

    def add_friend(self, name):
        if self._friends.count(name) == 0:  # stop duplication of friends
            self._friends.append(name)

    def remove_friend(self, name):
        if self._friends.count(name) != 0:  # remove friend from a person
            self._friends.remove(name)

    def is_friends_with(self, name):
        return name in self._friends  # return a person that is friends with the person

    # class of the network
    # Handles the creation and manipulation of the social network


class SocialNetwork:
    def __init__(self, size):
        self._size = size
        self._people = {}

    # get size of network
    def get_network_size(self):
        return len(self._people)  # Get number of people inside the network

    # Get everyone in the network
    def get_list_of_members(self):
        return self._people  # Get the list of names inside the network

    # Add a new person the network
    def add_person(self, new_person):
        if not self.find_member(new_person):
            self._people[new_person] = Person(new_person)  # Add a new object into the person Class
        return self._people[new_person]

    # Find the member in the network
    def find_member(self, member_name):
        try:
            return self._people[member_name]  # Check if the member exists within the network
        except:
            return None

    def find_least_number_of_friends(self):
        no_friends = {}
        least_friends = {}
        found_first_min = False
        min_friends_count = 0

        for name in self._people:  # # get all people in the network and store into list
            person = self._people[name]
            friends_count = person.get_friends_count()  # get the number of friends  of a singular person and store
            # in a variable

            if friends_count != 0 and not found_first_min:
                min_friends_count = friends_count
                found_first_min = True

            if friends_count == 0:  # check if the person has no friends
                no_friends[name] = person
            elif friends_count == min_friends_count:  # check if the person has the current minimum friend count
                least_friends[name] = person
            elif friends_count < min_friends_count:  # check if the person has less than the current minimum friend
                # count
                least_friends = {name: person}
                min_friends_count = friends_count  # If less then, a new minimum is used

        for name in no_friends:
            print(f"{name} has no friends")  # print all those that have no friends

        for name in least_friends:
            print(
                f"{name} has {min_friends_count} friend(s). {self._people[name].get_friends()}")
            # print all those that have the minimum friend count

    def Show_single_member_of_network(self):
        found_person = None
        while not found_person:  # Check if the member exists and loop if it does not until valid answer given
            person_in_network = input("Enter the name of the person")
            c_person_in_network = person_in_network.capitalize()  # For ease of use for the user
            found_person = self.find_member(c_person_in_network)  # Find the person in the network
            if found_person:  # Check if the person exists
                print(f"{found_person.get_name()} has {len(found_person.get_friends())} friend(s)")
                print(found_person)
                # print the member and
                # their friends
            else:
                print("Person not found")

    def show_network(self):
        for person in self.get_list_of_members():
            found_person = self.find_member(person)  # Check if the person exist
            if found_person.get_name() == "":
                pass
            else:
                print(found_person)  #
                # Prints the name of the member and their friends

    def find_friend_of_friend(self):
        friend_of_found_person = []
        found_person = None
        while not found_person:  # Check if the member exists and loop if it does not until valid answer given
            person_in_network = input("Enter the name of the person")
            c_person_in_network = person_in_network.capitalize()  # For ease of use for the user
            found_person = self.find_member(c_person_in_network)  # Find the person in the network

            if found_person:  # Check if the person exists
                friend_of_found_person = found_person.get_friends()
                for friend in friend_of_found_person:
                    found_person = self.find_member(friend)  # Find the friend of person in the network
                    list_of_friends = found_person.get_friends()  # get the list of friends of the friend
                    list_of_friend_of_friend = []
                    for i in list_of_friends:  # loop through the list of friends for the friend
                        if i != c_person_in_network:  # if the original person is found remove from list
                            list_of_friend_of_friend.append(i)
                            print(f"Indirect relationship of {person_in_network}: {friend} ->"
                                  f" {list_of_friend_of_friend}")
            else:
                print("Person not found")

    def create_social_network(self, list_of_pairs_to_make):
        try:
            for pairing in list_of_pairs_to_make:
                if pairing:
                    pair = pairing.split(' ')  # split by the spaces in the pair

                    if len(pair) > 2:  # if length of pair more than 2 skip this iteration
                        continue

                    if check_for_numbers(pair[0]):  # check for numbers and skip iteration if found
                        continue

                    person = self.add_person(pair[0])  # Create a new person in the Person Class

                    if len(pair) == 2:  # Attempt to create friend if there's one
                        if check_for_numbers(pair[1]):
                            continue

                        person2 = None
                        if pair[1]:
                            person.add_friend(pair[1])  # Add a friend to the person

                            person2 = self.add_person(
                                pair[1])  # Create a second person as friend parings can be
                            # reversed.
                        if person2:
                            person2.add_friend(person.get_name())  # Add the original member to the friend list
        except:
            print("Invalid network data")
            return False

        return True


class CommonFriends(SocialNetwork):
    def __init__(self, count):
        super().__init__(count)
        self._pairs = []
        self._common_friends_count = []

    def get_pairs(self):
        return self._pairs

    def get_common_friends_count(self):
        return self._common_friends_count

    def __str__(self):
        return f"{self._pairs} \n {self._common_friends_count}"  # print the pairs and the common friend count

    def generates_pairs(self):  # Find all possible parings
        self._pairs.clear()  # empty pairs list

        for name in self._people:  # loop through the members in the network
            for second_name in self._people:  # loop through the members in the network again
                self._pairs.append([name, second_name])  # add the pairs to the list

        return self._pairs

    def get_common_friends_for_pairs(self):
        self._common_friends_count.clear()  # clear the count of friends

        for pair in self._pairs:
            person1 = self.find_member(pair[0]).get_friends()  # get the friends of the first person in the pair
            person2 = self.find_member(pair[1]).get_friends()  # get the friends of the second person in the pair

            common_friends = frozenset(person1).intersection(person2)  # find the duplicates
            self._common_friends_count.append(len(common_friends))  # add the number of common friends to the count
        print(self._common_friends_count)

        return self._common_friends_count

    def find_common_friends__count_for_pairing(self, person1,
                                               person2):  # method to split lists by the size of the network
        count = 0
        for pair in self._pairs:
            if pair[0] == person1 and pair[1] == person2:
                return self._common_friends_count[count]
            count = count + 1

        return 0

    def get_recommendation(self):

        self.generates_pairs()  # find all possible parings
        self.get_common_friends_for_pairs()  # find the common friends between the parings
        try:
            person_name = input("Get friends recommendation for person: ")  # get input from user
            c_person_name = person_name.capitalize()  # for ease of the user
            friends = self.find_member(c_person_name).get_friends()  # find the person in the network and get
            # their friends
            potential_recommend_friend_names = []  # holds the potential friends
            max_count = 0  # holds the max count of friends
            pair_index = 0
            for pair in self.get_pairs():  # loop through the pairs
                if pair[0] == c_person_name and pair[1] != c_person_name and pair[1] not in friends: # check if the
                    # person the user has asked for is not a pair so (adam,adam) will not be considered as a possible
                    # match
                    friend_count = self.get_common_friends_count()[pair_index]  # get the number of common friends that
                    ## paring has
                    if friend_count != 0 and friend_count >= max_count:  # if the member has a common friend and if
                        # bigger than or equal to current max count
                        if friend_count > max_count:  # if friend count is bigger than max count
                            potential_recommend_friend_names.clear()  # clear the potential list of friends as a higher#
                            # common friend count has been found
                            max_count = friend_count  # max count is now equal to the friend count
                        potential_recommend_friend_names.append(pair[1])  # append the friend to be recommended as a
                        # potential friend

                pair_index = pair_index + 1  # check next pair

            for name in potential_recommend_friend_names:
                print(f"{name} is recommended for {c_person_name}")  # print the potential friends

            if not potential_recommend_friend_names:
                print(f"No one has been recommended for {c_person_name}")  # if the list of potential friends is empty
                # No on is recommended
        except:
            print("Person not found")  # if the user does not enter a valid name


def read_social_network_list():

    data_into_list = []
    file = input("Enter the file name")

    try:
        my_file = open(file, "r")  # opening the file in read mode

        # reading the file
        data = my_file.read()

        # Find all new line and split the items
        data_into_list = data.split('\n')
        my_file.close()  # close the file
        data_into_list.pop(0)  # Get rid of size of network at the start of the list as that is not needed
    except:
        print("File not found")

    return data_into_list


def check_for_numbers(input_word):
    return any(char.isdigit() for char in input_word)  # check if there is number in name


def check_data_from_file():
    network_data = read_social_network_list()
    while not network_data:  # check if the network data is empty
        network_data = read_social_network_list()  # call the read_social_network_list function and store
        # in network_data
    return network_data


def main_menu():
    network_data = check_data_from_file()
    social_network = CommonFriends(len(network_data))  # get the number of pairs

    while not social_network.create_social_network(network_data):  # Creating the social network and passing through
        # the data
        network_data = check_data_from_file()

    flag = False
    while not flag:  # Loop until the user breaks out of the loop
        print("")
        print("1. Show network")
        print("2. Show member of network")
        print("3. Find indirect relationships")
        print("4. Recommendation for a member of the network")
        print("5. Show member with least number of friends")
        print("6. Try different network")
        print("7. Show number of members in network")
        print("8. Exit")
        ans = input("Enter the number to select an option")
        if ans == "1":  # Check for valid input
            social_network.show_network()

        elif ans == "2":
            social_network.Show_single_member_of_network()

        elif ans == "3":
            social_network.find_friend_of_friend()

        elif ans == "4":
            social_network.get_recommendation()

        elif ans == "5":
            social_network.find_least_number_of_friends()

        elif ans == "6":
            network_data = check_data_from_file()  # read data from text file
            social_network = CommonFriends(network_data)  # Create social network

            while not social_network.create_social_network(network_data):  # check if empty
                network_data = check_data_from_file()  # if empty read data from new file

        elif ans == "7":
            size = social_network.get_network_size()
            print(f"There are {size} people inside the network")

        elif ans == "8":
            flag = True

        else:
            print("Invalid answer")


main_menu()
print("Goodbye")
