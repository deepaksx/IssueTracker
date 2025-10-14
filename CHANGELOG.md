# Changelog

All notable changes to the EFI IT Issue Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-15

### Added
- **Role-Based Access Control (RBAC)**: Three-tier user roles system
  - Admin: Full access to all features and data
  - HOD (Head of Department): Can create/edit issues within their company/department
  - Viewer: Read-only access within their company/department
- **Database Management System**: Complete backup and restore functionality
  - Download full backups as ZIP archives (includes database + PDF files)
  - Restore from backup with automatic current state backup
  - Reset database to factory defaults with confirmation
  - Database statistics dashboard
- **Edit History Tracking**: Comprehensive change tracking for issue descriptions
  - Preserves full text of previous versions
  - Timestamps and user attribution for each edit
  - Chronological history display with original content
- **Enhanced Issue Management**:
  - Auto-assignment of company/department for HOD users
  - Restricted filter options based on user role
  - Company, Department, and Application management
- **Document Management**:
  - PDF upload and storage
  - Inline PDF viewer with mobile optimization
  - Document download functionality
  - Auto-upload on file selection

### Changed
- **UI/UX Enhancements**:
  - Fixed sidebar collapse behavior during page navigation
  - Sidebar toggle button now moves with sidebar state
  - Auto-submit filters on dropdown selection
  - Smooth fade-in transitions to eliminate page flash
  - Fixed header/filter panel with scrollable issue table
  - Compact filter panel design
- **Dashboard Improvements**:
  - Grayed-out company/department filters for HOD/Viewer users
  - Role-based data filtering
  - Improved responsive design for mobile devices
- **Network Access**: Configured for LAN access with IP detection and display

### Fixed
- Sidebar collapse glitch during page navigation
- Filter panel layout on mobile devices
- PDF viewing on mobile browsers
- Page flash during transitions

### Security
- Enhanced session management
- Role-based route protection
- Improved password hashing
- Audit logging for all data changes

## [1.0.0] - 2025-10-01

### Added
- Initial release of EFI IT Issue Tracker
- User authentication with Flask-Login
- Basic admin/viewer role system
- Issue creation, editing, and deletion
- Audit logging system
- CSV export functionality
- Dashboard with filtering and search
- Bootstrap 5 responsive UI
- SQLite database backend
