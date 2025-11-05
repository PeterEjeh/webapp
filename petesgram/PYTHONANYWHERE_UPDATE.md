# PythonAnywhere Deployment Guide

## Step 1: Collect Static Files Locally
Run this command in your project directory:
```bash
python manage.py collectstatic --noinput
```

Or double-click the `update_static.bat` file I created.

## Step 2: Upload to PythonAnywhere

### Option A: Using Git (Recommended)
1. Commit your changes:
```bash
git add .
git commit -m "Fixed Instagram feed styling and image aspect ratios"
git push
```

2. On PythonAnywhere, open a Bash console and run:
```bash
cd ~/webapp/petesgram
git pull
python manage.py collectstatic --noinput
```

### Option B: Manual Upload
1. Upload these files to PythonAnywhere using the Files tab:
   - `posts/templates/posts/feed.html`
   - `static/css/feed.css`

2. Then run in PythonAnywhere Bash console:
```bash
cd ~/webapp/petesgram
python manage.py collectstatic --noinput
```

## Step 3: Reload Your Web App
1. Go to the "Web" tab in PythonAnywhere
2. Click the green "Reload" button for your web app

## What Was Fixed:

### 1. Image Aspect Ratios
- Images now maintain their original aspect ratio
- Maximum height of 585px (Instagram's standard)
- Black background for letterboxing
- No more stretched/distorted images

### 2. Profile Pictures
- Fixed at 32x32px in post headers
- Circular with proper object-fit: cover
- Won't stretch or distort

### 3. Media Display
- Uses `object-fit: contain` to show full image
- Black background fills empty space
- Responsive on mobile devices

### 4. Video Handling
- Videos maintain proper aspect ratio
- Mute button properly positioned
- No stretching or distortion

## Troubleshooting

If images still look wrong after updating:

1. **Clear Browser Cache**
   - Chrome/Edge: Ctrl + Shift + R
   - Firefox: Ctrl + Shift + R
   - Safari: Cmd + Shift + R

2. **Check Static Files Path**
   Make sure in PythonAnywhere Web tab:
   - URL: `/static/`
   - Directory: `/home/YOUR_USERNAME/webapp/petesgram/staticfiles/`

3. **Verify Files Were Uploaded**
   Check that feed.css was updated in:
   `/home/YOUR_USERNAME/webapp/petesgram/staticfiles/css/feed.css`

4. **Check for Errors**
   Look at error log in PythonAnywhere Web tab

## Expected Result
- Post images maintain proper aspect ratio
- No more ultra-wide stretched images
- Profile pics are small and circular (32x32px)
- Everything looks clean like Instagram
- Black background fills space for non-square images
