# WaveBook Hotel Management System

## Admin Panel Overview

The WaveBook Hotel Management System includes a comprehensive admin panel for managing all aspects of hotel operations.

## Features

### 🏨 Complete Hotel Management
- **Dashboard**: Overview of hotel statistics, occupancy rates, and recent activity
- **Guest Management**: View, search, and manage guest information and reservation history
- **Room Management**: Monitor room status, manage availability, and track maintenance
- **Reservation Management**: Handle check-ins, check-outs, and reservation lifecycle
- **Staff Management**: Manage hotel personnel and their roles
- **Reports**: Generate comprehensive reports on revenue, occupancy, and performance
- **Audit Log**: Complete system activity tracking for compliance and security

### 🔐 Security Features
- Role-based access control
- Session management
- Audit trail for all administrative actions
- Secure password handling

### 📊 Analytics & Reports
- Revenue tracking and analysis
- Occupancy rate monitoring
- Popular rooms analysis
- Payment method statistics
- Interactive charts and graphs

## Setup Instructions

### 1. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Admin User and Sample Data
```bash
python manage.py setup_hotel
```

This command will create:
- Admin user (username: `admin`, password: `admin123`)
- Sample staff members with different roles
- Sample rooms across 4 floors

### 3. Access the Admin Panel

#### Hotel Admin Panel
- URL: `http://localhost:8000/admin/login/`
- Username: `admin`
- Password: `admin123`

#### Django Admin Panel
- URL: `http://localhost:8000/admin/`
- Create a Django superuser: `python manage.py createsuperuser`

## Admin Panel Structure

### Main Sections

1. **Dashboard** (`/admin/dashboard/`)
   - Key performance indicators
   - Recent reservations
   - Quick action buttons
   - Real-time statistics

2. **Guest Management** (`/admin/guests/`)
   - List all guests with search and pagination
   - View detailed guest profiles
   - Access reservation history
   - Guest statistics

3. **Room Management** (`/admin/rooms/`)
   - Visual room status overview
   - Quick status changes
   - Room details and maintenance
   - Occupancy tracking

4. **Reservation Management** (`/admin/reservations/`)
   - Complete reservation lifecycle management
   - Check-in/check-out processes
   - Payment tracking
   - Status updates

5. **Staff Management** (`/admin/staff/`)
   - Employee information and roles
   - Access control management
   - Performance tracking
   - Role-based permissions

6. **Reports** (`/admin/reports/`)
   - Financial reports
   - Occupancy analytics
   - Popular rooms analysis
   - Exportable data

7. **Audit Log** (`/admin/audit/`)
   - Complete system activity log
   - User action tracking
   - Change history
   - Compliance reporting

## User Roles

### Administrator
- Full system access
- User management
- System configuration
- All reports and analytics

### Receptionist
- Guest management
- Reservation handling
- Check-in/check-out
- Payment processing

### Maintenance
- Room status updates
- Maintenance requests
- Equipment tracking

### Cleaning
- Room cleaning status
- Inventory management
- Cleaning schedules

## Navigation

The admin panel features:
- **Sidebar Navigation**: Quick access to all sections
- **Breadcrumb Navigation**: Track your location in the system
- **Search Functionality**: Find guests, reservations, or rooms quickly
- **Filter Options**: Narrow down data by various criteria
- **Pagination**: Handle large datasets efficiently

## Key Features

### Real-time Updates
- Live occupancy status
- Automatic status changes during check-in/out
- Real-time availability tracking

### Responsive Design
- Mobile-friendly interface
- Bootstrap-based responsive layout
- Touch-friendly controls

### Data Export
- Export reports to various formats
- Printable reports
- Data backup capabilities

### Audit Trail
- Complete change tracking
- User action logging
- Compliance reporting
- Security monitoring

## Technical Details

### Frontend Technologies
- Bootstrap 5.1.3
- Font Awesome 6.0.0
- Chart.js for analytics
- Responsive design principles

### Backend Features
- Django-based architecture
- Session-based authentication
- Database optimization
- Security best practices

### Database Models
- Guest management (Huesped)
- Staff management (PersonalHotel)
- Room management (Habitacion)
- Reservation system (Reserva, ReservaHabitacion)
- Payment tracking (Pago)
- Audit logging (ReporteAuditoria)

## Customization

The admin panel is highly customizable:
- Add new user roles
- Modify permissions
- Customize reports
- Add new features
- Integrate with external systems

## Support

For technical support or feature requests, contact the development team.

## Security Notes

- Change default passwords immediately
- Use HTTPS in production
- Regular backup procedures
- Monitor audit logs regularly
- Keep user permissions minimal

---

**WaveBook Hotel Management System** - Professional hotel administration made simple.