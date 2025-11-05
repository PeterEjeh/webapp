# Instagram-Style Post Header with Media Preview

## What We Added:

### 1. Post Header Layout
The header now has THREE sections:

```
[Profile Pic + Username + "Original audio"]  [Preview Thumbnail]  [⋯ Menu]
         (Left Side)                          (Right Side)
```

### 2. Components:

#### Left Side:
- **Profile Picture**: 32x32px circular
- **User Details** (stacked):
  - Username (bold, 14px)
  - "Original audio" (gray, 12px) - you can change this text

#### Right Side:
- **Media Preview**: 48x48px thumbnail (40px on mobile)
  - Shows a preview of the video/image
  - Rounded corners (4px radius)
  - Covers the entire square area
- **Three-dot menu**: Options button

### 3. Styling Features:
- Clean spacing between elements
- Flexible layout that adapts to content
- Preview thumbnail uses `object-fit: cover` for perfect square crop
- Responsive: Scales down on mobile devices

### 4. How It Works:
The preview thumbnail shows:
- For **videos**: First frame of the video
- For **images**: The uploaded image

### 5. Customization Options:

To change "Original audio" text, edit in `feed.html`:
```html
<span class="post-info">Original audio</span>
```

You could make it dynamic:
```html
<span class="post-info">{{ post.created_at|timesince }} ago</span>
```

Or add music/sound info:
```html
<span class="post-info">{{ post.audio_name|default:"Original audio" }}</span>
```

## Visual Layout:

```
┌─────────────────────────────────────────────────┐
│  ●  username                    [▓▓▓▓]    ⋯    │
│     Original audio              preview         │
└─────────────────────────────────────────────────┘
│                                                 │
│            [MAIN VIDEO/IMAGE]                   │
│                                                 │
└─────────────────────────────────────────────────┘
│  ♡  💬  ✈                            🔖         │
└─────────────────────────────────────────────────┘
```

## Mobile Adaptation:
- Preview thumbnail: 48px → 40px
- Header height adjusts automatically
- All spacing scales proportionally

## Benefits:
✅ Matches Instagram Reels/Video post style
✅ Shows content preview before scrolling
✅ Clean, professional look
✅ Fully responsive
✅ Easy to customize
