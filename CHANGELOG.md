# Changelog

## Version 2.0 - Modern UI Update (2025-11-06)

### ✨ Major Features

#### Fixed Import Error
- **Fixed**: Application can now be run directly with `python main.py` from the app directory
- **Added**: Smart import path detection that works both as a module and direct script
- **Added**: Cross-platform launcher scripts (`run.py`, `run.bat`, `run.sh`)

#### Modernized GUI
- **Complete UI overhaul** with professional, modern design
- **Material Design inspired** color scheme with consistent theming
- **Modern styling** including:
  - Rounded corners on all UI elements
  - Smooth hover effects and transitions
  - Professional color palette (blue primary, green success, orange warning, red danger)
  - Better visual hierarchy and spacing
  - Clean, minimal aesthetic

#### Enhanced Visual Elements
- **Emoji icons** throughout the interface for better visual clarity
- **Color-coded file changes**:
  - 🟢 Green for additions
  - 🟠 Orange for updates
  - 🔴 Red for removals
  - ⚪ Gray for skipped items
- **Dark-themed log console** with monospace font for technical output
- **Professional status bar** with real-time progress tracking

#### Improved User Experience
- **Better organization** with clearly grouped sections
- **Enhanced readability** with improved typography and spacing
- **Responsive layout** that adapts to window resizing
- **Helpful tooltips** and error messages
- **Visual feedback** for all interactions (hover states, pressed states)
- **Clear action buttons** with descriptive icons and labels

#### Bug Fixes and Safety Improvements
- **Enhanced path validation** with better error messages
- **Input sanitization** for path entries (trim whitespace, validate format)
- **Existence checks** before sync operations to prevent errors
- **Better error handling** with user-friendly messages
- **Safe operations** with multiple confirmation dialogs
- **Comprehensive logging** with timestamps for all operations

#### UI Components Modernized
1. **Header**: Large, bold title with emoji icon
2. **Directory Configuration**: Cleaner layout with better labels
3. **Modpack List**: Enhanced selection with hover effects
4. **Preview Tree**: Better formatting with alternating row colors
5. **Action Buttons**: Professional styling with appropriate colors
6. **Log Output**: Dark console-style output for better readability
7. **Progress Bar**: Modern design with smooth animations
8. **Status Bar**: Clear indicators with icons

### 🔧 Technical Improvements

#### Code Quality
- Added comprehensive input validation
- Improved error handling throughout the application
- Better separation of concerns in UI code
- More descriptive variable and function names
- Enhanced type hints and documentation

#### Performance
- Optimized UI rendering with proper styling
- Efficient event handling
- Better memory management

#### Maintainability
- Well-organized stylesheet system
- Consistent color scheme using constants
- Modular UI setup for easy modifications
- Clear code comments and documentation

### 📚 Documentation
- **Updated README** with:
  - Emoji icons for better visual appeal
  - Detailed feature descriptions
  - Multiple running options
  - UI features section
  - Enhanced getting started guide
- **Added launcher scripts** for easy application startup
- **Comprehensive changelog** documenting all changes

### 🎨 Style Guide

#### Colors
- Primary: #2196F3 (Blue)
- Primary Dark: #1976D2 (Darker Blue)
- Success: #4CAF50 (Green)
- Warning: #FF9800 (Orange)
- Danger: #F44336 (Red)
- Background: #F5F5F5 (Light Gray)
- Surface: #FFFFFF (White)

#### Typography
- Headers: Bold, 24px
- Labels: 12-13px, semibold for important text
- Body: 12px regular
- Console: 11px monospace

#### Spacing
- Padding: 10-16px for containers
- Margins: 12-16px between sections
- Border radius: 6-8px for most elements

### 🐛 Bug Fixes
1. Fixed relative import error when running main.py directly
2. Added validation for empty path inputs
3. Fixed potential None pointer issues
4. Improved error messages for invalid paths
5. Better handling of non-existent directories

### 🚀 New Features
- Clear log button in log panel
- Better visual feedback during sync operations
- Enhanced modpack details display with HTML formatting
- Improved confirmation dialogs with better messaging
- Path resolution with expanduser() and resolve()

### ⚠️ Breaking Changes
None - All changes are backward compatible

### 📝 Migration Notes
- No migration needed - existing configurations will work as-is
- Existing sync history and exclusions are preserved
- Users will immediately benefit from the improved UI

### 🔮 Future Enhancements (Potential)
- Custom theme support (dark/light mode toggle)
- Drag-and-drop for path selection
- Recent paths history
- Advanced filtering options
- Batch sync operations
- Export/import configuration
- Sync scheduling
- Desktop notifications
