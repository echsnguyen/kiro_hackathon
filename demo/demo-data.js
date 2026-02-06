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

// OT Form-based structure
const mockFormFields = [
    // Client Information
    {
        id: "client_name",
        label: "Client Name",
        value: "Margaret Thompson",
        confidence: 0.95,
        flagged: false,
        category: "client_information"
    },
    {
        id: "dob",
        label: "Date of Birth",
        value: "15/03/1946",
        confidence: 0.92,
        flagged: false,
        category: "client_information"
    },
    {
        id: "address",
        label: "Address",
        value: "Unit 5, 123 Main Street, Suburb VIC 3000",
        confidence: 0.88,
        flagged: false,
        category: "client_information"
    },
    {
        id: "phone",
        label: "Phone Number",
        value: "0412 345 678",
        confidence: 0.94,
        flagged: false,
        category: "client_information"
    },
    {
        id: "emergency_contact",
        label: "Emergency Contact",
        value: "Sarah Thompson (Daughter) - 0423 456 789",
        confidence: 0.91,
        flagged: false,
        category: "client_information"
    },
    
    // Referral Information
    {
        id: "referral_source",
        label: "Referral Source",
        value: "GP - Dr. James Wilson",
        confidence: 0.89,
        flagged: false,
        category: "referral_information"
    },
    {
        id: "referral_date",
        label: "Referral Date",
        value: "10/01/2024",
        confidence: 0.93,
        flagged: false,
        category: "referral_information"
    },
    {
        id: "referral_reason",
        label: "Reason for Referral",
        value: "Decreased mobility, fall risk assessment, ADL support",
        confidence: 0.87,
        flagged: false,
        category: "referral_information"
    },
    
    // Medical History
    {
        id: "diagnosis",
        label: "Primary Diagnosis",
        value: "Osteoarthritis (bilateral knees), Hypertension",
        confidence: 0.91,
        flagged: false,
        category: "medical_history"
    },
    {
        id: "secondary_conditions",
        label: "Secondary Conditions",
        value: "Hypercholesterolemia, Previous left hip replacement (2019)",
        confidence: 0.88,
        flagged: false,
        category: "medical_history"
    },
    {
        id: "medications",
        label: "Current Medications",
        value: "Lisinopril 10mg daily, Atorvastatin 20mg daily, Vitamin D 1000IU daily",
        confidence: 0.85,
        flagged: false,
        category: "medical_history"
    },
    {
        id: "allergies",
        label: "Allergies",
        value: "No known drug allergies",
        confidence: 0.96,
        flagged: false,
        category: "medical_history"
    },
    
    // Functional Assessment - Mobility
    {
        id: "mobility_indoor",
        label: "Indoor Mobility",
        value: "Independent with furniture support, slow gait",
        confidence: 0.78,
        flagged: true,
        category: "functional_mobility"
    },
    {
        id: "mobility_outdoor",
        label: "Outdoor Mobility",
        value: "Requires walking stick, limited to short distances (<100m)",
        confidence: 0.82,
        flagged: false,
        category: "functional_mobility"
    },
    {
        id: "transfers",
        label: "Transfers (bed/chair/toilet)",
        value: "Independent but slow, uses armrests for support",
        confidence: 0.86,
        flagged: false,
        category: "functional_mobility"
    },
    {
        id: "stairs",
        label: "Stairs",
        value: "Avoids stairs, uses handrail when necessary, one step at a time",
        confidence: 0.79,
        flagged: true,
        category: "functional_mobility"
    },
    {
        id: "falls_history",
        label: "Falls History",
        value: "One fall in bathroom 2 weeks ago (slipped on wet floor), minor bruising to right hip",
        confidence: 0.89,
        flagged: false,
        category: "functional_mobility"
    },
    
    // Functional Assessment - Self Care
    {
        id: "bathing",
        label: "Bathing/Showering",
        value: "Requires shower chair, difficulty with lower body washing",
        confidence: 0.73,
        flagged: true,
        category: "functional_selfcare"
    },
    {
        id: "dressing",
        label: "Dressing",
        value: "Independent upper body, difficulty with socks/shoes, takes extra time",
        confidence: 0.81,
        flagged: false,
        category: "functional_selfcare"
    },
    {
        id: "grooming",
        label: "Grooming",
        value: "Independent with grooming and hygiene",
        confidence: 0.92,
        flagged: false,
        category: "functional_selfcare"
    },
    {
        id: "toileting",
        label: "Toileting",
        value: "Independent, no continence issues",
        confidence: 0.94,
        flagged: false,
        category: "functional_selfcare"
    },
    {
        id: "feeding",
        label: "Feeding",
        value: "Independent with eating and drinking",
        confidence: 0.96,
        flagged: false,
        category: "functional_selfcare"
    },
    
    // Functional Assessment - Domestic Tasks
    {
        id: "meal_prep",
        label: "Meal Preparation",
        value: "Difficulty with prolonged standing, relies on pre-made meals and simple cooking",
        confidence: 0.76,
        flagged: true,
        category: "functional_domestic"
    },
    {
        id: "housework",
        label: "Housework",
        value: "Unable to perform heavy cleaning, manages light tasks only",
        confidence: 0.84,
        flagged: false,
        category: "functional_domestic"
    },
    {
        id: "laundry",
        label: "Laundry",
        value: "Difficulty bending to load/unload machine, daughter assists weekly",
        confidence: 0.79,
        flagged: false,
        category: "functional_domestic"
    },
    {
        id: "shopping",
        label: "Shopping",
        value: "Unable to walk to shops, relies on online delivery and daughter's assistance",
        confidence: 0.88,
        flagged: false,
        category: "functional_domestic"
    },
    
    // Home Environment
    {
        id: "home_type",
        label: "Home Type",
        value: "Ground floor apartment, no stairs to entry",
        confidence: 0.91,
        flagged: false,
        category: "home_environment"
    },
    {
        id: "home_access",
        label: "Access/Entry",
        value: "Level entry, no steps, adequate doorway widths",
        confidence: 0.87,
        flagged: false,
        category: "home_environment"
    },
    {
        id: "bathroom_setup",
        label: "Bathroom Setup",
        value: "Standard shower over bath, no grab rails currently installed",
        confidence: 0.82,
        flagged: true,
        category: "home_environment"
    },
    {
        id: "home_hazards",
        label: "Home Hazards",
        value: "Loose bathroom mat (removed during visit), adequate lighting",
        confidence: 0.78,
        flagged: false,
        category: "home_environment"
    },
    
    // Cognitive/Psychosocial
    {
        id: "cognitive_status",
        label: "Cognitive Status",
        value: "Alert and oriented x3, memory intact, occasional word-finding difficulty",
        confidence: 0.89,
        flagged: false,
        category: "cognitive_psychosocial"
    },
    {
        id: "mood",
        label: "Mood/Mental Health",
        value: "Reports feeling frustrated with limitations, some social isolation",
        confidence: 0.74,
        flagged: true,
        category: "cognitive_psychosocial"
    },
    {
        id: "social_support",
        label: "Social Support",
        value: "Daughter visits weekly, limited contact with friends due to mobility",
        confidence: 0.86,
        flagged: false,
        category: "cognitive_psychosocial"
    },
    
    // Client Goals
    {
        id: "client_goals",
        label: "Client's Goals",
        value: "1. Walk to local shops independently\n2. Visit daughter more frequently\n3. Shower safely without fear of falling\n4. Prepare own meals",
        confidence: 0.91,
        flagged: false,
        category: "goals_plan"
    },
    
    // OT Assessment Summary
    {
        id: "assessment_summary",
        label: "Assessment Summary",
        value: "78yo female with decreased mobility due to OA. Fall risk due to bathroom hazards and reduced lower limb strength. Requires equipment and home modifications for safety. Reduced participation in valued activities (shopping, visiting family).",
        confidence: 0.68,
        flagged: true,
        category: "goals_plan"
    },
    
    // Recommendations
    {
        id: "recommendations",
        label: "Recommendations",
        value: "1. Install grab rails in bathroom\n2. Provide shower chair\n3. Mobility aid review (walking stick assessment)\n4. Strength and balance exercises\n5. Meal preparation strategies\n6. Community transport options",
        confidence: 0.72,
        flagged: true,
        category: "goals_plan"
    }
];
