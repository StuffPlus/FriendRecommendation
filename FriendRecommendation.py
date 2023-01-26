# class for the person inside the network
class Person:
    def __init__(self, name):
        self.name = name
        self.friends = []

    def __str__(self):
        return f"{self.name} -> {self.friends}"

    def get_name(self):
        return self.name  # return the name of the person

    def get_friends(self):
        return self.friends  # return friends of a person

    def get_friends_count(self):
        return len(self.friends)  # return the number of friends a person has

    def add_friend(self, name):
        if self.friends.count(name) == 0:  # stop duplication of friends
            self.friends.append(name)

    def remove_friend(self, name):
        if self.friends.count(name) != 0:  # remove friend from a person
            self.friends.remove(name)

    def is_friends_with(self, name):
        return name in self.friends  # return a person that is friends with the person


    # class of the network
    # Handles the creation and manipulation of the social network
    class SocialNetwork:
        def __init__(self, size):
            self.size = size
            self.people = {}

        # get size of network
        def get_network_size(self):
            return len(self.people)  # Get number of people inside the network

        # Get everyone in the network
        def get_list_of_members(self):
            return self.people  # Get the list of names inside the network

        # Add a new person the network
        def add_person(self, new_person):
            if not self.find_member(new_person):
                self.people[new_person] = Person(new_person) # Add a new object into the person Class
            return self.people[new_person]

        # Find the member in the network
        def find_member(self, member_name):
            try:
                return self.people[member_name]  # Check if the member exists within the network
            except:
                return None

        def find_least_number_of_friends(self):
            no_friends = {}
            least_friends = {}
            found_first_min = False
            min_friends_count = 0

            for name in self.people:  # # get all people in the network and store into list
                person = self.people[name]
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
                    f"{name} has {min_friends_count} friend(s). {self.people[name].get_friends()}")  # print all those that
                # have the minimum friend count

        def Show_single_member_of_network(self):
            found_person = None
            while not found_person:  # Check if the member exists and loop if it does not until valid answer given
                person_in_network = input("Enter the name of the person")
                c_person_in_network = person_in_network.capitalize()  # For ease of use for the user
                found_person = self.find_member(c_person_in_network)  # Find the person in the network
                if found_person:  # Check if the person exists
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
                        for i in list_of_friends:  # loop through the list of friends for the friend
                            if i == c_person_in_network:  # if the original person is found remove from list
                                list_of_friends.remove(i)
                                print(f"Indirect relationship of {person_in_network}: {friend} --> {list_of_friends}")
                else:
                    print("Person not found")

        def create_social_network(self, unique_class_list):
            try:
                for pairing in unique_class_list:
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
        self.pairs = []
        self.common_friends_count = []

    def __str__(self):
        return f"{self.pairs} \n {self.common_friends_count}"  # print the pairs and the common friend count

    def generates_pairs(self):  # Find all possible parings
        self.pairs.clear()  # empty pairs list

        for name in self.people:  # loop through the members in the network
            for second_name in self.people:  # loop through the members in the network again
                self.pairs.append([name, second_name])  # add the pairs to the list

        return self.pairs

    # def recommendation(self, for_person):
    #     list_of_recommendation = {}
    #
    #     person_to_recommend_to = self.find_member(for_person)
    #     if person_to_recommend_to:
    #         friends = person_to_recommend_to.get_friends()
    #         for friend_name in friends:
    #             friend = self.find_member(friend_name)
    #             friends_of_friend = friend.get_friends()
    #             for name in friends_of_friend:
    #                 if name != for_person and not person_to_recommend_to.is_friends_with(name):
    #                     list_of_recommendation[name] = name
    #
    #     return list(list_of_recommendation)

    def get_common_friends(self):
        self.common_friends_count.clear()  # clear the count of friends

        for pair in self.pairs:
            person1 = self.find_member(pair[0]).get_friends()  # get the friends of the first person in the pair
            person2 = self.find_member(pair[1]).get_friends()  # get the friends of the second person in the pair

            common_friends = frozenset(person1).intersection(person2)  # find the duplicates
            # print(f"{pair[0]} has {len(common_friends)} friends in common with {pair[1]}")
            self.common_friends_count.append(len(common_friends))  # add the number of common friends to the count

        return self.common_friends_count

    def listSplit(self):  # method to split lists by the size of the network
        size_of_list = self.get_network_size()
        for i in range(0, len(self.common_friends_count), size_of_list):
            print(f"{self.pairs[i:i + size_of_list][0][0]} \t->\t {self.common_friends_count[i:i + size_of_list]}")

    def get_recommendation(self):
        pass


def read_social_network_list():
    # opening the file in read mode
    data_into_list = []
    file = input("Enter the file name")

    try:
        my_file = open(file, "r")

        # reading the file
        data = my_file.read()

        # Find all new line and split the items
        data_into_list = data.split('\n')
        my_file.close()  # close the file
        # Store the size of the network
        data_into_list.pop(0)  # Get rid of size of network at the start of the list as that is not needed
    except:
        print("File not found")

    return data_into_list


def check_for_numbers(input_word):
    return any(char.isdigit() for char in input_word)


def check_data_from_file():
    network_data = read_social_network_list()
    while not network_data:  # check if the network data is empty
        network_data = read_social_network_list()  # call the read_social_network_list function and store
        # in network_data
    return network_data


def main_menu():
    network_data = check_data_from_file()
    social_network = CommonFriends(len(network_data))  # Creating the social network and passing through the data

    while not social_network.create_social_network(network_data):
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
            social_network.generates_pairs()
            social_network.get_common_friends()
            social_network.listSplit()
            print(social_network)
            # name = input("Name of person to recommend friends for: ")
            # c_name = name.capitalize()
            # list_of_recommendations = social_network.recommendation(c_name)
            # if len(name) > 0:
            #     print(f"Recommended friends for {c_name} are {list_of_recommendations}")
            # else:
            #     print(f"Cannot find new friends for {c_name}")

        elif ans == "5":
            social_network.find_least_number_of_friends()

        elif ans == "6":
            network_data = check_data_from_file()
            social_network = CommonFriends(
                len(network_data))  # Creating the social network and passing through the data

            while not social_network.create_social_network(network_data):
                network_data = check_data_from_file()

        elif ans == "7":
            size = social_network.get_network_size()
            print(f" There are {size} people inside the network")

        elif ans == "8":
            flag = True

        else:
            print("Invalid answer")


main_menu()
print("Goodbye")