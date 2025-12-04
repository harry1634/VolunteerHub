import requests
import sys
import json
from datetime import datetime

class VolunteerPlatformTester:
    def __init__(self, base_url="https://helperhub-5.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.volunteer_token = None
        self.organizer_token = None
        self.volunteer_user = None
        self.organizer_user = None
        self.test_event_id = None
        self.test_signup_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None, token=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json() if response.content else {}
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                self.failed_tests.append({
                    'name': name,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'response': response.text[:200]
                })
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                'name': name,
                'error': str(e)
            })
            return False, {}

    def test_volunteer_registration(self):
        """Test volunteer registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        volunteer_data = {
            "email": f"volunteer_{timestamp}@test.com",
            "password": "TestPass123!",
            "full_name": f"Test Volunteer {timestamp}",
            "role": "volunteer",
            "skills": ["Communication", "Teaching"],
            "interests": ["Education", "Community"],
            "availability": "Weekends",
            "phone": "123-456-7890"
        }
        
        success, response = self.run_test(
            "Volunteer Registration",
            "POST",
            "auth/register",
            200,
            data=volunteer_data
        )
        
        if success and 'token' in response:
            self.volunteer_token = response['token']
            self.volunteer_user = response['user']
            return True
        return False

    def test_organizer_registration(self):
        """Test organizer registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        organizer_data = {
            "email": f"organizer_{timestamp}@test.com",
            "password": "TestPass123!",
            "full_name": f"Test Organizer {timestamp}",
            "role": "organizer",
            "organization_name": "Test NGO",
            "phone": "098-765-4321"
        }
        
        success, response = self.run_test(
            "Organizer Registration",
            "POST",
            "auth/register",
            200,
            data=organizer_data
        )
        
        if success and 'token' in response:
            self.organizer_token = response['token']
            self.organizer_user = response['user']
            return True
        return False

    def test_login(self):
        """Test login functionality"""
        if not self.volunteer_user:
            return False
            
        login_data = {
            "email": self.volunteer_user['email'],
            "password": "TestPass123!"
        }
        
        success, response = self.run_test(
            "Volunteer Login",
            "POST",
            "auth/login",
            200,
            data=login_data
        )
        
        return success and 'token' in response

    def test_get_profile(self):
        """Test getting user profile"""
        success, response = self.run_test(
            "Get Profile",
            "GET",
            "auth/me",
            200,
            token=self.volunteer_token
        )
        return success

    def test_update_profile(self):
        """Test updating user profile"""
        update_data = {
            "full_name": "Updated Test Volunteer",
            "skills": ["Updated Skill"],
            "phone": "555-123-4567"
        }
        
        success, response = self.run_test(
            "Update Profile",
            "PUT",
            "auth/profile",
            200,
            data=update_data,
            token=self.volunteer_token
        )
        return success

    def test_create_event(self):
        """Test event creation by organizer"""
        if not self.organizer_token:
            return False
            
        event_data = {
            "title": "Test Community Cleanup",
            "description": "Help clean up the local park",
            "location": "Central Park",
            "date": "2024-12-25",
            "time": "09:00",
            "cause": "environment",
            "skills_required": ["Physical Work"],
            "total_spots": 20
        }
        
        success, response = self.run_test(
            "Create Event",
            "POST",
            "events",
            200,
            data=event_data,
            token=self.organizer_token
        )
        
        if success and 'id' in response:
            self.test_event_id = response['id']
            return True
        return False

    def test_get_events(self):
        """Test getting all events"""
        success, response = self.run_test(
            "Get All Events",
            "GET",
            "events",
            200
        )
        return success

    def test_get_event_details(self):
        """Test getting specific event details"""
        if not self.test_event_id:
            return False
            
        success, response = self.run_test(
            "Get Event Details",
            "GET",
            f"events/{self.test_event_id}",
            200
        )
        return success

    def test_search_events(self):
        """Test event search functionality"""
        success, response = self.run_test(
            "Search Events",
            "GET",
            "events?search=cleanup&cause=environment",
            200
        )
        return success

    def test_volunteer_signup(self):
        """Test volunteer signing up for event"""
        if not self.test_event_id or not self.volunteer_token:
            return False
            
        signup_data = {
            "event_id": self.test_event_id
        }
        
        success, response = self.run_test(
            "Volunteer Signup",
            "POST",
            "signups",
            200,
            data=signup_data,
            token=self.volunteer_token
        )
        
        if success and 'id' in response:
            self.test_signup_id = response['id']
            return True
        return False

    def test_get_my_signups(self):
        """Test getting volunteer's signups"""
        success, response = self.run_test(
            "Get My Signups",
            "GET",
            "signups/volunteer/me",
            200,
            token=self.volunteer_token
        )
        return success

    def test_get_event_signups(self):
        """Test organizer getting event signups"""
        if not self.test_event_id or not self.organizer_token:
            return False
            
        success, response = self.run_test(
            "Get Event Signups",
            "GET",
            f"signups/event/{self.test_event_id}",
            200,
            token=self.organizer_token
        )
        return success

    def test_update_attendance(self):
        """Test organizer updating volunteer attendance"""
        if not self.test_signup_id or not self.organizer_token:
            return False
            
        attendance_data = {
            "signup_id": self.test_signup_id,
            "status": "attended",
            "hours_contributed": 3.5
        }
        
        success, response = self.run_test(
            "Update Attendance",
            "PUT",
            "signups/attendance",
            200,
            data=attendance_data,
            token=self.organizer_token
        )
        return success

    def test_submit_feedback(self):
        """Test volunteer submitting feedback"""
        if not self.test_event_id or not self.volunteer_token:
            return False
            
        feedback_data = {
            "event_id": self.test_event_id,
            "rating": 5,
            "comment": "Great event! Well organized and impactful."
        }
        
        success, response = self.run_test(
            "Submit Feedback",
            "POST",
            "feedback",
            200,
            data=feedback_data,
            token=self.volunteer_token
        )
        return success

    def test_get_event_feedback(self):
        """Test getting event feedback"""
        if not self.test_event_id:
            return False
            
        success, response = self.run_test(
            "Get Event Feedback",
            "GET",
            f"feedback/event/{self.test_event_id}",
            200
        )
        return success

    def test_send_message(self):
        """Test sending message to event discussion"""
        if not self.test_event_id or not self.volunteer_token:
            return False
            
        message_data = {
            "event_id": self.test_event_id,
            "message": "Looking forward to this event!"
        }
        
        success, response = self.run_test(
            "Send Message",
            "POST",
            "messages",
            200,
            data=message_data,
            token=self.volunteer_token
        )
        return success

    def test_get_event_messages(self):
        """Test getting event messages"""
        if not self.test_event_id:
            return False
            
        success, response = self.run_test(
            "Get Event Messages",
            "GET",
            f"messages/event/{self.test_event_id}",
            200
        )
        return success

    def test_get_volunteers(self):
        """Test organizer getting volunteers list"""
        success, response = self.run_test(
            "Get Volunteers List",
            "GET",
            "volunteers",
            200,
            token=self.organizer_token
        )
        return success

    def test_get_volunteer_stats(self):
        """Test getting volunteer stats"""
        success, response = self.run_test(
            "Get Volunteer Stats",
            "GET",
            "stats/volunteer",
            200,
            token=self.volunteer_token
        )
        return success

    def test_get_organizer_stats(self):
        """Test getting organizer stats"""
        success, response = self.run_test(
            "Get Organizer Stats",
            "GET",
            "stats/organizer",
            200,
            token=self.organizer_token
        )
        return success

    def test_update_event(self):
        """Test updating event"""
        if not self.test_event_id or not self.organizer_token:
            return False
            
        update_data = {
            "title": "Updated Community Cleanup",
            "total_spots": 25
        }
        
        success, response = self.run_test(
            "Update Event",
            "PUT",
            f"events/{self.test_event_id}",
            200,
            data=update_data,
            token=self.organizer_token
        )
        return success

    def test_withdraw_from_event(self):
        """Test volunteer withdrawing from event"""
        if not self.test_event_id or not self.volunteer_token:
            return False
            
        success, response = self.run_test(
            "Withdraw from Event",
            "DELETE",
            f"signups/{self.test_event_id}",
            200,
            token=self.volunteer_token
        )
        return success

    def test_delete_event(self):
        """Test deleting event"""
        if not self.test_event_id or not self.organizer_token:
            return False
            
        success, response = self.run_test(
            "Delete Event",
            "DELETE",
            f"events/{self.test_event_id}",
            200,
            token=self.organizer_token
        )
        return success

def main():
    print("🚀 Starting Volunteer Platform API Tests...")
    tester = VolunteerPlatformTester()
    
    # Test sequence
    test_sequence = [
        # Authentication Tests
        ("Volunteer Registration", tester.test_volunteer_registration),
        ("Organizer Registration", tester.test_organizer_registration),
        ("Login", tester.test_login),
        ("Get Profile", tester.test_get_profile),
        ("Update Profile", tester.test_update_profile),
        
        # Event Management Tests
        ("Create Event", tester.test_create_event),
        ("Get All Events", tester.test_get_events),
        ("Get Event Details", tester.test_get_event_details),
        ("Search Events", tester.test_search_events),
        ("Update Event", tester.test_update_event),
        
        # Signup and Participation Tests
        ("Volunteer Signup", tester.test_volunteer_signup),
        ("Get My Signups", tester.test_get_my_signups),
        ("Get Event Signups", tester.test_get_event_signups),
        ("Update Attendance", tester.test_update_attendance),
        
        # Feedback and Communication Tests
        ("Submit Feedback", tester.test_submit_feedback),
        ("Get Event Feedback", tester.test_get_event_feedback),
        ("Send Message", tester.test_send_message),
        ("Get Event Messages", tester.test_get_event_messages),
        
        # Stats and Reporting Tests
        ("Get Volunteers List", tester.test_get_volunteers),
        ("Get Volunteer Stats", tester.test_get_volunteer_stats),
        ("Get Organizer Stats", tester.test_get_organizer_stats),
        
        # Cleanup Tests
        ("Withdraw from Event", tester.test_withdraw_from_event),
        ("Delete Event", tester.test_delete_event),
    ]
    
    # Run all tests
    for test_name, test_func in test_sequence:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            tester.failed_tests.append({
                'name': test_name,
                'error': str(e)
            })
    
    # Print final results
    print(f"\n📊 Test Results:")
    print(f"   Tests Run: {tester.tests_run}")
    print(f"   Tests Passed: {tester.tests_passed}")
    print(f"   Tests Failed: {len(tester.failed_tests)}")
    print(f"   Success Rate: {(tester.tests_passed/tester.tests_run*100):.1f}%" if tester.tests_run > 0 else "0%")
    
    if tester.failed_tests:
        print(f"\n❌ Failed Tests:")
        for failure in tester.failed_tests:
            error_msg = failure.get('error', f"Expected {failure.get('expected')}, got {failure.get('actual')}")
            print(f"   - {failure['name']}: {error_msg}")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())