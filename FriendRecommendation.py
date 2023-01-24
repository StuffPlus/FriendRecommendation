# class for the person inside the network
class Person:
    def __init__(self, name):
        self.name = name
        self.friends = []

    def get_name(self):
        return self.name

    def get_friends(self):
        return self.friends

    def get_friends_count(self):
        return len(self.friends)

    def set_member(self, name):
        if not isinstance(name, str):
            return 'not valid input'
        else:
            self.name = name
            return 'valid'

    def add_friend(self, name):
        if self.friends.count(name) == 0:  # stop duplication of friends
            self.friends.append(name)

    def remove_friend(self, name):
        if self.friends.count(name) != 0:
            self.friends.remove(name)

    def is_friends_with(self, name):
        return name in self.friends


# class of the network
# Handles the creation and manipulation of the social network
class SocialNetwork:
    def __init__(self, size):
        self.size = size
        self.people = {}

    # get size of network
    def get_network_size(self):
        return len(self.people)

    def get_list_of_members(self):
        return self.people

    def add_person(self, new_person):
        if not self.find_member(new_person):
            self.people[new_person] = Person(new_person)
        return self.people[new_person]

    def find_member(self, member_name):
        try:
            return self.people[member_name]
        except:
            return None

    def find_least_number_of_friends(self):
        no_friends = {}
        least_friends = {}
        found_first_min = False
        min_friends_count = 0

        for name in self.people:  #
            person = self.people[name]
            friends_count = person.get_friends_count()

            if friends_count != 0 and not found_first_min:
                min_friends_count = friends_count
                found_first_min = True

            if friends_count == 0:
                no_friends[name] = person
            elif friends_count == min_friends_count:
                least_friends[name] = person
            elif friends_count < min_friends_count:
                least_friends = {name: person}
                min_friends_count = friends_count

        for name in no_friends:
            print(f"{name} has no friends")

        for name in least_friends:
            print(f"{name} has {min_friends_count} friend(s). {self.people[name].get_friends()}")


class FriendRecommendation(SocialNetwork):
    def __init__(self):
        super().__init__()

    def recommend(self):
        pass


def read_social_network_list():
    # opening the file in read mode
    data_into_list = []
    file = input("Enter the file name")
    if not file:
        file = "nw_data1.txt"

    try:
        my_file = open(file, "r")

        # reading the file
        data = my_file.read()

        # Find all new line and split the items
        data_into_list = data.split('\n')
        my_file.close()
        # Store the size of the network
        sizeofnetwork = data_into_list[0]
        data_into_list.pop(0)  # Get rid of size of network as that is not needed
    except:
        print("File not found")

    return data_into_list


def create_social_network(unique_class_list):
    social_network = SocialNetwork(len(unique_class_list))
    for pairing in unique_class_list:
        if pairing:
            pair = pairing.split(' ')
            person = social_network.add_person(pair[0])  # Create a new person in the Person Class
            if len(pair) == 2:  # Attempt to create friend if there's one
                person2 = None
                if pair[1]:
                    person.add_friend(pair[1])  # Add a friend to the person
                    person2 = social_network.add_person(
                        pair[1])  # Create a second person as friend parings can be reversed.
                if person2:
                    person2.add_friend(person.get_name())  # Add the original member to the friend list

    return social_network


def find_friends_of_friend(social_network):
    friend_of_found_person = []
    found_person = None
    while not found_person:  # Check if the member exists and loop if it does not until valid answer given
        person_in_network = input("Enter the name of the person")
        c_person_in_network = person_in_network.capitalize()  # For ease of use for the user
        found_person = social_network.find_member(c_person_in_network)  # Find the person in the network

        if found_person:  # Check if the person exists
            friend_of_found_person = found_person.get_friends()
            for friend in friend_of_found_person:
                found_person = social_network.find_member(friend)  # Find the friend of person in the network
                list_of_friends = found_person.get_friends()
                for i in list_of_friends:
                    if i == c_person_in_network:
                        list_of_friends.remove(i)
                        print(f"Indirect relationship of {person_in_network}: {friend} --> {list_of_friends}")
        else:
            print("Person not found")


def main_menu():
    network_data = read_social_network_list()
    while not network_data:
        network_data = read_social_network_list()

    social_network = create_social_network(network_data)

    flag = False
    while not flag:  # Loop to check for valid input and to loop until valid answer is given
        print("")
        print("1. Show network")
        print("2. Show member of network")
        print("3. Find indirect relationships")
        print("4. Recommendation for a member of the network")
        print("5. Show member with least number of friends")
        print("6. Try different network")
        print("7. Exit")
        ans = input("Enter the number to select an option")
        if ans == "1":  # Check for vali input
            for person in social_network.get_list_of_members():
                found_person = social_network.find_member(person)  # Check if the person exist
                print("")
                if found_person.get_member_name() == "":
                    pass
                else:
                    print(f"{found_person.get_member_name()} ------> {found_person.get_friends()}")  #
                    # Prints the name of the member and their friends

        elif ans == "2":
            found_person = None
            while not found_person:  # Check if the member exists and loop if it does not until valid answer given
                person_in_network = input("Enter the name of the person")
                c_person_in_network = person_in_network.capitalize()  # For ease of use for the user
                found_person = social_network.find_member(c_person_in_network)  # Find the person in the network
                if found_person:  # Check if the person exists
                    print(
                        f"{found_person.get_member_name()}-----> {found_person.get_friends()}")  # print the member and
                    # their friends
                else:
                    print("Person not found")
                flag = True

        elif ans == "3":
            find_friends_of_friend(social_network)

        elif ans == "4":
            pass

        elif ans == "5":
            social_network.find_least_number_of_friends()

        elif ans == "6":
            network_data = read_social_network_list()
            while not network_data:
                network_data = read_social_network_list()
            social_network = create_social_network(network_data)

        elif ans == "7":
            quit()

        else:
            print("Invalid answer")
            ans = input("Enter the number to select an option")


main_menu()
