import datetime
import json
import os
import random
from colorama import init, Fore, Style
init(autoreset=True)


class Completion:
    """The Completion class represents a single completion of a habit task."""
    def __init__(self, date):
        self.completion_date = date

def generate_random_completion_dates(num_completions):
    """Generate a list of random Completion instances within the past 4 weeks"""
    completion_dates = []
    start_date = datetime.datetime.now() - datetime.timedelta(weeks=4)

    for _ in range(num_completions):
        random_date = start_date + datetime.timedelta(days=random.randint(0, 28))
        completion = Completion(random_date)
        completion_dates.append(completion)

    return completion_dates


class Habit:
    """A class to represent a habit with its task, periodicity, completions, and creation date"""
    def __init__(self, task, periodicity, completions=None):
        self.task = task
        self.periodicity = periodicity
        if completions is None:
            completions = []
        self.completions = completions
        self.creation_date = datetime.datetime.now()

    def check_off(self, timestamp):
        """Add the given timestamp to the list of completions"""
        self.completions.append(timestamp)

    def is_completed_within_period(self, period_start, period_end):
        """Check if the habit was completed within the specified period"""
        for completion_date in self.completions:
            if period_start <= completion_date <= period_end:
                return True
        return 

    def get_completion_dates(self):
        """Get a list of completion dates for the habit"""
        return [completion.completion_date for completion in self.completions]


    @classmethod
    def from_dict(cls, data):
        """Create a Habit object from the dictionary"""
        task = data["task"]
        periodicity = data["periodicity"]
        completions = [Completion(datetime.datetime.fromisoformat(date_str)) for date_str in data["completions"]]
        habit = cls(task, periodicity, completions)
        habit.creation_date = datetime.datetime.fromisoformat(data["creation_date"])
        return habit

    def to_dict(self):
        """Convert the Habit object to a dictionary"""
        return {
            "task": self.task,
            "periodicity": self.periodicity,
            "completions": [completion.completion_date.isoformat() for completion in self.completions],
            "creation_date": self.creation_date.isoformat(),
        }



class User:
    """A class representing a user in the habittracker"""
    def __init__(self, username, password):
        """Initialize a User object with a username, password, and an empty list of habits"""
        self.username = username
        self.password = password
        self.habits = []

    def add_habit(self, habit):
        """Add a habit to the user's list of habits"""
        self.habits.append(habit)

    def remove_habit(self, habit):
        """Remove a habit from the user's list of habits"""
        self.habits.remove(habit)

    def complete_task(self, habit, timestamp):
        """Mark a habit as completed at a given timestamp"""
        habit.check_off(timestamp)

    def get_habits(self):
        """Return the user's list of habits"""
        return self.habits

    def get_habits_by_periodicity(self, periodicity):
        """Return a list of the users habits with the specified periodicity"""
        return [habit for habit in self.habits if habit.periodicity == periodicity]

    def get_habit_by_task(self, task):
        """Find and return the users habit with the specified task"""
        for habit in self.habits:
            if habit.task == task:
                return habit
        return None
    
    def to_dict(self):
        """Convert the User object to the dictionary"""
        return {
            "username": self.username,
            "password": self.password,
            "habits": [habit.to_dict() for habit in self.habits],
        }

    @classmethod
    def from_dict(cls, data):
        """Create a User object from a dictionary"""
        user = cls(data["username"], data["password"])
        user.habits = [Habit.from_dict(habit_data) for habit_data in data["habits"]]
        return user



class HabitTracker:
    """The HabitTracker class manages a collection of users and their habits, it provides methods for adding, removing, and saving users and their data"""
    def __init__(self):
        """
        Initialize the HabitTracker with an empty list of users and load existing users from the JSON file.
        """
        self.users = []
        self.load_users()

    def add_user(self, user):
        """Add a user to the list of users and save the updated list"""
        self.users.append(user)
        self.save_users()

    def get_user(self, username):
        """Retrieve a user from the list of users by their username"""
        for user in self.users:
            if user.username == username:
                return user
        return None

    def remove_user(self, user):
        """Remove a user from the list of users and save the updated list"""
        self.users.remove(user)
        self.save_users()

    def save_users(self):
        """Save the list of users"""
        user_data = [user.to_dict() for user in self.users]
        with open("users.json", "w") as f:
            json.dump(user_data, f)

    def load_users(self):
        """Load the list of users from a JSON file if it exists"""
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                user_data = json.load(f)
                for data in user_data:
                    user = User.from_dict(data)
                    self.users.append(user)

    def add_predefined_habits_to_user(self, user):
        """Add a predefined set of habits to a user and save the updated list of users"""
        for habit in predefined_habits:
            user.add_habit(habit)
        self.save_users()

class Analytics:
    """The Analytics class provides methods for analyzing habits"""
    @staticmethod
    def longest_streak(habit, period_start, period_end):
        completion_dates = [completion_date.date() for completion_date in habit.get_completion_dates()]
        period_start = period_start.date() if isinstance(period_start, datetime.datetime) else period_start
        period_end = period_end.date() if isinstance(period_end, datetime.datetime) else period_end
        completion_dates_in_period = [date for date in completion_dates if period_start <= date <= period_end]
        if not completion_dates_in_period:
            return 0
        streak = 1
        max_streak = 1
        for i in range(1, len(completion_dates_in_period)):
            if (completion_dates_in_period[i] - completion_dates_in_period[i - 1]).days == 1:
                streak += 1
            else:
                streak = 1
            max_streak = max(max_streak, streak)
        return max_streak



    @staticmethod
    def longest_streak_of_all_habits(user, period_start, period_end):
        """Calculate the longest streak of consecutive habit completions across all habits of a user within a specified period"""
        max_streak = 0
        max_streak_habit_task = None
        for habit in user.get_habits():
            streak = Analytics.longest_streak(habit, period_start, period_end)
            if streak > max_streak:
                max_streak = streak
                max_streak_habit_task = habit.task
        return max_streak, max_streak_habit_task

"""10 predefinded habits with random completion dates. Users can use them when creating an account"""
predefined_habits = [
    Habit("Read for 30 minutes", "daily", generate_random_completion_dates(10)),
    Habit("Meditate for 10 minutes", "daily", generate_random_completion_dates(12)),
    Habit("Drink 2 liters of water", "daily", generate_random_completion_dates(20)),
    Habit("Exercise for 1 hour", "weekly", generate_random_completion_dates(3)),
    Habit("Complete a coding challenge", "weekly", generate_random_completion_dates(2)),
    Habit("Practice an instrument for 30 minutes", "daily", generate_random_completion_dates(15)),
    Habit("Discover and listen to a new song", "daily", generate_random_completion_dates(25)),
    Habit("Run 5 kilometers", "weekly", generate_random_completion_dates(4)),
    Habit("Join a group run or a local running club", "monthly", generate_random_completion_dates(1)),
    Habit("Study a new subject for 1 hour", "daily", generate_random_completion_dates(18)),
    Habit("Teach someone a new skill or concept", "weekly", generate_random_completion_dates(3)),
    Habit("Participate in a study group or online forum", "weekly", generate_random_completion_dates(6))
]








def main():
    """"The main function that drives the habittracker.
    This function contains the main loop that displays the list of available commands to the user,
    takes user input, and calls the appropriate functionality based on the input"""
    habit_tracker = HabitTracker()
    current_user = None

    """The logic behind the habittracker operates based on a state machine approach"""

    while True:
        print("\nCommands:")
        print("1: Register user")
        print("2: Select user")
        print("3: Add habit")
        print("4: Remove habit")
        print("5: Complete habit task")
        print("6: List habits")
        print("7: List habits by periodicity")
        print("8: Longest streak for habit")
        print("9: Longest streak among all habits")
        print("0: Quit")

        command = input("Enter the command number: ")

        if command == '1':
            username = input("Enter username: ")

            existing_user = habit_tracker.get_user(username)
            if existing_user:
                print(Fore.RED + "A user with this username already exists." + Style.RESET_ALL)
            else:
                password = input("Enter password: ")
                user = User(username, password)
                habit_tracker.add_user(user)
                
                add_predefined_habits = input("Do you want to add predefined habits? (yes/no): ")
                if add_predefined_habits.lower() == 'yes':
                        habit_tracker.add_predefined_habits_to_user(user)
                        habit_tracker.save_users()
                
                print(f"User {username} registered.")

        elif command == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")

            current_user = habit_tracker.get_user(username)
            if current_user:
                if current_user.password == password:
                    print(f"Current user: {current_user.username}")
                    
                    if not current_user.get_habits():
                        add_predefined_habits = input("Do you want to add predefined habits? (yes/no): ")
                        if add_predefined_habits.lower() == 'yes':
                            habit_tracker.add_predefined_habits_to_user(current_user)
                else:
                    print(Fore.RED + "Incorrect password." + Style.RESET_ALL)
            else:
                print(Fore.RED + "User not found."  + Style.RESET_ALL)


        elif command == '3':
            if current_user:
                task = input("Enter habit task: ")
                periodicity = input("Enter habit periodicity (daily or weekly): ")
                habit = Habit(task, periodicity)
                current_user.add_habit(habit)
                print(f"Habit '{task}' added.")
                habit_tracker.save_users()
            else:
                print(Fore.RED + "Please select a user first."  + Style.RESET_ALL)



        elif command == '4':
            if current_user:
                task = input("Enter habit task: ")
                habit = current_user.get_habit_by_task(task)
                if habit:
                    current_user.remove_habit(habit)
                    print(f"Habit '{task}' removed.")
                    habit_tracker.save_users()
                else:
                    print(Fore.RED + "Habit not found." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Please select a user first."  + Style.RESET_ALL)


        elif command == '5':
            if current_user:
                task = input("Enter habit task: ")
                habit = current_user.get_habit_by_task(task)
                if habit:
                    timestamp = datetime.datetime.now()
                    completion = Completion(timestamp)  # Create a Completion object
                    current_user.complete_task(habit, completion)  # Pass the Completion object
                    print(Fore.GREEN + f"Task '{task}' completed at {timestamp}.")
                    print(Fore.YELLOW + "Congratulations! Keep up the good work!" + Style.RESET_ALL)
                    habit_tracker.save_users()
                else:
                    print(Fore.RED + "Habit not found." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Please select a user first."  + Style.RESET_ALL)


        elif command == '6':
            if current_user:
                habits = current_user.get_habits()
                print("\nCurrent habits:")
                for habit in habits:
                    print(f"- {habit.task} ({habit.periodicity})")
            else:
                print(Fore.RED + "Please select a user first."  + Style.RESET_ALL)

        elif command == '7':
            if current_user:
                periodicity = input("Enter periodicity (daily or weekly): ")
                habits = current_user.get_habits_by_periodicity(periodicity)
                print(f"\n{periodicity.capitalize()} habits:")
                for habit in habits:
                    print(f"- {habit.task}")
            else:
                print(Fore.RED + "Please select a user first." + Style.RESET_ALL)

        elif command == '8':
            if current_user:
                task = input("Enter habit task: ")
                habit = current_user.get_habit_by_task(task)
                if habit:
                    period_start = datetime.datetime.now() - datetime.timedelta(days=28)
                    period_end = datetime.datetime.now()
                    longest_streak = Analytics.longest_streak(habit, period_start, period_end)
                    print(f"Longest streak for '{task}': {longest_streak} days")
                else:
                    print(Fore.RED +"Habit not found."  + Style.RESET_ALL)
            else:
                print(Fore.RED + "Please select a user first."  + Style.RESET_ALL)

        elif command == '9':
            if current_user:
                period_start = datetime.datetime.now() - datetime.timedelta(days=28)
                period_end = datetime.datetime.now()
                longest_streak, habit_task = Analytics.longest_streak_of_all_habits(current_user, period_start, period_end)
                print(f"Longest streak among all habits: {longest_streak} days (for '{habit_task}')")
            else:
                print(Fore.RED + "Please select a user first."  + Style.RESET_ALL)

        elif command == '0':
            print("Goodbye!")
            break

        else:
            print("Invalid command. Please try again.")



if __name__ == '__main__':
    main()
    




