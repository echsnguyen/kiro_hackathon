# AI Allied Health Assessment Automator - Demo

This is a **frontend-only demo** with mock data showing the complete workflow of the AI Allied Health Assessment Automator system.

## 🎯 What This Demo Shows

This demo demonstrates the complete end-to-end workflow:

1. **Consent Management** - Client consent collection before recording
2. **Audio Recording** - Simulated consultation recording
3. **Speech-to-Text** - Transcription with medical vocabulary (simulated)
4. **Clinical Data Extraction** - AI-powered extraction of structured data (simulated)
5. **Review & Validation** - Interactive review interface with:
   - Side-by-side transcript and form view
   - Click-to-highlight source segments
   - Confidence scoring for extracted fields
   - Manual validation workflow
6. **Portal Submission** - Final submission to provider portal

## 🚀 How to Run

### Option 1: Open Directly in Browser
Simply open `index.html` in any modern web browser:
```bash
# On Windows
start index.html

# On macOS
open index.html

# On Linux
xdg-open index.html
```

### Option 2: Use a Local Server (Recommended)
For the best experience, use a local web server:

**Using Python:**
```bash
cd demo
python -m http.server 8080
# Then open http://localhost:8080 in your browser
```

**Using Node.js (http-server):**
```bash
cd demo
npx http-server -p 8080
# Then open http://localhost:8080 in your browser
```

**Using VS Code:**
- Install the "Live Server" extension
- Right-click on `index.html` and select "Open with Live Server"

## 📋 Demo Features

### Interactive Elements

- **Workflow Steps**: Click on any step in the top navigation to jump to that stage
- **Recording Simulation**: Click the red button to simulate a 3-second recording
- **Transcript Highlighting**: Click on any transcript segment to highlight it
- **Form Field Linking**: Click on a form field to see its source segments highlighted in the transcript
- **Validation**: Check the "Validated" checkbox for each field to mark it as reviewed
- **Progress Tracking**: Watch the validation progress bar fill as you validate fields
- **Submit Button**: Becomes enabled only when all fields are validated

### Mock Data

The demo includes realistic mock data:
- **23 transcript segments** from a consultation with Mrs. Thompson (78 years old)
- **13 form fields** across 4 categories:
  - Demographics (name, age, living arrangements)
  - Clinical History (medications, surgeries, chronic conditions)
  - Functional Status (mobility, falls, ADLs)
  - Goals & Aspirations (client goals)
  - Risk Assessment (cognitive state, skin integrity, nutrition)
- **Confidence scores** for each extracted field
- **3 flagged fields** requiring review (low confidence)

## 🎨 Key UI Components

### Transcript Panel
- Speaker labels (Clinician, Client, Carer)
- Timestamps for each segment
- Click-to-highlight functionality
- Automatic scrolling to relevant segments

### Form Panel
- Auto-populated fields from AI extraction
- Confidence badges (High/Medium/Low)
- Warning flags for low-confidence fields
- Inline editing capability
- Validation checkboxes

### Validation Status
- Total fields count
- Validated fields count
- Flagged fields count
- Visual progress bar

## 🔄 Workflow Navigation

You can navigate through the workflow in two ways:

1. **Linear Flow**: Use the "Continue" and "Back" buttons
2. **Direct Navigation**: Click on any workflow step at the top

The demo automatically progresses through:
- Consent → Recording (after consent given)
- Recording → Transcription (after 3 seconds)
- Transcription → Extraction (progress bar simulation)
- Extraction → Review (progress bar simulation)
- Review → Submit (after all fields validated)

## 💡 Tips for Presenting

1. **Start at Consent**: Click "Start New Assessment" to begin from the beginning
2. **Show Recording**: Demonstrate the recording interface
3. **Skip to Review**: Click directly on "Review" step to show the main interface
4. **Demonstrate Linking**: Click on form fields to show source segment highlighting
5. **Show Validation**: Check validation boxes to demonstrate the workflow
6. **Complete Submission**: Validate all fields to enable submission

## 🎯 Use Cases

This demo is perfect for:
- **Stakeholder presentations** - Show the complete workflow without backend setup
- **User testing** - Get feedback on UI/UX before building the backend
- **Requirements validation** - Verify the workflow meets user needs
- **Training materials** - Help clinicians understand the system
- **Sales demos** - Demonstrate value proposition quickly

## 📝 Customization

To customize the demo data:

1. **Edit `demo-data.js`**:
   - Modify `mockTranscript` array to change transcript content
   - Modify `mockFormFields` array to change form fields
   - Update `linkedFields` to change which segments link to which fields

2. **Edit `index.html`**:
   - Change colors in the `<style>` section
   - Modify text content and labels
   - Add or remove workflow steps

3. **Edit `demo-app.js`**:
   - Adjust timing for simulations
   - Modify validation logic
   - Add custom interactions

## 🚧 Limitations

This is a **demo only** and does not include:
- Real audio recording or playback
- Actual AI/ML processing
- Backend API integration
- Database persistence
- Authentication/authorization
- Encryption
- Real-time transcription
- Actual portal integration

For the full production system, see the main project documentation.

## 📚 Next Steps

After reviewing this demo:

1. **Gather Feedback**: Share with stakeholders and collect requirements
2. **Refine UI/UX**: Make adjustments based on user feedback
3. **Build Backend**: Implement the actual services (see main project tasks)
4. **Integrate**: Connect the frontend to real backend services
5. **Test**: Conduct thorough testing with real data
6. **Deploy**: Deploy to production environment

## 🤝 Contributing

To improve this demo:
1. Enhance the mock data with more realistic scenarios
2. Add more interactive features
3. Improve the visual design
4. Add accessibility features
5. Create additional demo scenarios

## 📄 License

Proprietary - All rights reserved

---

**Questions?** Refer to the main project documentation in the parent directory.
