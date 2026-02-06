// Mock data for the demo

const mockTranscript = [
    {
        id: 1,
        speaker: "clinician",
        text: "Good morning, Mrs. Thompson. How are you feeling today?",
        startTime: 0,
        endTime: 3.5,
        linkedFields: []
    },
    {
        id: 2,
        speaker: "client",
        text: "Good morning, Doctor. I'm doing okay, but I've been having some trouble with my mobility lately.",
        startTime: 4,
        endTime: 9,
        linkedFields: ["mobility"]
    },
    {
        id: 3,
        speaker: "clinician",
        text: "I see. Can you tell me more about that? When did you first notice the mobility issues?",
        startTime: 9.5,
        endTime: 14,
        linkedFields: []
    },
    {
        id: 4,
        speaker: "client",
        text: "It started about three months ago. I'm 78 years old, and I live alone in my apartment. I've noticed it's getting harder to walk to the shops.",
        startTime: 14.5,
        endTime: 23,
        linkedFields: ["age", "living_arrangements", "mobility"]
    },
    {
        id: 5,
        speaker: "clinician",
        text: "Have you had any falls recently?",
        startTime: 23.5,
        endTime: 25.5,
        linkedFields: []
    },
    {
        id: 6,
        speaker: "client",
        text: "Yes, I had a fall in my bathroom about two weeks ago. Thankfully I wasn't seriously hurt, just some bruising.",
        startTime: 26,
        endTime: 33,
        linkedFields: ["falls_history"]
    },
    {
        id: 7,
        speaker: "clinician",
        text: "I'm glad you weren't seriously injured. Let's talk about your current medications. What are you taking?",
        startTime: 33.5,
        endTime: 39,
        linkedFields: []
    },
    {
        id: 8,
        speaker: "client",
        text: "I take blood pressure medication - I think it's called Lisinopril - and I also take a statin for cholesterol. Oh, and I take vitamin D supplements.",
        startTime: 39.5,
        endTime: 49,
        linkedFields: ["current_medications"]
    },
    {
        id: 9,
        speaker: "clinician",
        text: "Good. Have you had any surgeries in the past?",
        startTime: 49.5,
        endTime: 52,
        linkedFields: []
    },
    {
        id: 10,
        speaker: "client",
        text: "Yes, I had a hip replacement about five years ago on my left side. That went well, actually.",
        startTime: 52.5,
        endTime: 58,
        linkedFields: ["past_surgeries"]
    },
    {
        id: 11,
        speaker: "clinician",
        text: "And do you have any chronic conditions we should be aware of?",
        startTime: 58.5,
        endTime: 61.5,
        linkedFields: []
    },
    {
        id: 12,
        speaker: "client",
        text: "I have high blood pressure and high cholesterol, which is why I'm on those medications. I also have mild arthritis in my hands and knees.",
        startTime: 62,
        endTime: 71,
        linkedFields: ["chronic_conditions"]
    },
    {
        id: 13,
        speaker: "clinician",
        text: "How are you managing with daily activities? Can you dress yourself, prepare meals, that sort of thing?",
        startTime: 71.5,
        endTime: 77,
        linkedFields: []
    },
    {
        id: 14,
        speaker: "client",
        text: "I can dress myself, but it takes longer than it used to. Preparing meals is getting difficult because standing for long periods makes my legs tired. I've been relying more on pre-made meals.",
        startTime: 77.5,
        endTime: 89,
        linkedFields: ["adls"]
    },
    {
        id: 15,
        speaker: "clinician",
        text: "What are your goals for your health and mobility?",
        startTime: 89.5,
        endTime: 92.5,
        linkedFields: []
    },
    {
        id: 16,
        speaker: "client",
        text: "I really want to be able to walk to the local shops again without feeling exhausted. I'd also like to visit my daughter more often - she lives about 20 minutes away by bus.",
        startTime: 93,
        endTime: 104,
        linkedFields: ["goals"]
    },
    {
        id: 17,
        speaker: "clinician",
        text: "Those are great goals. How's your memory and thinking? Any concerns there?",
        startTime: 104.5,
        endTime: 109,
        linkedFields: []
    },
    {
        id: 18,
        speaker: "client",
        text: "My memory is pretty good, I think. I sometimes forget where I put my keys, but doesn't everyone?",
        startTime: 109.5,
        endTime: 115,
        linkedFields: ["cognitive_state"]
    },
    {
        id: 19,
        speaker: "clinician",
        text: "That's normal. How about your skin? Any pressure sores or wounds?",
        startTime: 115.5,
        endTime: 119,
        linkedFields: []
    },
    {
        id: 20,
        speaker: "client",
        text: "No, my skin is fine. No problems there.",
        startTime: 119.5,
        endTime: 122,
        linkedFields: ["skin_integrity"]
    },
    {
        id: 21,
        speaker: "clinician",
        text: "And how's your appetite? Are you eating well?",
        startTime: 122.5,
        endTime: 125,
        linkedFields: []
    },
    {
        id: 22,
        speaker: "client",
        text: "My appetite is okay, but I've lost a bit of weight recently. Maybe 5 or 6 pounds over the last few months. I think it's because cooking is more difficult.",
        startTime: 125.5,
        endTime: 135,
        linkedFields: ["nutritional_risks"]
    },
    {
        id: 23,
        speaker: "clinician",
        text: "Thank you for sharing all of this information, Mrs. Thompson. This will help us create a care plan that addresses your needs and helps you reach your goals.",
        startTime: 135.5,
        endTime: 144,
        linkedFields: []
    }
];

const mockFormFields = [
    {
        id: "name",
        label: "Client Name",
        value: "Margaret Thompson",
        confidence: 0.95,
        flagged: false,
        category: "demographics"
    },
    {
        id: "age",
        label: "Age",
        value: "78",
        confidence: 0.98,
        flagged: false,
        category: "demographics"
    },
    {
        id: "living_arrangements",
        label: "Living Arrangements",
        value: "Lives alone in apartment",
        confidence: 0.92,
        flagged: false,
        category: "demographics"
    },
    {
        id: "current_medications",
        label: "Current Medications",
        value: "Lisinopril (blood pressure), Statin (cholesterol), Vitamin D supplements",
        confidence: 0.88,
        flagged: false,
        category: "clinical_history"
    },
    {
        id: "past_surgeries",
        label: "Past Surgeries",
        value: "Left hip replacement (5 years ago)",
        confidence: 0.94,
        flagged: false,
        category: "clinical_history"
    },
    {
        id: "chronic_conditions",
        label: "Chronic Conditions",
        value: "Hypertension, Hypercholesterolemia, Mild arthritis (hands and knees)",
        confidence: 0.91,
        flagged: false,
        category: "clinical_history"
    },
    {
        id: "mobility",
        label: "Mobility Status",
        value: "Decreased mobility, difficulty walking to shops, legs tire easily",
        confidence: 0.65,
        flagged: true,
        category: "functional_status"
    },
    {
        id: "falls_history",
        label: "Falls History",
        value: "One fall in bathroom 2 weeks ago, minor bruising",
        confidence: 0.89,
        flagged: false,
        category: "functional_status"
    },
    {
        id: "adls",
        label: "Activities of Daily Living",
        value: "Can dress self (slower), difficulty preparing meals due to prolonged standing, relying on pre-made meals",
        confidence: 0.62,
        flagged: true,
        category: "functional_status"
    },
    {
        id: "goals",
        label: "Client Goals",
        value: "Walk to local shops without exhaustion, visit daughter more frequently (20 min bus ride)",
        confidence: 0.93,
        flagged: false,
        category: "goals_aspirations"
    },
    {
        id: "cognitive_state",
        label: "Cognitive State",
        value: "Memory intact, occasional minor forgetfulness (keys)",
        confidence: 0.87,
        flagged: false,
        category: "risk_assessment"
    },
    {
        id: "skin_integrity",
        label: "Skin Integrity",
        value: "No pressure sores or wounds reported",
        confidence: 0.96,
        flagged: false,
        category: "risk_assessment"
    },
    {
        id: "nutritional_risks",
        label: "Nutritional Assessment",
        value: "Recent weight loss (5-6 lbs over few months), reduced appetite, difficulty cooking",
        confidence: 0.58,
        flagged: true,
        category: "risk_assessment"
    }
];
