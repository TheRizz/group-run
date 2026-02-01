import os
from datetime import datetime
from stravalib.client import Client


class StravaActivityFetcher:
    """
    A class to interact with the Strava API and fetch activities.
    """
    
    def __init__(self):
        """Initialize the Strava client and load credentials from environment."""
        self.client = Client()
        self.access_token = os.getenv('STRAVA_ACCESS_TOKEN')
        
        if not self.access_token:
            raise ValueError("STRAVA_ACCESS_TOKEN not found in .env file")
        
        self.client.access_token = self.access_token
        self.athlete = None
    
    def authenticate(self):
        """Authenticate with Strava and get athlete information."""
        try:
            self.athlete = self.client.get_athlete()
            print(f"Successfully authenticated as: {self.athlete.firstname} {self.athlete.lastname}")
            return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def get_activities_this_year(self):
        """
        Fetch all activities from the current year.
        
        Returns:
            list: List of activity objects from this year
        """
        # Get the start of the current year
        year_start = datetime(datetime.now().year, 1, 1)
        
        try:
            activities = list(self.client.get_activities(after=year_start))
            print(f"\nFound {len(activities)} activities in {datetime.now().year}")
            return activities
        except Exception as e:
            print(f"Error fetching activities: {e}")
            return []
    
    def display_activities(self, activities):
        """
        Display activity information in a formatted way.
        
        Args:
            activities (list): List of activity objects to display
        """
        if not activities:
            print("No activities to display.")
            return
        
        print("\n" + "="*80)
        print(f"{'Date':<20} {'Name':<30} {'Type':<15} {'Distance (km)':<15}")
        print("="*80)
        
        for activity in activities:
            date = activity.start_date_local.strftime("%Y-%m-%d %H:%M")
            name = activity.name[:28] + "..." if len(activity.name) > 30 else activity.name
            activity_type = activity.type
            distance = f"{float(activity.distance) / 1000:.2f}" if activity.distance else "N/A"
            
            print(f"{date:<20} {name:<30} {activity_type:<15} {distance:<15}")
        
        print("="*80)
    
    def get_activity_summary(self, activities):
        """
        Calculate and display summary statistics for activities.
        
        Args:
            activities (list): List of activity objects
        """
        if not activities:
            return
        
        total_distance = sum(float(a.distance or 0) for a in activities) / 1000  # Convert to km
        total_time = sum(float(a.moving_time.total_seconds() or 0) for a in activities) / 3600  # Convert to hours
        
        activity_types = {}
        for activity in activities:
            activity_type = activity.type
            activity_types[activity_type] = activity_types.get(activity_type, 0) + 1
        
        print("\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        print(f"Total Activities: {len(activities)}")
        print(f"Total Distance: {total_distance:.2f} km")
        print(f"Total Moving Time: {total_time:.2f} hours")
        print("\nActivities by Type:")
        for activity_type, count in sorted(activity_types.items()):
            print(f"  {activity_type}: {count}")
        print("="*50)


def main():
    """Main function to run the Strava activity fetcher."""
    print("Strava Activity Fetcher")
    print("="*50)
    
    try:
        # Initialize the fetcher
        fetcher = StravaActivityFetcher()
        
        # Authenticate
        if not fetcher.authenticate():
            print("Exiting due to authentication failure.")
            return
        
        # Fetch activities from this year
        activities = fetcher.get_activities_this_year()
        
        # Display activities
        fetcher.display_activities(activities)
        
        # Show summary
        fetcher.get_activity_summary(activities)
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease ensure you have created a .env file with your STRAVA_ACCESS_TOKEN")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
