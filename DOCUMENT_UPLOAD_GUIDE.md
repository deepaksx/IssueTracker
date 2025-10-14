# Document Upload Feature Guide

## Overview
The IT Issue Tracker now supports uploading PDF documents to issues. This allows you to attach relevant documentation, screenshots (exported as PDFs), reports, or any other PDF files to issues.

## Features

### 1. **Upload PDF Documents**
- Any authenticated user can upload PDF files to issues
- Maximum file size: 16MB per file
- Only PDF format is supported
- Files are stored securely with unique identifiers

### 2. **View & Download Documents**
- All users can view the list of documents attached to an issue
- Documents show:
  - Original filename
  - File size (human-readable format)
  - Uploader name
  - Upload date
- Click the download button to download the PDF

### 3. **Delete Documents**
- Only admin users can delete documents
- Deleting a document removes both the database record and the physical file

## How to Use

### For Existing Installations

If you already have the IT Issue Tracker installed, you need to run the migration script:

1. **Stop the application** if it's running
2. **Run the migration**:
   ```bash
   # Windows
   migrate_documents.bat

   # Or run directly:
   python migrate_documents.py
   ```
3. **Restart the application**:
   ```bash
   start.bat
   ```

### For New Installations

The documents table is automatically created when you run `setup.bat` or `init_db.py`.

### Uploading Documents

1. Navigate to any issue detail page
2. In the right sidebar, you'll see a "Documents" card
3. Click "Choose File" and select a PDF file (max 16MB)
4. Click "Upload PDF"
5. The document will appear in the list below

### Downloading Documents

1. Go to the issue detail page
2. In the "Documents" section, find the file you want
3. Click the download icon (⬇)
4. The file will download with its original filename

### Deleting Documents (Admin Only)

1. Go to the issue detail page
2. In the "Documents" section, find the file you want to delete
3. Click the trash icon (🗑)
4. Confirm the deletion in the modal dialog
5. The file and database record will be permanently deleted

## Technical Details

### File Storage
- Files are stored in the `uploads/` directory
- Each file is renamed with a unique UUID to prevent conflicts
- Original filenames are preserved in the database

### Database Schema
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_id INTEGER NOT NULL,
    filename TEXT NOT NULL,              -- UUID-based filename
    original_filename TEXT NOT NULL,      -- Original name shown to users
    file_size INTEGER NOT NULL,          -- Size in bytes
    uploaded_by TEXT NOT NULL,           -- Username who uploaded
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issues (id) ON DELETE CASCADE
);
```

### Security Features
- File extension validation (PDF only)
- Secure filename generation using UUID
- File size limit enforcement (16MB)
- Authentication required for all operations
- Admin-only deletion

## File Structure
```
IssueTracker/
├── uploads/                      # Document storage directory
│   ├── abc123def456.pdf         # Stored files (UUID names)
│   └── ...
├── migrate_documents.py         # Migration script
├── migrate_documents.bat        # Windows migration runner
└── app.py                       # Main application with upload routes
```

## API Endpoints

- `POST /issue/<id>/upload` - Upload a document
- `GET /document/<id>/download` - Download a document
- `POST /document/<id>/delete` - Delete a document (admin only)

## Troubleshooting

### "Only PDF files are allowed"
- Make sure your file has a `.pdf` extension
- The system only accepts PDF files for security reasons

### "File too large"
- Maximum file size is 16MB
- Compress your PDF or split it into smaller files

### "File not found on server"
- The physical file may have been deleted from the uploads directory
- Contact your administrator to investigate

### Migration Issues
- If migration fails, check that you have write permissions in the application directory
- Make sure the database file isn't locked by another process
- Try stopping the application before running migration

## Best Practices

1. **Use descriptive filenames** before uploading (e.g., "Error_Screenshot_2025.pdf")
2. **Keep file sizes reasonable** - compress PDFs when possible
3. **Delete obsolete documents** to save storage space
4. **Convert images to PDF** before uploading (use tools like Adobe Acrobat, online converters, or print-to-PDF)

## Future Enhancements

Potential future improvements:
- Support for additional file types (images, Word documents, etc.)
- Bulk upload functionality
- Document preview in browser
- Search documents by content
- Document versioning
- Compression for large files
