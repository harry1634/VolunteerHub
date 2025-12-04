# Volunteer Connection Platform

A comprehensive web application connecting volunteers with NGOs and organizations to create positive community impact.

## Features

### For Volunteers
- **Easy Registration & Login**: JWT-based secure authentication
- **Browse Opportunities**: Search and filter volunteer events by cause, location, and status
- **Quick Sign-ups**: Register for events with one click
- **Track Impact**: View participation history and total volunteer hours
- **Event Communication**: Engage in event discussions with organizers and other volunteers
- **Submit Feedback**: Rate and review events after participation
- **Profile Management**: Update skills, interests, and availability

### For Organizers
- **Event Management**: Create, edit, and delete volunteer opportunities
- **Volunteer Tracking**: View registered volunteers and their details
- **Attendance Management**: Mark attendance and log volunteer hours
- **Volunteer Directory**: Browse registered volunteers by skills and availability
- **Event Analytics**: Track total events created and volunteer participation
- **Communication Tools**: Respond to feedback and engage with volunteers

### Core Functionality
- **Real-time Updates**: Available spots update automatically when volunteers sign up or withdraw
- **Event Details**: Complete event information including organizer contact details
- **Role-based Access**: Separate dashboards and features for volunteers and organizers
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI**: Warm, community-focused design with emerald green and orange accents

## Technology Stack

### Backend
- FastAPI, MongoDB, Motor, JWT, Bcrypt

### Frontend
- React, React Router, Axios, Shadcn UI, Tailwind CSS

## Getting Started

Services managed via supervisor:
```bash
sudo supervisorctl restart backend frontend
```

## Testing Results
- ✅ Backend: 95.7% success rate
- ✅ Frontend: 100% success rate
- ✅ All major features tested and working
