// Mock data for development and testing
import { TranscriptSegment, FormField } from '../types';

export const mockTranscript: TranscriptSegment[] = [
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
    linkedFields: ["mobility_indoor"]
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
    linkedFields: ["client_name", "dob", "address"]
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
  }
];

export const mockFormFields: FormField[] = [
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
  }
];
