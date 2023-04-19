import unittest
from habit_tracker_final_01 import Habit, User, Analytics, Completion
from datetime import datetime

class TestHabitTracker(unittest.TestCase):
    def test_longest_streak(self):
        completion_dates = [
            Completion(datetime(2023, 1, 1)),
            Completion(datetime(2023, 1, 2)),
            Completion(datetime(2023, 1, 4)),
            Completion(datetime(2023, 1, 5)),
            Completion(datetime(2023, 1, 6)),
            Completion(datetime(2023, 1, 8)),
        ]

        habit = Habit("Test habit", "daily", completion_dates)
        period_start = datetime(2023, 1, 1).date()
        period_end = datetime(2023, 1, 8).date()

        longest_streak = Analytics.longest_streak(habit, period_start, period_end)
        self.assertEqual(longest_streak, 3)

    def test_longest_streak_of_all_habits(self):
        habit1 = Habit("Habit 1", "daily", [
            Completion(datetime(2023, 1, 1)),
            Completion(datetime(2023, 1, 2)),
            Completion(datetime(2023, 1, 3)),
            Completion(datetime(2023, 1, 4)),
        ])

        habit2 = Habit("Habit 2", "daily", [
            Completion(datetime(2023, 1, 1)),
            Completion(datetime(2023, 1, 2)),
            Completion(datetime(2023, 1, 3)),
        ])

        habit3 = Habit("Habit 3", "daily", [
            Completion(datetime(2023, 1, 1)),
            Completion(datetime(2023, 1, 2)),
        ])

        user = User("testuser", "password")
        user.add_habit(habit1)
        user.add_habit(habit2)
        user.add_habit(habit3)

        period_start = datetime(2023, 1, 1).date()
        period_end = datetime(2023, 1, 8).date()

        longest_streak, habit_task = Analytics.longest_streak_of_all_habits(user, period_start, period_end)
        self.assertEqual(longest_streak, 4)
        self.assertEqual(habit_task, "Habit 1")



if __name__ == '__main__':
    unittest.main()
