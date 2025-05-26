
class Timing:
    def __init__(self, days=0, hours=0, minutes=0):
        self.days = int(days)
        self.hours = int(hours)
        self.minutes = int(minutes)

    def get_minutes(self):
        return self.days*24*60 + self.hours*60 + self.minutes
